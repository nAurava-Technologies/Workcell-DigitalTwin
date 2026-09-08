# SimReady Detailed Validation Report

| Metadata | Value |
| :--- | :--- |
| **Date/Time of Run** | 2026-09-07 20:45:28 |
| **Asset Path** | `D:\NVidia\Omniverse\Projects\Factory\Workcell-DigitalTwin\ur10\simready_usd\ur10.usda` |
| **Profile Target** | `Robot-Body-Neutral` v`1.0.0` |

## Feature Summary Table

| Feature ID | Feature Name | Description | Passed | Failing Requirements |
| :--- | :--- | :--- | :---: | :--- |
| `FET001_BASE_NEUTRAL` | **Minimal Editor** | The minimal placeable visual feature comprises a list of requirements that enable the digital representation of a real world object to be visualized in a broad range of applications. It additionally provides a list of requirements to ensure that the scale, units and placement of the object may be correctly represented, so that the object can be placed and aggregated with other objects in a scene. | ✅ **PASSED** | `None` |
| `FET003_BASE_NEUTRAL` | **Rigid Body Physics** | Support for rigid body dynamics (RBD). This feature enables simulation of physically accurate motion and collisions for props and dynamic assets. It is suitable for testing, validation, or reference applications where basic physical interactions are required. | ✅ **PASSED** | `None` |
| `FET004_BASE_NEUTRAL` | **Simulate Multi-Body Physics** | Features needed to support Simulate Multi-Body physics. This feature enables simulation of physically accurate motion and collisions for props and dynamic assets that have multibody bodies that need to be joined or simulated together. The enables real world "joints" to describe how two bodies work together. It is suitable for testing, validation, or reference applications where basic physical interactions are required. | ✅ **PASSED** | `None` |
| `FET022_DRIVEN_JOINTS_NEUTRAL` | **Driven Joints Neutral** | Driven joints enable physics-driven joint simulation for articulated bodies and robotic mechanisms, with proper drive/state configuration, PhysX drive or mimic APIs, and robot-schema integration for Isaac Sim. | ❌ **FAILED** | `['DJ.003', 'DJ.001', 'DJ.002']` |
| `FET024_BASE_ARTICULATION_NEUTRAL` | **Base Articulation Neutral** | Base articulation requirements for assets with articulated physics bodies. | ✅ **PASSED** | `None` |

## Detailed Rule Verification

### Feature: **Minimal Editor** (`FET001_BASE_NEUTRAL` v0.1.0)
*The minimal placeable visual feature comprises a list of requirements that enable the digital representation of a real world object to be visualized in a broad range of applications. It additionally provides a list of requirements to ensure that the scale, units and placement of the object may be correctly represented, so that the object can be placed and aggregated with other objects in a scene.*

