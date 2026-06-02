# OVERSEE governed recommendation package

Package ID: `governed_package_DF_COMP_001_CONTROLLED_MONITORING`
Case ID: `DF_COMP_001_CONTROLLED_MONITORING`
Asset ID: `COMP-001`
Generated at: `2026-06-02T22:06:48.074215+00:00`

## Final recommendation

- Recommended action: Plan immediate inspection and maintenance preparation.
- Priority: high
- Execution mode: controlled_planning
- Human review required: True
- Decision ready: True

## Governance summary

- Source payloads: 7
- Triggered rules: 6
- Recommendation paths: 2
- Traceability entries: 6

## Layer completion

| Layer | Complete |
|---|---:|
| layer_1_external_sources | True |
| layer_2_canonical_context | True |
| layer_3_case_lifecycle | True |
| layer_4_decision_rules | True |
| layer_5_governed_package | True |

## Reviewer notes

- This package is generated from an end-to-end five-layer OVERSEE execution.
- The package is inspectable and preserves source-to-recommendation traceability.
- The current recommendation path uses the migrated deterministic anchor plus explicit DMN-like governance context.

## Traceability overview

| Layer | Artifact | Summary |
|---|---|---|
| Layer 1 | external_source_payloads | Industrial information is exposed as external source payloads. |
| Layer 2 | canonical_case_context | External payloads are normalized into a canonical compressor case context. |
| Layer 3 | case_management_state | The compressor case is managed through events, tasks and milestones. |
| Layer 4 | dmn_like_decision_evaluation | Explicit DMN-like rules evaluate urgency, criticality, feasibility, review and priority. |
| Layer 4 | recommendation_path_outputs | Recommendation paths produce decision outputs under governance context. |
| Layer 5 | governed_recommendation_package | All evidence is packaged into a governed recommendation with traceability. |