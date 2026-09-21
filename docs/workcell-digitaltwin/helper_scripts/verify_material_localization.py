import sys
from pxr import Usd, UsdShade, Sdf

def verify_materials():
    stage = Usd.Stage.Open("workcell_digitaltwin.usd")
    if not stage:
        print("ERROR: Failed to open workcell_digitaltwin.usd")
        sys.exit(1)

    print("Stage opened successfully.")

    # 1. Verify /World/Looks is gone
    looks_root = stage.GetPrimAtPath("/World/Looks")
    if looks_root.IsValid():
        print("FAIL: /World/Looks still exists on the composed stage!")
        sys.exit(1)
    else:
        print("PASS: /World/Looks does not exist on the composed stage.")

    # 2. Collect all bound materials and verify their locality
    direct_bindings = {}
    physics_bindings = {}
    broken_bindings = []

    for prim in stage.Traverse():
        bapi = UsdShade.MaterialBindingAPI(prim)
        # Check direct surface binding
        db = bapi.GetDirectBinding()
        mat = db.GetMaterial()
        rel = bapi.GetDirectBindingRel()
        if rel and rel.GetTargets():
            targets = rel.GetTargets()
            if not mat:
                broken_bindings.append((prim.GetPath(), targets, "surface"))
            else:
                direct_bindings[prim.GetPath()] = mat.GetPath()

        # Check physics material binding
        pb = bapi.GetDirectBinding("physics")
        pmat = pb.GetMaterial()
        prel = bapi.GetDirectBindingRel("physics")
        if prel and prel.GetTargets():
            ptargets = prel.GetTargets()
            if not pmat:
                broken_bindings.append((prim.GetPath(), ptargets, "physics"))
            else:
                physics_bindings[prim.GetPath()] = pmat.GetPath()

    if broken_bindings:
        print(f"FAIL: Found {len(broken_bindings)} broken material bindings:")
        for b in broken_bindings:
            print(f"  {b[0]} ({b[2]}) -> {b[1]}")
        sys.exit(1)
    else:
        print("PASS: 0 broken material bindings across entire stage.")

    print(f"\nTotal surface material bindings: {len(direct_bindings)}")
    print(f"Total physics material bindings: {len(physics_bindings)}")

    # 3. Verify component encapsulation (material belongs to component subtree or GroundPlane)
    non_local = []
    for prim_path, mat_path in direct_bindings.items():
        prim_str = str(prim_path)
        mat_str = str(mat_path)
        
        # Determine the owning component / root fixture
        # E.g. /World/Workcell/Left_Workcell_Fence_02/... -> /World/Workcell/Left_Workcell_Fence_02
        # E.g. /World/Table/... -> /World/Table
        # E.g. /World/GroundPlane -> /World/GroundPlane
        # E.g. /World/RobotStation/Robot_Base/... -> /World/RobotStation/Robot_Base
        if not mat_str.startswith(prim_str) and not prim_str.startswith(mat_str[:mat_str.rfind("/Looks")]):
            non_local.append((prim_path, mat_path))

    if non_local:
        print(f"FAIL: Found non-localized material bindings: {non_local}")
        sys.exit(1)
    else:
        print("PASS: 100% of material bindings are strictly localized within their component or GroundPlane hierarchy.")

    # 4. Verify GroundPlane material specifically
    gp_mat = direct_bindings.get(Sdf.Path("/World/GroundPlane"))
    if gp_mat == Sdf.Path("/World/GroundPlane/Looks/Chalk_Paint_Pebbles_Charcoal_Blue"):
        print(f"PASS: GroundPlane binds locally to {gp_mat}")
    else:
        print(f"FAIL: GroundPlane binding is {gp_mat}")
        sys.exit(1)

    # 5. Verify Table roughness texture colorSpace
    table_stage = Usd.Stage.Open("components/fixtures/table/Table.usd")
    table_attr = table_stage.GetPrimAtPath("/Table/Looks/White_Strong_Metallic/Shader").GetAttribute("inputs:roughness_texture")
    if table_attr.GetMetadata("colorSpace") in ("auto", "raw"):
        print(f"PASS: Table roughness_texture colorSpace is '{table_attr.GetMetadata('colorSpace')}'.")
    else:
        print(f"FAIL: Table roughness_texture colorSpace is {table_attr.GetMetadata('colorSpace')}")
        sys.exit(1)

    # 6. Verify Bin roughness texture
    bin_stage = Usd.Stage.Open("components/fixtures/bin/Bin.usd")
    bin_attr = bin_stage.GetPrimAtPath("/Bin/Looks/Graphite_Metallic/Shader").GetAttribute("inputs:roughness_texture")
    if bin_attr.IsValid() and bin_attr.GetMetadata("colorSpace") == "raw":
        print(f"PASS: Bin roughness_texture is authored with value {bin_attr.Get()} and colorSpace 'raw'.")
    else:
        print(f"FAIL: Bin roughness_texture missing or invalid: {bin_attr}")
        sys.exit(1)

    # 7. Print all active materials
    print("\n=== VERIFIED BOUND MATERIALS SUMMARY ===")
    for prim_path, mat_path in sorted(direct_bindings.items()):
        print(f"  {prim_path} -> {mat_path}")

    print("\nALL MATERIAL LOCALIZATION AUDIT CHECKS PASSED!")

if __name__ == "__main__":
    verify_materials()