<table width="100%" style="border-collapse: collapse; table-layout: auto;">
  <thead>
    <tr>
      <th align="left" style="width: 12%; min-width: 90px; padding: 8px; border: 1px solid #44474a;">Requirement Code</th>
      <th align="left" style="width: 30%; min-width: 240px; padding: 8px; border: 1px solid #44474a;">Capability Description</th>
      <th align="left" style="width: 23%; min-width: 180px; padding: 8px; border: 1px solid #44474a;">Requirement Description</th>
      <th align="left" style="width: 15%; min-width: 120px; padding: 8px; border: 1px solid #44474a;">Rule Class</th>
      <th align="center" style="width: 10%; min-width: 70px; padding: 8px; border: 1px solid #44474a;">Status</th>
      <th align="left" style="width: 10%; min-width: 150px; padding: 8px; border: 1px solid #44474a;">Details / Issues</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>AA.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Atomic Asset</strong>: The Atomic Asset capability enables transport of assets between different environments and platforms. This includes requirements and recommendations for file packaging, asset references and supported file types.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Asset references should use anchored paths</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>AnchoredAssetPathsChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>AA.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Atomic Asset</strong>: The Atomic Asset capability enables transport of assets between different environments and platforms. This includes requirements and recommendations for file packaging, asset references and supported file types.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Asset must use only supported file types</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>SupportedFileTypesChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>HI.004</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Hierarchy</strong>: This capability provides requirements for the organization and structure of USD assets through: - Correct scene hierarchy using Xform primitives for spatial organization - Stage metadata including defaultPrim specification - Correct transform stack management - Scene graph organization guidance The capability provides guidelines and best practices for USD scene graph organization, ensuring that assets can be properly composed and organized, while maintaining correct spatial relationships and transformations.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Stage must specify a default prim to define the root entry point.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>StageHasDefaultPrimChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>UN.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Units</strong>: This capability enables proper scaling and composition of assets with different unit systems, accurate physics simulation through consistent mass and scale units, correct time-sampled animation playback via standardized time units, and reliable color reproduction through defined colorspace units. These requirements ensure that assets have consistent and well-defined units for proper scaling when composed together as well as interpretation in simulation and rendering environments.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Stage must specify upAxis to define the orientation of the stage</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>StageMetadataChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>UN.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Units</strong>: This capability enables proper scaling and composition of assets with different unit systems, accurate physics simulation through consistent mass and scale units, correct time-sampled animation playback via standardized time units, and reliable color reproduction through defined colorspace units. These requirements ensure that assets have consistent and well-defined units for proper scaling when composed together as well as interpretation in simulation and rendering environments.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Stage must specify metersPerUnit to define the linear unit scale</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>StageMetadataChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>UN.007</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Units</strong>: This capability enables proper scaling and composition of assets with different unit systems, accurate physics simulation through consistent mass and scale units, correct time-sampled animation playback via standardized time units, and reliable color reproduction through defined colorspace units. These requirements ensure that assets have consistent and well-defined units for proper scaling when composed together as well as interpretation in simulation and rendering environments.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Stage must specify metersPerUnit = 1.0 to define the linear unit scale</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>MetersPerUnit1Checker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>VG.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Visual Geometry</strong>: This capability contains requirements which relate to Geometry.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Assets must contain at least one Imageable Geometry</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ImageableGeometryChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
  </tbody>
</table>

### Feature: **Rigid Body Physics** (`FET003_BASE_NEUTRAL` v0.1.0)
*Support for rigid body dynamics (RBD). This feature enables simulation of physically accurate motion and collisions for props and dynamic assets. It is suitable for testing, validation, or reference applications where basic physical interactions are required.*

<table width="100%" style="border-collapse: collapse; table-layout: auto;">
  <thead>
    <tr>
      <th align="left" style="width: 12%; min-width: 90px; padding: 8px; border: 1px solid #44474a;">Requirement Code</th>
      <th align="left" style="width: 30%; min-width: 240px; padding: 8px; border: 1px solid #44474a;">Capability Description</th>
      <th align="left" style="width: 23%; min-width: 180px; padding: 8px; border: 1px solid #44474a;">Requirement Description</th>
      <th align="left" style="width: 15%; min-width: 120px; padding: 8px; border: 1px solid #44474a;">Rule Class</th>
      <th align="center" style="width: 10%; min-width: 70px; padding: 8px; border: 1px solid #44474a;">Status</th>
      <th align="left" style="width: 10%; min-width: 150px; padding: 8px; border: 1px solid #44474a;">Details / Issues</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Assets must contain at least one rigid body</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies have to be UsdGeomXformable prims.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.005</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies cannot be part of a scene graph instance.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.006</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies can not be nested unless xformOp reset xform stack is used.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.007</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies _or_ their descendant collision shapes must have a mass specification.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyMassChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.009</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies have to be UsdGeomXformable prims without skew matrix.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.010</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Invisible collision meshes must have their purpose attribute set to 'guide' to be properly excluded from rendering.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>InvisibleCollisionMeshHasPurposeGuide</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Colliding Gprims must apply the Collision API.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">**UsdPhysicsMeshCollisionAPI** may only be applied to **UsdGeom.Mesh** prims, and any prim with MeshCollisionAPI must also have **UsdPhysicsCollisionAPI** applied.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderMeshChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The Mesh Collision API can only be assigned to Mesh Prims.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderNonUniformScaleChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.004</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The collision shape scale must be uniform for the following geometries: Sphere, Capsule, Cylinder, Cone & Points.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ColliderChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
  </tbody>
</table>

### Feature: **Simulate Multi-Body Physics** (`FET004_BASE_NEUTRAL` v0.1.0)
*Features needed to support Simulate Multi-Body physics. This feature enables simulation of physically accurate motion and collisions for props and dynamic assets that have multibody bodies that need to be joined or simulated together. The enables real world "joints" to describe how two bodies work together. It is suitable for testing, validation, or reference applications where basic physical interactions are required.*

