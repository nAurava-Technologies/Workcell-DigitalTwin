"""Fresh Neutral-profile evidence using Isaac Sim's real PhysxSchema bindings.

Run with Isaac Sim python.bat. No source USD layers are saved. Raw feature
failures are retained, including floor profile mismatches and diagnostic modes.
"""
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path
from isaacsim import SimulationApp

app = SimulationApp({"headless": True})
from pxr import PhysxSchema, Usd
from station_checks import ROOT
from verify_robotiq_isaac import FOUNDATION

OUTPUT = ROOT / "docs/simready/neutral_profile_verification.json"


def main():
    sys.path.append(str(FOUNDATION / ".venv/Lib/site-packages"))
    import omni
    from pkgutil import extend_path
    omni.__path__ = extend_path(omni.__path__, "omni")
    import simready.validate as sv
    from simready.validate.api import _validate_asset_with_profile, _build_features_validation_summary
    specs = FOUNDATION / "nv_core/sr_specs/docs"
    sv.initialize(rules_and_requirements_paths=[specs / "capabilities"],
                  features_paths=[specs / "features"], profiles_paths=[specs / "profiles/profiles.toml"])
    report = {"executed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "isaac_version": (Path(os.environ["ISAAC_PATH"]) / "VERSION").read_text().strip(),
              "physx_schema_available": bool(PhysxSchema.JointStateAPI), "cases": {}}
    assets = [
        "components/fixtures/bin/Bin.usd", "components/fixtures/table/Table.usd",
        "components/robot_station/robot_base/Robot_Base.usd", "components/enclosure/Workcell_Wall.usd",
        "components/xray_scanner/xray_scanner.usd", "components/ev_battery_pack/EVBatteryPack.usd",
        "components/conveyor/conveyor.usd", "components/fixtures/ground_plane/GroundPlane.usd",
        "components/robot_station/ur10/simready_usd/ur10.usda",
        "components/robot_station/Robotiq/2F-85/simready_isaac_usd/Robotiq_2F_85.usda",
        "components/robot_station/robot_station.usd"]
    try:
        for index, asset in enumerate(assets):
            stage = Usd.Stage.Open(str(ROOT / asset))
            stage.SetEditTarget(stage.GetSessionLayer())
            profile = "Prop-Robotics-Neutral" if index < 8 else "Robot-Body-Neutral"
            gripper_path = "/Robotiq_2F_85" if index == 9 else "/RobotStation/Robotiq_2F_85"
            variants = stage.GetPrimAtPath(gripper_path).GetVariantSet("Physics") if index >= 9 else None
            for variant in variants.GetVariantNames() if variants else ["default"]:
                if variants:
                    variants.SetVariantSelection(variant)
                issues = _validate_asset_with_profile(stage, profile, "1.0.0")
                features = _build_features_validation_summary(issues, profile, "1.0.0", True)
                key = asset + "/" + variant
                report["cases"][key] = {
                    "profile": profile, "version": "1.0.0", "features": features,
                    "input_sha256": {str(Path(l.realPath).relative_to(ROOT)): hashlib.sha256(Path(l.realPath).read_bytes()).hexdigest()
                                     for l in stage.GetUsedLayers() if l.realPath},
                    "issues": list({(i.code, i.message, str(i.at), str(i.severity)):
                        {"code": i.code, "message": i.message, "at": str(i.at), "severity": str(i.severity)} for i in issues}.values())}
                OUTPUT.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
                print("NEUTRAL_RESULT", key, json.dumps(features), flush=True)
        report["execution_complete"] = True
        report["all_features_pass"] = all(f["passed"] for c in report["cases"].values() for f in c["features"].values())
    finally:
        OUTPUT.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    finally:
        app.close()
