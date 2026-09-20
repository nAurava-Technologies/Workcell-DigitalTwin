# SimReady CAD Remediation Cheatsheet

A rapid triage reference for engineers and automation scripts encountering SimReady validation errors in OpenUSD assets.

---

## Quick Reference Index

| Error Code | Capability / Domain | Common Root Cause | Solution Summary |
| :--- | :--- | :--- | :--- |
| **`UN.007`** | Units & Scale | Stage `metersPerUnit` is missing or not `1.0` (e.g. `0.001` for mm). | Set `metersPerUnit = 1.0` and rescale geometry points. |
| **`UN.006`** | Coordinate Axis | Stage `upAxis` is missing or set to `"Y"`. | Set `upAxis = "Z"`. |
| **`AA.001`** | Asset Atomicity | Assets point to external AWS S3 or Nucleus URLs. | Download to local `./material/` or `./textures/` and repath relative. |
| **`NP.008`** | Path Resolution | Asset paths contain hardcoded absolute paths or unresolvable URIs. | Rewrite to clean relative paths `./...`. |
| **`VM.TEX.002`** | Texture Color Space | `inputs:diffuse_texture` missing `colorSpace` or incorrectly set. | Explicitly author `colorSpace = "raw"`. |
| **`VM.MDL.001`** | MDL Shader | Shaders point to missing or remote `.mdl` files. | Bundle `OmniPBR.mdl` locally in `./material/`. |
| **`PMT.001`** | Physics Material | Colliders lack a bound `UsdPhysics.MaterialAPI`. | Create physics material with friction/restitution and bind to collider. |
| **`GSP.001`** | Grasp Affordance | Prop missing vision-guided grasp curve. | Author `UsdGeom.BasisCurves` linear grasp vector. |
| **`RB.COL.001`** | Collision Scope | `UsdPhysics.CollisionAPI` applied to an `Xform` prim. | Remove from `Xform`, apply only to leaf `UsdGeom.Mesh`. |
| **`RB.007`** | Rigid Body Mass | Rigid body has zero or missing mass properties. | Apply `UsdPhysics.MassAPI` with positive mass in kg. |
| **`HI.010`** | Model Hierarchy | Missing `kind = "component"` on root prim. | Author `Usd.ModelAPI(root).SetKind(Kind.Tokens.component)`. |
| **`SR.001`** | SimReady Metadata | Missing `SimReady_Metadata` dictionary in `customLayerData`. | Author required dictionary in layer root. |

---

## 1. Units & Axis (`UN.007`, `UN.006`)

```python
from pxr import Usd, UsdGeom

def fix_units_and_axis(stage_path: str, scale_points: bool = False, scale_factor: float = 0.001):
    stage = Usd.Stage.Open(stage_path)
    
    # 1. Author Stage Metadata
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    
    # 2. Rescale raw CAD geometry points (e.g. from mm to meters)
    if scale_points:
        for prim in stage.Traverse():
            if prim.IsA(UsdGeom.Mesh):
                mesh = UsdGeom.Mesh(prim)
                points_attr = mesh.GetPointsAttr()
                pts = points_attr.Get()
                if pts:
                    scaled_pts = [p * scale_factor for p in pts]
                    points_attr.Set(scaled_pts)
                    
    stage.GetRootLayer().Save()
    print("Units set to 1.0m, upAxis set to Z.")
```

---

## 2. Physics Materials (`PMT.001`)

```python
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf

def bind_physics_material(stage_path: str, material_scope: str = "/World/material"):
    stage = Usd.Stage.Open(stage_path)
    mat_path = f"{material_scope}/SteelPhysicsMaterial"
    
    # Create or get physics material prim
    mat_prim = stage.DefinePrim(Sdf.Path(mat_path), "Material")
    phys_mat = UsdPhysics.MaterialAPI.Apply(mat_prim)
    phys_mat.CreateStaticFrictionAttr().Set(0.6)
    phys_mat.CreateDynamicFrictionAttr().Set(0.5)
    phys_mat.CreateRestitutionAttr().Set(0.1)
    
    # Bind to all collision meshes
    shade_material = UsdShade.Material(mat_prim)
    for prim in stage.Traverse():
        if prim.HasAPI(UsdPhysics.CollisionAPI):
            binding_api = UsdShade.MaterialBindingAPI.Apply(prim)
            binding_api.Bind(shade_material, UsdShade.Tokens.strongerThanDescendants, "physics")
            
    stage.GetRootLayer().Save()
    print(f"Physics material bound at {mat_path}.")
```

---

## 3. Atomic Assets & S3 Purging (`AA.001`, `NP.008`)

