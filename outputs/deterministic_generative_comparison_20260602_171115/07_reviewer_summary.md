# OVERSEE reviewer demo summary

## Purpose

This demo package shows an executable OVERSEE flow using the migrated Digital
Factory, deterministic anchor, and live generative path.

The purpose is not to prove that the live generative path is universally better
than the deterministic anchor. The purpose is to expose comparable outputs,
fallback behavior, governance signals, and traceability across the same Digital
Factory cases.

## Execution mode

This reviewer package is generated in offline-safe mode by default. The script
removes `OPENAI_API_KEY` from the local process before execution. Therefore, the
live generative path is expected to activate safe fallback behavior rather than
performing an external model call.

## Summary metrics

| Metric | Value |
|---|---:|
| Cases evaluated | 3 |
| Action differences | 0 |
| Priority differences | 0 |
| Rationale differences | 3 |
| Live generative fallback count | 3 |
| Live generative model response count | 0 |
| Live generative evidence reference count | 0 |
| Live generative priority governance count | 0 |

## Interpretation

In the offline-safe run, the live generative path does not call an external
model. It falls back to the governed internal path while preserving comparable
recommendation outputs and traceability signals.

The expected offline pattern is:

- deterministic anchor and live generative path preserve the same action when
  fallback is active;
- deterministic anchor and live generative path preserve the same priority when
  fallback is active;
- rationales differ because the live generative path records the fallback chain
  and governance-relevant execution context;
- model response identifiers are absent because external model execution is
  disabled.

## Generated artifacts

| File | Meaning |
|---|---|
| `01_digital_factory_scenarios.json` | Synthetic Digital Factory cases used as input. |
| `02_oversee_input_candidates.json` | OVERSEE input candidates derived from Digital Factory scenarios. |
| `03_deterministic_anchor_results.json` | Recommendations from the deterministic anchor. |
| `04_live_generative_path_results.json` | Recommendations from the live generative path. |
| `05_deterministic_generative_comparison.json` | Case-by-case comparison rows in JSON format. |
| `05_deterministic_generative_comparison.csv` | Case-by-case comparison rows in CSV format. |
| `06_comparison_summary.json` | Compact summary metrics. |
| `07_reviewer_summary.md` | Human-readable reviewer summary. |
| `08_traceability_index.json` | File-level traceability index with checksums. |
| `09_execution_manifest.json` | Execution manifest for the reviewer demo. |

## Output folder

```text
C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation\outputs\deterministic_generative_comparison_20260602_171115
```
