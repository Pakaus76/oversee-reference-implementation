# Reviewer demo walkthrough

## Purpose

This document explains how to run and interpret the final reviewer-facing OVERSEE demo package.

The demo package is designed to show the implemented OVERSEE flow in a way that can be inspected without reading the full source code first.

## Main command

From the repository root:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_oversee_reviewer_demo.py
```

The command creates a timestamped folder under:

```text
outputs/deterministic_generative_comparison_YYYYMMDD_HHMMSS/
```

## Execution mode

The reviewer demo runs in offline-safe mode by default.

This means:

- the script removes `OPENAI_API_KEY` from the local process;
- the live generative path does not perform an external model call;
- fallback behavior is expected;
- the fallback chain is recorded in the live generative rationale.

This mode is useful for reviewers because it makes the package executable without relying on external credentials.

## Execution flow

The implemented flow is:

```text
Digital Factory scenarios
â†’ OVERSEE input candidates
â†’ deterministic anchor recommendations
â†’ live generative path recommendations
â†’ deterministic-versus-generative comparison
â†’ reviewer-facing evidence package
```

## Generated files

| File | What to inspect |
|---|---|
| `01_digital_factory_scenarios.json` | The three Digital Factory cases. |
| `02_oversee_input_candidates.json` | The mapped OVERSEE inputs. |
| `03_deterministic_anchor_results.json` | Deterministic anchor recommendations. |
| `04_live_generative_path_results.json` | Live generative path recommendations and fallback metadata. |
| `05_deterministic_generative_comparison.json` | Case-by-case comparison. |
| `05_deterministic_generative_comparison.csv` | Spreadsheet-readable comparison. |
| `06_comparison_summary.json` | Compact metrics. |
| `07_reviewer_summary.md` | Human-readable explanation. |
| `08_traceability_index.json` | File inventory, sizes and checksums. |
| `09_execution_manifest.json` | Execution metadata and summary. |

## Expected offline summary

In offline-safe mode, the expected summary is:

```json
{
  "case_count": 3,
  "action_differences": 0,
  "priority_differences": 0,
  "rationale_differences": 3,
  "live_generative_fallback_count": 3,
  "live_generative_model_response_count": 0,
  "live_generative_evidence_reference_count": 0,
  "live_generative_priority_governance_count": 0
}
```

## Interpretation

The offline-safe result means that the live generative path was invoked but could not call an external model because the API key was intentionally removed.

Therefore:

- fallback activation is expected;
- actions remain aligned with the deterministic anchor;
- priorities remain aligned with the deterministic anchor;
- rationales differ because the live generative path records the fallback chain;
- no model response identifiers are present.

This is a governance and traceability result, not a performance superiority claim.

## Recommended review order

1. Open `07_reviewer_summary.md`.
2. Open `06_comparison_summary.json`.
3. Open `05_deterministic_generative_comparison.csv`.
4. Compare `03_deterministic_anchor_results.json` and `04_live_generative_path_results.json`.
5. Open `08_traceability_index.json` to inspect artifact completeness and checksums.
6. Open `09_execution_manifest.json` to verify execution mode.

## Current limitation

The current reviewer package validates the offline-safe behavior. A later online run can be added when external model credentials and execution conditions are intentionally configured.