```python
from pxr import Usd, Sdf

def purge_remote_s3_and_localize(stage_path: str):
    stage = Usd.Stage.Open(stage_path)
    
    for prim in stage.Traverse():
        for attr in prim.GetAttributes():
            # Check for asset paths pointing to remote HTTP/S3
            val = attr.Get()
            if isinstance(val, Sdf.AssetPath):
                path_str = val.path
                if "http://" in path_str or "https://" in path_str or "s3://" in path_str:
                    filename = path_str.split("/")[-1].split("?")[0]
                    local_rel_path = f"./material/{filename}"
                    attr.Set(Sdf.AssetPath(local_rel_path))
                    print(f"Repathed {attr.GetPath()} -> {local_rel_path}")
                
                # CRITICAL TRAP: Purge hidden S3 URLs in customData['default']
                custom_data = attr.GetCustomData()
                if "default" in custom_data:
                    def_val = str(custom_data["default"])
                    if "http://" in def_val or "s3://" in def_val:
                        del custom_data["default"]
                        attr.SetCustomData(custom_data)
                        print(f"Purged S3 customData['default'] on {attr.GetPath()}")

    stage.GetRootLayer().Save()
```

---

## 4. Texture Color Spaces (`VM.TEX.002`)

```python
from pxr import Usd, UsdShade, Sdf

def fix_texture_colorspaces(stage_path: str):
    stage = Usd.Stage.Open(stage_path)
    
    for prim in stage.Traverse():
        if prim.IsA(UsdShade.Shader):
            for attr in prim.GetAttributes():
                name = attr.GetName()
                if name.startswith("inputs:") and ("texture" in name or "map" in name):
                    # Set colorSpace = "raw" for generic / normal / roughness textures
                    # Keep "sRGB" only if strictly designated as standard diffuse
                    attr.SetColorSpace("raw")
                    print(f"Set colorSpace='raw' on {attr.GetPath()}")
                    
    stage.GetRootLayer().Save()
```

---

## 5. Collision Prim Placement (`RB.COL.001`, `RB.COL.002`)

```python
from pxr import Usd, UsdGeom, UsdPhysics

def fix_collider_placement(stage_path: str):
    stage = Usd.Stage.Open(stage_path)
    
    for prim in stage.Traverse():
        # Check if an Xform incorrectly has CollisionAPI
        if prim.IsA(UsdGeom.Xform) and prim.HasAPI(UsdPhysics.CollisionAPI):
            print(f"Found illegal CollisionAPI on Xform: {prim.GetPath()}. Relocating...")
            
            # Remove from Xform
            prim.RemoveAPI(UsdPhysics.CollisionAPI)
            if prim.HasAPI(UsdPhysics.MeshCollisionAPI):
                prim.RemoveAPI(UsdPhysics.MeshCollisionAPI)
                
            # Find or define child leaf Mesh to receive collision
            for child in prim.GetChildren():
                if child.IsA(UsdGeom.Mesh):
                    UsdPhysics.CollisionAPI.Apply(child)
                    mesh_col = UsdPhysics.MeshCollisionAPI.Apply(child)
                    mesh_col.CreateApproximationAttr().Set("convexHull")
                    print(f"Applied CollisionAPI to leaf Mesh: {child.GetPath()}")
                    break
                    
    stage.GetRootLayer().Save()
```

---

## 6. Robotic Grasp Affordance (`GSP.001`)

```python
from pxr import Usd, UsdGeom, Sdf, Vt, Gf

def author_grasp_curve(stage_path: str, asset_root_path: str):
    stage = Usd.Stage.Open(stage_path)
    curve_path = f"{asset_root_path}/grasp_identifier_01"
    
    curves = UsdGeom.BasisCurves.Define(stage, Sdf.Path(curve_path))
    curves.CreateTypeAttr().Set(UsdGeom.Tokens.linear)
    curves.CreateCurveVertexCountsAttr().Set(Vt.IntArray([2]))
    
    # 2 control points in meters defining approach/pinch vector (e.g. 10cm vector)
    pts = Vt.Vec3fArray([
        Gf.Vec3f(0.0, 0.0, 0.0),
        Gf.Vec3f(0.0, 0.0, 0.10)
    ])
    curves.CreatePointsAttr().Set(pts)
    
    # Author SimReady grasp semantic metadata
    prim = curves.GetPrim()
    prim.SetCustomDataByKey("simready:grasp:type", "parallel_jaw")
    
    stage.GetRootLayer().Save()
    print(f"Grasp curve authored at {curve_path}.")
```

---

## 7. Model Hierarchy & Metadata (`SR.001`, `HI.010`)

```python
from pxr import Usd, Kind, Sdf
import datetime

def author_simready_metadata(stage_path: str, asset_name: str, asset_type: str = "prop"):
    stage = Usd.Stage.Open(stage_path)
    root = stage.GetDefaultPrim()
    if not root:
        root = stage.GetPrimAtPath(f"/{asset_name}")
        stage.SetDefaultPrim(root)
        
    # 1. Author kind = component
    Usd.ModelAPI(root).SetKind(Kind.Tokens.component)
    
    # 2. Author customLayerData
    layer = stage.GetRootLayer()
    cdata = dict(layer.customLayerData) if layer.customLayerData else {}
    cdata["SimReady_Metadata"] = {
        "asset_name": asset_name,
        "asset_type": asset_type,
        "source_format": "CAD",
        "simready_version": "1.0.0",
        "usd_date_generated": datetime.datetime.utcnow().isoformat()
    }
    layer.customLayerData = cdata
    layer.Save()
    print(f"SimReady metadata authored for {asset_name}.")
```
