# OVERSEE Reference Implementation

This repository contains an executable reference implementation of **OVERSEE** for governed industrial asset-management decision support.

The current milestone is:

```text
v0.4.0 - Generative Digital Factory and live generative OVERSEE workbench
```

The workbench demonstrates a full governed flow where generative AI is used in two controlled places:

1. **Before OVERSEE**, inside the Generative Digital Factory, to generate synthetic external source payloads.
2. **Inside OVERSEE**, as a live generative recommendation path compared against a deterministic anchor.

The final result is not just a model response. It is a governed recommendation package with traceability, deterministic-vs-generative comparison, validation metadata and reviewer-facing outputs.

## Current architecture

The advanced workbench executes this flow:

```text
Generative Digital Factory
-> Layer 1: external source payloads
-> Layer 2: canonical compressor case context
-> Layer 3: CMMN-inspired case lifecycle
-> Layer 4: DMN-like rules
-> Layer 4: deterministic anchor
-> Layer 4: live generative recommendation path
-> Layer 5: advanced governed recommendation package
```

## What the workbench demonstrates

The workbench shows that OVERSEE can:

- generate synthetic industrial source data with generative AI;
- transform generated source-level data into governed Layer 1 payloads;
- normalize the case into a canonical compressor context;
- manage the case through an explicit lifecycle inspired by CMMN;
- evaluate explicit DMN-like decision rules;
- execute a deterministic recommendation path;
- execute a live generative recommendation path;
- compare deterministic and generative recommendations;
- preserve prompt hashes, model-call status, fallback status and validation metadata;
- package the final recommendation as a governed and traceable artifact.

## Main command

From the repository root:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_generative_digital_factory_workbench_smoke.py
```

The script also loads the local `.env` file if present.

The `.env` file is intentionally ignored by Git and must never be committed.

## Expected successful live result

A successful live execution should include:

```json
{
  "factory_model_call_attempted": true,
  "factory_model_call_successful": true,
  "factory_fallback_used": false,
  "oversee_model_call_attempted": true,
  "oversee_model_call_successful": true,
  "oversee_fallback_used": false,
  "final_priority": "high",
  "generative_priority": "high",
  "priority_alignment": true
}
```

## Generated output folder

Each advanced workbench run creates a timestamped folder under:

```text
outputs/generative_digital_factory_workbench_YYYYMMDD_HHMMSS/
```

The v0.4.0 committed evidence package is:

```text
outputs/generative_digital_factory_workbench_20260603_173209/
```

## Generated artifacts

| File | Meaning |
|---|---|
| `00_generative_factory_result.json` | Full Generative Digital Factory execution metadata, including model-call status and fallback status. |
| `00_generative_factory_prompt.txt` | Prompt used to generate synthetic external sources. |
| `00_generative_factory_raw_response.txt` | Raw model response from the Generative Digital Factory call. |
| `00_generative_factory_parsed_sources.json` | Parsed source package generated or validated from the factory output. |
| `01_external_source_payloads.json` | Layer 1 external source payload package. |
| `02_canonical_case_context.json` | Layer 2 canonical compressor context. |
| `03_case_lifecycle_trace.json` | Layer 3 ordered case lifecycle events. |
| `03_case_management_state.json` | Layer 3 case-management state, tasks and milestones. |
| `04_dmn_decision_evaluation.json` | Layer 4 explicit DMN-like rule evaluation. |
| `04_recommendation_path_outputs.json` | Layer 4 deterministic path and rule-governance outputs. |
| `04_live_generative_recommendation.json` | Layer 4 live generative recommendation result and validation metadata. |
| `04_deterministic_vs_generative_comparison.json` | Comparison between deterministic and generative outputs. |
| `05_governed_recommendation_package.json` | Layer 5 advanced governed recommendation package. |
| `05_traceability_index.json` | Traceability index for the package. |
| `05_reviewer_summary.md` | Reviewer-facing summary. |
| `05_execution_manifest.json` | Execution manifest and metadata. |

## Version history

| Tag | Meaning |
|---|---|
| `v0.1.0` | Initial reviewer-facing reference implementation. |
| `v0.2.0` | Five-layer compressor execution. |
| `v0.3.0` | Five-layer OVERSEE with live generative recommendation path. |
| `v0.4.0` | Generative Digital Factory plus live generative OVERSEE workbench. |

## Main source packages

```text
src/oversee/
├── case_context/
├── case_management/
├── comparison/
├── config/
├── decision_rules/
├── deterministic_anchor/
├── digital_factory/
├── domain/
├── governance/
├── grounded_model_path/
├── live_generative_path/
├── model_backed_anchor/
├── reporting/
├── retrieval/
└── utils/
```

## Main modules

| Area | Module |
|---|---|
| Generative Digital Factory | `src/oversee/digital_factory/generative_external_source_factory.py` |
| External sources | `src/oversee/external_sources/` |
| Canonical context | `src/oversee/case_context/` |
| Case lifecycle | `src/oversee/case_management/` |
| DMN-like rules | `src/oversee/decision_rules/dmn_like_rules.py` |
| Live generative recommendation | `src/oversee/decision_rules/live_generative_recommendation.py` |
| Deterministic-vs-generative comparison | `src/oversee/reporting/generative_comparison.py` |
| Governed recommendation package | `src/oversee/reporting/governed_recommendation_package.py` |

## Validation commands

Run the full test suite:

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests\oversee -q
```

Expected result at v0.4.0:

```text
28 passed
```

Run the advanced workbench:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_generative_digital_factory_workbench_smoke.py
```

## Important governance note

The generative model is not allowed to operate as an uncontrolled decision maker.

In this implementation:

- the Digital Factory model generates synthetic source data before Layer 1;
- OVERSEE normalizes and governs the generated data through Layers 1 to 5;
- the live generative recommendation path operates inside Layer 4;
- Layer 5 records model-call status, fallback status, prompt hash, validation metadata and deterministic-vs-generative comparison;
- human review remains required for the high-criticality compressor case.
