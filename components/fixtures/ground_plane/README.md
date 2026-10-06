# GroundPlane: static environment floor

`GroundPlane.usd` is an unlimited static environment floor at Z=0, in metres,
with Z up. `VisualMesh` is a 50 x 50 metre render surface. `CollisionPlane` is
an infinite plane collider: objects remain supported beyond the visible edges.
The finite `extentsHint` describes the visual footprint, not a collision boundary.
For a bounded platform, replace the plane with a finite static collider and
retest edge behavior; do not infer collision bounds from the visible mesh.

`Looks/FloorPhysics` applies `UsdPhysics.MaterialAPI` and is bound directly to
`CollisionPlane` through `material:binding:physics`. Static friction is 0.6,
dynamic friction is 0.5, and restitution is 0.0. These are uncalibrated dry,
moderately grippy industrial-floor defaults, not measured surface properties.
Actual pair response also depends on the other body's material and the
simulator's combine rules. The visual chalk-paint material is unchanged.

## Provenance and static-floor requirements

The existing procedural USD plane and visual quad are retained. Original
authorship and generation date are unknown; metadata records this explicitly
instead of inventing provenance. The conditioning date is 2026-10-02.

The project requires an enabled plane collider, a direct valid physics-material
binding, and no rigid-body API on the floor or its ancestors. It does not require
mass, joints, or grasp affordances for this environment asset. This matches
[NVIDIA's static-collider requirement](https://docs.omniverse.nvidia.com/kit/docs/asset-requirements/1.11.2/capabilities/physics_bodies/physics_rigid_bodies/requirements/static-collider.html).
[OpenUSD physics documentation](https://openusd.org/dev/api/usd_physics_page_front.html)
defines plane collision as infinite and permits static colliders without a rigid body.
An assembly referencing this asset must preserve that static ancestry.

## Validation and explicit profile exceptions

The installed `Prop-Robotics-Neutral` v1.0.0 validator was rerun after conditioning.
See `GroundPlane_validation.json` for its unmodified feature verdicts.

| Requirement | Result / project disposition |
| --- | --- |
| NP.006 | Fixed: root-layer `customLayerData["SimReady_Metadata"]` is present. |
| PMT.001 | Fixed: the actual collider has a direct physics-material binding. |
| RB.001 | Validator failure retained; project exception because the floor must remain static. |
| RB.MB.001 | Validator finding retained in optional FET004; project exception because the floor is not a multibody mechanism. FET004 also reports RB.001. |
| GSP.001 | Validator failure retained; project exception because this environment floor is not graspable. |

These are asset-specific project exceptions, not changes to NVIDIA's validator
or a certified static-environment profile. **This asset does not receive a full
Prop-Robotics-Neutral pass.** No dynamic body, artificial joints, or grasp guides
were added to hide the profile mismatch.

From the repository root, rerun the audit (exit code 1 is expected for this profile):

```powershell
& "..\..\SimReady\simready-foundation\.venv\Scripts\python.exe" `
  docs/simready/gemini_skills/simready-cad-pipeline/scripts/audit_asset.py `
  components/fixtures/ground_plane/GroundPlane.usd --quiet `
  --json-output components/fixtures/ground_plane/GroundPlane_validation.json
```

## Contact test

Run the isolated smoke test using the target Isaac Sim installation:

```powershell
& "D:\NVidia\Omniverse\IsaacSim\Isaac6\python.bat" `
  docs/workcell-digitaltwin/helper_scripts/test_ground_plane_contact.py
```

The test references the actual asset into an in-memory scene and does not save
changes to the asset or open workcell. It uses CPU PhysX at 120 Hz for four
simulated seconds, with 0.2 metre, 1 kg cubes carrying the same physics material:

- Drop from 1 metre above the floor: require support and less than 3 cm rebound.
- Slide at 2 m/s with zero body damping: require a 0.15–0.8 m stopping distance
  and final speed below 0.05 m/s.
- Drop at X=30 m: require support outside the visible 25 m half-width.

Measurements, assertions, and an asset SHA-256 are written to
`GroundPlane_contact_test.json`. This is a controlled contact smoke test, not
calibration against a real floor or a complete workcell dynamics acceptance test.

### Measured result, 2026-10-02

Passed in installed Isaac Sim `6.0.1-rc.7+release.42383.32955d8d.gl` with CPU
PhysX. Both dropped cubes settled with their centres approximately 0.100 m
above the plane. Maximum sampled rebound after contact was below 0.00001 m.
The sliding cube stopped after 0.39945 m, with final speed 0.000169 m/s.
The X=30 m drop confirmed the intentional infinite collision footprint.
All eight contact assertions passed. These values are numerical smoke-test
observations, not claims of real-world accuracy at that precision.

The runtime logged Replicator extension startup errors unrelated to the test's
direct PhysX calls; the physics test nevertheless completed. Existing
`full_system_verification.py` and `verify_material_localization.py` checks also
passed, with 15 direct physics bindings after adding the floor material.
