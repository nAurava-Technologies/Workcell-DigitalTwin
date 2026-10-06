"""Isolated Isaac Sim / PhysX floor smoke test; never saves the source stage.

Run with Isaac Sim's python.bat. Writes measured results next to the floor asset.
"""
import hashlib
import json
from pathlib import Path

from isaacsim import SimulationApp

app = SimulationApp({"headless": True})

import carb
import omni.physx
from pxr import Gf, PhysxSchema, Usd, UsdGeom, UsdPhysics, UsdShade, UsdUtils

def _find_root():
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "workcell_digitaltwin.usd").exists() or (p / ".git").exists():
            return p
        p = p.parent
    return Path(__file__).resolve().parents[3]

ROOT = _find_root()
ASSET = ROOT / "components/fixtures/ground_plane/GroundPlane.usd"
OUTPUT = ASSET.with_name("GroundPlane_contact_test.json")


def main():
    stage = Usd.Stage.CreateInMemory()
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    stage.DefinePrim("/GroundPlane").GetReferences().AddReference(str(ASSET))
    floor = stage.GetPrimAtPath("/GroundPlane/CollisionPlane")
    assert floor.IsA(UsdGeom.Plane) and floor.HasAPI(UsdPhysics.CollisionAPI)
    assert not stage.GetPrimAtPath("/GroundPlane/CollisionMesh")
    assert stage.GetPrimAtPath("/GroundPlane/VisualMesh").IsA(UsdGeom.Mesh)
    assert not any(p.HasAPI(UsdPhysics.RigidBodyAPI) for p in stage.Traverse())
    material = UsdShade.MaterialBindingAPI(floor).GetDirectBinding("physics").GetMaterial()
    assert material and material.GetPrim().HasAPI(UsdPhysics.MaterialAPI)
    scene = UsdPhysics.Scene.Define(stage, "/PhysicsScene")
    scene.CreateGravityDirectionAttr(Gf.Vec3f(0, 0, -1))
    scene.CreateGravityMagnitudeAttr(9.81)
    PhysxSchema.PhysxSceneAPI.Apply(scene.GetPrim()).CreateEnableGPUDynamicsAttr(False)

    # Known counterpart: same physics material on each 0.2 m, 1 kg test cube.
    # Zero body damping ensures the slide slows from contact friction, not air drag.
    specs = {"drop": (0, 0, 1.1), "slide": (0, 2, 0.1), "beyond_visual_edge": (30, 0, 1.1)}
    bodies = {}
    for name, pos in specs.items():
        cube = UsdGeom.Cube.Define(stage, f"/Test_{name}")
        cube.CreateSizeAttr(0.2)
        cube.AddTranslateOp().Set(Gf.Vec3d(*pos))
        prim = cube.GetPrim()
        UsdPhysics.CollisionAPI.Apply(prim)
        body = UsdPhysics.RigidBodyAPI.Apply(prim)
        body.CreateVelocityAttr(Gf.Vec3f(2, 0, 0) if name == "slide" else Gf.Vec3f(0))
        UsdPhysics.MassAPI.Apply(prim).CreateMassAttr(1.0)
        physx_body = PhysxSchema.PhysxRigidBodyAPI.Apply(prim)
        physx_body.CreateLinearDampingAttr(0.0)
        physx_body.CreateAngularDampingAttr(0.0)
        UsdShade.MaterialBindingAPI.Apply(prim).Bind(material, materialPurpose="physics")
        bodies[name] = prim

    settings = carb.settings.get_settings()
    settings.set_bool("/physics/updateToUsd", True)
    settings.set_bool("/physics/updateVelocitiesToUsd", True)
    cache = UsdUtils.StageCache.Get()
    stage_id = cache.Insert(stage)
    sim = omni.physx.get_physx_simulation_interface()
    assert sim.attach_stage(stage_id.ToLongInt()), "PhysX could not attach the test stage"
    samples = {name: [] for name in specs}
    try:
        dt = 1 / 120
        for i in range(480):
            sim.simulate(dt, i * dt)
            sim.fetch_results()
            omni.physx.get_physx_interface().update_transformations(False, True, True)
            for name, prim in bodies.items():
                pos = UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()
                vel = UsdPhysics.RigidBodyAPI(prim).GetVelocityAttr().Get()
                samples[name].append({"position": list(pos), "velocity": list(vel)})
        checks, metrics = {}, {}
        for name, data in samples.items():
            final = data[-1]
            z_values = [x["position"][2] for x in data]
            checks[f"{name}_supported"] = min(z_values) >= 0.08 and abs(final["position"][2] - 0.1) < 0.02
            metrics[name] = {"final": final, "minimum_center_z_m": min(z_values)}
            if name != "slide":
                hit = next((i for i, x in enumerate(data) if x["position"][2] < 0.12), None)
                rebound = max((x["position"][2] - 0.1 for x in data[hit:]), default=999) if hit is not None else 999
                checks[f"{name}_fell"] = min(z_values) < 0.2
                checks[f"{name}_low_rebound"] = rebound < 0.03
                metrics[name]["rebound_height_m"] = rebound
        distance = samples["slide"][-1]["position"][0]
        speed = Gf.Vec3f(*samples["slide"][-1]["velocity"]).GetLength()
        checks["slide_friction_stops_body"] = 0.15 < distance < 0.8 and speed < 0.05
        metrics["slide"].update(distance_m=distance, final_speed_m_s=speed)
        report = {"asset": ASSET.relative_to(ROOT).as_posix(),
                  "asset_sha256": hashlib.sha256(ASSET.read_bytes()).hexdigest(),
                  "simulator": "Isaac Sim / PhysX CPU", "dt_s": dt, "duration_s": 4,
                  "counterpart": "0.2 m cube, 1 kg, floor physics material, zero damping",
                  "checks": checks, "metrics": metrics, "passed": all(checks.values())}
        OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("GROUND_PLANE_CONTACT_RESULT " + json.dumps(report), flush=True)
        assert report["passed"], "Ground-plane contact smoke test failed"
    finally:
        sim.detach_stage()
        cache.Erase(stage_id)


try:
    main()
finally:
    app.close()
