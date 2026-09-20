# Workcell Digital Twin Documentation & AI Skills Suite

Welcome to the **Workcell Digital Twin** engineering, architecture, and automation suite.

This directory consolidates the engineering manuals, multi-agent AI skills, and verification automation for the OpenUSD workcell digital twin asset (`workcell_digitaltwin.usd`):

```text
docs/workcell-digitaltwin/
├── README.md                      # This directory guide
│
├── human_guide/                   # Human Engineering Manual
│   └── workcell_digitaltwin_skills.md  # Comprehensive OpenUSD architectural guide
│
├── antigravity_skill/             # Antigravity & Gemini AI Agent Skill
│   └── SKILL.md                   # AI skill entry point (with YAML frontmatter)
│
├── generic_ai_skill/              # Generic AI Agent Skill
│   └── SKILL.md                   # Model-agnostic AI agent playbook & system prompt
│
└── helper_scripts/                # CI/CD & Validation Test Runners
    ├── full_system_verification.py     # Complete stage integrity verification
    └── verify_material_localization.py # Material encapsulation & binding audit
```

---

## Directory Guides

### 1. [`human_guide/`](./human_guide/)
* **Target Audience:** Robotics engineers, simulation architects, 3D technical directors, and pipeline developers.
* **Purpose:** A publication-grade architectural blueprint detailing:
  - The 4-sublayer stack (`layout.usda`, `physics.usda`, `lighting.usda`, `automation.usda`) and LIVRPS composition order.
  - Strict USD Model Hierarchy rules (`assembly`, `group`, `component`, `subcomponent`).
  - Cold-start spatial indexing via `GeomModelAPI` and `extentsHint` for $O(1)$ zero-payload bounds calculation.
  - Multi-prototype `UsdGeomPointInstancer` CAD optimization (-87.1% prims on 16 EV battery cells).
  - Decoupled robot workstation assembly with hot-swappable `EndEffector` variant sets (`Robotiq_2F_85`, `Vacuum_Gripper`, `None`).
  - Featherstone articulation unification: Suppressing dual roots via `delete apiSchemas = ["PhysicsArticulationRootAPI"]` and applying `IsaacRobotAPI` (14 joints, 16 links).
  - 100% component-local material encapsulation and GroundPlane fixture packaging.
* **Key File:** [`human_guide/workcell_digitaltwin_skills.md`](./human_guide/workcell_digitaltwin_skills.md).

### 2. [`antigravity_skill/`](./antigravity_skill/)
* **Target Audience:** Google Antigravity, Gemini CLI, and Gemini IDE autonomous agents.
* **Purpose:** Packaged according to the **Antigravity Customization System** standard (`SKILL.md` with YAML frontmatter). It utilizes progressive disclosure so that an autonomous agent can diagnose stage health, execute procedural refactoring, and verify invariants without hallucination.
* **Key File:** [`antigravity_skill/SKILL.md`](./antigravity_skill/SKILL.md).

### 3. [`generic_ai_skill/`](./generic_ai_skill/)
* **Target Audience:** Any AI coding assistant (Claude Code, Cursor, Windsurf, GPT, AutoGen, Copilot).
* **Purpose:** Model-agnostic operational manual, persona definition, inviolable rules, and procedural playbooks for OpenUSD and Isaac Sim 6.0 digital twins.
* **Key File:** [`generic_ai_skill/SKILL.md`](./generic_ai_skill/SKILL.md).

### 4. [`helper_scripts/`](./helper_scripts/)
* **Target Audience:** Automated test suites, CI/CD pipelines, and validation runbooks.
* **Key Files:**
  * [`helper_scripts/full_system_verification.py`](./helper_scripts/full_system_verification.py): Validates unloaded bbox extents, model hierarchy, articulation root unification, `IsaacRobotAPI` kinematic mapping, variants, and material bindings.
  * [`helper_scripts/verify_material_localization.py`](./helper_scripts/verify_material_localization.py): Validates that 100% of bound materials reside strictly within their component hierarchy and confirms zero root `/World/Looks` dependencies.
