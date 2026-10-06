"""Run Robotiq variant and station checks in Isaac Sim, without saving USD assets.

Launch using Isaac Sim's python.bat. SIMREADY_FOUNDATION_ROOT may override the
neighboring SimReady installation. Reports preserve failures, not inferred passes.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--behavior", action="store_true")
    parser.add_argument("--behavior-only", action="store_true", help="Reuse validation only if USD hashes still match")
    args, _ = parser.parse_known_args()
    from isaacsim import SimulationApp
    app = SimulationApp({"headless": True})

from pxr import Gf, PhysxSchema, Sdf, Usd, UsdGeom, UsdPhysics, UsdShade, UsdUtils

def _find_root():
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "workcell_digitaltwin.usd").exists() or (p / ".git").exists():
            return p
        p = p.parent
    return Path(__file__).resolve().parents[3]

ROOT = _find_root()
ASSET_DIR = ROOT / "components/robot_station/Robotiq/2F-85/simready_isaac_usd"
ASSET = ASSET_DIR / "Robotiq_2F_85.usda"
FOUNDATION = Path(os.environ.get("SIMREADY_FOUNDATION_ROOT", ROOT.parent.parent / "SimReady/simready-foundation"))
OUTPUT = ROOT / "docs/simready/Robotiq_isaac_verification.json"


def save_report(report):
    """Publish complete JSON atomically; tolerate brief Windows reader locks."""
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    for attempt in range(10):
        try:
            temporary.replace(OUTPUT)
            return
        except OSError:
            if attempt == 9:
                raise
            time.sleep(0.2)


def structural(stage, gripper_path):
    gripper = stage.GetPrimAtPath(gripper_path)
    prims = list(Usd.PrimRange(gripper, Usd.TraverseInstanceProxies()))
    colliders = [p for p in prims if p.HasAPI(UsdPhysics.CollisionAPI)]
    moving = [p for p in prims if p.IsA(UsdPhysics.RevoluteJoint)]
    states = {str(p.GetPath()): bool(PhysxSchema.JointStateAPI(p, "angular")) for p in moving}
    invalid_targets = []
    for p in stage.Traverse():
        for rel in p.GetRelationships():
            if rel.GetName() in ("physics:body0", "physics:body1", "isaac:physics:robotJoints", "isaac:physics:robotLinks"):
                invalid_targets.extend(str(x) for x in rel.GetTargets() if not stage.GetPrimAtPath(x))
    frame_errors = {}
    for prim in prims:
        if not prim.IsA(UsdPhysics.Joint):
            continue
        frames = []
        for i in (0, 1):
            targets = prim.GetRelationship(f"physics:body{i}").GetTargets()
            if not targets:
                break
            body = stage.GetPrimAtPath(targets[0])
            local = Gf.Matrix4d().SetRotate(Gf.Quatd(prim.GetAttribute(f"physics:localRot{i}").Get()))
            local.SetTranslateOnly(Gf.Vec3d(prim.GetAttribute(f"physics:localPos{i}").Get()))
            frames.append(local * UsdGeom.Xformable(body).ComputeLocalToWorldTransform(Usd.TimeCode.Default()))
        if len(frames) == 2:
            frame_errors[str(prim.GetPath())] = max(abs(frames[0][i][j] - frames[1][i][j]) for i in range(4) for j in range(4))
    mapping = {}
    for owner in (gripper, stage.GetDefaultPrim()):
        if not owner:
            continue
        entry = {}
        for name in ("robotJoints", "robotLinks"):
            targets = owner.GetRelationship("isaac:physics:" + name).GetTargets()
            entry[name] = {"count": len(targets), "invalid_type": [str(x) for x in targets
                if not (stage.GetPrimAtPath(x).IsA(UsdPhysics.Joint) if name == "robotJoints"
                        else stage.GetPrimAtPath(x).HasAPI(UsdPhysics.RigidBodyAPI))]}
        mapping[str(owner.GetPath())] = entry
    return {
        "articulation_roots": [str(p.GetPath()) for p in stage.Traverse() if p.HasAPI(UsdPhysics.ArticulationRootAPI)],
        "mesh_colliders": sum(p.IsA(UsdGeom.Mesh) for p in colliders),
        "invalid_parent_colliders": [str(p.GetPath()) for p in colliders if p.IsA(UsdGeom.Xform)],
        "joint_state_api": states,
        "drives": [str(p.GetPath()) for p in moving if p.HasAPI(UsdPhysics.DriveAPI, "angular")],
        "invalid_joint_or_mapping_targets": invalid_targets,
        "mapping": mapping,
        "zero_state_joint_frame_matrix_errors": frame_errors,
        "mount_gap_m": mount_gap(stage) if stage.GetPrimAtPath("/RobotStation/ToolMountJoint") else None,
        "mimic": {str(p.GetPath()): {a.GetName(): a.Get() for a in p.GetAttributes() if "gearing" in a.GetName()}
                  for p in moving if p.HasAPI(PhysxSchema.PhysxMimicJointAPI)},
    }


def validate_all(report):
    # Append the Foundation packages only after Kit's USD/PhysX schemas are loaded.
    # Do not substitute the standalone pxr package for Isaac Sim's bindings.
    sys.path.append(str(FOUNDATION / ".venv/Lib/site-packages"))
    import omni
    from pkgutil import extend_path
    omni.__path__ = extend_path(omni.__path__, "omni")
    import simready.validate as sv
    from simready.validate.api import _validate_asset_with_profile, _build_features_validation_summary
    specs = FOUNDATION / "nv_core/sr_specs/docs"
    sv.initialize(rules_and_requirements_paths=[specs / "capabilities"],
                  features_paths=[specs / "features"], profiles_paths=[specs / "profiles/profiles.toml"])
    for scope, path, gripper_path in (
        ("standalone", ASSET, "/Robotiq_2F_85"),
        ("station", ROOT / "components/robot_station/robot_station.usd", "/RobotStation/Robotiq_2F_85"),
    ):
        stage = Usd.Stage.Open(str(path))
        stage.SetEditTarget(stage.GetSessionLayer())
        variants = stage.GetPrimAtPath(gripper_path).GetVariantSet("Physics")
        for variant in variants.GetVariantNames():
            variants.SetVariantSelection(variant)
            print(f"VALIDATING {scope} {variant}", flush=True)
            issues = _validate_asset_with_profile(stage, "Robot-Body-Isaac", "1.0.0")
            item = {"structure": structural(stage, gripper_path),
                    "features": _build_features_validation_summary(issues, "Robot-Body-Isaac", "1.0.0", True),
                    "raw_issue_count": len(issues),
                    "issues": list({(i.code, i.message, str(i.at), str(i.severity)):
                        {"code": i.code, "message": i.message, "at": str(i.at), "severity": str(i.severity)}
                        for i in issues}.values())}
            report["validation"][f"{scope}/{variant}"] = item
            save_report(report)
            print("VALIDATED", scope, variant, json.dumps(item["features"]), flush=True)


def run_behavior(report, scopes=("standalone", "station")):
    import math
    import carb
    import omni.physx
    import omni.physics.tensors as tensors
    settings = carb.settings.get_settings()
    settings.set_bool("/physics/updateToUsd", True)
    settings.set_bool("/physics/updateVelocitiesToUsd", True)
    sim = omni.physx.get_physx_simulation_interface()
    cache = UsdUtils.StageCache.Get()
    dt = 1 / 120

    def case(scope, variant):
        stage = Usd.Stage.CreateInMemory()
        UsdGeom.SetStageMetersPerUnit(stage, 1)
        UsdGeom.SetStageUpAxis(stage, "Z")
        mounted = scope == "station"
        path = "/RobotStation/Robotiq_2F_85" if mounted else "/Robotiq_2F_85"
        root = stage.DefinePrim("/RobotStation" if mounted else path)
        root.GetReferences().AddReference(str(ROOT / "components/robot_station/robot_station.usd" if mounted else ASSET))
        gripper = stage.GetPrimAtPath(path)
        gripper.GetVariantSet("Physics").SetVariantSelection(variant)
        if not mounted:
            mount = UsdPhysics.FixedJoint.Define(stage, "/TestMount")
            mount.CreateBody1Rel().SetTargets([path + "/base_link"])
        scene = UsdPhysics.Scene.Define(stage, "/TestScene")
        scene.CreateGravityDirectionAttr(Gf.Vec3f(1, 0, 0))
        scene.CreateGravityMagnitudeAttr(0)
        PhysxSchema.PhysxSceneAPI.Apply(scene.GetPrim()).CreateEnableGPUDynamicsAttr(False)
        # Isolate mechanism control from gravity while testing commanded movement.
        # The grasp phase later loads only the object, avoiding a change in arm posture.
        for prim in stage.Traverse():
            if prim.HasAPI(UsdPhysics.RigidBodyAPI):
                PhysxSchema.PhysxRigidBodyAPI.Apply(prim).CreateDisableGravityAttr(True)
        cube = UsdGeom.Cube.Define(stage, "/TestObject")
        cube.CreateSizeAttr(1)
        cube_pos = cube.AddTranslateOp()
        cube_orient = cube.AddOrientOp()
        cube.AddScaleOp().Set(Gf.Vec3f(0.016, 0.04, 0.07))
        cube_pos.Set(Gf.Vec3d(10, 10, 10))
        cube_orient.Set(Gf.Quatf(1))
        object_collision = UsdPhysics.CollisionAPI.Apply(cube.GetPrim())
        object_collision.CreateCollisionEnabledAttr(False)
        object_body = UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
        object_body.CreateKinematicEnabledAttr(True)
        UsdPhysics.MassAPI.Apply(cube.GetPrim()).CreateMassAttr(0.02)
        # A declared test counterpart, without changing the gripper's materials.
        material = UsdShade.Material.Define(stage, "/TestMaterial")
        pm = UsdPhysics.MaterialAPI.Apply(material.GetPrim())
        pm.CreateStaticFrictionAttr(0.8)
        pm.CreateDynamicFrictionAttr(0.8)
        pm.CreateRestitutionAttr(0)
        UsdShade.MaterialBindingAPI.Apply(cube.GetPrim()).Bind(material, materialPurpose="physics")
        stage_id = cache.Insert(stage)
        view = None
        result = {"dt_s": dt, "variant": variant, "scope": scope, "phases": {}}
        try:
            assert sim.attach_stage(stage_id.ToLongInt())
            # PhysX creates articulation handles on the first simulation step.
            sim.simulate(dt, 0)
            sim.fetch_results()
            view = tensors.create_simulation_view("numpy", stage_id.ToLongInt())
            art = view.create_articulation_view("/RobotStation/ur10/root_joint" if mounted else path)
            assert art.count == 1, f"Expected one articulation, got {art.count}"
            names = list(art.shared_metatype.dof_names)
            result["dof_names"] = names
            drive = UsdPhysics.DriveAPI(stage.GetPrimAtPath(path + "/Joints/finger_joint"), "angular")
            elapsed = dt

            def step(seconds):
                nonlocal elapsed
                for _ in range(round(seconds / dt)):
                    sim.simulate(dt, elapsed)
                    sim.fetch_results()
                    elapsed += dt
                    if round(elapsed / dt) % 120 == 0:
                        print("STEP", scope, variant, round(elapsed, 2), flush=True)
                omni.physx.get_physx_interface().update_transformations(False, True, True)

            def sample():
                q = dict(zip(names, [math.degrees(float(x)) for x in art.get_dof_positions()[0]]))
                tips = []
                for side in ("left", "right"):
                    body = stage.GetPrimAtPath(path + f"/{side}_inner_finger")
                    local = Gf.Vec3d(0, -0.048 if side == "left" else 0.048, 0.135)
                    tips.append(UsdGeom.Xformable(body).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).Transform(local))
                residuals = {}
                for joint in stage.GetPrimAtPath(path + "/Joints").GetChildren():
                    for api in PhysxSchema.PhysxMimicJointAPI.GetAll(joint):
                        ref = api.GetReferenceJointRel().GetTargets()[0].name
                        if joint.GetName() in q and ref in q:
                            residuals[joint.GetName()] = q[joint.GetName()] + api.GetGearingAttr().Get() * q[ref] + api.GetOffsetAttr().Get()
                return {"q_degrees": q, "tip_distance_m": (tips[0] - tips[1]).GetLength(),
                        "mimic_residual_degrees": residuals}

            for phase, target in (("open", 0), ("close", 35), ("reopen", 0), ("close_again", 35)):
                drive.GetTargetPositionAttr().Set(target)
                step(2)
                result["phases"][phase] = sample()
                print("PHASE", scope, variant, phase, json.dumps(result["phases"][phase]), flush=True)
            phases = result["phases"]
            result["open_close_pass"] = (phases["close"]["q_degrees"]["finger_joint"] > 25
                                          and abs(phases["reopen"]["q_degrees"]["finger_joint"]) < 3)
            result["synchronized_pass"] = (bool(phases["close"]["mimic_residual_degrees"])
                and max(abs(v) for p in phases.values() for v in p["mimic_residual_degrees"].values()) < 1)
            result["repeat_cycle_pass"] = abs(phases["close_again"]["q_degrees"]["finger_joint"] - phases["close"]["q_degrees"]["finger_joint"]) < 1
            # Hold a test coupon in place during acquisition, then remove that
            # support and apply a load tangent to the finger pads. No grasp joint.
            drive.GetTargetPositionAttr().Set(0)
            step(2)
            base = stage.GetPrimAtPath(path + "/base_link")
            base_tm = UsdGeom.Xformable(base).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
            object_start = base_tm.Transform(Gf.Vec3d(0, 0, 0.16))
            cube_pos.Set(object_start)
            cube_orient.Set(Gf.Quatf(base_tm.ExtractRotationQuat()))
            object_collision.GetCollisionEnabledAttr().Set(True)
            step(0.1)
            drive.GetTargetPositionAttr().Set(35)
            step(2)
            result["grasp_acquired"] = sample()
            object_body.GetKinematicEnabledAttr().Set(False)
            load_direction = base_tm.TransformDir(Gf.Vec3d(1, 0, 0)).GetNormalized()
            scene.GetGravityDirectionAttr().Set(Gf.Vec3f(load_direction))
            scene.GetGravityMagnitudeAttr().Set(9.81)
            step(1)
            held_pos = UsdGeom.Xformable(cube).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()
            held_drift = (held_pos - object_start).GetLength()
            result["grasp_hold_drift_m"] = held_drift
            result["grasp_hold_pass"] = held_drift < 0.01
            drive.GetTargetPositionAttr().Set(0)
            step(1)
            released_pos = UsdGeom.Xformable(cube).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()
            result["release_travel_m"] = Gf.Dot(released_pos - held_pos, load_direction)
            result["release_pass"] = result["release_travel_m"] > 0.1
            result["grasp_conditions"] = "20 g coupon 16 x 40 x 70 mm, friction 0.8, held kinematically during acquisition; then dynamic under 9.81 m/s^2 pad-tangent load; robot gravity disabled"
            # Release resources, then rebuild from the same authored asset as a hard reset.
            result["final_mount_gap_m"] = mount_gap(stage) if mounted else None
        finally:
            if view:
                view.invalidate()
            sim.detach_stage()
            cache.Erase(stage_id)
        return result

    for scope in scopes:
        for variant in ("Physx_Mimic", "Physx_Loop", "Physics"):
            key = f"{scope}/{variant}"
            print("SIMULATING", key, flush=True)
            try:
                first = case(scope, variant)
                reset = case(scope, variant)
                first["reset_reproducible_pass"] = abs(first["phases"]["close"]["q_degrees"]["finger_joint"] - reset["phases"]["close"]["q_degrees"]["finger_joint"]) < 0.5
                report["behavior"][key] = first
            except Exception:
                report["behavior"][key] = {"error": traceback.format_exc()}
            save_report(report)
            print("SIMULATED", key, json.dumps(report["behavior"][key]), flush=True)


def mount_gap(stage):
    prim = stage.GetPrimAtPath("/RobotStation/ToolMountJoint")
    frames = []
    for i in (0, 1):
        body = stage.GetPrimAtPath(prim.GetRelationship(f"physics:body{i}").GetTargets()[0])
        transform = UsdGeom.Xformable(body).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        frames.append(transform.Transform(Gf.Vec3d(prim.GetAttribute(f"physics:localPos{i}").Get())))
    return (frames[0] - frames[1]).GetLength()


def main():
    inputs = {p for p in ASSET_DIR.rglob("*") if p.suffix in (".usd", ".usda")}
    station = Usd.Stage.Open(str(ROOT / "components/robot_station/robot_station.usd"))
    inputs.update(Path(layer.realPath) for layer in station.GetUsedLayers() if layer.realPath)
    report = {"executed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "isaac_version": (Path(os.environ["ISAAC_PATH"]) / "VERSION").read_text().strip(),
              "physx_schema_available": True,
              "asset_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(inputs)},
              "validation": {}, "behavior": {}}
    try:
        previous = json.loads(OUTPUT.read_text()) if OUTPUT.exists() else None
        if args.behavior_only:
            assert previous, "Run validation first"
            assert previous["asset_sha256"] == report["asset_sha256"], "Revalidate changed assets first"
            report["validation"] = previous["validation"]
        else:
            validate_all(report)
            if previous and previous["asset_sha256"] == report["asset_sha256"] and not args.behavior:
                report["behavior"] = previous.get("behavior", {})
                report["behavior_executed_utc"] = previous.get("behavior_executed_utc", previous["executed_utc"])
                for key in ("behavior_asset_sha256", "formatting_equivalence"):
                    if key in previous:
                        report[key] = previous[key]
        if args.behavior or args.behavior_only:
            report["behavior_executed_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            run_behavior(report)
    except Exception:
        report["runner_error"] = traceback.format_exc()
        raise
    finally:
        save_report(report)


if __name__ == "__main__":
    try:
        main()
    finally:
        app.close()
