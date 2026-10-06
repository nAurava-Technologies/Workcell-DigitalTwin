# SimReady Profiles & Validation Rules Reference

This reference catalog defines the standard profiles, features, and atomic requirement rule codes enforced by the NVIDIA SimReady foundation validator.

---

## 1. SimReady Profiles

### 1.1 `Prop-Robotics-Neutral` (v1.0.0)
* **Target:** Industrial props, tables, bins, fences, fixtures, scanners, conveyor frames, pallets, workpieces, and batteries.
* **Contract:** Assets must be simulation-ready, atomic (self-contained), scaled in meters, physically reactive, and afford robotic interaction without proprietary platform locks.
* **Feature Manifest:**
  * `FET000_CORE` (v0.1.0) — Core naming, relative asset paths, metadata sidecars, atomicity.
  * `FET001_BASE_NEUTRAL` (v0.1.0) — Meters scale (`1.0`), Z-up axis, model hierarchy, manifold meshes.
  * `FET003_BASE_NEUTRAL` (v0.1.0) — Rigid body physics, collision meshes, mass/density, bound physics materials.
  * `FET004_BASE_NEUTRAL` (v0.1.0) — **Optional (`optional = true`)**. Required only if the prop is explicitly authored as a multi-body jointed mechanism. Single-rigid-body props pass conformance without this feature.
  * `FET005_BASE_NEUTRAL` (v0.1.0) — Vision-guided grasp interaction affordance vector.
  * `FET006_BASE_MDL` (v0.1.0) — Standard MDL shaders, local texture references, color space conformance.

### 1.2 `Robot-Body-Isaac` (v1.0.0) — Digital Twin Native Target
* **Target:** Isaac Sim-native articulated robot manipulators (e.g., UR10 at `components/robot_station/ur10/simready_isaac_usd/ur10.usda`).
* **Contract:** Isaac Sim payload structure, Isaac namespace declarations, drive controllers, dynamic link mass/inertia, and PhysX kinematic articulations.
* **Feature Manifest:**
  * `FET001_BASE_NEUTRAL` (v0.1.0) — Meters scale (`1.0`), Z-up axis, manifold geometries.
  * `FET004_ROBOT_PHYSX` (v0.2.0) — Multi-body kinematic joints, revolute joint limits, and PhysX colliders.
  * `FET021_ROBOT_CORE_ISAAC` (v0.2.0) — Isaac robot metadata, namespaces, sensor attachments, and camera bindings.
  * `FET022_DRIVEN_JOINTS_ISAAC` (v0.1.0) — Isaac Sim joint drive controllers, damping/stiffness, velocity targets (`pxr.PhysxSchema`).
  * `FET024_BASE_ARTICULATION_PHYSX` (v0.1.0) — Unified articulation root on root link or world joint with PhysX clearance.
  * `FET100_BASE_ISAACSIM` (v0.1.0) — Isaac Sim composition structure (payloads, references, variant sets).

### 1.3 `Robot-Body-Neutral` (v1.0.0) — OpenUSD Portable Baseline
* **Target:** OpenUSD-neutral robot manipulators (e.g., `components/robot_station/ur10/simready_usd/ur10.usda`).
* **Contract:** Kinematic link tree, mass and inertia tensors, revolute/prismatic joint definitions, and root articulation without proprietary runtime schemas.
* **Feature Manifest:**
  * `FET001_BASE_NEUTRAL` (v0.1.0) — Scale, units, orientation.
  * `FET003_BASE_NEUTRAL` (v0.1.0) — Link mass properties and dynamic link colliders.
  * `FET004_BASE_NEUTRAL` (v0.1.0) — Multi-body joint limits, kinematics, link connections.
  * `FET024_BASE_ARTICULATION_NEUTRAL` (v0.1.0) — Unified articulation root on root link or world joint.
  * `FET022_DRIVEN_JOINTS_NEUTRAL` (v0.1.0) — Evaluated in Omniverse Kit / Isaac Sim runtime where `pxr.PhysxSchema` joint states are loaded.

---

## 2. Atomic Requirement Rule Catalog

### 2.1 Core & Layout (`FET000_CORE`)

