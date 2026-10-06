#!/usr/bin/env python3
"""
SimReady Asset Audit CLI
------------------------
Audits an OpenUSD asset against a target SimReady Profile using the official
NVIDIA SimReady Foundation validation engine.

Usage:
  python audit_asset.py path/to/asset.usd [--profile Prop-Robotics-Neutral] [--json-output report.json]
"""

import argparse
import json
import logging
import os
import sys
import warnings
from pathlib import Path

# Suppress known harmless upstream coroutine warning in Python 3.12
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Ensure UTF-8 output encoding across Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Locate simready-foundation directory dynamically
def _resolve_foundation_root() -> Path:
    if os.environ.get("SIMREADY_FOUNDATION_ROOT"):
        return Path(os.environ["SIMREADY_FOUNDATION_ROOT"])
    candidates = [
        Path(r"D:\NVidia\Omniverse\Projects\SimReady\simready-foundation"),
        Path(__file__).resolve().parents[7] / "SimReady" / "simready-foundation",
        Path(__file__).resolve().parents[5] / "SimReady" / "simready-foundation",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return candidates[0]

DEFAULT_FOUNDATION_ROOT = _resolve_foundation_root()

FEATURE_NAMES = {
    "FET000_CORE": "Core Naming, Layout & Portability",
    "FET001_BASE_NEUTRAL": "Base Units (1.0m), Up-Axis & Geometry",
    "FET003_BASE_NEUTRAL": "Rigid Body Dynamics (Neutral)",
    "FET003_BASE_PHYSX": "Rigid Body Dynamics (PhysX)",
    "FET004_BASE_NEUTRAL": "Multi-Body Articulation (Neutral)",
    "FET004_ROBOT_PHYSX": "Multi-Body Kinematics & Colliders (PhysX)",
    "FET005_BASE_NEUTRAL": "Grasp Affordance & Physics Materials",
    "FET006_BASE_MDL": "MDL Shaders & Texture Localizations",
    "FET021_ROBOT_CORE_ISAAC": "Robot Core Isaac Composition & Namespaces",
    "FET021_ROBOT_CORE_RUNNABLE": "Robot Core Runnable Profile",
    "FET022_DRIVEN_JOINTS_ISAAC": "Isaac Sim Driven Joint State Drives",
    "FET022_DRIVEN_JOINTS_NEUTRAL": "Robot Driven Joint State APIs",
    "FET022_DRIVEN_JOINTS_PHYSX": "PhysX Driven Joint State Drives",
    "FET024_BASE_ARTICULATION_NEUTRAL": "Robot Base Articulation Root (Neutral)",
    "FET024_BASE_ARTICULATION_PHYSX": "Robot Base Articulation Root (PhysX)",
    "FET100_BASE_ISAACSIM": "Isaac Sim Composition & Articulation Layout",
}

def audit_asset(asset_path: Path, profile_id: str, profile_version: str, foundation_root: Path, quiet: bool = False) -> dict:
    if not asset_path.is_file():
        print(f"Error: Asset file not found: '{asset_path}'", file=sys.stderr)
        sys.exit(1)

    if not foundation_root.is_dir():
        print(f"Error: SimReady Foundation root not found at: '{foundation_root}'", file=sys.stderr)
        sys.exit(1)

    # Configure logging
    log_level = logging.ERROR if quiet else logging.WARNING
    logging.basicConfig(level=log_level)
    for log_name in ["omni.asset_validator", "SimReady Validation", "Validation Sample"]:
        logging.getLogger(log_name).setLevel(log_level)

    # Insert foundation root into sys.path
    if str(foundation_root) not in sys.path:
        sys.path.insert(0, str(foundation_root))

    try:
        import simready.validate as sv
        from simready.validate import AssetValidationConfig
    except ImportError as e:
        print(f"Error: Could not import simready.validate module: {e}", file=sys.stderr)
        print(f"Make sure to execute with the foundation python interpreter:\n  & \"{foundation_root}\\.venv\\Scripts\\python.exe\"", file=sys.stderr)
        sys.exit(1)

    # Initialize specifications
    specs_dir = foundation_root / "nv_core" / "sr_specs" / "docs"
    sv.initialize(
        rules_and_requirements_paths=[specs_dir / "capabilities"],
        features_paths=[specs_dir / "features"],
        profiles_paths=[specs_dir / "profiles" / "profiles.toml"]
    )

    # Execute asset validation
    config = AssetValidationConfig(
        asset_path=str(asset_path),
        profile_id=profile_id,
        profile_version=profile_version
    )
    result = sv.validate_asset(config)
    if not result:
        print(f"Error: No validation result returned for '{asset_path}'", file=sys.stderr)
        sys.exit(1)

    # Analyze features and account for profile specifications
    is_prop_profile = profile_id.startswith("Prop-Robotics")
    summary = {}
    is_overall_compliant = True

    for feat_id, feat_data in sorted(result.features_summary.items()):
        passed = feat_data.get("passed", False)
        failing_reqs = feat_data.get("failing requirements", [])
        if isinstance(failing_reqs, str):
            try:
                import ast
                failing_reqs = ast.literal_eval(failing_reqs)
            except Exception:
                failing_reqs = [failing_reqs]

        # Check for Prop-Robotics optional multi-body rule (FET004)
        is_optional = False
        notes = ""
        if is_prop_profile and feat_id == "FET004_BASE_NEUTRAL":
            # The project exception covers only absent multibody structure on
            # single-body props, never unrelated physics failures in FET004.
            is_optional = passed or set(failing_reqs) == {"RB.MB.001"}
            if not passed and set(failing_reqs) == {"RB.MB.001"}:
                notes = "Project single-body exception; raw multibody finding retained."
            elif passed:
                notes = "Multi-body articulation verified."
            else:
                is_overall_compliant = False
        elif not passed:
            if feat_id.startswith("FET022"):
                try:
                    from pxr import PhysxSchema
                    schema_available = hasattr(PhysxSchema, "JointStateAPI")
                except ImportError:
                    schema_available = False
                notes = ("Joint-state schemas available; inspect actual rule findings."
                         if schema_available else
                         "Joint-state environment unavailable; rerun with Isaac Sim PhysxSchema. No pass inferred.")
            elif feat_id.startswith(("FET021", "FET024", "FET100")):
                notes = "Validation failed; embedded telemetry is not evidence of a current pass."
            is_overall_compliant = False

        summary[feat_id] = {
            "name": FEATURE_NAMES.get(feat_id, feat_id),
            "passed": passed,
            "optional": is_optional,
            "failing_requirements": failing_reqs,
            "notes": notes
        }

    return {
        "asset": str(asset_path),
        "profile": f"{profile_id} (v{profile_version})",
        "compliant": is_overall_compliant,
        "features": summary
    }

def print_audit_report(report: dict):
    print("================================================================================")
    print("SIMREADY COMPLIANCE AUDIT REPORT")
    print("================================================================================")
    print(f"Asset:    {report['asset']}")
    print(f"Profile:  {report['profile']}")
    print("--------------------------------------------------------------------------------")
    print(f"{'Feature ID':<30} | {'Status':<12} | {'Notes / Failing Requirements'}")
    print("--------------------------------------------------------------------------------")

    for feat_id, data in report["features"].items():
        if data["passed"]:
            status_str = "🟢 PASS"
            detail_str = data["notes"] if data["notes"] else "All requirements satisfied"
        elif data["optional"]:
            status_str = "ℹ️  OPTIONAL"
            detail_str = data["notes"] if data["notes"] else f"Optional ({data['failing_requirements']})"
        else:
            status_str = "❌ FAIL"
            if data["notes"]:
                detail_str = f"{data['notes']} | Failing: {data['failing_requirements']}"
            else:
                detail_str = f"Failing: {data['failing_requirements']}"

        print(f"{feat_id:<30} | {status_str:<12} | {detail_str}")

    print("================================================================================")
    if report["compliant"]:
        print("VERDICT: 🟢 100% SIMREADY COMPLIANT")
        print("================================================================================")
    else:
        print("VERDICT: ❌ NON-COMPLIANT (Remediation Required)")
        print("================================================================================")

def main():
    parser = argparse.ArgumentParser(description="Audit an OpenUSD asset for SimReady compliance.")
    parser.add_argument("asset_path", type=str, help="Path to the USD file to audit.")
    parser.add_argument("--profile", "-p", type=str, default="Prop-Robotics-Neutral", help="SimReady Profile ID.")
    parser.add_argument("--profile-version", "-pv", type=str, default="1.0.0", help="SimReady Profile version.")
    parser.add_argument("--foundation-root", type=str, default=str(DEFAULT_FOUNDATION_ROOT), help="Path to simready-foundation.")
    parser.add_argument("--json-output", "-j", type=str, default=None, help="Optional output JSON report path.")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress logs.")
    args = parser.parse_args()

    asset_path = Path(args.asset_path).resolve()
    foundation_root = Path(args.foundation_root).resolve()

    report = audit_asset(asset_path, args.profile, args.profile_version, foundation_root, quiet=args.quiet)
    print_audit_report(report)

    if args.json_output:
        out_path = Path(args.json_output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"JSON audit report saved to: {out_path}")

    sys.exit(0 if report["compliant"] else 1)

if __name__ == "__main__":
    main()
