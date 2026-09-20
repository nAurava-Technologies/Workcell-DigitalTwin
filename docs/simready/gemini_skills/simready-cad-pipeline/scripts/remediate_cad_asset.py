#!/usr/bin/env python3
"""
SimReady CAD-to-SimReady Remediation Pipeline CLI
-------------------------------------------------
Automates the 8-step engineering remediation pipeline on an OpenUSD asset
to bring it into full compliance with the SimReady Prop-Robotics-Neutral specification.

Usage:
  python remediate_cad_asset.py path/to/raw_asset.usd [--output path/to/remediated.usd] [--scale-points]
"""

import argparse
import datetime
import os
import sys
import warnings
from pathlib import Path

# Suppress harmless coroutine warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdPhysics, UsdShade, Vt
except ImportError as e:
    print(f"Error: OpenUSD (pxr) Python libraries not found: {e}", file=sys.stderr)
    print("Please execute this script within the SimReady Python environment.", file=sys.stderr)
    sys.exit(1)


def remediate_asset(
    usd_path: Path,
    output_path: Path = None,
    scale_points: bool = False,
    scale_factor: float = 0.001,
    asset_name: str = None,
    asset_type: str = "prop",
    default_mass: float = 10.0
) -> Path:
    if not usd_path.is_file():
        raise FileNotFoundError(f"USD asset not found: {usd_path}")

    target_file = output_path if output_path else usd_path
    if output_path and output_path != usd_path:
        import shutil
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(usd_path, output_path)

    stage = Usd.Stage.Open(str(target_file))
    if not stage:
        raise RuntimeError(f"Failed to open USD stage: {target_file}")

    print(f"[*] Beginning SimReady remediation for: {target_file}")

    # -------------------------------------------------------------------------
    # STEP 1: Normalize Stage Units & Axis (UN.006, UN.007)
    # -------------------------------------------------------------------------
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    print("  [✓] Stage metadata normalized: metersPerUnit=1.0, upAxis=Z")

    if scale_points:
        print(f"  [*] Rescaling geometry points by factor {scale_factor} (mm -> meters)...")
        for prim in stage.Traverse():
            if prim.IsA(UsdGeom.Mesh):
                mesh = UsdGeom.Mesh(prim)
                pts_attr = mesh.GetPointsAttr()
                pts = pts_attr.Get()
                if pts:
                    scaled_pts = [p * scale_factor for p in pts]
                    pts_attr.Set(scaled_pts)
        print("  [✓] Mesh vertex coordinates scaled.")

    # -------------------------------------------------------------------------
    # STEP 2: Hierarchy & SimReady Metadata (HI.001, HI.002, SR.001)
    # -------------------------------------------------------------------------
    root_prim = stage.GetDefaultPrim()
    if not root_prim or not root_prim.IsValid():
        # Fallback to first non-class root prim
        for prim in stage.GetPseudoRoot().GetChildren():
            if prim.GetName() != "Looks" and not prim.GetName().startswith("_"):
                root_prim = prim
                break
        if root_prim:
            stage.SetDefaultPrim(root_prim)

    if root_prim:
        model_api = Usd.ModelAPI(root_prim)
        model_api.SetKind(Kind.Tokens.component)
        print(f"  [✓] Root prim '{root_prim.GetPath()}' set as defaultPrim with kind='component'")

    # Author SimReady Layer Metadata
    layer = stage.GetRootLayer()
    cdata = dict(layer.customLayerData) if layer.customLayerData else {}
    name = asset_name if asset_name else (root_prim.GetName() if root_prim else usd_path.stem)
    cdata["SimReady_Metadata"] = {
        "asset_name": name,
        "asset_type": asset_type,
        "simready_version": "1.0.0",
        "source_format": "CAD",
        "usd_date_remediated": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    layer.customLayerData = cdata
    print(f"  [✓] Authored SimReady_Metadata for asset '{name}'")

    # -------------------------------------------------------------------------
    # STEP 3 & 4: Localize Dependencies, Purge Ghost URLs & Normalize Colorspaces
    # (AA.001, NP.008, VM.TEX.002)
    # -------------------------------------------------------------------------
    for prim in stage.Traverse():
        # Purge ghost S3 URLs from attribute customData
        for attr in prim.GetAttributes():
            custom_data = attr.GetCustomData()
            if "default" in custom_data:
                def_str = str(custom_data["default"])
                if any(p in def_str for p in ["http://", "https://", "s3://", "omniverse://"]):
                    del custom_data["default"]
                    attr.SetCustomData(custom_data)
                    print(f"  [✓] Purged ghost S3 URL in customData['default'] on {attr.GetPath()}")

        # Fix texture color spaces on shaders
        if prim.IsA(UsdShade.Shader):
            for attr in prim.GetAttributes():
                aname = attr.GetName()
                if aname.startswith("inputs:") and ("texture" in aname or "map" in aname):
                    # Enforce raw for non-sRGB channels or auto channels
                    current_cs = attr.GetColorSpace()
                    if current_cs in ["auto", "", None]:
                        attr.SetColorSpace("raw")
                        print(f"  [✓] Set colorSpace='raw' on texture attribute {attr.GetPath()}")

    # -------------------------------------------------------------------------
    # STEP 5 & 6: Rigid Body Dynamics, Mass & Clean Leaf Colliders
    # (RB.001, RB.007, RB.COL.001, RB.COL.002)
    # -------------------------------------------------------------------------
    # 5a. Ensure collider APIs are on leaf Meshes, NOT Xforms
    for prim in stage.Traverse():
        if prim.IsA(UsdGeom.Xform) and prim.HasAPI(UsdPhysics.CollisionAPI):
            print(f"  [*] Relocating misplaced CollisionAPI from Xform '{prim.GetPath()}' to leaf Mesh...")
            prim.RemoveAPI(UsdPhysics.CollisionAPI)
            if prim.HasAPI(UsdPhysics.MeshCollisionAPI):
                prim.RemoveAPI(UsdPhysics.MeshCollisionAPI)
            for child in prim.GetChildren():
                if child.IsA(UsdGeom.Mesh):
                    UsdPhysics.CollisionAPI.Apply(child)
                    mcol = UsdPhysics.MeshCollisionAPI.Apply(child)
                    mcol.CreateApproximationAttr().Set("convexHull")
                    print(f"  [✓] Applied CollisionAPI to child leaf Mesh: '{child.GetPath()}'")

    # 5b. Ensure at least one rigid body exists with mass
    has_rigid_body = any(prim.HasAPI(UsdPhysics.RigidBodyAPI) for prim in stage.Traverse())
    if not has_rigid_body and root_prim:
        print(f"  [*] Applying UsdPhysics.RigidBodyAPI on root prim '{root_prim.GetPath()}'")
        rb = UsdPhysics.RigidBodyAPI.Apply(root_prim)
        rb.CreateRigidBodyEnabledAttr().Set(True)

    for prim in stage.Traverse():
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            mass_api = UsdPhysics.MassAPI.Apply(prim)
            mass_attr = mass_api.GetMassAttr()
            if not mass_attr or mass_attr.Get() is None or mass_attr.Get() <= 0:
                mass_api.CreateMassAttr().Set(default_mass)
                print(f"  [✓] Authored default mass ({default_mass} kg) on '{prim.GetPath()}'")

    # -------------------------------------------------------------------------
    # STEP 7: Physics Material Binding (PMT.001)
    # -------------------------------------------------------------------------
    # Check if a physics material is needed
    colliders = [prim for prim in stage.Traverse() if prim.HasAPI(UsdPhysics.CollisionAPI)]
    if colliders:
        material_scope_path = f"{root_prim.GetPath()}/material" if root_prim else "/World/material"
        phys_mat_path = Sdf.Path(f"{material_scope_path}/DefaultPhysicsMaterial")

        phys_mat_prim = stage.GetPrimAtPath(phys_mat_path)
        if not phys_mat_prim or not phys_mat_prim.IsValid():
            phys_mat_prim = stage.DefinePrim(phys_mat_path, "Material")
            papi = UsdPhysics.MaterialAPI.Apply(phys_mat_prim)
            papi.CreateStaticFrictionAttr().Set(0.6)
            papi.CreateDynamicFrictionAttr().Set(0.5)
            papi.CreateRestitutionAttr().Set(0.1)
            print(f"  [✓] Defined default physics material at '{phys_mat_path}'")

        phys_mat = UsdShade.Material(phys_mat_prim)
        for col_prim in colliders:
            mb_api = UsdShade.MaterialBindingAPI.Apply(col_prim)
            direct_phys = mb_api.GetDirectBinding("physics")
            if not direct_phys.GetMaterial():
                mb_api.Bind(phys_mat, UsdShade.Tokens.strongerThanDescendants, "physics")
                print(f"  [✓] Bound physics material to collider '{col_prim.GetPath()}'")

    # -------------------------------------------------------------------------
    # STEP 8: Grasp Affordance Curve (GSP.001)
    # -------------------------------------------------------------------------
    if root_prim:
        grasp_path = Sdf.Path(f"{root_prim.GetPath()}/grasp_identifier_01")
        if not stage.GetPrimAtPath(grasp_path).IsValid():
            curves = UsdGeom.BasisCurves.Define(stage, grasp_path)
            curves.CreateTypeAttr().Set(UsdGeom.Tokens.linear)
            curves.CreateCurveVertexCountsAttr().Set(Vt.IntArray([2]))
            pts = Vt.Vec3fArray([
                Gf.Vec3f(0.0, 0.0, 0.0),
                Gf.Vec3f(0.0, 0.0, 0.10)
            ])
            curves.CreatePointsAttr().Set(pts)
            curves.GetPrim().SetCustomDataByKey("simready:grasp:type", "parallel_jaw")
            print(f"  [✓] Authored grasp affordance guide curve at '{grasp_path}'")

    # Save changes
    stage.GetRootLayer().Save()
    print(f"[✓] Remediation completed and saved to: {target_file}")
    return target_file


def main():
    parser = argparse.ArgumentParser(description="Remediate raw CAD OpenUSD assets for SimReady compliance.")
    parser.add_argument("usd_path", type=str, help="Path to the input USD asset.")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output USD file path (default: in-place).")
    parser.add_argument("--scale-points", "-s", action="store_true", help="Rescale vertex points (e.g. mm to meters).")
    parser.add_argument("--scale-factor", type=float, default=0.001, help="Point scale factor (default: 0.001).")
    parser.add_argument("--asset-name", type=str, default=None, help="Explicit asset name.")
    parser.add_argument("--asset-type", type=str, default="prop", help="Asset type (default: 'prop').")
    parser.add_argument("--mass", type=float, default=10.0, help="Default mass in kg (default: 10.0).")
    args = parser.parse_args()

    usd_path = Path(args.usd_path).resolve()
    output_path = Path(args.output).resolve() if args.output else None

    remediate_asset(
        usd_path=usd_path,
        output_path=output_path,
        scale_points=args.scale_points,
        scale_factor=args.scale_factor,
        asset_name=args.asset_name,
        asset_type=args.asset_type,
        default_mass=args.mass
    )


if __name__ == "__main__":
    main()
