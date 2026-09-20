# Workcell Digital Twin: Engineering & AI Skills Documentation

This directory is the consolidated base repository for all engineering specifications, architecture manuals, and autonomous AI agent skills across the **Workcell Digital Twin** project.

```text
docs/
├── simready/                          # SimReady (Simulation-Ready) Asset Standards
│   ├── README.md                      # Track overview and navigation
│   ├── standalone/                    # Human engineering specification & CAD triage
│   │   ├── README.md
│   │   └── cad_remediation_cheatsheet.md
│   └── gemini_skills/                 # AI agent skill (SimReady CAD conditioning)
│       └── simready-cad-pipeline/
│           ├── SKILL.md
│           ├── references/
│           └── scripts/
│
└── workcell-digitaltwin/              # Workcell Stage Architecture & Kinematics
    ├── README.md                      # Track overview and navigation
    ├── human_guide/                   # Human engineering manual & architectural blueprint
    │   └── workcell_digitaltwin_skills.md
    ├── antigravity_skill/             # Antigravity/Gemini agent skill
    │   └── SKILL.md
    ├── generic_ai_skill/              # Model-agnostic AI agent skill
    │   └── SKILL.md
    └── helper_scripts/                # CI/CD validation runners
        ├── full_system_verification.py
        └── verify_material_localization.py
```

---

## Directory Tracks

### 1. [`simready/`](./simready/)
Focuses on individual OpenUSD assets adhering to **NVIDIA SimReady standards**:
- CAD ingestion, mass properties, physics colliders, and metadata profiles (`Prop-Robotics-Neutral`, `Robot-Body-Neutral`).
- Automated triage scripts and fixes for SimReady compliance codes (`UN.007`, `PMT.001`, `NP.008`, `AA.001`, `VM.TEX.002`, `GSP.001`).

### 2. [`workcell-digitaltwin/`](./workcell-digitaltwin/)
Focuses on the composed multi-component industrial digital twin (`workcell_digitaltwin.usd`):
- 4-sublayer stack decomposition (`layout`, `physics`, `lighting`, `automation`).
- Strict USD Model Hierarchy (`assembly`, `group`, `component`, `subcomponent`).
- Cold-start spatial indexing with `GeomModelAPI` `extentsHint`.
- `UsdGeomPointInstancer` CAD optimization (-87.1% prims on 16 EV battery cells).
- Robot station decoupling with `EndEffector` variant sets (`Robotiq_2F_85`, `Vacuum_Gripper`, `None`).
- Featherstone articulation unification: Single root at UR10 base and `IsaacRobotAPI` kinematic mapping (14 joints, 16 links).
- 100% component-local material encapsulation and GroundPlane fixture componentization.
- Continuous integration automated verification test suite.
