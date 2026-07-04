# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `ROBOT-001`
- Title: Safety-sensitive robot axis case
- Asset: `ROBOT-001`
- Asset type: `industrial_robot`
- Failure mode: `axis_abnormality`
- Decision pattern: `safety_sensitive_review_required`

## Layer 1 - Evidence package

- Case ID: `SCENARIO_ROBOT_001_ALERT-ROBOT-001-20260603`
- Source payload count: `7`
- Data quality flags: `[]`

## Layer 2 - Contextualization

- Layer 2 ready: `True`
- Derived context: `{'technical_urgency': 'high', 'asset_escalation': 'required', 'operational_constraint': 'high', 'downtime_window': 'near', 'intervention_feasible': True, 'recurrence_risk': 'normal', 'human_review_required': True, 'layer2_decision_ready': True}`

## Layer 3 - Case lifecycle

- Case status: `open`
- Lifecycle stage: `decision_ready`
- Event count: `7`
- Task count: `2`
- Milestone count: `5`
- Blockers: `[]`

## Layer 4 - Decision logic

- Final priority: `high`
- Recommended execution mode: `controlled_planning`
- Intervention feasible: `True`
- Human review required: `True`
- Triggered rule count: `6`

## Layer 5 - Governed package

- Package ID: `governed_package_SCENARIO_ROBOT_001_ALERT-ROBOT-001-20260603`
- Traceability count: `6`
- Recommendation count: `0`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.
