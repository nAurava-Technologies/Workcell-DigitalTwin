# Workcell Digital Twin Project

This repository contains the USD assembly and individual digital twin components for a factory workcell, configured for **SimReady** validation of **OpenUSD** assets. The objective is to provide sample assets that adhere to **OpenUSDs SimReady specification** https://github.com/NVIDIA/simready-foundation/tree/main

## Overview

The project models an automated robot workcell featuring a Universal Robots UR10 robot arm equipped with a Robotiq gripper. The workcell automates inspection task of moving battery pack (mimicking EV battery inspection) on a conveyor belt, scanning them via an X-Ray Scanner, and sorting the batteries as good or bad.

All assets are structured following the **SimReady specifications** to ensure physics, material properties, scale (meters), orientation (Z-up), and metadata are fully compatible with dynamic simulation environments.

## Project Structure

```
Workcell-DigitalTwin/
├── workcell_digitaltwin.usd           # Main assembly composition root stage
│
├── layers/                            # Domain-Specific Workstream Layer Stack
│   ├── layout.usda                    # Assembly hierarchy, Xforms, component payloads
│   ├── physics.usda                   # PhysicsScene, ground plane, inter-machine colliders
│   ├── lighting.usda                  # Ambient and task lighting (DomeLight, RectLight), render settings
│   └── automation.usda                # OmniGraph ActionGraph for conveyor logic & sensor gates
│
├── components/                        # Discrete, Reusable Component Models
│   ├── robot_station/                 # Modular Robot Station assembly
│   │   ├── robot_station.usd          # Station Assembly with EndEffector variant set (Robotiq_2F_85 vs None)
│   │   ├── ur10/                      # UR10 Robot arm assembly & config
│   │   ├── Robotiq/                   # Robotiq robot gripper
│   │   └── robot_base/                # Mounting base for the robot arm
│   ├── fixtures/                      # Workcell fixtures and containers
│   │   ├── table/                     # Table component (SimReady compliant)
│   │   │   ├── Table.step             # Source CAD geometry
│   │   │   ├── Table.usd              # Processed OpenUSD asset
│   │   │   └── Table_validation.json  # Validation summary output
│   │   └── bin/                       # Part storage bin
│   │       ├── Bin.step               # Source CAD geometry
│   │       ├── Bin.usd                # Processed OpenUSD asset
│   │       └── Bin_validation.json    # Validation summary output
│   ├── conveyor/                      # Conveyor belt assembly
│   ├── ev_battery_pack/               # EV Battery Pack model with PointInstancer cells
│   ├── xray_scanner/                  # X-ray inspection system model
│   └── enclosure/                     # Workcell perimeter safety fencing
│
├── materials/                         # Localized Core Material Library (MDL)
└── README.md                          # Project documentation
```

## Main Component Assets

*   **Robot Station (`components/robot_station/robot_station.usd`):** Assembly entrypoint for the manipulator station featuring an `EndEffector` variant set (`Robotiq_2F_85`, `Vacuum_Gripper`, `None`) and `ToolMountJoint`.
*   **UR10 (`components/robot_station/ur10/`):** The robot arm asset configured with physics joints and joint limits for kinematic and dynamic control.
*   **Robotiq (`components/robot_station/Robotiq/`):** The gripper attachment for grasping parts.
*   **Robot Base (`components/robot_station/robot_base/`):** Mounting pedestal for the robot arm.
*   **Table (`components/fixtures/table/`):** A SimReady table asset converted from CAD with convex hull colliders, mass, and grasp guides.
*   **Bin (`components/fixtures/bin/`):** A storage bin configured with colliders and physics materials for part collection.
*   **Conveyor (`components/conveyor/`):** Conveyor assembly used to transport parts in the workcell.
*   **X-Ray Scanner (`components/xray_scanner/`):** Inspection equipment model for scanning EV battery packs.
*   **EV Battery Pack (`components/ev_battery_pack/`):** The primary object of interest for assembly manipulation, optimized with `UsdGeomPointInstancer`.
*   **Enclosure (`components/enclosure/`):** Modular safety fence panels guarding the automated workcell.

## SimReady Processing Workflow

To convert raw CAD models into simulation-ready assets (e.g. the Table), we followed this workflow:

1.  **CAD-to-USD Conversion:** 
    Converted STEP geometry to USD using the Omniverse CAD Converter, forcing a unit scale of meters (`metersPerUnit = 1.0`), Z-Up axis, and disabling instancing (`instancingStyle = 0`) to preserve raw mesh access.
2.  **Metadata & Kind Setup:** 
    Set the USD Model Kind of the root asset to `component` and write validation profile tags (`Prop-Robotics-Neutral`) to the root layer's `customLayerData`.
3.  **Rigid Body & Collider Setup:** 
    Configured the mesh as a dynamic rigid body by applying `UsdPhysics.RigidBodyAPI`, setting a mass of `20.0 kg` (via `UsdPhysics.MassAPI`), and assigning a collider with a `convexHull` approximation.
4.  **Material Binding:** 
    Bound standard Omniverse `Looks/OmniPBR` materials to the mesh for both visual render purposes and physics material purposes (governing friction and restitution).
5.  **Grasp Vector Authoring (For Props):** 
    Added visual guide lines (represented by `BasisCurves` with guide purpose) to serve as robotic gripper approach axes.
6.  **SimReady Validation:** 
    Validated the asset against the target profile using `simready-validate` to generate `Table_validation.json` (machine-readable summary).

## How to Run

1.  Open **NVIDIA Omniverse (USD Composer / Create)** or **Isaac Sim**.
2.  Open the assembly stage [`workcell_digitaltwin.usd`](./workcell_digitaltwin.usd).
3.  In **Isaac Sim** Click **Play** to start the simulation and observe the rigid body dynamics and joint behaviors.


## Licensing & Third-Party Assets

This project is licensed under the Apache License 2.0. However, this license **does not apply** to the following third-party assets located in the repository:

* **UR10 Robot Model** (`components/robot_station/ur10`)
* **Robotiq 2F-85 Gripper Model** (`components/robot_station/Robotiq/2F-85`)
* **Conveyor Model** (`components/conveyor`)

These assets are the property of their respective owners and are excluded from the Apache 2.0 terms of this repository. 

### References to Excluded Assets
Please review and accept the licensing terms before using these assets:

- For **UR10** and **Robotiq** assets refer to https://github.com/NVIDIA/simready-foundation/tree/main
- For **Conveyor Model** from NVIDIA Isaacsim, refer to [https://github.com/isaac-sim/IsaacSim](https://github.com/isaac-sim/IsaacSim) and [https://catalog.ngc.nvidia.com/orgs/nvidia/containers/isaac-sim](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/isaac-sim)

