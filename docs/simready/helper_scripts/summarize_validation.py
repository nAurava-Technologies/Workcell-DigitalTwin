"""Summarize measured evidence; never convert runtime success into profile success."""
import ast
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs/simready"


def load(name):
    return json.loads((DOCS / name).read_text(encoding="utf-8"))


def failures(features):
    result = set()
    for value in features.values():
        if not value["passed"]:
            codes = value.get("failing requirements", [])
            result.update(ast.literal_eval(codes) if isinstance(codes, str) else codes)
    return sorted(result)


def main():
    neutral = load("neutral_profile_verification.json")
    station = load("RobotStation_isaac_verification.json")
    floor = json.loads((ROOT / "components/fixtures/ground_plane/GroundPlane_contact_test.json").read_text())
    assert neutral.get("execution_complete"), "Neutral sweep incomplete"
    assert len(neutral["cases"]) == 17, "Missing Neutral asset/variant cases"
    assert len(station.get("validation", {})) == 8, "Missing Isaac profile cases"
    assert set(station.get("behavior", {})) == {"station/" + v for v in ("Physx_Mimic", "Physx_Loop", "Physics")}, "Station behavior sweep incomplete"
    stale = []
    for case in list(neutral["cases"].values()) + [station]:
        for name, digest in case.get("input_sha256", {}).items():
            path = ROOT / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                stale.append(name)
    assert not stale, f"Stale evidence: {sorted(set(stale))}"
    assert hashlib.sha256((ROOT / floor["asset"]).read_bytes()).hexdigest() == floor["asset_sha256"]
    lines = ["# Workcell SimReady validation report", "", "Reviewed October 6, 2026 (America/New_York).",
        "", "**Full SimReady conformance is NOT achieved.** The Neutral profile sweep completed in Isaac Sim with real PhysxSchema bindings. Runtime behavior and project exceptions are reported separately from unmodified validator results.",
        "", f"Neutral execution UTC: `{neutral['executed_utc']}`. Station execution UTC: `{station['executed_utc']}`. Recorded input hashes match the current USD files.",
        "", "## Neutral profile results", "", "Profiles are version 1.0.0. Raw evidence: [neutral_profile_verification.json](neutral_profile_verification.json).", "",
        "| Asset / Physics selection | Profile | Failing requirements |", "| --- | --- | --- |"]
    for name, case in neutral["cases"].items():
        lines.append(f"| `{name}` | {case['profile']} | {', '.join(failures(case['features'])) or 'PASS'} |")
    lines += ["", "Seven ordinary props pass all features except FET004's single-body RB.MB.001 finding. The installed profile comments describe multibody as optional; the project treats this as a single-body exception and retains the raw failure. The floor additionally fails RB.001 and GSP.001 because it is deliberately static and not graspable. This is not a full Prop Neutral pass.",
        "", "The UR10 passes all Neutral features, including DJ.001–DJ.003. The default gripper and station still fail DJ.003; the issue text compares equivalent axis-angle representations (opposite axes with 120/240 degree angles). Existing frame-matrix checks corroborate alignment, but this diagnostic does not erase the official failure. Physx_Loop also reports DJ.001. No independent drives or artificial floor rigid bodies were added to force a pass.",
        "", "Physics=None below the mounted gripper is a diagnostic composition; its profile pass does not establish a valid operational tool. EndEffector=None is the supported bare-arm selection. Vacuum_Gripper remains an explicitly labelled placeholder.",
        "", "## HTML recommendation reconciliation", "",
        "| Report items | Current evidence / disposition |", "| --- | --- |",
        "| Gripper 1–2; station 1–2: paths and seven parent colliders | Existing source-layer fixes retained; fresh Isaac audits contain no AA.001 or RB.COL.001–002 findings. Eleven gripper mesh colliders retained, including instance proxies. |",
        "| Floor 1–5: metadata, material, naming, footprint, static role | Metadata and FloorPhysics binding present; VisualMesh is 50 × 50 m; CollisionPlane is intentionally infinite and static. Profile exceptions remain explicit. |",
        "| Floor 6: contact behavior | Fresh drop, slide and beyond-visible-edge tests: " + str(sum(floor['checks'].values())) + "/" + str(len(floor['checks'])) + " pass. Sliding distance " + str(round(floor['metrics']['slide']['distance_m'], 5)) + " m. |",
        "| Station 3–4: pedestal, world anchor, tool mount | Static installation override retained. Two fresh gravity runs at each of station/workcell placements; aligned tool-mount contract checked. |",
        "| Gripper 3; station 5: joint-state environment | Resolved environment gap: Neutral and Isaac validation executed with PhysxSchema. Remaining rule failures are retained above. |",
        "| Gripper 4–5: coupling and articulation | One-drive/five-mimic default preserved. Standalone root retained; mounted root suppressed. |",
        "| Station 6: vacuum variant | Explicit placeholder; no vacuum-tool capability claimed. |",
        "| Station 7; gripper 6: static and runtime verification | Six assembly contracts, four negative regression tests and material localization pass. Fresh station runtime results below; remaining coverage limits are explicit. |",
        "", "## Runtime evidence", "", "[Station evidence](RobotStation_isaac_verification.json); [floor evidence](../../components/fixtures/ground_plane/GroundPlane_contact_test.json).", "",
        f"Station harness acceptance: **{station.get('acceptance_pass', False)}**. This is a behavioral verdict, not a SimReady profile pass.", "",
        "| Station Physics variant | Failed behavioral checks |", "| --- | --- |"]
    for name, case in station.get("behavior", {}).items():
        bad = [key for key, value in case.items() if key.endswith("_pass") and not value]
        if case.get("error"):
            bad.append("runner error")
        lines.append(f"| {name} | {', '.join(bad) or 'None recorded'} |")
    lines += ["", "Physics is an uncoupled diagnostic and is not accepted for coordinated grasping. Physx_Mimic and Physx_Loop are the intended grasp modes. Tests use a 20 g coupon, robot gravity disabled during gripper motion, and fresh-stage rebuilds for reset. Anchoring tests independently enable gravity.",
        "", "**Remaining validation scope:** no new commanded arm-trajectory test, full-workcell grasp test, or interactive Play/Stop/soft-reset test was executed. Standalone gripper behavioral evidence is historical in Robotiq_isaac_verification.json; the fresh profile sweep covers every Physics variant. These limits prevent declaring the entire HTML functional acceptance scope complete. The Isaac profile also retains packaging, mass/kinematic and drive findings; consult its raw issues rather than inferring compliance from motion.",
        "", "The first station run is retained in [RobotStation_isaac_verification_first_run.json](RobotStation_isaac_verification_first_run.json). It failed the default Physx_Mimic open/close, synchronization, repeat-cycle and hold checks (approximately 4.946 m coupon drift). An isolated retry encountered a report-write error, retained in RobotStation_isaac_verification_interrupted.json. Report publication now uses atomic replacement with retries. The current station report is the subsequent isolated run; failures must not be hidden by older passing evidence.",
        "", "Kit logged Replicator startup errors. Direct PhysX and profile results are recorded independently; no Replicator or rendered-sensor readiness is inferred.",
        "", "## Reproduce", "", "Use the skills in docs/workcell-digitaltwin/generic_ai_skill and docs/simready/gemini_skills/simready-cad-pipeline. No .agents directory is required.",
        "", "From the repository root, run full_system_verification.py, test_station_checks.py and verify_material_localization.py under the Foundation Python. Under Isaac Sim python.bat run verify_neutral_profiles.py, verify_station_isaac.py and test_ground_plane_contact.py from docs/workcell-digitaltwin/helper_scripts. Then run docs/simready/helper_scripts/summarize_validation.py. Keep raw failures and logs with the evidence.", ""]
    (DOCS / "final_simready_validation_report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