| Rule Code | Description | Conformance Requirement |
| :--- | :--- | :--- |
| **`AA.001`** | Atomic Asset Requirement | The asset must be 100% self-contained. All referenced textures, shaders, and payloads must resolve to local relative paths (`./...`). Zero remote URLs (`http://`, `https://`, `s3://`, `omniverse://`). |
| **`NP.002`** | Lowercase Naming | Directory and asset file names must use lowercase alphanumeric characters and underscores only. |
| **`NP.005`** | Asset Path Layout | The main USD stage must reside at standard hierarchy: `asset_root/<asset_file>.usd` or `asset_root/<intermediate>/<asset_file>.usd`. |
| **`NP.008`** | Path Resolution | All asset path attributes (`SdfAssetPath`) must successfully resolve to existing files on disk. |
| **`SR.001`** | SimReady Metadata | The root USD layer must contain a `customLayerData["SimReady_Metadata"]` dictionary with `asset_name`, `asset_type`, and `simready_version`. |

### 2.2 Units & Model Hierarchy (`FET001_BASE_NEUTRAL`)

| Rule Code | Description | Conformance Requirement |
| :--- | :--- | :--- |
| **`UN.006`** | Up-Axis Standard | Stage metadata `upAxis` must be authored and set to `"Z"`. |
| **`UN.007`** | Length Scale Standard | Stage metadata `metersPerUnit` must be authored and set to `1.0` (meters). |
| **`HI.001`** | Single Default Prim | Stage must define exactly one `defaultPrim` pointing to the asset root. |
| **`HI.002`** | Root Prim Kind | The root prim must have `kind = "component"` (or `"assembly"` for multi-asset stages). |
| **`HI.010`** | Defined Prims | No uncomposed or undefined `over` prims at stage root. |
| **`VG.001`** | Manifold Geometry | Meshes must have valid face vertex counts, non-empty indices, and manifold topologies. |

### 2.3 Physics Bodies & Colliders (`FET003_BASE_NEUTRAL`)

| Rule Code | Description | Conformance Requirement |
| :--- | :--- | :--- |
| **`RB.001`** | Rigid Body API | Dynamic entities must have `UsdPhysics.RigidBodyAPI` applied. |
| **`RB.007`** | Explicit Mass / Density | Bodies must have `UsdPhysics.MassAPI` applied with positive `physics:mass` or `physics:density`. |
| **`RB.COL.001`** | Collision Geometry | Collider meshes must have `UsdPhysics.CollisionAPI` applied. Must be leaf `UsdGeom.Mesh` prims. |
| **`RB.COL.002`** | Collision Approximation | Meshes acting as colliders must have `UsdPhysics.MeshCollisionAPI` with `approximation = "convexHull"` or `"convexDecomposition"`. |
| **`PMT.001`** | Physics Material Binding | Every collider prim must have a direct `material:binding:physics` relationship to a valid `UsdPhysics.MaterialAPI` defining static/dynamic friction and restitution. |

### 2.4 Multi-Body & Articulation (`FET004`, `FET024`)

| Rule Code | Description | Conformance Requirement |
| :--- | :--- | :--- |
| **`RB.MB.001`** | Multibody Assembly | Asserts asset has $\ge 2$ rigid bodies connected by joints (optional for props). |
| **`DJ.001`** | Driven Joint Definition | Articulated joints must specify `UsdPhysics.DriveAPI` with target stiffness, damping, and force limits. |
| **`AR.001`** | Articulation Root | Exactly one `UsdPhysics.ArticulationRootAPI` must be authored on the kinematic chain root or base joint. |

### 2.5 Robotic Affordances (`FET005_BASE_NEUTRAL`)

| Rule Code | Description | Conformance Requirement |
| :--- | :--- | :--- |
| **`GSP.001`** | Grasp Affordance Vector | Asset must have a `UsdGeom.BasisCurves` prim authored under `/<AssetRoot>/grasp_identifier_01` (type `"linear"`, 2 vertices) indicating the valid gripper approach/grasp orientation. |

### 2.6 Visual Materials & Shaders (`FET006_BASE_MDL`)

| Rule Code | Description | Conformance Requirement |
| :--- | :--- | :--- |
| **`VM.MDL.001`** | MDL Shader Definition | Shaders must reference a valid MDL file (e.g. `./material/OmniPBR.mdl`) via `info:mdl:sourceAsset`. |
| **`VM.TEX.001`** | Texture Resolution | Texture maps should adhere to power-of-two dimensions (e.g. 1024x1024, 2048x2048). |
| **`VM.TEX.002`** | Texture Color Space | Texture asset inputs (e.g., `inputs:diffuse_texture`) must explicitly define `colorSpace = "raw"` unless matching standard sRGB diffuse color channels. |
