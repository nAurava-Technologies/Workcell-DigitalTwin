"""Assembly contracts, usable with standalone USD or Isaac Sim's USD bindings."""
from pathlib import Path
from pxr import Gf, Usd, UsdGeom, UsdPhysics

def _find_root():
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "workcell_digitaltwin.usd").exists() or (p / ".git").exists():
            return p
        p = p.parent
    return Path(__file__).resolve().parents[3]

ROOT = _find_root()
PEDESTAL = "/Robot_Base/Robot_Base/tn__Part1_f5/Mesh"


def check_station(stage, path):
    root = stage.GetPrimAtPath(path)
    variant = root.GetVariantSet("EndEffector").GetVariantSelection()
    tool = variant == "Robotiq_2F_85"
    joints = root.GetRelationship("isaac:physics:robotJoints").GetTargets()
    links = root.GetRelationship("isaac:physics:robotLinks").GetTargets()
    assert len(joints) == len(set(joints)) == (14 if tool else 7), "Joint mapping count/duplicates"
    assert len(links) == len(set(links)) == (16 if tool else 7), "Link mapping count/duplicates"
    for target in joints + links:
        assert target.HasPrefix(root.GetPath()), f"Nonlocal mapping: {target}"
        prim = stage.GetPrimAtPath(target)
        assert prim and prim.IsDefined(), f"Missing mapping: {target}"
        assert prim.IsA(UsdPhysics.Joint) if target in joints else prim.HasAPI(UsdPhysics.RigidBodyAPI), f"Wrong mapping type: {target}"
    for target in joints:
        prim = stage.GetPrimAtPath(target)
        for side in (0, 1):
            for body in prim.GetRelationship(f"physics:body{side}").GetTargets():
                assert body in links, f"Unmapped joint body: {body}"
    roots = [str(p.GetPath()) for p in Usd.PrimRange(root) if p.HasAPI(UsdPhysics.ArticulationRootAPI)]
    assert roots == [path + "/ur10/root_joint"], f"Articulation roots: {roots}"
    anchor = UsdPhysics.FixedJoint(stage.GetPrimAtPath(roots[0]))
    assert anchor and anchor.GetJointEnabledAttr().Get(), "Disabled or nonfixed world anchor"
    assert not anchor.GetBody0Rel().GetTargets(), "Root no longer anchored to world"
    assert anchor.GetBody1Rel().GetTargets() == [path + "/ur10/base_link"], "Wrong root link"
    pedestal = stage.GetPrimAtPath(path + PEDESTAL)
    assert pedestal.HasAPI(UsdPhysics.CollisionAPI), "Missing pedestal collider"
    assert UsdPhysics.CollisionAPI(pedestal).GetCollisionEnabledAttr().Get(), "Disabled pedestal collider"
    assert not any(p.HasAPI(UsdPhysics.RigidBodyAPI) for p in Usd.PrimRange(stage.GetPrimAtPath(path + "/Robot_Base"))), "Dynamic pedestal"
    mount = stage.GetPrimAtPath(path + "/ToolMountJoint")
    if tool:
        assert mount and mount.IsA(UsdPhysics.FixedJoint), "Missing tool mount"
        assert mount.GetRelationship("physics:body0").GetTargets() == [path + "/ur10/wrist_3_link"]
        assert mount.GetRelationship("physics:body1").GetTargets() == [path + "/Robotiq_2F_85/base_link"]
        frames = []
        for side in (0, 1):
            body = stage.GetPrimAtPath(mount.GetRelationship(f"physics:body{side}").GetTargets()[0])
            local = Gf.Matrix4d().SetRotate(Gf.Quatd(mount.GetAttribute(f"physics:localRot{side}").Get()))
            local.SetTranslateOnly(Gf.Vec3d(mount.GetAttribute(f"physics:localPos{side}").Get()))
            frames.append(local * UsdGeom.Xformable(body).ComputeLocalToWorldTransform(Usd.TimeCode.Default()))
        assert max(abs(frames[0][i][j] - frames[1][i][j]) for i in range(4) for j in range(4)) < 1e-5, "Tool mount frames differ"
        gripper = stage.GetPrimAtPath(path + "/Robotiq_2F_85")
        colliders = [p for p in Usd.PrimRange(gripper, Usd.TraverseInstanceProxies()) if p.HasAPI(UsdPhysics.CollisionAPI)]
        assert len(colliders) == 11 and all(p.IsA(UsdGeom.Mesh) for p in colliders), "Gripper collider regression"
    else:
        assert not (mount and mount.IsDefined()), "Unexpected tool mount"
        gripper = stage.GetPrimAtPath(path + "/Robotiq_2F_85")
        assert not (gripper and gripper.IsDefined()), "Unexpected gripper"
        if variant == "Vacuum_Gripper":
            assert root.GetAttribute("workcell:toolStatus").Get() == "placeholder", "Unlabelled vacuum placeholder"
    return {"variant": variant, "joint_count": len(joints), "link_count": len(links), "static_pedestal": True, "articulation_roots": roots}


def check_all_variants():
    results = {}
    for asset, path in (("components/robot_station/robot_station.usd", "/RobotStation"), ("workcell_digitaltwin.usd", "/World/RobotStation")):
        stage = Usd.Stage.Open(str(ROOT / asset))
        stage.SetEditTarget(stage.GetSessionLayer())
        variants = stage.GetPrimAtPath(path).GetVariantSet("EndEffector")
        assert set(variants.GetVariantNames()) == {"None", "Robotiq_2F_85", "Vacuum_Gripper"}
        for variant in variants.GetVariantNames():
            variants.SetVariantSelection(variant)
            results[asset + "/" + variant] = check_station(stage, path)
    return results


if __name__ == "__main__":
    import json
    print(json.dumps(check_all_variants(), indent=2))
