# Composed robot station

Current validation status (2026-10-06): see the
[repository validation report](../../docs/simready/final_simready_validation_report.md).
Full SimReady conformance is not achieved. Measurements dated 2026-10-02 below
are historical and must not override newer runtime failures.

`robot_station.usd` represents a stationary installation. The assembly removes
`PhysicsRigidBodyAPI` from the referenced pedestal mesh while preserving its
collision API and geometry. The standalone pedestal source remains unchanged.
The pedestal is therefore a static collider, not an unconstrained dynamic prop.

The UR10 retains one fixed-base articulation rooted at `ur10/root_joint`.
Its world joint selects the base link; its local joint frames are ignored by
PhysX for fixed-base articulations, as documented in
[NVIDIA's articulation guide](https://docs.omniverse.nvidia.com/kit/docs/omni_physics/latest/dev_guide/rigid_bodies_articulations/articulations.html).
Do not compensate for apparent world-frame differences by hardcoding the
workcell's placement into this reusable component.

`ToolMountJoint` retains its aligned wrist-to-gripper frames. The mounted
Robotiq shares the UR10 articulation, while the standalone Robotiq keeps its own
root. The default gripper retains one drive and five mimic followers. Its source
layers contain the dependency-path and seven parent-collider fixes; all eleven
child mesh colliders remain. See [Robotiq details](Robotiq/2F-85/README.md).

## End-effector variants

| Variant | Contents |
| --- | --- |
| `Robotiq_2F_85` | Working tool, fixed mount, 14 mapped joints and 16 links. |
| `None` | UR10 only, seven mapped joints and seven links. |
| `Vacuum_Gripper` | Explicit placeholder, seven UR10 joints and seven links; no vacuum tool, mounting joint, or grasp capability. |

The vacuum variant keeps its existing name for compatibility and authors
`workcell:toolStatus = "placeholder"` plus a descriptive Isaac description.
It must not be selected expecting an implemented vacuum tool.

## Reproduce verification

From the repository root:

```powershell
& "..\..\SimReady\simready-foundation\.venv\Scripts\python.exe" docs/workcell-digitaltwin/helper_scripts/full_system_verification.py
& "..\..\SimReady\simready-foundation\.venv\Scripts\python.exe" docs/workcell-digitaltwin/helper_scripts/test_station_checks.py
& "D:\NVidia\Omniverse\IsaacSim\Isaac6\python.bat" docs/workcell-digitaltwin/helper_scripts/verify_station_isaac.py
```

Structural checks exercise every EndEffector selection in both the component and
assembled workcell, checking mapping existence, types, uniqueness, joint bodies,
articulation roots, static pedestal, tool frame alignment and collider contents.
Negative tests inject broken mappings, mounting and placeholder declarations
into temporary session layers.

The Isaac runner records gravity-enabled world anchoring at every step for three
seconds, twice from fresh stages, in both station and placed workcell. It reruns
the installed Robot-Body-Isaac profile with PhysxSchema and reuses the gripper
motion/contact harness for all three articulated physics variants, each with a
fresh-stage reset. `Physx_Mimic` and `Physx_Loop` are the intended grasp variants;
base `Physics` lacks coupling and is retained as a diagnostic, not a working
single-command grasp configuration. `None` has no actuation to exercise.

Reports live in `docs/simready/RobotStation_isaac_verification.json`. Acceptance
checks are distinct from a full SimReady profile pass. Packaging, mass-authoring,
rotation-representation and hard-mimic profile findings remain visible.
Grasp tests use a controlled 20 g coupon and disable robot gravity to isolate
mechanism behavior; they do not certify payload ratings, arbitrary trajectories,
or an external controller's soft-reset procedure.

## World-anchor measurements

The gravity tests on 2026-10-02 used CPU PhysX at 120 Hz. Both independent
fresh-stage runs passed for each placement. Maximum base translation change was
zero in the component and 6.36e-8 m in the workcell; pedestal movement was zero.
Maximum base transform element error was 1.34e-7, including the first simulation
step. All twelve moving-joint state APIs were recognized by PhysxSchema.
The apparent root-joint frame mismatch therefore required no asset correction.

The final station motion/contact rerun passed opening, closing, mimic
synchronization, repeated cycles, fresh-stage reset, hold and release for both
`Physx_Mimic` and `Physx_Loop`. Coupon drift during the one-second hold was
2.36 mm and 0.16 mm respectively (10 mm threshold). Final tool-mount separation
was 7.16e-8 m. The uncoupled `Physics` diagnostic failed synchronization and
hold (4.95 m drift), as expected from its missing coupling; it is not accepted
as an operational grasp variant. All eight gripper/station validation cases
were free of AA.001, RB.COL.001, RB.COL.002 and DJ.002 findings. Other profile
findings remain, so these results do not constitute a full SimReady pass.
