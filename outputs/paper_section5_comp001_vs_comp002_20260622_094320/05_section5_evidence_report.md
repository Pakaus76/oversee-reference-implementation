# Section 5 Evidence Report

## Execution runs

- **COMP-001**: `C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation\outputs\scenario_all_layers_comp_001_paper_20260622_094320`
- **COMP-002**: `C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation\outputs\scenario_all_layers_comp_002_paper_20260622_094320`

## Scenario overview

### COMP-001

- **asset_id**: COMP-001
- **asset_type**: industrial_air_compressor
- **failure_mode**: bearing_degradation
- **decision_pattern**: critical_but_feasible_controlled_planning
- **confidence_score**: 0.88
- **predictive_horizon_hours**: 48
- **production_pressure**: high
- **production_load_pct**: 92.0
- **next_planned_downtime_hours**: 36.0
- **spare_part_available**: True
- **technician_available_next_shift**: True
- **intervention_feasible**: True
- **human_review_required**: True
- **management_escalation_required**: False

### COMP-002

- **asset_id**: COMP-002
- **asset_type**: industrial_air_compressor
- **failure_mode**: bearing_degradation
- **decision_pattern**: critical_but_constrained_escalation
- **confidence_score**: 0.86
- **predictive_horizon_hours**: 48
- **production_pressure**: very_high
- **production_load_pct**: 98.0
- **next_planned_downtime_hours**: None
- **spare_part_available**: False
- **technician_available_next_shift**: False
- **intervention_feasible**: False
- **human_review_required**: True
- **management_escalation_required**: True

## Cross-scenario matrix

| Demonstration aspect | COMP-001 | COMP-002 | Interpretation |
|---|---|---|---|
| Asset type | industrial_air_compressor | industrial_air_compressor | Comparable asset type. |
| Predictive condition | confidence=0.88; horizon=48h | confidence=0.86; horizon=48h | Predictive conditions are comparable and do not alone explain the recommendation divergence. |
| Operational context | high load; downtime in 36.0h | very_high load; downtime=None | The operational context starts to separate the scenarios. |
| Resource feasibility | spare=True; technician=True; feasible=True | spare=False; technician=False; feasible=False | Resource feasibility is a major source of divergence. |
| Governance context | human_review=True; escalation=False | human_review=True; escalation=True | Both require human review, but only COMP-002 requires management escalation. |
| Layer 2 divergence | Operationally feasible and governance-cleared. | Operationally constrained and escalation-required. | The main divergence begins at contextualization. |
| Expected governed recommendation | Controlled planned intervention. | Deferred intervention, enhanced monitoring, and escalation. | Similar prediction does not imply similar recommendation. |

## Paper claim supported

The two scenarios exhibit comparable predictive conditions, but the contextualization layer introduces operational and governance divergence. This supports the paper claim that prediction similarity does not imply recommendation similarity.

## Generated artifacts

- `00_execution_manifest.json`
- `01_scenario_pair_overview.json`
- `02_figure5_input.json`
- `03_appendix_evidence_bundle.json`
- `04_cross_scenario_matrix.csv`
- `run_comp_001`
- `run_comp_002`