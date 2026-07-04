# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `COMP-003`
- Title: Rapid compressor degradation with missing specialist case
- Asset: `COMP-003`
- Asset type: `industrial_air_compressor`
- Failure mode: `rapid_degradation_missing_specialist`
- Decision pattern: `high_urgency_missing_specialist_escalation`

## Layer 1 - Evidence package

- Case ID: `SCENARIO_COMP_003_ALERT-COMP-003-20260603`
- Source payload count: `7`
- Data quality flags: `[]`

## Layer 2 - Contextualization

- Layer 2 ready: `True`
- Derived context: `{'technical_urgency': 'high', 'asset_escalation': 'required', 'operational_constraint': 'high', 'downtime_window': 'near', 'intervention_feasible': False, 'recurrence_risk': 'high', 'human_review_required': True, 'layer2_decision_ready': True}`

## Layer 3 - Case lifecycle

- Case status: `open`
- Lifecycle stage: `evidence_review`
- Event count: `7`
- Task count: `2`
- Milestone count: `5`
- Blockers: `['specialist_technician_not_available']`

## Layer 4 - Decision logic

- Final priority: `critical`
- Recommended execution mode: `constrained_execution`
- Intervention feasible: `False`
- Human review required: `True`
- Triggered rule count: `5`

## Layer 5 - Governed package

- Package ID: `governed_package_SCENARIO_COMP_003_ALERT-COMP-003-20260603`
- Traceability count: `6`
- Recommendation count: `0`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.
