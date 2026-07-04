# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `VALVE-001`
- Title: Intermittent critical valve fault case
- Asset: `VALVE-001`
- Asset type: `critical_valve`
- Failure mode: `intermittent_actuation_fault`
- Decision pattern: `diagnostic_action_before_intervention`

## Layer 1 - Evidence package

- Case ID: `SCENARIO_VALVE_001_ALERT-VALVE-001-20260603`
- Source payload count: `7`
- Data quality flags: `['sensor_historian:intermittent_actuation_signal_requires_confirmation']`

## Layer 2 - Contextualization

- Layer 2 ready: `True`
- Derived context: `{'technical_urgency': 'medium', 'asset_escalation': 'not_required', 'operational_constraint': 'medium', 'downtime_window': 'distant', 'intervention_feasible': True, 'recurrence_risk': 'normal', 'human_review_required': True, 'layer2_decision_ready': True}`

## Layer 3 - Case lifecycle

- Case status: `open`
- Lifecycle stage: `evidence_review`
- Event count: `7`
- Task count: `2`
- Milestone count: `5`
- Blockers: `['sensor_historian:intermittent_actuation_signal_requires_confirmation']`

## Layer 4 - Decision logic

- Final priority: `medium`
- Recommended execution mode: `diagnostic_review`
- Intervention feasible: `True`
- Human review required: `True`
- Triggered rule count: `4`

## Layer 5 - Governed package

- Package ID: `governed_package_SCENARIO_VALVE_001_ALERT-VALVE-001-20260603`
- Traceability count: `6`
- Recommendation count: `0`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.
