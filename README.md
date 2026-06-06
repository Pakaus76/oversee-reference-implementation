# OVERSEE Reference Implementation

## Current baseline

Current validated baseline:

```text
v0.6.0 - 20 executable OVERSEE scenarios formally validated
```

This repository contains an executable reference implementation of **OVERSEE** for governed industrial asset-management decision support.

OVERSEE demonstrates how an industrial predictive alert can be transformed into a governed recommendation package through an explicit five-layer architecture:

```text
Enterprise sources
-> API access layer
-> Layer 1: evidence intake, aggregation and validation
-> Layer 2: contextualization
-> Layer 3: case lifecycle management
-> Layer 4: decision logic and recommendation formulation
-> Layer 5: governed packaging, traceability and workflow handoff
```

The current v0.6.0 baseline extends the earlier paper-aligned compressor case into a formally validated executable scenario library.

---

## What v0.6.0 adds

The current milestone provides:

- 20 executable industrial scenarios.
- 5 master cases for detailed manuals and guided walkthroughs.
- 15 additional coverage cases for broader industrial validation.
- Scenario-backed enterprise API simulation.
- A real multi-scenario Layer 1 to Layer 5 runner.
- Interactive walkthrough support for executable scenarios.
- Formal regression testing of the full scenario library.
- Diagnostic review behaviour for evidence-quality cases such as `DATA-001` and `SENSOR-001`.

---

## Core execution paths

### 1. Multi-scenario all-layers runner

Use this runner when you want to execute one scenario through the real Layer 1 to Layer 5 OVERSEE path:

```powershell
$env:PYTHONPATH = "."
python scripts\run_scenario_all_layers_demo.py --scenario COMP-001
```

List available scenarios:

```powershell
$env:PYTHONPATH = "."
python scripts\run_scenario_all_layers_demo.py --list-scenarios
```

The runner creates a temporary output folder under:

```text
outputs/scenario_all_layers_<scenario_id>_YYYYMMDD_HHMMSS/
```

Each run generates evidence, context, case lifecycle, decision, recommendation and traceability artifacts.

### 2. Interactive walkthrough

Use this runner when you want to explain the architecture step by step:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001
```

Run without pauses:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario DATA-001 --no-pause
```

Show copied artifacts:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario SENSOR-001 --no-pause --show-artifacts
```

### 3. Earlier paper-aligned all-layers demo

The earlier paper-aligned compressor demo remains available for continuity:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_paper_aligned_all_layers_demo.py
```

The recommended v0.6.0 demonstration path is now the multi-scenario runner and the interactive walkthrough.

---

## Scenario library

The executable scenario library contains 20 scenarios.

### Master cases

The 5 master cases are intended for manuals, reviewer-facing explanations and detailed walkthroughs.

| Scenario | Role | Expected behaviour |
|---|---|---|
| `COMP-001` | Paper-aligned compressor case | Critical risk, feasible intervention, controlled planning |
| `COMP-002` | Lower-urgency compressor case | Early warning, standard planning, no overreaction |
| `PUMP-001` | Resource-constrained pump case | High risk, execution constrained by unavailable resources |
| `CONV-001` | Production-maintenance conflict case | High risk with production-window constraint |
| `DATA-001` | Evidence-quality stop case | Contradictory evidence, diagnostic review before action |

### Coverage cases

The 15 additional coverage cases broaden the industrial decision space.

| Scenario | Coverage pattern |
|---|---|
| `FAN-001` | Low-criticality monitoring |
| `MOTOR-001` | Moderate overheating and planned inspection |
| `GEAR-001` | Repeated wear and recurrence-driven intervention |
| `ROBOT-001` | Safety-sensitive robot review |
| `CHILLER-001` | Energy efficiency degradation |
| `BOILER-001` | Safety and compliance escalation |
| `VALVE-001` | Intermittent evidence requiring diagnostic review |
| `AGV-001` | Redundant asset planned replacement |
| `PACK-001` | Bottleneck-driven operational priority |
| `CIP-001` | Quality and availability coordination |
| `HVAC-001` | Environmental condition control |
| `PUMP-002` | Spare available but technician unavailable |
| `COMP-003` | High urgency with missing specialist |
| `SENSOR-001` | Sensor drift validation before intervention |
| `MIXER-001` | Product-quality-driven controlled planning |

