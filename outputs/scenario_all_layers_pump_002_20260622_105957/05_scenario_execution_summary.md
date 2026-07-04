# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `PUMP-002`
- Title: Pump spare available but technician unavailable case
- Asset: `PUMP-002`
- Asset type: `industrial_pump`
- Failure mode: `bearing_wear`
- Decision pattern: `spare_available_technician_unavailable`

## Layer 1 - Evidence package

- Case ID: `SCENARIO_PUMP_002_ALERT-PUMP-002-20260603`
- Source payload count: `7`
- Data quality flags: `[]`

## Layer 2 - Contextualization

- Layer 2 ready: `True`
- Derived context: `{'technical_urgency': 'high', 'asset_escalation': 'not_required', 'operational_constraint': 'medium', 'downtime_window': 'near', 'intervention_feasible': False, 'recurrence_risk': 'normal', 'human_review_required': True, 'layer2_decision_ready': True}`

## Layer 3 - Case lifecycle

- Case status: `open`
- Lifecycle stage: `evidence_review`
- Event count: `7`
- Task count: `2`
- Milestone count: `5`
- Blockers: `['specialist_technician_not_available']`

## Layer 4 - Decision logic

- Final priority: `medium`
- Recommended execution mode: `constrained_execution`
- Intervention feasible: `False`
- Human review required: `True`
- Triggered rule count: `4`

## Layer 5 - Governed package

- Package ID: `governed_package_SCENARIO_PUMP_002_ALERT-PUMP-002-20260603`
- Traceability count: `6`
- Recommendation count: `0`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.
