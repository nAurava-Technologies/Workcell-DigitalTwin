# Robotiq 2F-85 conditioning and verification

For the 2026-10-06 Neutral-profile and mounted runtime rerun, see the
[current repository report](../../../../docs/simready/final_simready_validation_report.md).
Historical behavioral passes below are not a current full SimReady verdict.

The USD entry point is `simready_isaac_usd/Robotiq_2F_85.usda`. The default physics
variant remains `Physx_Mimic`. Changes on 2026-10-02 normalize local USD reference,
payload, and sublayer paths to explicit `./` paths and remove collision APIs and
collision properties from seven parent Xform specs in `payloads/instances.usda`.
All eleven composed mesh colliders are preserved, including instance proxies.
Geometry, mass data, authored joint states, drive gains, gearing, root selection,
and station mounting have not been retuned as part of those changes.

## Physics variants

| Variant | Authored purpose and control |
| --- | --- |
| `Physx_Mimic` | Default coupled mechanism: one angular drive on `finger_joint`, five mimic followers, eight joints including two fixed joints. |
| `Physx_Loop` | Alternate closed-loop topology with two joints excluded from the articulation, compliant outer-knuckle mimic, and existing passive/weak spring drives. It is not the same control model as `Physx_Mimic`. |
| `Physics` | Base USD rigid bodies and joints, without the PhysX mimic coupling layer. It is not a synchronized single-command gripper. |
| `None` | No rigid bodies or joints; geometry and mesh collision declarations remain. Opening/closing and grasping do not apply to this variant. |

For the default variant the coupling equation is `q_follower + G*q_finger = 0`:
`G=-1` for `right_outer_knuckle_joint` and `right_inner_finger_joint`; `G=+1`
for the other three followers. Do not add independent drives to those followers.
[NVIDIA's articulation guidance](https://docs.omniverse.nvidia.com/kit/docs/omni_physics/latest/dev_guide/rigid_bodies_articulations/articulations.html)
describes this coupling. Zero natural frequency and damping are retained for
the existing hard constraints; the
[PhysX API](https://nvidia-omniverse.github.io/PhysX/physx/latest/_api_build/classPxArticulationReducedCoordinate.html)
explicitly supports this configuration, although the installed SimReady profile
requires nonzero natural frequency.

## Articulation and mounting

Standalone articulated variants retain their root at `/Robotiq_2F_85`. In the
station, the gripper's root API remains suppressed so that the mechanism belongs
to `/RobotStation/ur10/root_joint`. `ToolMountJoint` still connects the UR10
`wrist_3_link` to gripper `base_link`. Its authored world-space anchor separation
was approximately 6.3e-11 m. The default station still maps 14 joints and 16 links;
the standalone gripper maps six movable joints and nine links.

## Validation scope

The installed Robot-Body-Isaac v1.0.0 profile was run inside Isaac Sim with
`pxr.PhysxSchema` available, on every variant of both the gripper and station.
Detailed feature verdicts and issues are saved outside the strict asset package
in `docs/simready/Robotiq_isaac_verification.json`.

- AA.001 and RB.COL.001–002 are resolved for the gripper.
- All six default-variant joint-state APIs are recognized in Isaac Sim. No
  joint-state data was added to compensate for missing standalone bindings.
- DJ.003 still flags equivalent rotation representations. Direct comparison of
  the two world joint-frame matrices gives zero elementwise difference for all
  eight default gripper joints, both standalone and mounted. The installed rule
  compares rotation representations without accounting for their equivalence.
- DJ.007 still flags hard mimic constraints with zero natural frequency and a
  follower limit equal to the mapped reference limit. These remain visible
  profile findings rather than reasons to change functioning coupling blindly.
- Packaging/naming/layer-placement and relationship-list-op findings remain.
  RB.011 reports missing explicit mass on three bodies whose colliders are
  instanced descendants. The station also has a COL.001 mesh-approximation finding.

**Neither the gripper nor station is claimed to fully pass Robot-Body-Isaac.**
Missing runtime bindings, authoring-convention findings, and behavioral results
are distinct; the report does not replace failures with inferred compliance.

## Reproduce

From the repository root:

```powershell
& "D:\NVidia\Omniverse\IsaacSim\Isaac6\python.bat" `
  docs/workcell-digitaltwin/helper_scripts/verify_robotiq_isaac.py --behavior
```

Set `SIMREADY_FOUNDATION_ROOT` if the Foundation checkout is elsewhere.
Validation uses the existing installed Foundation implementation with Isaac's
USD schemas. The behavior harness references the assets into temporary in-memory
stages and never saves simulation poses into source assets. A standalone test
mount anchors the gripper without changing its authored articulation root.
Motion tests disable robot gravity to isolate command response. The contact test
uses a declared 20 g coupon with friction 0.8, initially held during acquisition,
then made dynamic under a 9.81 m/s² load tangent to the finger pads. This is a
mechanism smoke test, not a calibrated payload rating or production grasp plan.

## Measured behavior, 2026-10-02

Tested in Isaac Sim `6.0.1-rc.7+release.42383.32955d8d.gl`, CPU PhysX, 120 Hz.
Commands were 0 → 35 → 0 → 35 degrees, followed by coupon acquisition, hold,
and release. Each case was rebuilt from its authored stage and repeated to test
a hard reset. This does not test an external controller's soft-reset procedure.

| Context / variant | Open/close, repeat, hard reset | Mimic synchronization | Coupon hold drift | Release |
| --- | --- | --- | --- | --- |
| Standalone / Physx_Mimic | Pass | Pass | 0.74 mm, pass | Pass |
| Station / Physx_Mimic | Pass | Pass | 1.55 mm, pass | Pass |
| Standalone / Physx_Loop | Pass | Pass | 0.17 mm, pass | Pass |
| Station / Physx_Loop | Pass | Pass | 0.15 mm, pass | Pass |
| Standalone / Physics | Driven finger only passes | No coupling; fails coordinated grasp | Falls, fails | Unheld object continues falling; not a successful grasp/release |
| Station / Physics | Driven finger only passes | No coupling; fails coordinated grasp | Falls, fails | Unheld object continues falling; not a successful grasp/release |
| None, either context | Not applicable: no articulated gripper | Not applicable | Not applicable | Not applicable |

The default mimic residual `q_follower + G*q_finger` was below 0.000004 degrees
at sampled free-motion poses. Mounted `ToolMountJoint` anchor separation after
the contact tests was approximately 7.2e-8 m. No gains, gearing, follower drives,
joint states, or mount transforms needed alteration for those tests.

Use `Physx_Mimic` or `Physx_Loop` for actuated grasping. Selecting `Physics` loads
the base joint topology without the additional coupling needed for synchronized
fingers; it is not an alternative ready-to-run grasping configuration. The report
retains its failed synchronization and hold checks. `None` retains static mesh
colliders and is unsuitable as an actuated tool on the station.

The test runtime emitted Replicator extension startup errors, but the direct
PhysX validation and simulation calls completed. The existing full-system
verification also passed. These results do not waive the remaining SimReady
profile findings listed above.