For the complete scenario matrix, see:

```text
docs/scenario_coverage_matrix.md
```
For the master-case reviewer demo guide, see:

```text
docs/master_cases_demo_guide.md
```

---

## Main generated artifacts

A real all-layers scenario execution generates the following artifact types:

| File | Meaning |
|---|---|
| `00_scenario.json` | Source scenario definition used for the run. |
| `00_predictive_alert_request.json` | Alert request built from scenario executable inputs. |
| `01_received_predictive_alert.json` | Layer 1 received alert. |
| `01_enterprise_api_calls.json` | Scenario-backed enterprise API calls. |
| `01_aggregated_evidence_package.json` | Layer 1 aggregated evidence package. |
| `01_validation_report.json` | Evidence validation report. |
| `02_canonical_case_context.json` | Canonical case context. |
| `02_layer2_contextualization_result.json` | Layer 2 contextualization output. |
| `03_case_management_state.json` | Case lifecycle and task state. |
| `04_dmn_decision_evaluation.json` | DMN-like decision-rule evaluation. |
| `04_recommendation_path_outputs.json` | Recommendation path outputs. |
| `05_governed_recommendation_package.json` | Final governed recommendation package. |
| `05_traceability_index.json` | Traceability index. |
| `05_execution_manifest.json` | Execution metadata. |
| `05_scenario_execution_summary.md` | Human-readable scenario summary. |

---

## Validation commands

Run the full test suite:

```powershell
$env:PYTHONPATH = "."
python -m pytest tests\oversee -q
```

Expected result at v0.6.0:

```text
88 passed
```

Run the formal full scenario library test only:

```powershell
$env:PYTHONPATH = "."
python -m pytest tests\oversee\integration\test_full_executable_scenario_library.py -q
```

Expected result:

```text
21 passed
```

---

## Main source packages

```text
src/oversee/
â”œâ”€â”€ case_context/
â”œâ”€â”€ case_management/
â”œâ”€â”€ comparison/
â”œâ”€â”€ config/
â”œâ”€â”€ decision_rules/
â”œâ”€â”€ deterministic_anchor/
â”œâ”€â”€ digital_factory/
â”œâ”€â”€ domain/
â”œâ”€â”€ external_sources/
â”œâ”€â”€ governance/
â”œâ”€â”€ grounded_model_path/
â”œâ”€â”€ integration/
â”œâ”€â”€ live_generative_path/
â”œâ”€â”€ model_backed_anchor/
â”œâ”€â”€ reporting/
â”œâ”€â”€ retrieval/
â””â”€â”€ utils/
```

---

## Important architectural boundary

The interactive walkthrough is a demo/presentation layer.

The dependency direction must remain:

```text
demo -> src/oversee
```

Never:

```text
src/oversee -> demo
```

If the `demo/` folder is removed, the OVERSEE core should continue to work.

---

## Version history

| Tag | Meaning |
|---|---|
| `v0.1.0` | Initial reviewer-facing reference implementation. |
| `v0.2.0` | Five-layer compressor execution. |
| `v0.3.0` | Five-layer OVERSEE with live generative recommendation path. |
| `v0.4.0` | Generative Digital Factory plus live generative OVERSEE workbench. |
| `v0.5.0` | Paper-aligned five-layer compressor demo. |
| `v0.5.1` | Documentation update for the paper-aligned demo. |
| `v0.5.2` | Initial interactive walkthrough demo. |
| `v0.5.3` | Interactive walkthrough demo manual. |
| `v0.5.4` | Public naming cleanup. |
| `v0.5.5` | Executable multi-scenario all-layers runner. |
| `v0.5.6` | Scenario runner test-output cleanup. |
| `v0.5.7` | Interactive walkthrough connected to the executable scenario runner. |
| `v0.5.8` | Five executable master scenarios. |
| `v0.5.9` | `DATA-001` diagnostic evidence-quality review case. |
| `v0.6.0` | 20 executable OVERSEE scenarios formally validated. |
