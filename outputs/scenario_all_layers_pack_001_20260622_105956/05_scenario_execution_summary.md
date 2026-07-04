# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `PACK-001`
- Title: Packaging bottleneck stoppage case
- Asset: `PACK-001`
- Asset type: `packaging_line_asset`
- Failure mode: `intermittent_stoppages`
- Decision pattern: `bottleneck_driven_operational_priority`

## Layer 1 - Evidence package

- Case ID: `SCENARIO_PACK_001_ALERT-PACK-001-20260603`
- Source payload count: `7`
- Data quality flags: `[]`

## Layer 2 - Contextualization

- Layer 2 ready: `True`
- Derived context: `{'technical_urgency': 'high', 'asset_escalation': 'not_required', 'operational_constraint': 'high', 'downtime_window': 'near', 'intervention_feasible': True, 'recurrence_risk': 'high', 'human_review_required': True, 'layer2_decision_ready': True}`

## Layer 3 - Case lifecycle

- Case status: `open`
- Lifecycle stage: `decision_ready`
- Event count: `7`
- Task count: `2`
- Milestone count: `5`
- Blockers: `[]`

## Layer 4 - Decision logic

- Final priority: `medium`
- Recommended execution mode: `controlled_planning`
- Intervention feasible: `True`
- Human review required: `True`
- Triggered rule count: `5`

## Layer 5 - Governed package

- Package ID: `governed_package_SCENARIO_PACK_001_ALERT-PACK-001-20260603`
- Traceability count: `6`
- Recommendation count: `0`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.
