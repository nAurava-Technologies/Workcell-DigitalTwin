# Workcell Digital Twin Project

This repository contains the USD assembly and individual digital twin components for a factory workcell, configured for **SimReady** validation of **OpenUSD** assets.

## Overview

The project models an automated robot workcell featuring a Universal Robots UR10 robot arm equipped with a Robotiq gripper. The workcell automates inspection task of moving battery pack (mimicking EV battery inspection) on a conveyor belt, scanning them via an X-Ray Scanner, and sorting the batteries as good or bad.

All assets are structured following the **SimReady specifications** to ensure physics, material properties, scale (meters), orientation (Z-up), and metadata are fully compatible with dynamic simulation environments.

## Project Structure

```
Workcell-DigitalTwin/
├── workcell_digitaltwin.usd    # Main assembly composition stage
├── ur10/                       # UR10 Robot arm assembly & config
├── Robotiq/                    # Robotiq robot gripper
├── robot_base/                 # Mounting base for the robot arm
├── table/                      # Table component (SimReady compliant)
│   ├── Table.step              # Source CAD geometry
│   ├── Table.usd               # Processed OpenUSD asset
│   ├── Table_validation.json   # Validation summary output
├── bin/                        # Part storage bin
│   ├── Bin.usd
│   └── Bin_validation.json
├── conveyor/                   # Conveyor belt assembly
├── EVBatteryPack/              # EV Battery Pack model
├── xray_scanner/               # X-ray inspection system model
├── workcell/                   # Miscellaneous workcell geometry
└── README.md                   # Project documentation
```

## Main Component Assets

*   **UR10 (`ur10/`):** The robot arm asset configured with physics joints and joint limits for kinematic and dynamic control.
*   **Robotiq (`Robotiq/`):** The gripper attachment for grasping parts.
*   **Table (`table/`):** A SimReady table asset converted from CAD with convex hull colliders, mass, and grasp guides.
*   **Bin (`bin/`):** A storage bin configured with colliders and physics materials for part collection.
*   **Conveyor (`conveyor/`):** Conveyor assembly used to transport parts in the workcell.
*   **X-Ray Scanner (`xray_scanner/`):** Inspection equipment model for scanning EV battery packs.
*   **EV Battery Pack (`EVBatteryPack/`):** The primary object of interest for assembly manipulation.

## SimReady Processing Workflow

To convert raw CAD models into simulation-ready assets (e.g. the Table), we followed this automation workflow:

1.  **CAD-to-USD Conversion:** 
    Converted STEP geometry to USD using the Omniverse CAD Converter, forcing a unit scale of meters (`metersPerUnit = 1.0`), Z-Up axis, and disabling instancing (`instancingStyle = 0`) to preserve raw mesh access.
2.  **Metadata & Kind Setup:** 
    Set the USD Model Kind of the root asset to `component` and write validation profile tags (`Prop-Robotics-Neutral`) to the root layer's `customLayerData`.
3.  **Rigid Body & Collider Setup:** 
    Configured the mesh as a dynamic rigid body by applying `UsdPhysics.RigidBodyAPI`, setting a mass of `20.0 kg` (via `UsdPhysics.MassAPI`), and assigning a collider with a `convexHull` approximation.
4.  **Material Binding:** 
    Bound standard Omniverse `Looks/OmniPBR` materials to the mesh for both visual render purposes and physics material purposes (governing friction and restitution).
5.  **Grasp Vector Authoring:** 
    Added visual guide lines (represented by `BasisCurves` with guide purpose) to serve as robotic gripper approach axes.
6.  **SimReady Validation:** 
    Validated the asset against the target profile using `simready-validate` to generate `Table_validation.json` (machine-readable summary).

## How to Run

1.  Open **NVIDIA Omniverse (USD Composer / Create)** or **Isaac Sim**.
2.  Open the assembly stage [workcell_digitaltwin.usd](file:///D:/NVidia/Omniverse/Projects/Factory/Workcell-DigitalTwin/workcell_digitaltwin.usd).
3.  In **Isaac Sim** Click **Play** to start the simulation and observe the rigid body dynamics and joint behaviors.
