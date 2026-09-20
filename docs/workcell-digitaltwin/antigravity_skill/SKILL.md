---
name: workcell-digitaltwin-skills
description: >-
  Audits, restructures, optimizes, and maintains production-grade OpenUSD and NVIDIA Isaac Sim digital twin assets.
  Use this skill when working with industrial automation workcells, robotics simulations, CAD-to-USD conversion bloat,
  sublayer decomposition (layout, physics, lighting, automation), Featherstone articulation root unification,
  IsaacRobotAPI kinematics, UsdGeomPointInstancer optimization, GeomModelAPI extentsHint, or component material localization.
---

# Workcell Digital Twin Engineering Skill for Antigravity & Gemini Agents

This skill equips the agent to audit, refactor, and maintain production-grade OpenUSD workcells designed for NVIDIA Omniverse and Isaac Sim 6.0. Follow these runbooks when diagnosing issues or applying restructuring steps.

---

## 1. Skill Activation & Diagnostic Runbook

When invoked on a digital twin workspace, execute this 4-step diagnostic protocol using Python `pxr.Usd`:

```python
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf

def audit_stage(stage_path):
    print("=== AUDITING STAGE:", stage_path)
    stage = Usd.Stage.Open(stage_path)
    
    # 1. Articulation Root Count (Must be <= 1 per robot kinematic chain)
    art_roots = [p.GetPath() for p in stage.Traverse() if p.HasAPI(UsdPhysics.ArticulationRootAPI)]
    print(f"Articulation roots ({len(art_roots)}):", art_roots)
    if len(art_roots) > 1:
        print("WARNING: Multiple articulation roots detected! Likely causing joint constraint instability.")

    # 2. Model Hierarchy Violations
    hierarchy_violations = []
    for prim in stage.Traverse():
        model = Usd.ModelAPI(prim)
        parent = prim.GetParent()
        if parent and parent.IsValid() and parent.GetPath() != Sdf.Path("/"):
            if model.IsModel() and not Usd.ModelAPI(parent).IsGroup():
                hierarchy_violations.append(f"Model {prim.GetPath()} inside non-group parent {parent.GetPath()}")
    print(f"Model hierarchy violations ({len(hierarchy_violations)}):", hierarchy_violations)

    # 3. Broken Material Bindings
    broken_materials = []
    for prim in stage.Traverse():
        bapi = UsdShade.MaterialBindingAPI(prim)
        db = bapi.GetDirectBinding()
        rel = bapi.GetDirectBindingRel()
        if rel and rel.GetTargets() and not db.GetMaterial():
            broken_materials.append((prim.GetPath(), rel.GetTargets()))
    print(f"Broken material bindings ({len(broken_materials)}):", broken_materials)

    # 4. Unloaded Extents Check
    stage_none = Usd.Stage.Open(stage_path, Usd.Stage.LoadNone)
    world = stage_none.GetPrimAtPath("/World")
    extents = UsdGeom.ModelAPI(world).GetExtentsHint() if world else None
    print("Unloaded /World extentsHint:", extents)
```

---

## 2. Core Operational Procedures

### Procedure A: Sublayer Decomposition (Separation of Concerns)

Never author transforms, physics, lighting, and automation in a single monolithic USD file. Decompose into 4 standard sublayers:

1. **`layers/layout.usda`**:
   - Encapsulate root `/World` (kind = `assembly`).
   - Define component payload placeholders (`kind = "component"`).
   - Author transforms (`xformOp:translate`, `xformOp:orient`, `xformOp:scale`) and `extentsHint`.
   - Never author raw mesh geometry here.
2. **`layers/physics.usda`**:
   - Define `/World/PhysicsScene` with `NewtonSceneAPI` and `PhysxSceneAPI`.
   - Author global gravity vector.
   - Introduce ground plane via payload to `components/fixtures/ground_plane/GroundPlane.usd`.
3. **`layers/lighting.usda`**:
   - Define `UsdLuxDomeLight` and `UsdLuxRectLight` prims.
   - Author render setting overrides under `/Render/Settings`.
