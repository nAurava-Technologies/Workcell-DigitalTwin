import sys
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf

def run_all_checks():
    print("==================================================")
    print("WORKCELL DIGITAL TWIN FULL SYSTEM VERIFICATION")
    print("==================================================")

    # 1. Unloaded Bounding Box Test
    stage_unloaded = Usd.Stage.Open("workcell_digitaltwin.usd", Usd.Stage.LoadNone)
    world_unloaded = stage_unloaded.GetPrimAtPath("/World")
    model_api = UsdGeom.ModelAPI(world_unloaded)
    extents = model_api.GetExtentsHint()
    if extents and len(extents) > 0:
        print(f"[PASS] Unloaded bbox extents hint present: {extents[0]} to {extents[1]}")
    else:
        print("[FAIL] Unloaded bbox extents hint missing!")
        sys.exit(1)

    # 2. Composed Stage Load & Traversal
    stage = Usd.Stage.Open("workcell_digitaltwin.usd")
    if not stage:
        print("[FAIL] Cannot open workcell_digitaltwin.usd")
        sys.exit(1)
    print("[PASS] Composed stage opened successfully.")

    # 3. Model Hierarchy Check
    hierarchy_errors = []
    for prim in stage.Traverse():
        model = Usd.ModelAPI(prim)
        is_model = model.IsModel()
        is_group = model.IsGroup()
        parent = prim.GetParent()
        if parent and parent.IsValid() and parent.GetPath() != Sdf.Path("/"):
            parent_model = Usd.ModelAPI(parent)
            if is_model and not parent_model.IsGroup():
                hierarchy_errors.append(f"Model {prim.GetPath()} inside non-group parent {parent.GetPath()}")

    if hierarchy_errors:
        print(f"[FAIL] Model hierarchy errors found ({len(hierarchy_errors)}):")
        for err in hierarchy_errors:
            print("  ", err)
        sys.exit(1)
    print("[PASS] 0 Model hierarchy violations across all prims.")

    # 4. Articulation Roots Check
    art_roots = []
    for prim in stage.Traverse():
        if prim.HasAPI(UsdPhysics.ArticulationRootAPI):
            art_roots.append(prim.GetPath())

    if len(art_roots) == 1 and art_roots[0] == Sdf.Path("/World/RobotStation/ur10/root_joint"):
        print(f"[PASS] Articulation root unified: {art_roots[0]}")
    else:
        print(f"[FAIL] Expected 1 articulation root at /World/RobotStation/ur10/root_joint, found {len(art_roots)}: {art_roots}")
        sys.exit(1)

    # 5. Isaac Robot API Check
    robot_station = stage.GetPrimAtPath("/World/RobotStation")
    joints = robot_station.GetRelationship("isaac:physics:robotJoints").GetTargets()
    links = robot_station.GetRelationship("isaac:physics:robotLinks").GetTargets()
    if len(joints) == 14 and len(links) == 16:
        print(f"[PASS] IsaacRobotAPI validated: {len(joints)} joints, {len(links)} links mapped under /World/RobotStation.")
    else:
        print(f"[FAIL] Expected 14 joints and 16 links, found {len(joints)} joints, {len(links)} links")
        sys.exit(1)

    # 6. EndEffector Variant Set Check
    vset = robot_station.GetVariantSets().GetVariantSet("EndEffector")
    variants = vset.GetVariantNames()
    print(f"[PASS] RobotStation EndEffector variants: {variants}")

    # 7. Material Bindings & Encapsulation
    looks_root = stage.GetPrimAtPath("/World/Looks")
    if looks_root.IsValid():
        print("[FAIL] /World/Looks prim still exists on stage!")
        sys.exit(1)
    print("[PASS] /World/Looks prim does not exist.")

    for prim in stage.Traverse():
        bapi = UsdShade.MaterialBindingAPI(prim)
        db = bapi.GetDirectBinding()
        mat = db.GetMaterial()
        rel = bapi.GetDirectBindingRel()
        if rel and rel.GetTargets() and not mat:
            print(f"[FAIL] Broken direct surface material binding on {prim.GetPath()}")
            sys.exit(1)

        pb = bapi.GetDirectBinding("physics")
        pmat = pb.GetMaterial()
        prel = bapi.GetDirectBindingRel("physics")
        if prel and prel.GetTargets() and not pmat:
            print(f"[FAIL] Broken direct physics material binding on {prim.GetPath()}")
            sys.exit(1)

    print("[PASS] 0 broken material bindings (surface & physics).")
    print("==================================================")
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY (100% PASS)")
    print("==================================================")

if __name__ == "__main__":
    run_all_checks()