<table width="100%" style="border-collapse: collapse; table-layout: auto;">
  <thead>
    <tr>
      <th align="left" style="width: 12%; min-width: 90px; padding: 8px; border: 1px solid #44474a;">Requirement Code</th>
      <th align="left" style="width: 30%; min-width: 240px; padding: 8px; border: 1px solid #44474a;">Capability Description</th>
      <th align="left" style="width: 23%; min-width: 180px; padding: 8px; border: 1px solid #44474a;">Requirement Description</th>
      <th align="left" style="width: 15%; min-width: 120px; padding: 8px; border: 1px solid #44474a;">Rule Class</th>
      <th align="center" style="width: 10%; min-width: 70px; padding: 8px; border: 1px solid #44474a;">Status</th>
      <th align="left" style="width: 10%; min-width: 150px; padding: 8px; border: 1px solid #44474a;">Details / Issues</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies which are not free floating should be connected using joints.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>PhysicsJointCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Targets set to Body0 and Body1 relationships must exist.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>PhysicsJointChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Body0 and Body1 relationships must not have more than one target.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>PhysicsJointChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.ART.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulation roots cannot be nested.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ArticulationChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.ART.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulations are not allowed on kinematic bodies.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ArticulationChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.ART.004</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulations are not allowed on static bodies.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ArticulationChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Assets must contain at least one rigid body</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies have to be UsdGeomXformable prims.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.005</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies cannot be part of a scene graph instance.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.006</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies can not be nested unless xformOp reset xform stack is used.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.007</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies _or_ their descendant collision shapes must have a mass specification.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyMassChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.009</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies have to be UsdGeomXformable prims without skew matrix.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.010</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Invisible collision meshes must have their purpose attribute set to 'guide' to be properly excluded from rendering.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>InvisibleCollisionMeshHasPurposeGuide</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Colliding Gprims must apply the Collision API.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">**UsdPhysicsMeshCollisionAPI** may only be applied to **UsdGeom.Mesh** prims, and any prim with MeshCollisionAPI must also have **UsdPhysicsCollisionAPI** applied.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderMeshChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The Mesh Collision API can only be assigned to Mesh Prims.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderNonUniformScaleChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.004</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The collision shape scale must be uniform for the following geometries: Sphere, Capsule, Cylinder, Cone & Points.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ColliderChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.MB.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The asset must contain at least two physics rigid bodies.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>MultibodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
  </tbody>
</table>

### Feature: **Driven Joints Neutral** (`FET022_DRIVEN_JOINTS_NEUTRAL` v0.1.0)
*Driven joints enable physics-driven joint simulation for articulated bodies and robotic mechanisms, with proper drive/state configuration, PhysX drive or mimic APIs, and robot-schema integration for Isaac Sim.*

