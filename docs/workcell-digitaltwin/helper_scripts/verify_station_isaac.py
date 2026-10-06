"""Isaac Sim python.bat runner. Uses session edits; never saves source USDs."""
import datetime
import hashlib
import json
from pathlib import Path
import traceback
from isaacsim import SimulationApp

app = SimulationApp({"headless": True})
from pxr import Gf, PhysxSchema, Usd, UsdGeom, UsdPhysics, UsdUtils
import carb
import omni.physx
import verify_robotiq_isaac as gripper
from station_checks import ROOT, PEDESTAL, check_all_variants

OUTPUT = ROOT / "docs/simready/RobotStation_isaac_verification.json"


def anchor_case(asset, path):
    stage = Usd.Stage.Open(str(ROOT / asset))
    stage.SetEditTarget(stage.GetSessionLayer())
    scenes = [p for p in stage.Traverse() if p.IsA(UsdPhysics.Scene)]
    scene = UsdPhysics.Scene(scenes[0]) if scenes else UsdPhysics.Scene.Define(stage, "/AnchorTestScene")
    scene.CreateGravityDirectionAttr(Gf.Vec3f(0, 0, -1))
    scene.CreateGravityMagnitudeAttr(9.81)
    PhysxSchema.PhysxSceneAPI.Apply(scene.GetPrim()).CreateEnableGPUDynamicsAttr(False)
    for prim in stage.Traverse():
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            PhysxSchema.PhysxRigidBodyAPI.Apply(prim).CreateDisableGravityAttr(False)
    tracked = [path + "/ur10/base_link", path + PEDESTAL]
    def matrices():
        return [UsdGeom.Xformable(stage.GetPrimAtPath(p)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()) for p in tracked]
    initial = matrices()
    states = {str(p.GetPath()): bool(PhysxSchema.JointStateAPI(p, "angular")) for p in Usd.PrimRange(stage.GetPrimAtPath(path)) if p.IsA(UsdPhysics.RevoluteJoint)}
    cache = UsdUtils.StageCache.Get()
    stage_id = cache.Insert(stage)
    sim = omni.physx.get_physx_simulation_interface()
    max_error = [0., 0.]
    max_position = [0., 0.]
    try:
        assert sim.attach_stage(stage_id.ToLongInt())
        # Sample every step, including initial PhysX creation: catches root snapping.
        for step in range(360):
            sim.simulate(1 / 120, step / 120)
            sim.fetch_results()
            omni.physx.get_physx_interface().update_transformations(False, True, True)
            for index, current in enumerate(matrices()):
                max_error[index] = max(max_error[index], max(abs(current[i][j] - initial[index][i][j]) for i in range(4) for j in range(4)))
                max_position[index] = max(max_position[index], (current.ExtractTranslation() - initial[index].ExtractTranslation()).GetLength())
        return {"duration_s": 3, "gravity_m_s2": 9.81, "tracked": tracked,
                "initial_positions_m": [list(m.ExtractTranslation()) for m in initial],
                "max_matrix_error": max_error, "max_position_drift_m": max_position,
                "joint_state_api": states, "pass": max(max_error) < 1e-5 and all(states.values())}
    finally:
        sim.detach_stage()
        cache.Erase(stage_id)


def main():
    report = {"executed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "physx_schema_available": True, "validation": {}, "behavior": {}, "anchoring": {}}
    # Include transitive USD layers, station overrides and full-workcell layout.
    files = set()
    for asset in ("components/robot_station/robot_station.usd", "workcell_digitaltwin.usd"):
        stage = Usd.Stage.Open(str(ROOT / asset))
        files.update(Path(layer.realPath) for layer in stage.GetUsedLayers() if layer.realPath)
    files.update(gripper.ASSET_DIR.rglob("*.usda"))
    report["input_sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    try:
        report["assembly_contracts"] = check_all_variants()
        carb.settings.get_settings().set_bool("/physics/updateToUsd", True)
        for asset, path in (("components/robot_station/robot_station.usd", "/RobotStation"), ("workcell_digitaltwin.usd", "/World/RobotStation")):
            report["anchoring"][asset] = [anchor_case(asset, path) for _ in range(2)]
            print("ANCHOR", asset, json.dumps(report["anchoring"][asset]), flush=True)
        gripper.OUTPUT = OUTPUT
        gripper.validate_all(report)
        gripper.run_behavior(report, scopes=("station",))
        intended = [report["behavior"].get("station/" + v, {}) for v in ("Physx_Mimic", "Physx_Loop")]
        report["acceptance_pass"] = all(item["pass"] for runs in report["anchoring"].values() for item in runs) and all(
            all(item.get(key) for key in ("grasp_hold_pass", "release_pass", "reset_reproducible_pass", "open_close_pass", "synchronized_pass", "repeat_cycle_pass"))
            and not item.get("error") for item in intended)
        assert report["acceptance_pass"], "Station runtime acceptance failed; see report"
    except Exception:
        report["runner_error"] = traceback.format_exc()
        raise
    finally:
        gripper.OUTPUT = OUTPUT
        gripper.save_report(report)


if __name__ == "__main__":
    try:
        main()
    finally:
        app.close()
