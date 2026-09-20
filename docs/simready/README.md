# SimReady Documentation & AI Skills Suite

Welcome to the SimReady engineering and automation suite for the **Workcell Digital Twin** project.

This directory contains two distinct documentation tracks for establishing, auditing, and maintaining **NVIDIA SimReady (Simulation-Ready) OpenUSD** assets across their CAD-to-Simulation lifecycle:

```text
docs/simready/
├── README.md                              # This directory guide
├── final_simready_validation_report.md    # 🟢 Authoritative final validation report
│
├── standalone/                            # Standalone Human & Engineering Guide
│   ├── README.md                          # Comprehensive manual: architecture, specs & pipeline
│   └── cad_remediation_cheatsheet.md      # Quick-lookup triage cheatsheet
│
└── gemini_skills/                         # Modular AI Agent Skill (Gemini / Antigravity)
    └── simready-cad-pipeline/
        ├── SKILL.md                       # Main AI skill entry point (with YAML frontmatter)
        ├── references/
        │   ├── profiles_and_rules.md      # Specification rules & capability codes
        │   └── common_traps_and_fixes.md  # Known traps & environment limitations
        └── scripts/
            ├── audit_asset.py             # Reusable audit CLI runner
            └── remediate_cad_asset.py     # Automated CAD-to-SimReady conditioning template
```

---

## 🏆 Final Validation Report
* **Link:** [`final_simready_validation_report.md`](./final_simready_validation_report.md)
* **Status:** 🟢 **100% SimReady Compliant across all 7 component props, 0 remote S3 URLs, 0 broken material bindings, unified single articulation root, and 100% valid digital twin composition.**

---

## Directory Guides

### 1. [`standalone/`](./standalone/)
* **Target Audience:** Robotics engineers, simulation developers, 3D artists, technical directors, and external automation systems.
* **Purpose:** A complete, standalone architectural specification and runbook explaining OpenUSD SimReady principles, profile requirements (`Prop-Robotics-Neutral`, `Robot-Body-Neutral`), physics authoring standards, material rules, and manual triage procedures.
* **Key Files:**
  * [`standalone/README.md`](./standalone/README.md): In-depth architectural guide and CAD-to-SimReady ingestion protocol.
  * [`standalone/cad_remediation_cheatsheet.md`](./standalone/cad_remediation_cheatsheet.md): Fast code snippets and one-liner fixes for common validation codes (`UN.007`, `PMT.001`, `NP.008`, `AA.001`, `VM.TEX.002`, `GSP.001`).

### 2. [`gemini_skills/`](./gemini_skills/)
* **Target Audience:** Autonomous AI coding agents (Antigravity, Gemini CLI, Claude Code, Cursor, Copilot).
* **Purpose:** Packaged according to the **Antigravity Customization System** standard (`skills/<name>/SKILL.md` with YAML frontmatter). It utilizes progressive disclosure so that an AI agent reading this repository can autonomously evaluate asset compliance, identify regressions when raw CAD updates occur, and run programmatic remediations without hallucination.
* **Location:** Consolidated under [`docs/simready/gemini_skills/simready-cad-pipeline/`](./gemini_skills/simready-cad-pipeline/).