<table width="100%" style="border-collapse: collapse; table-layout: auto;">
  <thead>
    <tr>
      <th align="left" style="width: 12%; min-width: 90px; padding: 8px; border: 1px solid #44474a;">Requirement Code</th>
      <th align="left" style="width: 30%; min-width: 240px; padding: 8px; border: 1px solid #44474a;">Capability Description</th>
      <th align="left" style="width: 23%; min-width: 180px; padding: 8px; border: 1px solid #44474a;">Requirement Description</th>
      <th align="left" style="width: 15%; min-width: 120px; padding: 8px; border: 1px solid #44474a;">Rule Class</th>
      <th align="center" style="width: 10%; min-width: 70px; padding: 8px; border: 1px solid #44474a;">Status</th>
      <th align="left" style="width: 10%; min-width: 150px; padding: 8px; border: 1px solid #44474a;">Details / Issues</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>DJ.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>DJ</strong>: General capability checks.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Physics driven joints must have proper drive and state configuration for controlled simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>PhysicsDriveAndJointState</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>DJ.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>DJ</strong>: General capability checks.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Driven joints must implement proper joint state API for simulation state management.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>JointHasJointStateAPI</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>DJ.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>DJ</strong>: General capability checks.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Driven joints must maintain correct transform relationships and state consistency.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>JointHasCorrectTransformAndState</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>DJ.011</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>DJ</strong>: General capability checks.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulation must have no loops and at most one joint between any two bodies.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ArticulationNoLoopsOrMultiJoint</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies which are not free floating should be connected using joints.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>PhysicsJointCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Targets set to Body0 and Body1 relationships must exist.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>PhysicsJointChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Body0 and Body1 relationships must not have more than one target.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>PhysicsJointChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.ART.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulation roots cannot be nested.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ArticulationChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.ART.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulations are not allowed on kinematic bodies.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ArticulationChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>JT.ART.004</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Joints</strong>: This capability enables creation of articulated mechanical systems with constrained motion, simulation of mechanical assemblies like robots and modeling of mechanical joints with specific degrees of freedom. Joints are fixed attachments that can represent the way a drawer is attached to a cabinet, a wheel to a car, or links of a robot to each other. A joint constrains the movement of rigid bodies and can be created between two rigid bodies or between one rigid body and world. Mathematically, jointed assemblies can be modeled either in maximal (world space) or reduced (relative to other bodies) coordinates. An extension to the joint system based on reduced coordinates is provided with **Articulations**.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulations are not allowed on static bodies.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ArticulationChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Assets must contain at least one rigid body</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies have to be UsdGeomXformable prims.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.005</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies cannot be part of a scene graph instance.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.006</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies can not be nested unless xformOp reset xform stack is used.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.007</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies _or_ their descendant collision shapes must have a mass specification.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyMassChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.009</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Rigid bodies have to be UsdGeomXformable prims without skew matrix.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.010</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Invisible collision meshes must have their purpose attribute set to 'guide' to be properly excluded from rendering.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>InvisibleCollisionMeshHasPurposeGuide</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Colliding Gprims must apply the Collision API.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderCapabilityChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.002</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">**UsdPhysicsMeshCollisionAPI** may only be applied to **UsdGeom.Mesh** prims, and any prim with MeshCollisionAPI must also have **UsdPhysicsCollisionAPI** applied.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderMeshChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.003</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The Mesh Collision API can only be assigned to Mesh Prims.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>RigidBodyColliderNonUniformScaleChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.COL.004</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The collision shape scale must be uniform for the following geometries: Sphere, Capsule, Cylinder, Cone & Points.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>ColliderChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>RB.MB.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>Rigid Bodies</strong>: This capability enables physical simulation of solid objects with constant shape and size as well as collision detection and response between objects, dynamic motion simulation including gravity, forces, and constraints, and integration with physics engines for real-time and offline simulation. A rigid body is an idealized solid object that maintains a constant shape and size regardless of the forces acting upon it, meaning the distance between any two points within the rigid body remains constant during simulation.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">The asset must contain at least two physics rigid bodies.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>MultibodyChecker</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
  </tbody>
</table>

### Feature: **Base Articulation Neutral** (`FET024_BASE_ARTICULATION_NEUTRAL` v0.1.0)
*Base articulation requirements for assets with articulated physics bodies.*

<table width="100%" style="border-collapse: collapse; table-layout: auto;">
  <thead>
    <tr>
      <th align="left" style="width: 12%; min-width: 90px; padding: 8px; border: 1px solid #44474a;">Requirement Code</th>
      <th align="left" style="width: 30%; min-width: 240px; padding: 8px; border: 1px solid #44474a;">Capability Description</th>
      <th align="left" style="width: 23%; min-width: 180px; padding: 8px; border: 1px solid #44474a;">Requirement Description</th>
      <th align="left" style="width: 15%; min-width: 120px; padding: 8px; border: 1px solid #44474a;">Rule Class</th>
      <th align="center" style="width: 10%; min-width: 70px; padding: 8px; border: 1px solid #44474a;">Status</th>
      <th align="left" style="width: 10%; min-width: 150px; padding: 8px; border: 1px solid #44474a;">Details / Issues</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><code>BA.001</code></td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;"><strong>BA</strong>: General capability checks.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a;">Articulated assets must have exactly one ArticulationRootAPI applied to establish the physics simulation root.</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-all;"><code>HasArticulationRoot</code></td>
      <td align="center" valign="top" style="padding: 8px; border: 1px solid #44474a;">✅<br>PASS</td>
      <td valign="top" style="padding: 8px; border: 1px solid #44474a; word-break: break-word; overflow-wrap: break-word;">Requirement met.</td>
    </tr>
  </tbody>
</table>