4. **`layers/automation.usda`**:
   - Author `OmniGraph` / `ActionGraph` networks and ROS2 bridge nodes.

---

### Procedure B: Multi-Part `UsdGeomPointInstancer` Conversion

When converting repetitive CAD geometry (battery cells, rollers, fasteners) into a `PointInstancer`:

1. **Extract Unique Prototypes**:
   - If parts have multiple materials (e.g. cell cap vs cell cylinder), create separate prototype meshes under a private, invisible `Prototypes` Scope.
   - Center all prototype vertex coordinates to $(0, 0, 0)$ local origin.
2. **Collect Instance Coordinates**:
   - Extract world/assembly transformation matrices of each individual CAD part.
   - Decompose into position translations and orientation quaternions.
3. **Author PointInstancer**:
   ```python
   instancer = UsdGeom.PointInstancer.Define(stage, "/EVBatteryPack/BatteryCells")
   instancer.CreatePositionsAttr(positions)        # VtVec3fArray
   instancer.CreateOrientationsAttr(orientations)  # VtQuathArray
   instancer.CreateProtoIndicesAttr(proto_indices) # VtIntArray (e.g. 0,1,2, 0,1,2...)
   instancer.CreatePrototypesRel().SetTargets([
       Sdf.Path("/EVBatteryPack/Prototypes/TopCap"),
       Sdf.Path("/EVBatteryPack/Prototypes/Body"),
       Sdf.Path("/EVBatteryPack/Prototypes/BottomCap")
   ])
   ```
4. **Delete Discrete Meshes**: Remove the hundreds of individual original CAD mesh prims to achieve an ~85%+ prim reduction.

---

### Procedure C: Unifying Robot Articulation Trees via `IsaacRobotAPI`

When mounting an end-effector / gripper to a robot arm:

1. **Suppress Gripper Articulation Root**:
   - The arm base holds the primary `PhysicsArticulationRootAPI`.
   - On the referenced gripper prim, suppress its internal root via:
     ```usda
     delete apiSchemas = ["PhysicsArticulationRootAPI"]
     ```
2. **Author `ToolMountJoint`**:
   - Create a `PhysicsFixedJoint` binding the arm tool flange (`wrist_3_link`) to the gripper base (`robotiq_base_link`).
   - Apply `IsaacJointAPI`.
3. **Apply `IsaacRobotAPI` to Assembly Root**:
   - Author `isaac:description`, `isaac:robotType = "manipulator"`, and `isaac:namespace`.
   - Author `rel isaac:physics:robotJoints` enumerating all joints from arm base to gripper fingers in order.
   - Author `rel isaac:physics:robotLinks` enumerating all rigid bodies in kinematic order.

---

### Procedure D: Material Localization & Zero-Root Discipline

To maintain 100% asset portability:

1. **Component Local Materials**:
   - Store all material definitions (`def Material`) inside the component's internal `Looks` scope (e.g. `/Table/Looks/...`, `/Bin/Looks/...`).
   - Store MDL files in the component's local `materials/` folder and textures in `textures/`.
   - Author internal bindings: `rel material:binding = </Table/Looks/MyMaterial>`.
2. **No Root `/World/Looks`**:
   - Eliminate any `/World/Looks` scope in the layout layer.
   - Never author stage-level binding overrides (`rel material:binding = None` or rebinding) unless dynamically overriding an appearance variant.
3. **Componentize Fixtures**:
   - Ground planes, safety fences, and test stands must each have their own `.usd` file in `components/fixtures/` or `components/enclosure/`.
   - The root workspace must contain zero loose `materials/` directories.

---

## 3. Automated Validation Script

To verify all digital twin invariants before completing any modification, run:

```bash
python scratch/full_system_verification.py
```

Expected verification criteria:
- `[PASS] Unloaded bbox extents hint present`
- `[PASS] 0 Model hierarchy violations across all prims`
- `[PASS] Articulation root unified: exactly 1 root`
- `[PASS] IsaacRobotAPI validated: joints and links mapped`
- `[PASS] RobotStation EndEffector variants present`
- `[PASS] /World/Looks prim does not exist`
- `[PASS] 0 broken material bindings (surface & physics)`
