# SimReady Common Traps & Failure Triage Matrix

This document captures mission-critical edge cases, schema nuances, and engine limitations discovered during the production validation of the Workcell Digital Twin. AI agents must consult this guide before attempting asset remediation.

---

## 1. The Ghost S3 URL in `customData` (`AA.001`)

### The Symptom
You successfully repathed all shader asset attributes (e.g. `inputs:diffuse_texture`, `info:mdl:sourceAsset`) to local paths like `./material/texture.png`, but `simready.validate` still reports:
```text
[FAIL] AA.001: Asset has external network dependency: https://omniverse-content-production.s3-us-west-2.amazonaws.com/...
```

### The Root Cause
When Omniverse Kit or USD tools create or modify shader attributes, they frequently cache the original fallback URL inside the attribute's metadata dictionary under `customData['default']`. Even if the attribute's main value `attr.Get()` is purely local, the validator inspects the underlying layer's `customData` and fails `AA.001`.

### The Fix
Inspect each property's `customData` dictionary and delete the `"default"` key if it contains an external URL:
```python
custom_data = attr.GetCustomData()
if "default" in custom_data:
    def_val = str(custom_data["default"])
    if any(prefix in def_val for prefix in ["http://", "https://", "s3://", "omniverse://"]):
        del custom_data["default"]
        attr.SetCustomData(custom_data)
```

---

## 2. Illegal Collider Placement on `Xform` Prims (`RB.COL.001`, `RB.COL.002`)

### The Symptom
Validator flags `RB.COL.001: CollisionAPI applied to non-mesh geometry` or `RB.COL.002: MeshCollisionAPI requires UsdGeomMesh`.

### The Root Cause
In standard DCC tools (Blender, Maya) or naive CAD conversions, developers often attach physics collision APIs directly to the parent transform (`UsdGeom.Xform`) expecting children to inherit collision properties. OpenUSD and PhysX require collision APIs to be placed directly on geometric leaf prims (`UsdGeom.Mesh`).

### The Fix
1. Remove `UsdPhysics.CollisionAPI` and `UsdPhysics.MeshCollisionAPI` from the `Xform` prim.
2. Traverse the children to locate the visual or dedicated collision `UsdGeom.Mesh`.
3. Apply the collision APIs directly to the leaf `Mesh`:
```python
# 1. Strip from Xform
if prim.IsA(UsdGeom.Xform) and prim.HasAPI(UsdPhysics.CollisionAPI):
    prim.RemoveAPI(UsdPhysics.CollisionAPI)
    prim.RemoveAPI(UsdPhysics.MeshCollisionAPI)

# 2. Apply to child Mesh
for child in prim.GetChildren():
    if child.IsA(UsdGeom.Mesh):
        UsdPhysics.CollisionAPI.Apply(child)
        mesh_col = UsdPhysics.MeshCollisionAPI.Apply(child)
        mesh_col.CreateApproximationAttr().Set("convexHull")
```

---

## 3. The Multi-Body Prop Trap (`FET004_BASE_NEUTRAL` / `RB.MB.001`)

### The Symptom
Validating a static or single-body prop (e.g. `Table.usd`, `Bin.usd`, `xray_scanner.usd`) outputs:
```text
FET004_BASE_NEUTRAL: passed: False, failing requirements: ['RB.MB.001']
```

### The Explanation & Correct Response
**DO NOT CREATE ARTIFICIAL JOINTS OR DUMMY SECOND BODIES.**
Under the official NVIDIA SimReady specification (`nv_core/sr_specs/docs/profiles/profiles.toml`), the `FET004_BASE_NEUTRAL` feature is explicitly defined with:
```toml
[profiles.Prop-Robotics-Neutral.features.FET004_BASE_NEUTRAL]
optional = true
```
A single-body prop satisfies robotics prop physics via `FET003_BASE_NEUTRAL` (rigid body + colliders + mass + physics material). `FET004` is only evaluated when an asset is intentionally authored as a multi-link articulated mechanism (e.g., a vise, a clamp, or a folding door). Single-body props are **100% compliant**.

---

## 4. Standalone Python vs Omniverse Kit Runtime for Robots (`FET022`)

### The Symptom
Evaluating an articulated robot arm (e.g. `ur10.usda`) in standalone Python reports:
```text
FET022_DRIVEN_JOINTS_NEUTRAL: passed: False, failing requirements: ['DJ.001', 'DJ.002', 'DJ.003']
```

### The Explanation
* `FET001` (Units & Geometry), `FET003` (Link Mass & Inertia), `FET004` (Kinematic Joints & Hierarchy), and `FET024` (Articulation Root) validate **100% PASS** in standalone OpenUSD.
* `FET022` checks for drive controller states authored via `pxr.PhysxSchema.JointStateAPI`. The `PhysxSchema` Python bindings are proprietary to NVIDIA Omniverse and only load when running inside an Omniverse Kit application or Isaac Sim (`isaac-sim.bat --python`).
* Do not attempt to hand-author fake string attributes in USDA to bypass `DJ.001-DJ.003` in standalone Python; verify `FET001`, `FET003`, `FET004`, and `FET024` statically, and run `FET022` inside the Kit runtime.

---

## 5. Texture Color Space Normalization (`VM.TEX.002`)

### The Symptom
Validator fails with `VM.TEX.002: Invalid or unspecified colorSpace on texture input`.

### The Root Cause
SimReady mandates explicit color space declarations on MDL texture inputs. Leaving `colorSpace` unset or relying on automatic DCC defaults can lead to incorrect gamma curves during rendering and sensor simulation.

### The Fix
Author `colorSpace = "raw"` on all texture attributes (normal maps, roughness, metallic, and generic textures):
```python
for attr in shader_prim.GetAttributes():
    if attr.GetName().startswith("inputs:") and "texture" in attr.GetName():
        attr.SetColorSpace("raw")
```

---

## 6. CAD Units: Baking Points vs Root Transform Scaling (`UN.007`)

### The Symptom
Raw CAD files imported into USD are often in millimeters ($1\text{ unit} = 1\text{ mm}$). Tools often fix this by adding:
```usda
xformOp:scale = (0.001, 0.001, 0.001)
```
While visually correct, physics engines (PhysX / Isaac Sim) often encounter numerical precision and collision margin issues when root transforms have non-unit scale.

### The Fix
1. Author stage metadata `metersPerUnit = 1.0`.
2. Multiply all vertex `points` in leaf `UsdGeom.Mesh` prims by $0.001$.
3. Clear the `xformOp:scale` or reset it to `(1.0, 1.0, 1.0)`.
