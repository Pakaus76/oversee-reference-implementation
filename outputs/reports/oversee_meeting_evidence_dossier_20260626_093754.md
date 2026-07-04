# OVERSEE Chapter 5 Meeting Evidence Dossier

Generated at: 2026-06-26T09:38:01

Repository root: `C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation`

## Selected runs

- **COMP-001**: `C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation\outputs\scenario_all_layers_comp_001_paper_20260622_103706`
- **COMP-002**: `C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation\outputs\scenario_all_layers_comp_002_paper_20260622_103706`

# Paper Section 5 detected

No LaTeX Section 5 was automatically detected.

# Cross-scenario decision-state comparison

| Evidence item | COMP-001 | COMP-002 |
|---|---|---|
| `decision_pattern` | `critical_but_feasible_controlled_planning` | `critical_but_constrained_escalation` |
| `predictive_horizon_hours` | `48` | `48` |
| `confidence_score` | `0.88` | `0.86` |
| `production_pressure` | `high` | `very_high` |
| `production_load_pct` | `92.0` | `98.0` |
| `next_planned_downtime_hours` | `36.0` | `36.0` |
| `spare_part_available` | `True` | `False` |
| `specialist_available_next_shift` | `True` | `False` |
| `intervention_feasible` | `True` | `False` |
| `layer2_derived_context` | `{'technical_urgency': 'high', 'asset_escalation': 'required', 'operational_constraint': 'high', 'downtime_window': 'near', 'intervention_feasible': True, 'recurrence_risk': 'high', 'human_review_required': True, 'layer2_decision_ready': True}` | `{'technical_urgency': 'high', 'asset_escalation': 'required', 'operational_constraint': 'medium', 'downtime_window': 'near', 'intervention_feasible': False, 'recurrence_risk': 'high', 'human_review_required': True, 'layer2_decision_ready': True}` |
| `layer3_lifecycle_stage` | `decision_ready` | `evidence_review` |
| `layer3_decision_ready` | `True` | `False` |
| `layer3_blockers` | `[]` | `['spare_part_not_available', 'specialist_technician_not_available']` |
| `layer4_final_priority` | `high` | `high` |
| `layer4_execution_mode` | `controlled_planning` | `constrained_execution` |
| `layer4_intervention_feasible` | `True` | `False` |
| `layer5_final_action` | `Plan immediate inspection and maintenance preparation.` | `Escalate the constrained maintenance case, resolve execution blockers, increase monitoring, and prepare intervention once feasibility is restored.` |
| `layer5_transformation_applied` | `False` | `True` |
| `layer5_transformation_reasons` | `[]` | `['intervention_not_feasible', 'case_not_decision_ready', 'constrained_execution_mode']` |
| `layer5_traceability_count` | `6` | `6` |

# COMP-001 technical walkthrough

Execution folder: `C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation\outputs\scenario_all_layers_comp_001_paper_20260622_103706`

## Scenario input

```json
{
  "scenario_id": "COMP-001",
  "title": "Paper compressor case",
  "description": "Industrial air compressor with bearing degradation risk. This is the default case aligned with Figure 3 and Section 4.",
  "asset_id": "COMP-001",
  "asset_type": "industrial_air_compressor",
  "failure_mode": "bearing_degradation",
  "paper_aligned": true,
  "master_case": true,
  "master_case_role": "main_paper_case",
  "decision_pattern": "critical_but_feasible_controlled_planning",
  "layer_inputs": {
    "layer1": [
      {
        "source": "PdM analytics service",
        "information": "Bearing degradation alert; confidence 0.88; 48h horizon"
      },
      {
        "source": "Condition monitoring / historian",
        "information": "Rising vibration and temperature trend"
      },
      {
        "source": "Asset registry / engineering master data",
        "information": "Industrial air compressor; high criticality; utility area"
      },
      {
        "source": "CMMS / EAM",
        "information": "Repeated bearing interventions in past 6 months"
      }
    ],
    "layer2": [
      {
        "source": "ERP / MES / production planning",
        "information": "High production pressure; next feasible stop in 36h"
      },
      {
        "source": "MRO inventory / workforce planning",
        "information": "Bearing kit available; technician available next shift"
      },
      {
        "source": "Policy governance / compliance rules",
        "information": "Human review mandatory for high-criticality intervention"
      }
    ],
    "layer3": [
      {
        "source": "Case / workflow management",
        "information": "Case owner assigned; review queue active"
      },
      {
        "source": "Maintenance planning / scheduling",
        "information": "Preparation feasible for next downtime window"
      }
    ],
    "layer4": [
      {
        "source": "Decision rules repository",
        "information": "High-priority rule: degradation risk + narrow downtime window"
      }
    ],
    "layer5": [
      {
        "source": "Human review interface",
        "information": "Reviewer summary prepared for maintenance lead"
      },
      {
        "source": "CMMS / EAM workflow",
        "information": "Work-order proposal ready"
      },
      {
        "source": "Audit / traceability repository",
        "information": "Traceability record stored"
      }
    ]
  },
  "expected_layer_outputs": {
    "layer1": "Validated evidence package: alert, condition trends, asset criticality, and maintenance history",
    "layer2": "Contextualized decision profile: high urgency, near downtime window, intervention feasible, review required",
    "layer3": "Decision-ready case: open, 2 tasks active, 5 milestones reached, no blockers",
    "layer4": "Decision record: high priority, controlled planning, human review retained",
    "layer5": "Governed recommendation package: reviewer summary, traceability index, and work-order proposal"
  },
  "executable_inputs": {
    "alert": {
      "alert_id": "ALERT-COMP-001-20260603",
      "asset_id": "COMP-001",
      "asset_type": "industrial_air_compressor",
      "line_id": "PKG-LINE-01",
      "suspected_failure_mode": "bearing_degradation",
      "alert_type": "predictive_degradation_alert",
      "predictive_horizon_hours": 48,
      "confidence_score": 0.88,
      "model_name": "compressor_failure_risk_model",
      "model_version": "v1.0-reference",
      "triggered_at": "2026-06-03T08:30:00Z"
    },
    "raw_sensor_context": {
      "sampling_window_hours": 24,
      "vibration_mms": [
        1.4,
        1.7,
        2.1,
        2.6,
        2.9
      ],
      "temperature_celsius": [
        74.0,
        77.5,
        81.2,
        85.0,
        88.5
      ],
      "pressure_bar": [
        7.8,
        7.6,
        7.4,
        7.1,
        6.9
      ],
      "alarm_count": 3,
      "last_sensor_timestamp": "2026-06-03T08:25:00Z"
    },
    "requested_context": {
      "maintenance_history_lookback_days": 180,
      "production_context_horizon_hours": 72,
      "include_inventory_and_resources": true,
      "include_policy_governance": true
    },
    "enterprise_sources": {
      "asset_metadata": {
        "asset_id": "COMP-001",
        "asset_type": "industrial_air_compressor",
        "line_id": "PKG-LINE-01",
        "asset_criticality": "high",
        "criticality_score": 5,
        "manufacturer": "Reference Compressor Systems",
        "model": "RC-5500",
        "location": "Packaging area - compressor station"
      },
      "maintenance_history": {
        "asset_id": "COMP-001",
        "lookback_days": 180,
        "recent_repeated_failures": true,
        "work_orders": [
          {
            "work_order_id": "WO-COMP-001-2026-0418",
            "type": "corrective",
            "failure_mode": "vibration_anomaly",
            "duration_hours": 2.0
          },
          {
            "work_order_id": "WO-COMP-001-2026-0522",
            "type": "corrective",
            "failure_mode": "bearing_noise",
            "duration_hours": 3.5
          }
        ]
      },
      "operational_context": {
        "asset_id": "COMP-001",
        "line_id": "PKG-LINE-01",
        "horizon_hours": 72,
        "production_pressure": "high",
        "production_load_pct": 92.0,
        "next_planned_downtime_hours": 36.0,
        "customer_impact": "medium",
        "shift_demand": "high"
      },
      "inventory_and_resources": {
        "asset_id": "COMP-001",
        "spare_part_available": true,
        "spare_part_id": "SP-COMP-BEARING-KIT",
        "specialist_technician_available_next_shift": true,
        "intervention_feasible": true
      },
      "policy_governance": {
        "asset_type": "industrial_air_compressor",
        "criticality_score": 5,
        "mandatory_human_review_for_high_criticality": true,
        "expected_human_review_required": true,
        "policy_id": "POL-COMP-HIGH-CRIT-001"
      }
    }
  }
}
```
## Layer 1: evidence intake and validation

### Validation report

```json
{
  "valid": true,
  "missing_sources": [],
  "payloads_with_quality_flags": [],
  "payload_count": 7,
  "required_source_count": 7
}
```
### Payload map

| Source | Source type | Normalized fields | Raw fields | Data quality flags |
|---|---|---|---|---|
| `asset_registry` | `master_data` | `asset_type, asset_criticality, criticality_score` | `asset_id, asset_type, line_id, asset_criticality, criticality_score, manufacturer, model, location` | `[]` |
| `sensor_historian` | `raw_sensor_context` | `vibration_trend, temperature_trend, sensor_severity` | `sampling_window_hours, vibration_mms, temperature_celsius, pressure_bar, alarm_count, last_sensor_timestamp` | `[]` |
| `predictive_maintenance` | `model_inference` | `alert_type, estimated_time_to_failure_hours, confidence_score, alert_severity` | `alert_id, asset_id, asset_type, line_id, suspected_failure_mode, alert_type, predictive_horizon_hours, confidence_score, model_name, model_version, triggered_at` | `[]` |
| `maintenance_history` | `work_order_history` | `recent_repeated_failures` | `asset_id, lookback_days, recent_repeated_failures, work_orders` | `[]` |
| `production_planning` | `operational_context` | `production_load_pct, next_planned_downtime_hours, production_pressure` | `asset_id, line_id, horizon_hours, production_pressure, production_load_pct, next_planned_downtime_hours, customer_impact, shift_demand` | `[]` |
| `inventory_and_resources` | `resource_availability` | `spare_part_available, specialist_technician_available_next_shift, intervention_feasible` | `asset_id, spare_part_available, spare_part_id, specialist_technician_available_next_shift, intervention_feasible` | `[]` |
| `policy_governance` | `governance_policy` | `mandatory_human_review_for_high_criticality, expected_human_review_required` | `asset_type, criticality_score, mandatory_human_review_for_high_criticality, expected_human_review_required, policy_id` | `[]` |

## Canonical Context: field-level evidence

| Canonical field | Value |
|---|---|
| `context_id` | `canonical_context_SCENARIO_COMP_001_ALERT-COMP-001-20260603` |
| `case_id` | `SCENARIO_COMP_001_ALERT-COMP-001-20260603` |
| `asset.asset_id` | `COMP-001` |
| `asset.asset_type` | `industrial_air_compressor` |
| `asset.line_id` | `PKG-LINE-01` |
| `asset.criticality_label` | `high` |
| `asset.criticality_score` | `5` |
| `asset.process_role` | `None` |
| `predictive_evidence.alert_type` | `predictive_degradation_alert` |
| `predictive_evidence.estimated_time_to_failure_hours` | `48.0` |
| `predictive_evidence.confidence_score` | `0.88` |
| `predictive_evidence.alert_severity` | `high` |
| `predictive_evidence.vibration_trend` | `increasing` |
| `predictive_evidence.temperature_trend` | `increasing` |
| `operational_context.production_load_pct` | `92.0` |
| `operational_context.next_planned_downtime_hours` | `36.0` |
| `operational_context.production_pressure` | `high` |
| `operational_context.business_impact_if_unavailable` | `None` |
| `maintenance_resources.recent_repeated_failures` | `True` |
| `maintenance_resources.spare_part_available` | `True` |
| `maintenance_resources.specialist_technician_available_next_shift` | `True` |
| `maintenance_resources.intervention_feasible` | `True` |
| `governance_policy.mandatory_human_review_for_high_criticality` | `True` |
| `governance_policy.expected_human_review_required` | `True` |
| `governance_policy.computed_human_review_required` | `True` |
| `source_payload_count` | `7` |
| `source_names` | `[list:7]` |
| `data_quality_flags` | `[list:0]` |
| `key_risk_drivers` | `[list:7]` |
| `context_version` | `0.1.0` |

### Layer 1 to Canonical Context transformation candidates

| Layer 1 source | Normalized field | Normalized value | Canonical target candidate | Transformation type |
|---|---|---|---|---|
| `asset_registry` | `asset_type` | `industrial_air_compressor` | `asset.asset_type` | `renamed/grouped` |
| `asset_registry` | `asset_criticality` | `high` | `not directly present` | `discarded or indirectly used` |
| `asset_registry` | `criticality_score` | `5` | `asset.criticality_score` | `renamed/grouped` |
| `sensor_historian` | `vibration_trend` | `increasing` | `predictive_evidence.vibration_trend` | `renamed/grouped` |
| `sensor_historian` | `temperature_trend` | `increasing` | `predictive_evidence.temperature_trend` | `renamed/grouped` |
| `sensor_historian` | `sensor_severity` | `high` | `not directly present` | `discarded or indirectly used` |
| `predictive_maintenance` | `alert_type` | `predictive_degradation_alert` | `predictive_evidence.alert_type` | `renamed/grouped` |
| `predictive_maintenance` | `estimated_time_to_failure_hours` | `48.0` | `predictive_evidence.estimated_time_to_failure_hours` | `renamed/grouped` |
| `predictive_maintenance` | `confidence_score` | `0.88` | `predictive_evidence.confidence_score` | `renamed/grouped` |
| `predictive_maintenance` | `alert_severity` | `high` | `predictive_evidence.alert_severity` | `renamed/grouped` |
| `maintenance_history` | `recent_repeated_failures` | `True` | `maintenance_resources.recent_repeated_failures` | `renamed/grouped` |
| `production_planning` | `production_load_pct` | `92.0` | `operational_context.production_load_pct` | `renamed/grouped` |
| `production_planning` | `next_planned_downtime_hours` | `36.0` | `operational_context.next_planned_downtime_hours` | `renamed/grouped` |
| `production_planning` | `production_pressure` | `high` | `operational_context.production_pressure` | `renamed/grouped` |
| `inventory_and_resources` | `spare_part_available` | `True` | `maintenance_resources.spare_part_available` | `renamed/grouped` |
| `inventory_and_resources` | `specialist_technician_available_next_shift` | `True` | `maintenance_resources.specialist_technician_available_next_shift` | `renamed/grouped` |
| `inventory_and_resources` | `intervention_feasible` | `True` | `maintenance_resources.intervention_feasible` | `renamed/grouped` |
| `policy_governance` | `mandatory_human_review_for_high_criticality` | `True` | `governance_policy.mandatory_human_review_for_high_criticality` | `renamed/grouped` |
| `policy_governance` | `expected_human_review_required` | `True` | `governance_policy.expected_human_review_required` | `renamed/grouped` |

## Layer 2: contextualization logic

| Rule ID | Rule name | Condition | Triggered | Output field | Output value | Rationale |
|---|---|---|---|---|---|---|
| `L2_R001` | Technical urgency from failure horizon | `IF estimated_time_to_failure_hours <= 72 THEN technical_urgency = high` | `True` | `technical_urgency` | `high` | Short failure horizon increases technical urgency. |
| `L2_R002` | Asset escalation from criticality | `IF criticality_score >= 5 THEN asset_escalation = required` | `True` | `asset_escalation` | `required` | High-criticality assets require explicit escalation. |
| `L2_R003` | Operational constraint from production pressure | `IF production_pressure = high THEN operational_constraint = high` | `True` | `operational_constraint` | `high` | High production pressure constrains maintenance timing. |
| `L2_R004` | Downtime window proximity | `IF next_planned_downtime_hours <= 48 THEN downtime_window = near` | `True` | `downtime_window` | `near` | A near downtime window creates a feasible planning opportunity. |
| `L2_R005` | Intervention feasibility from resources | `IF spare_part_available = true AND specialist_technician_available_next_shift = true THEN intervention_feasible = true` | `True` | `intervention_feasible` | `True` | Available spare parts and specialist capacity make intervention feasible. |
| `L2_R006` | Recurrence risk from repeated failures | `IF recent_repeated_failures = true THEN recurrence_risk = high` | `True` | `recurrence_risk` | `high` | Recent repeated failures increase recurrence risk. |
| `L2_R007` | Human review requirement from governance policy | `IF high criticality policy applies THEN human_review_required = true` | `True` | `human_review_required` | `True` | Governance policy requires accountable human review. |
| `L2_R008` | Layer 2 decision readiness | `IF technical urgency, feasibility and governance context exist THEN layer2_decision_ready = true` | `True` | `layer2_decision_ready` | `True` | Layer 2 has enough contextualized evidence for downstream case lifecycle and decision logic. |

### Derived context

| Variable | Value |
|---|---|
| `technical_urgency` | `high` |
| `asset_escalation` | `required` |
| `operational_constraint` | `high` |
| `downtime_window` | `near` |
| `intervention_feasible` | `True` |
| `recurrence_risk` | `high` |
| `human_review_required` | `True` |
| `layer2_decision_ready` | `True` |

## Layer 3: case lifecycle evidence

- `case_status`: `open`
- `lifecycle_stage`: `decision_ready`
- `human_review_required`: `True`
- `maintenance_planning_required`: `True`
- `decision_ready`: `True`
- `event_count`: `7`
- `task_count`: `2`
- `milestone_count`: `5`
- `blockers`: `[]`

### Tasks

| Task ID | Type | Name | Status | Required role | Trigger |
|---|---|---|---|---|---|
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_task_human_review` | `human_review` | Review compressor risk and approve decision path | `open` | `maintenance_decision_owner` | high criticality or high-severity predictive alert |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_task_maintenance_planning` | `maintenance_planning` | Prepare controlled compressor inspection or intervention | `open` | `maintenance_planner` | short failure horizon with intervention resources available |

### Milestones

| Milestone ID | Name | Status | Criteria |
|---|---|---|---|
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_ms_external_evidence_complete` | External evidence complete | `reached` | asset registry payload present; predictive maintenance payload present; production planning payload present; policy payload present |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_ms_canonical_context_available` | Canonical context available | `reached` | canonical asset context built; predictive evidence normalized; operational context normalized; governance policy normalized |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_ms_human_review_identified` | Human review identified | `reached` | high criticality or high severity; policy requires accountable human review |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_ms_maintenance_planning_required` | Maintenance planning required | `reached` | short failure horizon; resources support controlled planning |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_ms_decision_ready` | Decision-ready case package | `reached` | external evidence received; canonical context built; human review requirement evaluated; maintenance planning requirement evaluated; no unresolved blockers |

## Layer 4: DMN-like decision and recommendation formulation

- `evaluation_id`: `dmn_like_eval_SCENARIO_COMP_001_ALERT-COMP-001-20260603`
- `source_case_state`: `decision_ready`
- `final_priority`: `high`
- `recommended_execution_mode`: `controlled_planning`
- `human_review_required`: `True`
- `intervention_feasible`: `True`
- `triggered_rule_count`: `6`

### DMN rules

| Rule ID | Rule name | Triggered | Inputs | Outputs | Rationale |
|---|---|---|---|---|---|
| `DMN_R001` | Failure horizon urgency | `True` | `{"estimated_time_to_failure_hours": 48.0, "alert_severity": "high"}` | `{"urgency": "high"}` | Estimated failure horizon is within 72 hours. |
| `DMN_R002` | Asset criticality classification | `True` | `{"asset_criticality_label": "high", "asset_criticality_score": 5}` | `{"criticality_band": "high"}` | Asset criticality score is high. |
| `DMN_R003` | Intervention feasibility | `True` | `{"spare_part_available": true, "specialist_technician_available_next_shift": true}` | `{"intervention_feasible": true}` | Spare part and specialist support are available. |
| `DMN_R004` | Accountable human review requirement | `True` | `{"computed_human_review_required": true, "case_state_human_review_required": true}` | `{"human_review_required": true}` | High criticality or high-severity evidence requires accountable review. |
| `DMN_R005` | Execution constraint assessment | `True` | `{"production_pressure": "high", "next_planned_downtime_hours": 36.0, "intervention_feasible": true, "data_quality_flags": []}` | `{"recommended_execution_mode": "controlled_planning"}` | Production pressure is high, but resources are available. Controlled planning is preferred over uncontrolled stop. |
| `DMN_R006` | Final priority consolidation | `True` | `{"urgency": "high", "criticality_band": "high", "intervention_feasible": true, "human_review_required": true, "recommended_execution_mode": "controlled_planning"}` | `{"final_priority": "high", "escalation_required": false}` | Final priority consolidated from urgency=high, criticality=high, intervention_feasible=True, human_review_required=True, execution_mode=controlled_planning. |

### Recommendation path outputs

```json
{
  "bundle_id": "recommendation_paths_SCENARIO_COMP_001_ALERT-COMP-001-20260603",
  "case_id": "SCENARIO_COMP_001_ALERT-COMP-001-20260603",
  "asset_id": "COMP-001",
  "decision_rule_evaluation_id": "dmn_like_eval_SCENARIO_COMP_001_ALERT-COMP-001-20260603",
  "path_outputs": [
    {
      "path_name": "governed_recommendation_formulation",
      "path_type": "governed_recommendation_path",
      "status": "completed",
      "recommendation": {
        "recommendation_id": "governed_rec_SCENARIO_COMP_001_ALERT-COMP-001-20260603",
        "asset_id": "COMP-001",
        "action": "Plan immediate inspection and maintenance preparation.",
        "primary_action": "Plan immediate inspection and maintenance preparation.",
        "anchor_action": "Plan immediate inspection and maintenance preparation.",
        "priority": "high",
        "deterministic_anchor_priority": "high",
        "dmn_like_final_priority": "high",
        "recommended_execution_mode": "controlled_planning",
        "human_review_required": true,
        "intervention_feasible": true,
        "decision_ready": true,
        "transformation_applied": false,
        "transformation_reasons": [],
        "preconditions": [],
        "blockers": [],
        "required_reviews": [
          "Obtain accountable human review before execution."
        ],
        "escalations": [],
        "contingency_actions": [],
        "rationale": "Deterministic anchor proposed: Plan immediate inspection and maintenance preparation. DMN-like final priority: high Execution mode: controlled_planning Intervention feasible: True Decision ready: True Human review required: True The anchor was preserved because the case is feasible and decision-ready."
      },
      "input_refs": [
        "canonical_context_SCENARIO_COMP_001_ALERT-COMP-001-20260603",
        "SCENARIO_COMP_001_ALERT-COMP-001-20260603",
        "dmn_like_eval_SCENARIO_COMP_001_ALERT-COMP-001-20260603"
      ],
      "governance_refs": [
        "compressor_human_review_policy",
        "compressor_final_priority",
        "compressor_execution_mode",
        "recommendation_consistency_constraints"
      ],
      "notes": [
        "The deterministic anchor is used as an initial recommendation.",
        "Layer 4 formulates a governed recommendation by preserving, constraining, transforming, or escalating the anchor according to feasibility, readiness, execution mode, and governance signals."
      ]
    },
    {
      "path_name": "dmn_like_governance_summary",
      "path_type": "rule_governance_summary",
      "status": "completed",
      "recommendation": {
        "case_id": "SCENARIO_COMP_001_ALERT-COMP-001-20260603",
        "asset_id": "COMP-001",
        "final_priority": "high",
        "recommended_execution_mode": "controlled_planning",
        "human_review_required": true,
        "intervention_feasible": true,
        "decision_ready": true,
        "triggered_rule_count": 6
      },
      "input_refs": [
        "canonical_context_SCENARIO_COMP_001_ALERT-COMP-001-20260603",
        "SCENARIO_COMP_001_ALERT-COMP-001-20260603",
        "dmn_like_eval_SCENARIO_COMP_001_ALERT-COMP-001-20260603"
      ],
      "governance_refs": [
        "DMN_R001",
        "DMN_R002",
        "DMN_R003",
        "DMN_R004",
        "DMN_R005",
        "DMN_R006"
      ],
      "notes": [
        "This output summarizes explicit rule evaluation before final governed packaging."
      ]
    }
  ],
  "bundle_version": "0.1.0",
  "path_count": 2
}
```

## Layer 5: governed recommendation package

### Final recommendation

- `case_id`: `SCENARIO_COMP_001_ALERT-COMP-001-20260603`
- `asset_id`: `COMP-001`
- `recommended_action`: `Plan immediate inspection and maintenance preparation.`
- `primary_action`: `Plan immediate inspection and maintenance preparation.`
- `anchor_action`: `Plan immediate inspection and maintenance preparation.`
- `priority`: `high`
- `deterministic_anchor_priority`: `high`
- `dmn_like_final_priority`: `high`
- `recommended_execution_mode`: `controlled_planning`
- `human_review_required`: `True`
- `intervention_feasible`: `True`
- `decision_ready`: `True`
- `transformation_applied`: `False`
- `transformation_reasons`: `[]`
- `preconditions`: `[]`
- `blockers`: `[]`
- `required_reviews`: `['Obtain accountable human review before execution.']`
- `escalations`: `[]`
- `contingency_actions`: `[]`
- `key_risk_drivers`: `['high_asset_criticality', 'short_failure_horizon', 'high_model_confidence', 'high_production_pressure', 'recent_repeated_failures', 'intervention_resources_available', 'human_review_required']`
- `rationale`: `Deterministic anchor proposed: Plan immediate inspection and maintenance preparation. DMN-like final priority: high Execution mode: controlled_planning Intervention feasible: True Decision ready: True Human review required: True The anchor was preserved because the case is feasible and decision-ready.`

### Governance summary

- `source_payload_count`: `7`
- `source_names`: `['asset_registry', 'sensor_historian', 'predictive_maintenance', 'maintenance_history', 'production_planning', 'inventory_and_resources', 'policy_governance']`
- `canonical_context_id`: `canonical_context_SCENARIO_COMP_001_ALERT-COMP-001-20260603`
- `case_lifecycle_stage`: `decision_ready`
- `case_event_count`: `7`
- `case_task_count`: `2`
- `case_milestone_count`: `5`
- `triggered_rule_count`: `6`
- `decision_rule_evaluation_id`: `dmn_like_eval_SCENARIO_COMP_001_ALERT-COMP-001-20260603`
- `recommendation_path_count`: `2`
- `human_review_required`: `True`
- `decision_ready`: `True`

### Traceability index

| Trace ID | Layer | Artifact | Type | Summary |
|---|---|---|---|---|
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_trace_001_layer_1` | `Layer 1` | `external_source_payloads` | `external_source_package` | Industrial information is exposed as external source payloads. |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_trace_002_layer_2` | `Layer 2` | `canonical_case_context` | `canonical_context` | External payloads are normalized into a canonical compressor case context. |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_trace_003_layer_3` | `Layer 3` | `case_management_state` | `case_lifecycle` | The compressor case is managed through events, tasks and milestones. |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_trace_004_layer_4_rules` | `Layer 4` | `dmn_like_decision_evaluation` | `decision_rules` | Explicit DMN-like rules evaluate urgency, criticality, feasibility, review and priority. |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_trace_005_layer_4_paths` | `Layer 4` | `recommendation_path_outputs` | `recommendation_paths` | Layer 4 formulates a governed recommendation under feasibility, readiness, execution-mode and governance constraints. |
| `SCENARIO_COMP_001_ALERT-COMP-001-20260603_trace_006_layer_5` | `Layer 5` | `governed_recommendation_package` | `governed_package` | Layer 5 packages the governed recommendation with traceability and reviewer-facing controls. |

## Execution summary artifact

# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `COMP-001`
- Title: Paper compressor case
- Asset: `COMP-001`
- Asset type: `industrial_air_compressor`
- Failure mode: `bearing_degradation`
- Decision pattern: `critical_but_feasible_controlled_planning`

## Layer 1 - Evidence package

- Case ID: `SCENARIO_COMP_001_ALERT-COMP-001-20260603`
- Source payload count: `7`
- Data quality flags: `[]`

## Layer 2 - Contextualization

- Layer 2 ready: `True`
- Derived context: `{'technical_urgency': 'high', 'asset_escalation': 'required', 'operational_constraint': 'high', 'downtime_window': 'near', 'intervention_feasible': True, 'recurrence_risk': 'high', 'human_review_required': True, 'layer2_decision_ready': True}`

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

- Package ID: `governed_package_SCENARIO_COMP_001_ALERT-COMP-001-20260603`
- Traceability count: `6`
- Recommendation count: `0`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.

# COMP-002 technical walkthrough

Execution folder: `C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation\outputs\scenario_all_layers_comp_002_paper_20260622_103706`

## Scenario input

```json
{
  "scenario_id": "COMP-002",
  "title": "Paper compressor constrained case",
  "description": "Industrial air compressor with comparable bearing degradation risk but constrained operational and governance context. Designed for Section 5 comparison against COMP-001.",
  "asset_id": "COMP-002",
  "asset_type": "industrial_air_compressor",
  "failure_mode": "bearing_degradation",
  "paper_aligned": true,
  "master_case": true,
  "master_case_role": "section5_comparison_case",
  "decision_pattern": "critical_but_constrained_escalation",
  "layer_inputs": {
    "layer1": [
      {
        "source": "PdM analytics service",
        "information": "Bearing degradation alert; confidence 0.86; 48h horizon"
      },
      {
        "source": "Condition monitoring / historian",
        "information": "Rising vibration and temperature trend"
      },
      {
        "source": "Asset registry / engineering master data",
        "information": "Industrial air compressor; high criticality; utility area"
      },
      {
        "source": "CMMS / EAM",
        "information": "Repeated bearing interventions in past 6 months"
      }
    ],
    "layer2": [
      {
        "source": "ERP / MES / production planning",
        "information": "Very high production pressure; no feasible stop within 72h"
      },
      {
        "source": "MRO inventory / workforce planning",
        "information": "Bearing kit unavailable; specialist technician unavailable for next 72h"
      },
      {
        "source": "Policy governance / compliance rules",
        "information": "Human review and management escalation required before intervention"
      }
    ],
    "layer3": [
      {
        "source": "Case / workflow management",
        "information": "Case owner assigned; escalation queue active"
      },
      {
        "source": "Maintenance planning / scheduling",
        "information": "Preparation blocked by spare-part and workforce constraints"
      }
    ],
    "layer4": [
      {
        "source": "Decision rules repository",
        "information": "Escalation rule: degradation risk + infeasible intervention + operational constraint"
      }
    ],
    "layer5": [
      {
        "source": "Human review interface",
        "information": "Escalation summary prepared for maintenance and operations leads"
      },
      {
        "source": "CMMS / EAM workflow",
        "information": "Monitoring and contingency work-order proposal ready"
      },
      {
        "source": "Audit / traceability repository",
        "information": "Traceability record stored"
      }
    ]
  },
  "expected_layer_outputs": {
    "layer1": "Validated evidence package: alert, condition trends, asset criticality, and maintenance history",
    "layer2": "Contextualized decision profile: high urgency, no feasible downtime window, intervention constrained, escalation required",
    "layer3": "Escalation-required case: open, blockers active, escalation path required",
    "layer4": "Decision record: high priority, deferred intervention, enhanced monitoring, management escalation",
    "layer5": "Governed recommendation package: escalation summary, traceability index, and monitoring/contingency proposal"
  },
  "executable_inputs": {
    "alert": {
      "alert_id": "ALERT-COMP-002-20260603",
      "asset_id": "COMP-002",
      "asset_type": "industrial_air_compressor",
      "line_id": "PKG-LINE-02",
      "suspected_failure_mode": "bearing_degradation",
      "alert_type": "predictive_degradation_alert",
      "predictive_horizon_hours": 48,
      "confidence_score": 0.86,
      "model_name": "compressor_failure_risk_model",
      "model_version": "v1.0-reference",
      "triggered_at": "2026-06-03T08:30:00Z"
    },
    "raw_sensor_context": {
      "sampling_window_hours": 24,
      "vibration_mms": [
        1.5,
        1.8,
        2.2,
        2.7,
        3.0
      ],
      "temperature_celsius": [
        73.5,
        77.0,
        80.8,
        84.6,
        88.0
      ],
      "pressure_bar": [
        7.9,
        7.7,
        7.5,
        7.2,
        7.0
      ],
      "alarm_count": 3,
      "last_sensor_timestamp": "2026-06-03T08:25:00Z"
    },
    "requested_context": {
      "maintenance_history_lookback_days": 180,
      "production_context_horizon_hours": 72,
      "include_inventory_and_resources": true,
      "include_policy_governance": true
    },
    "enterprise_sources": {
      "asset_metadata": {
        "asset_id": "COMP-002",
        "asset_type": "industrial_air_compressor",
        "line_id": "PKG-LINE-02",
        "asset_criticality": "high",
        "criticality_score": 5,
        "manufacturer": "Reference Compressor Systems",
        "model": "RC-5500",
        "location": "Packaging area - compressor station"
      },
      "maintenance_history": {
        "asset_id": "COMP-002",
        "lookback_days": 180,
        "recent_repeated_failures": true,
        "work_orders": [
          {
            "work_order_id": "WO-COMP-002-2026-0416",
            "type": "corrective",
            "failure_mode": "vibration_anomaly",
            "duration_hours": 2.2
          },
          {
            "work_order_id": "WO-COMP-002-2026-0520",
            "type": "corrective",
            "failure_mode": "bearing_noise",
            "duration_hours": 3.8
          }
        ]
      },
      "operational_context": {
        "asset_id": "COMP-002",
        "line_id": "PKG-LINE-02",
        "horizon_hours": 72,
        "production_pressure": "very_high",
        "production_load_pct": 98.0,
        "next_planned_downtime_hours": null,
        "customer_impact": "high",
        "shift_demand": "very_high"
      },
      "inventory_and_resources": {
        "asset_id": "COMP-002",
        "spare_part_available": false,
        "spare_part_id": "SP-COMP-BEARING-KIT",
        "specialist_technician_available_next_shift": false,
        "intervention_feasible": false
      },
      "policy_governance": {
        "asset_type": "industrial_air_compressor",
        "criticality_score": 5,
        "mandatory_human_review_for_high_criticality": true,
        "expected_human_review_required": true,
        "management_escalation_required": true,
        "policy_id": "POL-COMP-HIGH-CRIT-ESC-002"
      }
    }
  }
}
```
## Layer 1: evidence intake and validation

### Validation report

```json
{
  "valid": true,
  "missing_sources": [],
  "payloads_with_quality_flags": [],
  "payload_count": 7,
  "required_source_count": 7
}
```
### Payload map

| Source | Source type | Normalized fields | Raw fields | Data quality flags |
|---|---|---|---|---|
| `asset_registry` | `master_data` | `asset_type, asset_criticality, criticality_score` | `asset_id, asset_type, line_id, asset_criticality, criticality_score, manufacturer, model, location` | `[]` |
| `sensor_historian` | `raw_sensor_context` | `vibration_trend, temperature_trend, sensor_severity` | `sampling_window_hours, vibration_mms, temperature_celsius, pressure_bar, alarm_count, last_sensor_timestamp` | `[]` |
| `predictive_maintenance` | `model_inference` | `alert_type, estimated_time_to_failure_hours, confidence_score, alert_severity` | `alert_id, asset_id, asset_type, line_id, suspected_failure_mode, alert_type, predictive_horizon_hours, confidence_score, model_name, model_version, triggered_at` | `[]` |
| `maintenance_history` | `work_order_history` | `recent_repeated_failures` | `asset_id, lookback_days, recent_repeated_failures, work_orders` | `[]` |
| `production_planning` | `operational_context` | `production_load_pct, next_planned_downtime_hours, production_pressure` | `asset_id, line_id, horizon_hours, production_pressure, production_load_pct, next_planned_downtime_hours, customer_impact, shift_demand` | `[]` |
| `inventory_and_resources` | `resource_availability` | `spare_part_available, specialist_technician_available_next_shift, intervention_feasible` | `asset_id, spare_part_available, spare_part_id, specialist_technician_available_next_shift, intervention_feasible` | `[]` |
| `policy_governance` | `governance_policy` | `mandatory_human_review_for_high_criticality, expected_human_review_required` | `asset_type, criticality_score, mandatory_human_review_for_high_criticality, expected_human_review_required, management_escalation_required, policy_id` | `[]` |

## Canonical Context: field-level evidence

| Canonical field | Value |
|---|---|
| `context_id` | `canonical_context_SCENARIO_COMP_002_ALERT-COMP-002-20260603` |
| `case_id` | `SCENARIO_COMP_002_ALERT-COMP-002-20260603` |
| `asset.asset_id` | `COMP-002` |
| `asset.asset_type` | `industrial_air_compressor` |
| `asset.line_id` | `PKG-LINE-02` |
| `asset.criticality_label` | `high` |
| `asset.criticality_score` | `5` |
| `asset.process_role` | `None` |
| `predictive_evidence.alert_type` | `predictive_degradation_alert` |
| `predictive_evidence.estimated_time_to_failure_hours` | `48.0` |
| `predictive_evidence.confidence_score` | `0.86` |
| `predictive_evidence.alert_severity` | `high` |
| `predictive_evidence.vibration_trend` | `increasing` |
| `predictive_evidence.temperature_trend` | `increasing` |
| `operational_context.production_load_pct` | `98.0` |
| `operational_context.next_planned_downtime_hours` | `36.0` |
| `operational_context.production_pressure` | `very_high` |
| `operational_context.business_impact_if_unavailable` | `None` |
| `maintenance_resources.recent_repeated_failures` | `True` |
| `maintenance_resources.spare_part_available` | `False` |
| `maintenance_resources.specialist_technician_available_next_shift` | `False` |
| `maintenance_resources.intervention_feasible` | `False` |
| `governance_policy.mandatory_human_review_for_high_criticality` | `True` |
| `governance_policy.expected_human_review_required` | `True` |
| `governance_policy.computed_human_review_required` | `True` |
| `source_payload_count` | `7` |
| `source_names` | `[list:7]` |
| `data_quality_flags` | `[list:0]` |
| `key_risk_drivers` | `[list:5]` |
| `context_version` | `0.1.0` |

### Layer 1 to Canonical Context transformation candidates

| Layer 1 source | Normalized field | Normalized value | Canonical target candidate | Transformation type |
|---|---|---|---|---|
| `asset_registry` | `asset_type` | `industrial_air_compressor` | `asset.asset_type` | `renamed/grouped` |
| `asset_registry` | `asset_criticality` | `high` | `not directly present` | `discarded or indirectly used` |
| `asset_registry` | `criticality_score` | `5` | `asset.criticality_score` | `renamed/grouped` |
| `sensor_historian` | `vibration_trend` | `increasing` | `predictive_evidence.vibration_trend` | `renamed/grouped` |
| `sensor_historian` | `temperature_trend` | `increasing` | `predictive_evidence.temperature_trend` | `renamed/grouped` |
| `sensor_historian` | `sensor_severity` | `high` | `not directly present` | `discarded or indirectly used` |
| `predictive_maintenance` | `alert_type` | `predictive_degradation_alert` | `predictive_evidence.alert_type` | `renamed/grouped` |
| `predictive_maintenance` | `estimated_time_to_failure_hours` | `48.0` | `predictive_evidence.estimated_time_to_failure_hours` | `renamed/grouped` |
| `predictive_maintenance` | `confidence_score` | `0.86` | `predictive_evidence.confidence_score` | `renamed/grouped` |
| `predictive_maintenance` | `alert_severity` | `high` | `predictive_evidence.alert_severity` | `renamed/grouped` |
| `maintenance_history` | `recent_repeated_failures` | `True` | `maintenance_resources.recent_repeated_failures` | `renamed/grouped` |
| `production_planning` | `production_load_pct` | `98.0` | `operational_context.production_load_pct` | `renamed/grouped` |
| `production_planning` | `next_planned_downtime_hours` | `None` | `operational_context.next_planned_downtime_hours` | `renamed/grouped` |
| `production_planning` | `production_pressure` | `very_high` | `operational_context.production_pressure` | `renamed/grouped` |
| `inventory_and_resources` | `spare_part_available` | `False` | `maintenance_resources.spare_part_available` | `renamed/grouped` |
| `inventory_and_resources` | `specialist_technician_available_next_shift` | `False` | `maintenance_resources.specialist_technician_available_next_shift` | `renamed/grouped` |
| `inventory_and_resources` | `intervention_feasible` | `False` | `maintenance_resources.intervention_feasible` | `renamed/grouped` |
| `policy_governance` | `mandatory_human_review_for_high_criticality` | `True` | `governance_policy.mandatory_human_review_for_high_criticality` | `renamed/grouped` |
| `policy_governance` | `expected_human_review_required` | `True` | `governance_policy.expected_human_review_required` | `renamed/grouped` |

## Layer 2: contextualization logic

| Rule ID | Rule name | Condition | Triggered | Output field | Output value | Rationale |
|---|---|---|---|---|---|---|
| `L2_R001` | Technical urgency from failure horizon | `IF estimated_time_to_failure_hours <= 72 THEN technical_urgency = high` | `True` | `technical_urgency` | `high` | Short failure horizon increases technical urgency. |
| `L2_R002` | Asset escalation from criticality | `IF criticality_score >= 5 THEN asset_escalation = required` | `True` | `asset_escalation` | `required` | High-criticality assets require explicit escalation. |
| `L2_R003` | Operational constraint from production pressure | `IF production_pressure = high THEN operational_constraint = high` | `False` | `operational_constraint` | `medium` | High production pressure constrains maintenance timing. |
| `L2_R004` | Downtime window proximity | `IF next_planned_downtime_hours <= 48 THEN downtime_window = near` | `True` | `downtime_window` | `near` | A near downtime window creates a feasible planning opportunity. |
| `L2_R005` | Intervention feasibility from resources | `IF spare_part_available = true AND specialist_technician_available_next_shift = true THEN intervention_feasible = true` | `False` | `intervention_feasible` | `False` | Available spare parts and specialist capacity make intervention feasible. |
| `L2_R006` | Recurrence risk from repeated failures | `IF recent_repeated_failures = true THEN recurrence_risk = high` | `True` | `recurrence_risk` | `high` | Recent repeated failures increase recurrence risk. |
| `L2_R007` | Human review requirement from governance policy | `IF high criticality policy applies THEN human_review_required = true` | `True` | `human_review_required` | `True` | Governance policy requires accountable human review. |
| `L2_R008` | Layer 2 decision readiness | `IF technical urgency, feasibility and governance context exist THEN layer2_decision_ready = true` | `True` | `layer2_decision_ready` | `True` | Layer 2 has enough contextualized evidence for downstream case lifecycle and decision logic. |

### Derived context

| Variable | Value |
|---|---|
| `technical_urgency` | `high` |
| `asset_escalation` | `required` |
| `operational_constraint` | `medium` |
| `downtime_window` | `near` |
| `intervention_feasible` | `False` |
| `recurrence_risk` | `high` |
| `human_review_required` | `True` |
| `layer2_decision_ready` | `True` |

## Layer 3: case lifecycle evidence

- `case_status`: `open`
- `lifecycle_stage`: `evidence_review`
- `human_review_required`: `True`
- `maintenance_planning_required`: `False`
- `decision_ready`: `False`
- `event_count`: `7`
- `task_count`: `2`
- `milestone_count`: `5`
- `blockers`: `['spare_part_not_available', 'specialist_technician_not_available']`

### Tasks

| Task ID | Type | Name | Status | Required role | Trigger |
|---|---|---|---|---|---|
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_task_human_review` | `human_review` | Review compressor risk and approve decision path | `open` | `maintenance_decision_owner` | high criticality or high-severity predictive alert |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_task_blocker_resolution` | `blocker_resolution` | Resolve missing evidence or resource blockers | `open` | `case_owner` | case has blockers before decision readiness |

### Milestones

| Milestone ID | Name | Status | Criteria |
|---|---|---|---|
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_ms_external_evidence_complete` | External evidence complete | `reached` | asset registry payload present; predictive maintenance payload present; production planning payload present; policy payload present |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_ms_canonical_context_available` | Canonical context available | `reached` | canonical asset context built; predictive evidence normalized; operational context normalized; governance policy normalized |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_ms_human_review_identified` | Human review identified | `reached` | high criticality or high severity; policy requires accountable human review |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_ms_maintenance_planning_required` | Maintenance planning required | `not_required` | short failure horizon; resources support controlled planning |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_ms_decision_ready` | Decision-ready case package | `blocked` | external evidence received; canonical context built; human review requirement evaluated; maintenance planning requirement evaluated; no unresolved blockers |

## Layer 4: DMN-like decision and recommendation formulation

- `evaluation_id`: `dmn_like_eval_SCENARIO_COMP_002_ALERT-COMP-002-20260603`
- `source_case_state`: `evidence_review`
- `final_priority`: `high`
- `recommended_execution_mode`: `constrained_execution`
- `human_review_required`: `True`
- `intervention_feasible`: `False`
- `triggered_rule_count`: `5`

### DMN rules

| Rule ID | Rule name | Triggered | Inputs | Outputs | Rationale |
|---|---|---|---|---|---|
| `DMN_R001` | Failure horizon urgency | `True` | `{"estimated_time_to_failure_hours": 48.0, "alert_severity": "high"}` | `{"urgency": "high"}` | Estimated failure horizon is within 72 hours. |
| `DMN_R002` | Asset criticality classification | `True` | `{"asset_criticality_label": "high", "asset_criticality_score": 5}` | `{"criticality_band": "high"}` | Asset criticality score is high. |
| `DMN_R003` | Intervention feasibility | `False` | `{"spare_part_available": false, "specialist_technician_available_next_shift": false}` | `{"intervention_feasible": false}` | At least one required intervention resource is unavailable. |
| `DMN_R004` | Accountable human review requirement | `True` | `{"computed_human_review_required": true, "case_state_human_review_required": true}` | `{"human_review_required": true}` | High criticality or high-severity evidence requires accountable review. |
| `DMN_R005` | Execution constraint assessment | `True` | `{"production_pressure": "very_high", "next_planned_downtime_hours": 36.0, "intervention_feasible": false, "data_quality_flags": []}` | `{"recommended_execution_mode": "constrained_execution"}` | Execution is constrained because intervention resources are incomplete. |
| `DMN_R006` | Final priority consolidation | `True` | `{"urgency": "high", "criticality_band": "high", "intervention_feasible": false, "human_review_required": true, "recommended_execution_mode": "constrained_execution"}` | `{"final_priority": "high", "escalation_required": true}` | Final priority consolidated from urgency=high, criticality=high, intervention_feasible=False, human_review_required=True, execution_mode=constrained_execution. |

### Recommendation path outputs

```json
{
  "bundle_id": "recommendation_paths_SCENARIO_COMP_002_ALERT-COMP-002-20260603",
  "case_id": "SCENARIO_COMP_002_ALERT-COMP-002-20260603",
  "asset_id": "COMP-002",
  "decision_rule_evaluation_id": "dmn_like_eval_SCENARIO_COMP_002_ALERT-COMP-002-20260603",
  "path_outputs": [
    {
      "path_name": "governed_recommendation_formulation",
      "path_type": "governed_recommendation_path",
      "status": "completed",
      "recommendation": {
        "recommendation_id": "governed_rec_SCENARIO_COMP_002_ALERT-COMP-002-20260603",
        "asset_id": "COMP-002",
        "action": "Escalate the constrained maintenance case, resolve execution blockers, increase monitoring, and prepare intervention once feasibility is restored.",
        "primary_action": "Escalate the constrained maintenance case, resolve execution blockers, increase monitoring, and prepare intervention once feasibility is restored.",
        "anchor_action": "Plan immediate inspection and maintenance preparation.",
        "priority": "high",
        "deterministic_anchor_priority": "high",
        "dmn_like_final_priority": "high",
        "recommended_execution_mode": "constrained_execution",
        "human_review_required": true,
        "intervention_feasible": false,
        "decision_ready": false,
        "transformation_applied": true,
        "transformation_reasons": [
          "intervention_not_feasible",
          "case_not_decision_ready",
          "constrained_execution_mode"
        ],
        "preconditions": [
          "Restore intervention feasibility before executing physical maintenance.",
          "Resolve open case blockers before approving execution.",
          "Resolve listed blockers: spare_part_not_available, specialist_technician_not_available."
        ],
        "blockers": [
          "spare_part_not_available",
          "specialist_technician_not_available"
        ],
        "required_reviews": [
          "Obtain accountable human review before execution."
        ],
        "escalations": [
          "Escalate the constrained execution case to the accountable maintenance and operations owners."
        ],
        "contingency_actions": [
          "Increase monitoring and prepare a contingency plan until resources and approval are available."
        ],
        "rationale": "Deterministic anchor proposed: Plan immediate inspection and maintenance preparation. DMN-like final priority: high Execution mode: constrained_execution Intervention feasible: False Decision ready: False Human review required: True The anchor was transformed because: intervention_not_feasible, case_not_decision_ready, constrained_execution_mode."
      },
      "input_refs": [
        "canonical_context_SCENARIO_COMP_002_ALERT-COMP-002-20260603",
        "SCENARIO_COMP_002_ALERT-COMP-002-20260603",
        "dmn_like_eval_SCENARIO_COMP_002_ALERT-COMP-002-20260603"
      ],
      "governance_refs": [
        "compressor_human_review_policy",
        "compressor_final_priority",
        "compressor_execution_mode",
        "recommendation_consistency_constraints"
      ],
      "notes": [
        "The deterministic anchor is used as an initial recommendation.",
        "Layer 4 formulates a governed recommendation by preserving, constraining, transforming, or escalating the anchor according to feasibility, readiness, execution mode, and governance signals."
      ]
    },
    {
      "path_name": "dmn_like_governance_summary",
      "path_type": "rule_governance_summary",
      "status": "completed",
      "recommendation": {
        "case_id": "SCENARIO_COMP_002_ALERT-COMP-002-20260603",
        "asset_id": "COMP-002",
        "final_priority": "high",
        "recommended_execution_mode": "constrained_execution",
        "human_review_required": true,
        "intervention_feasible": false,
        "decision_ready": false,
        "triggered_rule_count": 5
      },
      "input_refs": [
        "canonical_context_SCENARIO_COMP_002_ALERT-COMP-002-20260603",
        "SCENARIO_COMP_002_ALERT-COMP-002-20260603",
        "dmn_like_eval_SCENARIO_COMP_002_ALERT-COMP-002-20260603"
      ],
      "governance_refs": [
        "DMN_R001",
        "DMN_R002",
        "DMN_R004",
        "DMN_R005",
        "DMN_R006"
      ],
      "notes": [
        "This output summarizes explicit rule evaluation before final governed packaging."
      ]
    }
  ],
  "bundle_version": "0.1.0",
  "path_count": 2
}
```

## Layer 5: governed recommendation package

### Final recommendation

- `case_id`: `SCENARIO_COMP_002_ALERT-COMP-002-20260603`
- `asset_id`: `COMP-002`
- `recommended_action`: `Escalate the constrained maintenance case, resolve execution blockers, increase monitoring, and prepare intervention once feasibility is restored.`
- `primary_action`: `Escalate the constrained maintenance case, resolve execution blockers, increase monitoring, and prepare intervention once feasibility is restored.`
- `anchor_action`: `Plan immediate inspection and maintenance preparation.`
- `priority`: `high`
- `deterministic_anchor_priority`: `high`
- `dmn_like_final_priority`: `high`
- `recommended_execution_mode`: `constrained_execution`
- `human_review_required`: `True`
- `intervention_feasible`: `False`
- `decision_ready`: `False`
- `transformation_applied`: `True`
- `transformation_reasons`: `['intervention_not_feasible', 'case_not_decision_ready', 'constrained_execution_mode']`
- `preconditions`: `['Restore intervention feasibility before executing physical maintenance.', 'Resolve open case blockers before approving execution.', 'Resolve listed blockers: spare_part_not_available, specialist_technician_not_available.']`
- `blockers`: `['spare_part_not_available', 'specialist_technician_not_available']`
- `required_reviews`: `['Obtain accountable human review before execution.']`
- `escalations`: `['Escalate the constrained execution case to the accountable maintenance and operations owners.']`
- `contingency_actions`: `['Increase monitoring and prepare a contingency plan until resources and approval are available.']`
- `key_risk_drivers`: `['high_asset_criticality', 'short_failure_horizon', 'high_model_confidence', 'recent_repeated_failures', 'human_review_required']`
- `rationale`: `Deterministic anchor proposed: Plan immediate inspection and maintenance preparation. DMN-like final priority: high Execution mode: constrained_execution Intervention feasible: False Decision ready: False Human review required: True The anchor was transformed because: intervention_not_feasible, case_not_decision_ready, constrained_execution_mode.`

### Governance summary

- `source_payload_count`: `7`
- `source_names`: `['asset_registry', 'sensor_historian', 'predictive_maintenance', 'maintenance_history', 'production_planning', 'inventory_and_resources', 'policy_governance']`
- `canonical_context_id`: `canonical_context_SCENARIO_COMP_002_ALERT-COMP-002-20260603`
- `case_lifecycle_stage`: `evidence_review`
- `case_event_count`: `7`
- `case_task_count`: `2`
- `case_milestone_count`: `5`
- `triggered_rule_count`: `5`
- `decision_rule_evaluation_id`: `dmn_like_eval_SCENARIO_COMP_002_ALERT-COMP-002-20260603`
- `recommendation_path_count`: `2`
- `human_review_required`: `True`
- `decision_ready`: `False`

### Traceability index

| Trace ID | Layer | Artifact | Type | Summary |
|---|---|---|---|---|
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_trace_001_layer_1` | `Layer 1` | `external_source_payloads` | `external_source_package` | Industrial information is exposed as external source payloads. |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_trace_002_layer_2` | `Layer 2` | `canonical_case_context` | `canonical_context` | External payloads are normalized into a canonical compressor case context. |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_trace_003_layer_3` | `Layer 3` | `case_management_state` | `case_lifecycle` | The compressor case is managed through events, tasks and milestones. |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_trace_004_layer_4_rules` | `Layer 4` | `dmn_like_decision_evaluation` | `decision_rules` | Explicit DMN-like rules evaluate urgency, criticality, feasibility, review and priority. |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_trace_005_layer_4_paths` | `Layer 4` | `recommendation_path_outputs` | `recommendation_paths` | Layer 4 formulates a governed recommendation under feasibility, readiness, execution-mode and governance constraints. |
| `SCENARIO_COMP_002_ALERT-COMP-002-20260603_trace_006_layer_5` | `Layer 5` | `governed_recommendation_package` | `governed_package` | Layer 5 packages the governed recommendation with traceability and reviewer-facing controls. |

## Execution summary artifact

# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `COMP-002`
- Title: Paper compressor constrained case
- Asset: `COMP-002`
- Asset type: `industrial_air_compressor`
- Failure mode: `bearing_degradation`
- Decision pattern: `critical_but_constrained_escalation`

## Layer 1 - Evidence package

- Case ID: `SCENARIO_COMP_002_ALERT-COMP-002-20260603`
- Source payload count: `7`
- Data quality flags: `[]`

## Layer 2 - Contextualization

- Layer 2 ready: `True`
- Derived context: `{'technical_urgency': 'high', 'asset_escalation': 'required', 'operational_constraint': 'medium', 'downtime_window': 'near', 'intervention_feasible': False, 'recurrence_risk': 'high', 'human_review_required': True, 'layer2_decision_ready': True}`

## Layer 3 - Case lifecycle

- Case status: `open`
- Lifecycle stage: `evidence_review`
- Event count: `7`
- Task count: `2`
- Milestone count: `5`
- Blockers: `['spare_part_not_available', 'specialist_technician_not_available']`

## Layer 4 - Decision logic

- Final priority: `high`
- Recommended execution mode: `constrained_execution`
- Intervention feasible: `False`
- Human review required: `True`
- Triggered rule count: `5`

## Layer 5 - Governed package

- Package ID: `governed_package_SCENARIO_COMP_002_ALERT-COMP-002-20260603`
- Traceability count: `6`
- Recommendation count: `0`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.

# Source-code traceability

Candidate code locations where Chapter 5 evidence is created, transformed, persisted, or referenced.

## `scenario_all_layers`

### `collect_oversee_meeting_evidence.py` line 53

```text
49:     "05_scenario_execution_summary.md",
50: ]
51: 
52: CODE_SEARCH_TERMS = [
53:     "scenario_all_layers",
54:     "00_scenario.json",
55:     "predictive_alert_request",
56:     "received_predictive_alert",
57:     "enterprise_api_calls",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 12

```text
8: from demo.interactive_walkthrough.adapters.placeholder_adapter import (
9:     record_expected_layer_output,
10: )
11: from demo.interactive_walkthrough.demo_state import DemoRunState
12: from scripts.run_scenario_all_layers_demo import run_scenario_all_layers
13: 
14: 
15: LAYER_ARTIFACTS = {
16:     "layer1": [
```

### `demo\interactive_walkthrough\DEMO_MANUAL.md` line 358

```text
354: 
355: ```powershell
356: cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
357: $env:PYTHONPATH = "."
358: python scripts\run_scenario_all_layers_demo.py --scenario COMP-001
359: ```
360: 
361: ### What this does
362: 
```

### `demo\interactive_walkthrough\presenters\layer_presenter.py` line 6

```text
2: 
3: from __future__ import annotations
4: 
5: from demo.interactive_walkthrough.adapters.placeholder_adapter import record_expected_layer_output
6: from demo.interactive_walkthrough.adapters.scenario_all_layers_adapter import (
7:     run_real_scenario_layer,
8: )
9: from demo.interactive_walkthrough.demo_state import DemoRunState
10: from demo.interactive_walkthrough.display import print_bullets, print_key_values, print_section
```

### `docs\code_review_demo_script.md` line 31

```text
27: 
28: Open this file first:
29: 
30: ```text
31: scripts/run_scenario_all_layers_demo.py
32: ```
33: 
34: This is the main executable runner for the Layer 1 to Layer 5 demo.
35: 
```

### `docs\master_cases_demo_guide.md` line 445

```text
441: List the scenario library:
442: 
443: ```powershell
444: $env:PYTHONPATH = "."
445: python scripts\run_scenario_all_layers_demo.py --list-scenarios
446: ```
447: 
448: Run the full test suite:
449: 
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 221

```text
217: The direct runner is:
218: 
219: ```powershell
220: $env:PYTHONPATH = "."
221: python scripts\run_scenario_all_layers_demo.py --scenario COMP-001
222: ```
223: 
224: The runner performs this sequence:
225: 
```

### `docs\project_structure_spanish_report.md` line 293

```text
289: |   |-- run_live_generative_oversee_smoke.py
290: |   |-- run_live_generative_path_offline_smoke.py
291: |   |-- run_oversee_reviewer_demo.py
292: |   |-- run_paper_aligned_all_layers_demo.py
293: |   `-- run_scenario_all_layers_demo.py
294: |-- src/
295: |   `-- oversee/
296: |       |-- case_context/
297: |       |-- case_management/
```

## `00_scenario.json`

### `collect_oversee_deep_dive_evidence.py` line 10

```text
6: OUTPUT_DIR = ROOT / "outputs" / "reports"
7: OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
8: 
9: TARGET_FILES = [
10:     "00_scenario.json",
11:     "00_predictive_alert_request.json",
12:     "01_received_predictive_alert.json",
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
```

### `collect_oversee_evidence.py` line 13

```text
9: OUTPUT_DIR = ROOT / "outputs" / "reports"
10: OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
11: 
12: TARGET_FILES = [
13:     "00_scenario.json",
14:     "00_predictive_alert_request.json",
15:     "01_received_predictive_alert.json",
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
```

### `collect_oversee_meeting_evidence.py` line 33

```text
29: 
30: TARGET_SCENARIOS = {"COMP-001", "COMP-002"}
31: 
32: TARGET_ARTIFACTS = [
33:     "00_scenario.json",
34:     "00_predictive_alert_request.json",
35:     "01_received_predictive_alert.json",
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
```

### `docs\code_review_demo_script.md` line 377

```text
373: 
374: ### Preparation and trace artifacts
375: 
376: ```text
377: 00_scenario.json
378: 00_predictive_alert_request.json
379: 01_received_predictive_alert.json
380: 01_enterprise_api_calls.json
381: 01_validation_report.json
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 251

```text
247: ## 6. Layer 0 - Scenario and request preparation
248: 
249: This is not an OVERSEE layer, but it is important for understanding the demo.
250: 
251: ### 6.1 `00_scenario.json`
252: 
253: Stores the complete scenario definition used for the run.
254: 
255: It includes:
```

### `docs\project_structure_spanish_report.md` line 856

```text
852: Cuando se ejecuta un escenario, se generan carpetas temporales bajo `outputs/`.
853: 
854: Estas carpetas contienen artefactos como:
855: 
856: - `00_scenario.json`
857: - `00_predictive_alert_request.json`
858: - `01_output_layer1_aggregated_evidence_package.json`
859: - `01_validation_report.json`
860: - `02_canonical_case_context.json`
```

### `docs\release_v0_6_1_summary.md` line 230

```text
226: A real scenario execution produces traceable artifacts such as:
227: 
228: | File | Meaning |
229: |---|---|
230: | `00_scenario.json` | Scenario definition used for the run. |
231: | `00_predictive_alert_request.json` | Predictive alert request generated from executable inputs. |
232: | `01_received_predictive_alert.json` | Layer 1 received alert. |
233: | `01_enterprise_api_calls.json` | Scenario-backed enterprise API calls. |
234: | `01_output_layer1_aggregated_evidence_package.json` | Aggregated evidence package. |
```

### `docs\technical_code_review_map.md` line 213

```text
209: 
210: The current artifact set is:
211: 
212: ```text
213: 00_scenario.json
214: 00_predictive_alert_request.json
215: 01_received_predictive_alert.json
216: 01_enterprise_api_calls.json
217: 01_output_layer1_aggregated_evidence_package.json
```

## `predictive_alert_request`

### `collect_oversee_deep_dive_evidence.py` line 11

```text
7: OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
8: 
9: TARGET_FILES = [
10:     "00_scenario.json",
11:     "00_predictive_alert_request.json",
12:     "01_received_predictive_alert.json",
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
```

### `collect_oversee_evidence.py` line 14

```text
10: OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
11: 
12: TARGET_FILES = [
13:     "00_scenario.json",
14:     "00_predictive_alert_request.json",
15:     "01_received_predictive_alert.json",
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
```

### `collect_oversee_meeting_evidence.py` line 34

```text
30: TARGET_SCENARIOS = {"COMP-001", "COMP-002"}
31: 
32: TARGET_ARTIFACTS = [
33:     "00_scenario.json",
34:     "00_predictive_alert_request.json",
35:     "01_received_predictive_alert.json",
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 17

```text
13: 
14: 
15: LAYER_ARTIFACTS = {
16:     "layer1": [
17:         "00_predictive_alert_request.json",
18:         "01_received_predictive_alert.json",
19:         "01_enterprise_api_calls.json",
20:         "01_output_layer1_aggregated_evidence_package.json",
21:         "01_validation_report.json",
```

### `docs\code_review_demo_script.md` line 378

```text
374: ### Preparation and trace artifacts
375: 
376: ```text
377: 00_scenario.json
378: 00_predictive_alert_request.json
379: 01_received_predictive_alert.json
380: 01_enterprise_api_calls.json
381: 01_validation_report.json
382: 02_canonical_case_context.json
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 277

```text
273: ```text
274: It is the source of truth for the scenario execution.
275: ```
276: 
277: ### 6.2 `00_predictive_alert_request.json`
278: 
279: Stores the executable alert request created from the scenario.
280: 
281: It includes:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 65

```text
61: 
62: ### 1. Trigger and Layer 1 inputs
63: 
64: ```text
65: 00_predictive_alert_request.json
66: 01_received_predictive_alert.json
67: 01_enterprise_api_calls.json
68: 01_output_layer1_aggregated_evidence_package.json
69: 01_validation_report.json
```

### `docs\project_structure_spanish_report.md` line 181

```text
177: |   |   |-- 05_final_governed_recommendation_package.json
178: |   |   |-- 05_reviewer_summary.md
179: |   |   `-- 05_traceability_index.json
180: |   |-- paper_aligned_all_layers_demo_20260603_225140/
181: |   |   |-- 00_predictive_alert_request.json
182: |   |   |-- 01_output_layer1_aggregated_evidence_package.json
183: |   |   |-- 01_enterprise_api_calls.json
184: |   |   |-- 01_received_predictive_alert.json
185: |   |   |-- 01_validation_report.json
```

## `received_predictive_alert`

### `collect_oversee_deep_dive_evidence.py` line 12

```text
8: 
9: TARGET_FILES = [
10:     "00_scenario.json",
11:     "00_predictive_alert_request.json",
12:     "01_received_predictive_alert.json",
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
```

### `collect_oversee_evidence.py` line 15

```text
11: 
12: TARGET_FILES = [
13:     "00_scenario.json",
14:     "00_predictive_alert_request.json",
15:     "01_received_predictive_alert.json",
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
```

### `collect_oversee_meeting_evidence.py` line 35

```text
31: 
32: TARGET_ARTIFACTS = [
33:     "00_scenario.json",
34:     "00_predictive_alert_request.json",
35:     "01_received_predictive_alert.json",
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 18

```text
14: 
15: LAYER_ARTIFACTS = {
16:     "layer1": [
17:         "00_predictive_alert_request.json",
18:         "01_received_predictive_alert.json",
19:         "01_enterprise_api_calls.json",
20:         "01_output_layer1_aggregated_evidence_package.json",
21:         "01_validation_report.json",
22:     ],
```

### `docs\code_review_demo_script.md` line 379

```text
375: 
376: ```text
377: 00_scenario.json
378: 00_predictive_alert_request.json
379: 01_received_predictive_alert.json
380: 01_enterprise_api_calls.json
381: 01_validation_report.json
382: 02_canonical_case_context.json
383: 02_contextualization_rule_trace.json
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 312

```text
308: ```
309: 
310: Layer 1 receives the predictive alert and requests supporting evidence from the scenario-backed enterprise APIs.
311: 
312: ### 7.1 `01_received_predictive_alert.json`
313: 
314: Stores the alert after Layer 1 receives it.
315: 
316: Why it matters:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 66

```text
62: ### 1. Trigger and Layer 1 inputs
63: 
64: ```text
65: 00_predictive_alert_request.json
66: 01_received_predictive_alert.json
67: 01_enterprise_api_calls.json
68: 01_output_layer1_aggregated_evidence_package.json
69: 01_validation_report.json
70: ```
```

### `docs\project_structure_spanish_report.md` line 184

```text
180: |   |-- paper_aligned_all_layers_demo_20260603_225140/
181: |   |   |-- 00_predictive_alert_request.json
182: |   |   |-- 01_output_layer1_aggregated_evidence_package.json
183: |   |   |-- 01_enterprise_api_calls.json
184: |   |   |-- 01_received_predictive_alert.json
185: |   |   |-- 01_validation_report.json
186: |   |   |-- 02_canonical_case_context.json
187: |   |   |-- 02_context_enrichment_summary.md
188: |   |   |-- 02_contextualization_rule_trace.json
```

## `enterprise_api_calls`

### `collect_oversee_deep_dive_evidence.py` line 13

```text
9: TARGET_FILES = [
10:     "00_scenario.json",
11:     "00_predictive_alert_request.json",
12:     "01_received_predictive_alert.json",
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
```

### `collect_oversee_evidence.py` line 16

```text
12: TARGET_FILES = [
13:     "00_scenario.json",
14:     "00_predictive_alert_request.json",
15:     "01_received_predictive_alert.json",
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
```

### `collect_oversee_meeting_evidence.py` line 36

```text
32: TARGET_ARTIFACTS = [
33:     "00_scenario.json",
34:     "00_predictive_alert_request.json",
35:     "01_received_predictive_alert.json",
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 19

```text
15: LAYER_ARTIFACTS = {
16:     "layer1": [
17:         "00_predictive_alert_request.json",
18:         "01_received_predictive_alert.json",
19:         "01_enterprise_api_calls.json",
20:         "01_output_layer1_aggregated_evidence_package.json",
21:         "01_validation_report.json",
22:     ],
23:     "layer2": [
```

### `docs\code_review_demo_script.md` line 380

```text
376: ```text
377: 00_scenario.json
378: 00_predictive_alert_request.json
379: 01_received_predictive_alert.json
380: 01_enterprise_api_calls.json
381: 01_validation_report.json
382: 02_canonical_case_context.json
383: 02_contextualization_rule_trace.json
384: 03_case_lifecycle_trace.json
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 322

```text
318: ```text
319: It preserves the original predictive signal received by the system.
320: ```
321: 
322: ### 7.2 `01_enterprise_api_calls.json`
323: 
324: Stores the simulated enterprise API calls performed by the scenario-backed client.
325: 
326: It shows retrieved information such as:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 67

```text
63: 
64: ```text
65: 00_predictive_alert_request.json
66: 01_received_predictive_alert.json
67: 01_enterprise_api_calls.json
68: 01_output_layer1_aggregated_evidence_package.json
69: 01_validation_report.json
70: ```
71: 
```

### `docs\project_structure_spanish_report.md` line 183

```text
179: |   |   `-- 05_traceability_index.json
180: |   |-- paper_aligned_all_layers_demo_20260603_225140/
181: |   |   |-- 00_predictive_alert_request.json
182: |   |   |-- 01_output_layer1_aggregated_evidence_package.json
183: |   |   |-- 01_enterprise_api_calls.json
184: |   |   |-- 01_received_predictive_alert.json
185: |   |   |-- 01_validation_report.json
186: |   |   |-- 02_canonical_case_context.json
187: |   |   |-- 02_context_enrichment_summary.md
```

## `aggregated_evidence_package`

### `collect_oversee_deep_dive_evidence.py` line 14

```text
10:     "00_scenario.json",
11:     "00_predictive_alert_request.json",
12:     "01_received_predictive_alert.json",
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
```

### `collect_oversee_evidence.py` line 17

```text
13:     "00_scenario.json",
14:     "00_predictive_alert_request.json",
15:     "01_received_predictive_alert.json",
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
```

### `collect_oversee_meeting_evidence.py` line 37

```text
33:     "00_scenario.json",
34:     "00_predictive_alert_request.json",
35:     "01_received_predictive_alert.json",
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 20

```text
16:     "layer1": [
17:         "00_predictive_alert_request.json",
18:         "01_received_predictive_alert.json",
19:         "01_enterprise_api_calls.json",
20:         "01_output_layer1_aggregated_evidence_package.json",
21:         "01_validation_report.json",
22:     ],
23:     "layer2": [
24:         "02_canonical_case_context.json",
```

### `docs\code_review_demo_script.md` line 229

```text
225: 
226: Main inter-layer output:
227: 
228: ```text
229: 01_output_layer1_aggregated_evidence_package.json
230: ```
231: 
232: ### 6.2 Layer 2: contextualization
233: 
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 342

```text
338: ```text
339: It proves that the decision is not based only on the alert.
340: ```
341: 
342: ### 7.3 `01_output_layer1_aggregated_evidence_package.json`
343: 
344: Stores the consolidated evidence package.
345: 
346: It brings together:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 68

```text
64: ```text
65: 00_predictive_alert_request.json
66: 01_received_predictive_alert.json
67: 01_enterprise_api_calls.json
68: 01_output_layer1_aggregated_evidence_package.json
69: 01_validation_report.json
70: ```
71: 
72: What this shows:
```

### `docs\project_structure_spanish_report.md` line 182

```text
178: |   |   |-- 05_reviewer_summary.md
179: |   |   `-- 05_traceability_index.json
180: |   |-- paper_aligned_all_layers_demo_20260603_225140/
181: |   |   |-- 00_predictive_alert_request.json
182: |   |   |-- 01_output_layer1_aggregated_evidence_package.json
183: |   |   |-- 01_enterprise_api_calls.json
184: |   |   |-- 01_received_predictive_alert.json
185: |   |   |-- 01_validation_report.json
186: |   |   |-- 02_canonical_case_context.json
```

## `validation_report`

### `collect_oversee_deep_dive_evidence.py` line 15

```text
11:     "00_predictive_alert_request.json",
12:     "01_received_predictive_alert.json",
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
```

### `collect_oversee_evidence.py` line 18

```text
14:     "00_predictive_alert_request.json",
15:     "01_received_predictive_alert.json",
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
```

### `collect_oversee_meeting_evidence.py` line 38

```text
34:     "00_predictive_alert_request.json",
35:     "01_received_predictive_alert.json",
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 21

```text
17:         "00_predictive_alert_request.json",
18:         "01_received_predictive_alert.json",
19:         "01_enterprise_api_calls.json",
20:         "01_output_layer1_aggregated_evidence_package.json",
21:         "01_validation_report.json",
22:     ],
23:     "layer2": [
24:         "02_canonical_case_context.json",
25:         "02_contextualization_rule_trace.json",
```

### `docs\02_demo_walkthrough.md` line 92

```text
88: ### 6. Show Layer 4 governance
89: 
90: Open:
91: 
92:     50_governance_validation_report.json
93:     55_governance_decision_results.json
94:     60_governed_recommendation_package.json
95: 
96: Explain that governance validates the recommendation before release. In this case, the recommendation is released for human review because high criticality and short failure horizon require accountable human review.
```

### `docs\03_layer_mapping_to_paper.md` line 10

```text
6: |---|---|---|---|---|
7: | Evidence ingestion and normalization | src/oversee/layers/layer_1_ingestion.py | Predictive alert and simulated enterprise service responses | Alert ingestion, external evidence retrieval, schema validation, protected fact preservation | 10_structured_decision_case.json |
8: | Contextualization | src/oversee/layers/layer_2_contextualization.py | Structured decision case | DMN-like contextualization decision table | 20_context_enriched_decision_case.json |
9: | Deliberation and alternative evaluation | src/oversee/layers/layer_3_deliberation.py | Context-enriched decision case | Bounded action catalogue, eligibility table, ranking table | 30_ranked_alternatives.json and 40_preliminary_recommendation.json |
10: | Governance and review | src/oversee/layers/layer_4_governance.py | Context case, preliminary recommendation, traceability registry | Governance validators and DMN-like governance decision table | 50_governance_validation_report.json and 60_governed_recommendation_package.json |
11: | Decision-oriented output and persistence | src/oversee/layers/layer_5_output.py | Governed recommendation package and lifecycle objects | Markdown, JSON, traceability, and lifecycle persistence | 70_recommendation_summary.md, 90_case_lifecycle_trace.json, 91_traceability_index.json |
12: 
13: ## Layer 1 technical mechanism
14: 
```

### `docs\05_traceability_and_outputs.md` line 43

```text
39: ## Layer 4 outputs
40: 
41: | File | Meaning |
42: |---|---|
43: | 50_governance_validation_report.json | Governance validation report |
44: | 55_governance_decision_results.json | Governance decision-table result |
45: | 56_case_state_after_governance.json | Case-state snapshot after Layer 4 |
46: | 60_governed_recommendation_package.json | Governed recommendation package |
47: 
```

### `docs\code_review_demo_script.md` line 381

```text
377: 00_scenario.json
378: 00_predictive_alert_request.json
379: 01_received_predictive_alert.json
380: 01_enterprise_api_calls.json
381: 01_validation_report.json
382: 02_canonical_case_context.json
383: 02_contextualization_rule_trace.json
384: 03_case_lifecycle_trace.json
385: 05_traceability_index.json
```

## `canonical_case_context`

### `collect_oversee_deep_dive_evidence.py` line 16

```text
12:     "01_received_predictive_alert.json",
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
```

### `collect_oversee_evidence.py` line 19

```text
15:     "01_received_predictive_alert.json",
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
```

### `collect_oversee_meeting_evidence.py` line 39

```text
35:     "01_received_predictive_alert.json",
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 24

```text
20:         "01_output_layer1_aggregated_evidence_package.json",
21:         "01_validation_report.json",
22:     ],
23:     "layer2": [
24:         "02_canonical_case_context.json",
25:         "02_contextualization_rule_trace.json",
26:         "02_output_layer2_contextualization_result.json",
27:     ],
28:     "layer3": [
```

### `docs\advanced_workbench_demo_guide.md` line 58

```text
54: 05_final_governed_recommendation_package.json
55: 04_deterministic_vs_generative_comparison.json
56: 04_live_generative_recommendation.json
57: 00_generative_factory_result.json
58: 02_canonical_case_context.json
59: 03_output_layer3_case_management_state.json
60: 04_output_layer4_dmn_decision_evaluation.json
61: ```
62: 
```

### `docs\code_review_demo_script.md` line 382

```text
378: 00_predictive_alert_request.json
379: 01_received_predictive_alert.json
380: 01_enterprise_api_calls.json
381: 01_validation_report.json
382: 02_canonical_case_context.json
383: 02_contextualization_rule_trace.json
384: 03_case_lifecycle_trace.json
385: 05_traceability_index.json
386: 05_execution_manifest.json
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 407

```text
403: ```text
404: Layer 2 turns raw evidence into operational context.
405: ```
406: 
407: ### 8.1 `02_canonical_case_context.json`
408: 
409: Stores the normalized case context used by downstream layers.
410: 
411: It typically contains:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 85

```text
81: ### 2. Layer 2 contextualization
82: 
83: ```text
84: 02_contextualization_rule_trace.json
85: 02_canonical_case_context.json
86: 02_context_enrichment_summary.md
87: 02_output_layer2_contextualization_result.json
88: ```
89: 
```

## `contextualization_rule_trace`

### `collect_oversee_deep_dive_evidence.py` line 17

```text
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
```

### `collect_oversee_evidence.py` line 20

```text
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
```

### `collect_oversee_meeting_evidence.py` line 40

```text
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 25

```text
21:         "01_validation_report.json",
22:     ],
23:     "layer2": [
24:         "02_canonical_case_context.json",
25:         "02_contextualization_rule_trace.json",
26:         "02_output_layer2_contextualization_result.json",
27:     ],
28:     "layer3": [
29:         "03_case_lifecycle_trace.json",
```

### `docs\code_review_demo_script.md` line 383

```text
379: 01_received_predictive_alert.json
380: 01_enterprise_api_calls.json
381: 01_validation_report.json
382: 02_canonical_case_context.json
383: 02_contextualization_rule_trace.json
384: 03_case_lifecycle_trace.json
385: 05_traceability_index.json
386: 05_execution_manifest.json
387: 05_scenario_execution_summary.md
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 429

```text
425: ```text
426: It creates a common language for the rest of OVERSEE.
427: ```
428: 
429: ### 8.2 `02_contextualization_rule_trace.json`
430: 
431: Stores the trace of contextualization rules.
432: 
433: It may include reasoning about:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 84

```text
80: 
81: ### 2. Layer 2 contextualization
82: 
83: ```text
84: 02_contextualization_rule_trace.json
85: 02_canonical_case_context.json
86: 02_context_enrichment_summary.md
87: 02_output_layer2_contextualization_result.json
88: ```
```

### `docs\project_structure_spanish_report.md` line 188

```text
184: |   |   |-- 01_received_predictive_alert.json
185: |   |   |-- 01_validation_report.json
186: |   |   |-- 02_canonical_case_context.json
187: |   |   |-- 02_context_enrichment_summary.md
188: |   |   |-- 02_contextualization_rule_trace.json
189: |   |   |-- 02_output_layer2_contextualization_result.json
190: |   |   |-- 03_case_lifecycle_trace.json
191: |   |   |-- 03_output_layer3_case_management_state.json
192: |   |   |-- 03_layer3_case_lifecycle_summary.md
```

## `case_lifecycle_trace`

### `collect_oversee_deep_dive_evidence.py` line 19

```text
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
```

### `collect_oversee_evidence.py` line 22

```text
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
```

### `collect_oversee_meeting_evidence.py` line 42

```text
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 29

```text
25:         "02_contextualization_rule_trace.json",
26:         "02_output_layer2_contextualization_result.json",
27:     ],
28:     "layer3": [
29:         "03_case_lifecycle_trace.json",
30:         "03_output_layer3_case_management_state.json",
31:     ],
32:     "layer4": [
33:         "04_output_layer4_dmn_decision_evaluation.json",
```

### `docs\02_demo_walkthrough.md` line 103

```text
99: 
100: Open:
101: 
102:     70_recommendation_summary.md
103:     90_case_lifecycle_trace.json
104:     91_traceability_index.json
105:     demo_execution_log.txt
106: 
107: Explain that Layer 5 makes the result reviewable, auditable, and reusable as paper evidence.
```

### `docs\03_layer_mapping_to_paper.md` line 11

```text
7: | Evidence ingestion and normalization | src/oversee/layers/layer_1_ingestion.py | Predictive alert and simulated enterprise service responses | Alert ingestion, external evidence retrieval, schema validation, protected fact preservation | 10_structured_decision_case.json |
8: | Contextualization | src/oversee/layers/layer_2_contextualization.py | Structured decision case | DMN-like contextualization decision table | 20_context_enriched_decision_case.json |
9: | Deliberation and alternative evaluation | src/oversee/layers/layer_3_deliberation.py | Context-enriched decision case | Bounded action catalogue, eligibility table, ranking table | 30_ranked_alternatives.json and 40_preliminary_recommendation.json |
10: | Governance and review | src/oversee/layers/layer_4_governance.py | Context case, preliminary recommendation, traceability registry | Governance validators and DMN-like governance decision table | 50_governance_validation_report.json and 60_governed_recommendation_package.json |
11: | Decision-oriented output and persistence | src/oversee/layers/layer_5_output.py | Governed recommendation package and lifecycle objects | Markdown, JSON, traceability, and lifecycle persistence | 70_recommendation_summary.md, 90_case_lifecycle_trace.json, 91_traceability_index.json |
12: 
13: ## Layer 1 technical mechanism
14: 
15: Layer 1 simulates an alert ingestion interface. The predictive alert is generated by:
```

### `docs\04_case_and_decision_logic.md` line 21

```text
17: - AUDIT_ARCHIVED
18: 
19: The lifecycle trace is persisted as:
20: 
21:     90_case_lifecycle_trace.json
22: 
23: ## Why CMMN-inspired rather than formal CMMN
24: 
25: A formal CMMN implementation would require a CMMN model, case file items, tasks, milestones, entry and exit criteria, a runtime engine, and engine execution logs.
```

### `docs\05_traceability_and_outputs.md` line 53

```text
49: 
50: | File | Meaning |
51: |---|---|
52: | 70_recommendation_summary.md | Human-readable recommendation summary |
53: | 90_case_lifecycle_trace.json | Lifecycle trace across OVERSEE layers |
54: | 91_traceability_index.json | Index of generated artifacts |
55: | 95_case_state_after_output.json | Final case-state snapshot |
56: | demo_execution_log.txt | Plain-text execution log |
57: 
```

## `case_management_state`

### `collect_oversee_deep_dive_evidence.py` line 20

```text
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
```

### `collect_oversee_evidence.py` line 23

```text
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
```

### `collect_oversee_meeting_evidence.py` line 43

```text
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 30

```text
26:         "02_output_layer2_contextualization_result.json",
27:     ],
28:     "layer3": [
29:         "03_case_lifecycle_trace.json",
30:         "03_output_layer3_case_management_state.json",
31:     ],
32:     "layer4": [
33:         "04_output_layer4_dmn_decision_evaluation.json",
34:         "04_output_layer4_recommendation_path_outputs.json",
```

### `docs\advanced_workbench_demo_guide.md` line 59

```text
55: 04_deterministic_vs_generative_comparison.json
56: 04_live_generative_recommendation.json
57: 00_generative_factory_result.json
58: 02_canonical_case_context.json
59: 03_output_layer3_case_management_state.json
60: 04_output_layer4_dmn_decision_evaluation.json
61: ```
62: 
63: ## How to explain the deterministic-vs-generative difference
```

### `docs\code_review_demo_script.md` line 270

```text
266: 
267: Show:
268: 
269: ```text
270: build_case_management_state()
271: ```
272: 
273: What to say:
274: 
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 498

```text
494: ```text
495: It shows how the case evolved before a decision was produced.
496: ```
497: 
498: ### 9.2 `03_output_layer3_case_management_state.json`
499: 
500: Stores the current state of the case.
501: 
502: It typically includes:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 111

```text
107: ### 3. Layer 3 case lifecycle
108: 
109: ```text
110: 03_case_lifecycle_trace.json
111: 03_output_layer3_case_management_state.json
112: 03_layer3_case_lifecycle_summary.md
113: ```
114: 
115: What this shows:
```

## `dmn_decision_evaluation`

### `collect_oversee_deep_dive_evidence.py` line 21

```text
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
25:     "05_execution_manifest.json",
```

### `collect_oversee_evidence.py` line 24

```text
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
28:     "05_execution_manifest.json",
```

### `collect_oversee_meeting_evidence.py` line 44

```text
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
48:     "05_execution_manifest.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 33

```text
29:         "03_case_lifecycle_trace.json",
30:         "03_output_layer3_case_management_state.json",
31:     ],
32:     "layer4": [
33:         "04_output_layer4_dmn_decision_evaluation.json",
34:         "04_output_layer4_recommendation_path_outputs.json",
35:     ],
36:     "layer5": [
37:         "05_final_governed_recommendation_package.json",
```

### `docs\advanced_workbench_demo_guide.md` line 60

```text
56: 04_live_generative_recommendation.json
57: 00_generative_factory_result.json
58: 02_canonical_case_context.json
59: 03_output_layer3_case_management_state.json
60: 04_output_layer4_dmn_decision_evaluation.json
61: ```
62: 
63: ## How to explain the deterministic-vs-generative difference
64: 
```

### `docs\code_review_demo_script.md` line 308

```text
304: 
305: Main inter-layer output:
306: 
307: ```text
308: 04_output_layer4_dmn_decision_evaluation.json
309: ```
310: 
311: Then open:
312: 
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 547

```text
543: ```text
544: Layer 4 converts context into a governed recommendation.
545: ```
546: 
547: ### 10.1 `04_output_layer4_dmn_decision_evaluation.json`
548: 
549: Stores the DMN-like rule evaluation.
550: 
551: It includes outputs such as:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 128

```text
124: 
125: ### 4. Layer 4 decision and generative comparison
126: 
127: ```text
128: 04_output_layer4_dmn_decision_evaluation.json
129: 04_output_layer4_recommendation_path_outputs.json
130: 04_live_generative_recommendation.json
131: 04_deterministic_vs_generative_comparison.json
132: 04_layer4_decision_summary.md
```

## `recommendation_path_outputs`

### `collect_oversee_deep_dive_evidence.py` line 22

```text
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
25:     "05_execution_manifest.json",
26:     "05_scenario_execution_summary.md",
```

### `collect_oversee_evidence.py` line 25

```text
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
28:     "05_execution_manifest.json",
29:     "05_scenario_execution_summary.md",
```

### `collect_oversee_meeting_evidence.py` line 45

```text
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
48:     "05_execution_manifest.json",
49:     "05_scenario_execution_summary.md",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 34

```text
30:         "03_output_layer3_case_management_state.json",
31:     ],
32:     "layer4": [
33:         "04_output_layer4_dmn_decision_evaluation.json",
34:         "04_output_layer4_recommendation_path_outputs.json",
35:     ],
36:     "layer5": [
37:         "05_final_governed_recommendation_package.json",
38:         "05_traceability_index.json",
```

### `docs\code_review_demo_script.md` line 332

```text
328: 
329: Main inter-layer output:
330: 
331: ```text
332: 04_output_layer4_recommendation_path_outputs.json
333: ```
334: 
335: ### 6.5 Layer 5: governed packaging and traceability
336: 
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 578

```text
574: ```text
575: It makes the recommendation rule-driven and inspectable.
576: ```
577: 
578: ### 10.2 `04_output_layer4_recommendation_path_outputs.json`
579: 
580: Stores the recommendation-path output.
581: 
582: It may include:
```

### `docs\paper_aligned_all_layers_demo_guide.md` line 129

```text
125: ### 4. Layer 4 decision and generative comparison
126: 
127: ```text
128: 04_output_layer4_dmn_decision_evaluation.json
129: 04_output_layer4_recommendation_path_outputs.json
130: 04_live_generative_recommendation.json
131: 04_deterministic_vs_generative_comparison.json
132: 04_layer4_decision_summary.md
133: ```
```

### `docs\project_structure_spanish_report.md` line 138

```text
134: |   |   |-- 02_canonical_case_context.json
135: |   |   |-- 03_case_lifecycle_trace.json
136: |   |   |-- 03_output_layer3_case_management_state.json
137: |   |   |-- 04_output_layer4_dmn_decision_evaluation.json
138: |   |   `-- 04_output_layer4_recommendation_path_outputs.json
139: |   |-- five_layer_layer5_governed_package_20260603_000648/
140: |   |   |-- 01_external_source_payloads.json
141: |   |   |-- 02_canonical_case_context.json
142: |   |   |-- 03_case_lifecycle_trace.json
```

## `final_governed_recommendation_package`

### `collect_oversee_deep_dive_evidence.py` line 23

```text
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
25:     "05_execution_manifest.json",
26:     "05_scenario_execution_summary.md",
27: ]
```

### `collect_oversee_evidence.py` line 26

```text
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
28:     "05_execution_manifest.json",
29:     "05_scenario_execution_summary.md",
30: ]
```

### `collect_oversee_meeting_evidence.py` line 46

```text
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
48:     "05_execution_manifest.json",
49:     "05_scenario_execution_summary.md",
50: ]
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 37

```text
33:         "04_output_layer4_dmn_decision_evaluation.json",
34:         "04_output_layer4_recommendation_path_outputs.json",
35:     ],
36:     "layer5": [
37:         "05_final_governed_recommendation_package.json",
38:         "05_traceability_index.json",
39:         "05_execution_manifest.json",
40:         "05_scenario_execution_summary.md",
41:     ],
```

### `docs\advanced_workbench_demo_guide.md` line 54

```text
50: 
51: Then open:
52: 
53: ```text
54: 05_final_governed_recommendation_package.json
55: 04_deterministic_vs_generative_comparison.json
56: 04_live_generative_recommendation.json
57: 00_generative_factory_result.json
58: 02_canonical_case_context.json
```

### `docs\code_review_demo_script.md` line 360

```text
356: 
357: Final package:
358: 
359: ```text
360: 05_final_governed_recommendation_package.json
361: ```
362: 
363: ---
364: 
```

### `docs\implementation_status.md` line 126

```text
122: 
123: 1. `README.md`
124: 2. `docs/reviewer_demo_walkthrough.md`
125: 3. `outputs/generative_digital_factory_workbench_20260603_173209/05_reviewer_summary.md`
126: 4. `outputs/generative_digital_factory_workbench_20260603_173209/05_final_governed_recommendation_package.json`
127: 5. `outputs/generative_digital_factory_workbench_20260603_173209/04_deterministic_vs_generative_comparison.json`
128: 
129: <!-- BEGIN: V0.5.0_PAPER_ALIGNED_ALL_LAYERS_DEMO -->
130: ## v0.5.0 implementation status - paper-aligned all-layers compressor demo
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 608

```text
604: ```text
605: Layer 5 makes the recommendation auditable and ready for handoff.
606: ```
607: 
608: ### 11.1 `05_final_governed_recommendation_package.json`
609: 
610: This is the main final output of OVERSEE.
611: 
612: It packages:
```

## `traceability_index`

### `collect_oversee_deep_dive_evidence.py` line 24

```text
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
25:     "05_execution_manifest.json",
26:     "05_scenario_execution_summary.md",
27: ]
28: 
```

### `collect_oversee_evidence.py` line 27

```text
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
28:     "05_execution_manifest.json",
29:     "05_scenario_execution_summary.md",
30: ]
31: 
```

### `collect_oversee_meeting_evidence.py` line 47

```text
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
48:     "05_execution_manifest.json",
49:     "05_scenario_execution_summary.md",
50: ]
51: 
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 38

```text
34:         "04_output_layer4_recommendation_path_outputs.json",
35:     ],
36:     "layer5": [
37:         "05_final_governed_recommendation_package.json",
38:         "05_traceability_index.json",
39:         "05_execution_manifest.json",
40:         "05_scenario_execution_summary.md",
41:     ],
42: }
```

### `docs\02_demo_walkthrough.md` line 104

```text
100: Open:
101: 
102:     70_recommendation_summary.md
103:     90_case_lifecycle_trace.json
104:     91_traceability_index.json
105:     demo_execution_log.txt
106: 
107: Explain that Layer 5 makes the result reviewable, auditable, and reusable as paper evidence.
108: 
```

### `docs\03_layer_mapping_to_paper.md` line 11

```text
7: | Evidence ingestion and normalization | src/oversee/layers/layer_1_ingestion.py | Predictive alert and simulated enterprise service responses | Alert ingestion, external evidence retrieval, schema validation, protected fact preservation | 10_structured_decision_case.json |
8: | Contextualization | src/oversee/layers/layer_2_contextualization.py | Structured decision case | DMN-like contextualization decision table | 20_context_enriched_decision_case.json |
9: | Deliberation and alternative evaluation | src/oversee/layers/layer_3_deliberation.py | Context-enriched decision case | Bounded action catalogue, eligibility table, ranking table | 30_ranked_alternatives.json and 40_preliminary_recommendation.json |
10: | Governance and review | src/oversee/layers/layer_4_governance.py | Context case, preliminary recommendation, traceability registry | Governance validators and DMN-like governance decision table | 50_governance_validation_report.json and 60_governed_recommendation_package.json |
11: | Decision-oriented output and persistence | src/oversee/layers/layer_5_output.py | Governed recommendation package and lifecycle objects | Markdown, JSON, traceability, and lifecycle persistence | 70_recommendation_summary.md, 90_case_lifecycle_trace.json, 91_traceability_index.json |
12: 
13: ## Layer 1 technical mechanism
14: 
15: Layer 1 simulates an alert ingestion interface. The predictive alert is generated by:
```

### `docs\05_traceability_and_outputs.md` line 54

```text
50: | File | Meaning |
51: |---|---|
52: | 70_recommendation_summary.md | Human-readable recommendation summary |
53: | 90_case_lifecycle_trace.json | Lifecycle trace across OVERSEE layers |
54: | 91_traceability_index.json | Index of generated artifacts |
55: | 95_case_state_after_output.json | Final case-state snapshot |
56: | demo_execution_log.txt | Plain-text execution log |
57: 
58: ## Traceability index
```

### `docs\code_review_demo_script.md` line 385

```text
381: 01_validation_report.json
382: 02_canonical_case_context.json
383: 02_contextualization_rule_trace.json
384: 03_case_lifecycle_trace.json
385: 05_traceability_index.json
386: 05_execution_manifest.json
387: 05_scenario_execution_summary.md
388: ```
389: 
```

## `execution_manifest`

### `collect_oversee_deep_dive_evidence.py` line 25

```text
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
25:     "05_execution_manifest.json",
26:     "05_scenario_execution_summary.md",
27: ]
28: 
29: def read_json(path: Path):
```

### `collect_oversee_evidence.py` line 28

```text
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
28:     "05_execution_manifest.json",
29:     "05_scenario_execution_summary.md",
30: ]
31: 
32: SCENARIO_HINTS = ["comp_001", "comp-001", "COMP-001", "comp_002", "comp-002", "COMP-002"]
```

### `collect_oversee_meeting_evidence.py` line 48

```text
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
48:     "05_execution_manifest.json",
49:     "05_scenario_execution_summary.md",
50: ]
51: 
52: CODE_SEARCH_TERMS = [
```

### `demo\interactive_walkthrough\adapters\real_layer1_adapter.py` line 100

```text
96:         "expected_output_summary": output_summary,
97:         "returncode": completed.returncode,
98:     }
99: 
100:     manifest_path = state.output_dir / "01_layer1_real_execution_manifest.json"
101:     write_json(manifest_path, manifest)
102:     state.record_artifact("layer1_real_execution_manifest", manifest_path)
103: 
104:     for copied_file in copied_files:
```

### `demo\interactive_walkthrough\adapters\real_layer2_adapter.py` line 100

```text
96:         "expected_output_summary": output_summary,
97:         "returncode": completed.returncode,
98:     }
99: 
100:     manifest_path = state.output_dir / "02_layer2_real_execution_manifest.json"
101:     write_json(manifest_path, manifest)
102:     state.record_artifact("layer2_real_execution_manifest", manifest_path)
103: 
104:     for copied_file in copied_files:
```

### `demo\interactive_walkthrough\adapters\real_layer3_adapter.py` line 100

```text
96:         "expected_output_summary": output_summary,
97:         "returncode": completed.returncode,
98:     }
99: 
100:     manifest_path = state.output_dir / "03_layer3_real_execution_manifest.json"
101:     write_json(manifest_path, manifest)
102:     state.record_artifact("layer3_real_execution_manifest", manifest_path)
103: 
104:     for copied_file in copied_files:
```

### `demo\interactive_walkthrough\adapters\real_layer4_adapter.py` line 100

```text
96:         "expected_output_summary": output_summary,
97:         "returncode": completed.returncode,
98:     }
99: 
100:     manifest_path = state.output_dir / "04_layer4_real_execution_manifest.json"
101:     write_json(manifest_path, manifest)
102:     state.record_artifact("layer4_real_execution_manifest", manifest_path)
103: 
104:     for copied_file in copied_files:
```

### `demo\interactive_walkthrough\adapters\real_layer5_adapter.py` line 100

```text
96:         "expected_output_summary": output_summary,
97:         "returncode": completed.returncode,
98:     }
99: 
100:     manifest_path = state.output_dir / "05_layer5_real_execution_manifest.json"
101:     write_json(manifest_path, manifest)
102:     state.record_artifact("layer5_real_execution_manifest", manifest_path)
103: 
104:     for copied_file in copied_files:
```

## `scenario_execution_summary`

### `collect_oversee_deep_dive_evidence.py` line 26

```text
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
25:     "05_execution_manifest.json",
26:     "05_scenario_execution_summary.md",
27: ]
28: 
29: def read_json(path: Path):
30:     return json.loads(path.read_text(encoding="utf-8"))
```

### `collect_oversee_evidence.py` line 29

```text
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
28:     "05_execution_manifest.json",
29:     "05_scenario_execution_summary.md",
30: ]
31: 
32: SCENARIO_HINTS = ["comp_001", "comp-001", "COMP-001", "comp_002", "comp-002", "COMP-002"]
33: 
```

### `collect_oversee_meeting_evidence.py` line 49

```text
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
48:     "05_execution_manifest.json",
49:     "05_scenario_execution_summary.md",
50: ]
51: 
52: CODE_SEARCH_TERMS = [
53:     "scenario_all_layers",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 40

```text
36:     "layer5": [
37:         "05_final_governed_recommendation_package.json",
38:         "05_traceability_index.json",
39:         "05_execution_manifest.json",
40:         "05_scenario_execution_summary.md",
41:     ],
42: }
43: 
44: 
```

### `docs\code_review_demo_script.md` line 58

```text
54: run_scenario_all_layers()
55: print_all_layers_available_scenarios()
56: write_layer_artifact_json()
57: serialize_layer_artifact_default()
58: build_layer5_scenario_execution_summary()
59: ```
60: 
61: ### 3.1 `all_layers_cli_main()`
62: 
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 679

```text
675: ```text
676: It records how the run was executed.
677: ```
678: 
679: ### 11.4 `05_scenario_execution_summary.md`
680: 
681: This is a human-readable summary of the scenario execution.
682: 
683: Why it matters:
```

### `docs\project_structure_spanish_report.md` line 865

```text
861: - `03_output_layer3_case_management_state.json`
862: - `04_output_layer4_dmn_decision_evaluation.json`
863: - `05_final_governed_recommendation_package.json`
864: - `05_traceability_index.json`
865: - `05_scenario_execution_summary.md`
866: 
867: La idea es que OVERSEE no produzca solo una recomendacion final, sino una cadena de evidencia completa que permita explicar que entro, como se interpreto, que reglas se aplicaron y que salida final se genero.
868: 
869: ## 10. Resumen para explicar el proyecto
```

### `docs\release_v0_6_1_summary.md` line 244

```text
240: | `04_output_layer4_recommendation_path_outputs.json` | Recommendation path outputs. |
241: | `05_final_governed_recommendation_package.json` | Final governed recommendation package. |
242: | `05_traceability_index.json` | Traceability index. |
243: | `05_execution_manifest.json` | Execution metadata. |
244: | `05_scenario_execution_summary.md` | Human-readable scenario summary. |
245: 
246: ---
247: 
248: ## 8. Main validation commands
```

## `build_canonical`

### `collect_oversee_meeting_evidence.py` line 70

```text
66:     "final_governed_recommendation_package",
67:     "traceability_index",
68:     "execution_manifest",
69:     "scenario_execution_summary",
70:     "build_canonical",
71:     "canonical context",
72:     "contextualization",
73:     "case lifecycle",
74:     "DMN",
```

### `docs\technical_code_review_map.md` line 95

```text
91: |
92: |-- run_layer1_evidence_pipeline(...)
93: |   `-- src/oversee/integration/layer1_evidence_pipeline.py
94: |
95: |-- build_canonical_case_context(...)
96: |   `-- src/oversee/case_context/
97: |
98: |-- run_layer2_contextualization(...)
99: |   `-- src/oversee/case_context/contextualization_rules.py
```

### `paper_artifacts\migration_backups\step_10_live_generative_oversee_20260603_154102\scripts__run_live_generative_oversee_smoke.py` line 26

```text
22: if str(SRC_PATH) not in sys.path:
23:     sys.path.insert(0, str(SRC_PATH))
24: 
25: 
26: from oversee.case_context import build_canonical_case_context  # noqa: E402
27: from oversee.case_management import build_case_management_state  # noqa: E402
28: from oversee.decision_rules import (  # noqa: E402
29:     evaluate_dmn_like_rules,
30:     run_live_generative_recommendation,
```

### `paper_artifacts\migration_backups\step_10_live_generative_oversee_20260603_154102\tests__oversee__layers__test_live_generative_oversee.py` line 7

```text
3: from __future__ import annotations
4: 
5: import json
6: 
7: from oversee.case_context import build_canonical_case_context
8: from oversee.case_management import build_case_management_state
9: from oversee.decision_rules import (
10:     evaluate_dmn_like_rules,
11:     run_live_generative_recommendation,
```

### `scripts\run_generative_digital_factory_workbench_smoke.py` line 27

```text
23: if str(SRC_PATH) not in sys.path:
24:     sys.path.insert(0, str(SRC_PATH))
25: 
26: 
27: from oversee.case_context import build_canonical_case_context  # noqa: E402
28: from oversee.case_management import build_case_management_state  # noqa: E402
29: from oversee.decision_rules import (  # noqa: E402
30:     evaluate_dmn_like_rules,
31:     run_live_generative_recommendation,
```

### `scripts\run_layer1_layer2_compressor_smoke.py` line 23

```text
19: if str(SRC_PATH) not in sys.path:
20:     sys.path.insert(0, str(SRC_PATH))
21: 
22: 
23: from oversee.case_context import build_canonical_case_context  # noqa: E402
24: from oversee.external_sources import build_compressor_external_source_package  # noqa: E402
25: 
26: 
27: def main() -> None:
```

### `scripts\run_layer2_paper_aligned_demo.py` line 22

```text
18: if str(SRC_PATH) not in sys.path:
19:     sys.path.insert(0, str(SRC_PATH))
20: 
21: 
22: from oversee.case_context import build_canonical_case_context  # noqa: E402
23: from oversee.case_context.contextualization_rules import (  # noqa: E402
24:     run_layer2_contextualization,
25: )
26: from oversee.integration import (  # noqa: E402
```

### `scripts\run_layer3_case_lifecycle_smoke.py` line 25

```text
21: if str(SRC_PATH) not in sys.path:
22:     sys.path.insert(0, str(SRC_PATH))
23: 
24: 
25: from oversee.case_context import build_canonical_case_context  # noqa: E402
26: from oversee.case_management import build_case_management_state  # noqa: E402
27: from oversee.external_sources import build_compressor_external_source_package  # noqa: E402
28: 
29: 
```

## `canonical context`

### `collect_oversee_deep_dive_evidence.py` line 131

```text
127:                 out.write(f"\n### {name}\n\n")
128:                 out.write(markdown_code(data[name], "json" if name.endswith(".json") else "markdown"))
129:                 out.write("\n\n")
130: 
131:             out.write("## C. Canonical Context field map candidate\n\n")
132:             layer1 = data.get("01_output_layer1_aggregated_evidence_package.json", {})
133:             canonical = data.get("02_canonical_case_context.json", {})
134: 
135:             out.write("### Layer 1 normalized fields by source\n\n")
```

### `collect_oversee_meeting_evidence.py` line 71

```text
67:     "traceability_index",
68:     "execution_manifest",
69:     "scenario_execution_summary",
70:     "build_canonical",
71:     "canonical context",
72:     "contextualization",
73:     "case lifecycle",
74:     "DMN",
75:     "governed recommendation",
```

### `docs\technical_code_review_map.md` line 183

```text
179: ```text
180: Layer 1 output -> evidence package
181: Layer 2 input -> evidence package / canonical case context
182: Layer 2 output -> contextualized decision profile
183: Layer 3 input -> canonical context
184: Layer 3 output -> case management state
185: Layer 4 input -> canonical context + case management state
186: Layer 4 output -> decision evaluation + recommendation path outputs
187: Layer 5 input -> evidence package + context + case state + rule evaluation + recommendations
```

### `paper_artifacts\doc_backups\step_10_v05_docs_20260603_230128\README.md` line 150

```text
146: | Area | Module |
147: |---|---|
148: | Generative Digital Factory | `src/oversee/digital_factory/generative_external_source_factory.py` |
149: | External sources | `src/oversee/external_sources/` |
150: | Canonical context | `src/oversee/case_context/` |
151: | Case lifecycle | `src/oversee/case_management/` |
152: | DMN-like rules | `src/oversee/decision_rules/dmn_like_rules.py` |
153: | Live generative recommendation | `src/oversee/decision_rules/live_generative_recommendation.py` |
154: | Deterministic-vs-generative comparison | `src/oversee/reporting/generative_comparison.py` |
```

### `paper_artifacts\doc_backups\step_10_v05_docs_20260603_230159\README.md` line 200

```text
196: | Area | Module |
197: |---|---|
198: | Generative Digital Factory | `src/oversee/digital_factory/generative_external_source_factory.py` |
199: | External sources | `src/oversee/external_sources/` |
200: | Canonical context | `src/oversee/case_context/` |
201: | Case lifecycle | `src/oversee/case_management/` |
202: | DMN-like rules | `src/oversee/decision_rules/dmn_like_rules.py` |
203: | Live generative recommendation | `src/oversee/decision_rules/live_generative_recommendation.py` |
204: | Deterministic-vs-generative comparison | `src/oversee/reporting/generative_comparison.py` |
```

### `paper_artifacts\reuse_audit\step_3_recovery_inspection_pack_20260602_231532.md` line 7805

```text
7801: 
7802: Then assign it to one of:
7803: 
7804: - Layer 1 external source ingestion
7805: - Layer 2 canonical context
7806: - Layer 3 CMMN-inspired case lifecycle
7807: - Layer 4 DMN/rules/recommendation paths
7808: - Layer 5 governed recommendation package
7809: - Later role-agent enrichment
```

### `paper_artifacts\reuse_audit\step_9_generative_ai_readiness_audit_20260603_083316.md` line 31

```text
27: Target flow:
28: 
29: ```text
30: Layer 1 external sources
31: -> Layer 2 canonical context
32: -> Layer 3 case lifecycle
33: -> Layer 4 DMN-like rules
34: -> Layer 4 live generative recommendation path
35: -> Layer 5 governed package with deterministic-vs-generative comparison
```

### `scripts\run_scenario_all_layers_demo.py` line 168

```text
164:         alert_request, # The predictive alert prepared from the case Asset COMP-001, ...
165:         api_client=api_client, # The simulated APIs client.
166:         case_id_prefix=case_id_prefix, # The prefix to construct a traceable case identifier
167:     )
168:     canonical_context = build_canonical_case_context(layer1_result.evidence_package) # - Finally, evidence package is converted into a canonical context for Layer 2.
169:     layer2_result = run_layer2_contextualization(canonical_context)
170:     case_state = build_case_management_state(canonical_context)
171:     rule_evaluation = evaluate_dmn_like_rules(canonical_context, case_state)
172:     recommendation_bundle = run_recommendation_paths(
```

## `contextualization`

### `CHANGELOG.md` line 47

```text
43:   - inventory and resource service
44:   - policy service
45: - Implemented CMMN-inspired case-state tracker and lifecycle trace builder.
46: - Implemented generic DMN-like decision table engine.
47: - Added contextualization, action eligibility, action ranking, and governance validation decision tables.
48: - Added bounded action catalogue.
49: - Implemented Layer 1: evidence ingestion and normalization.
50: - Implemented Layer 2: contextualization.
51: - Implemented Layer 3: deliberation and alternative evaluation.
```

### `collect_oversee_deep_dive_evidence.py` line 17

```text
13:     "01_enterprise_api_calls.json",
14:     "01_output_layer1_aggregated_evidence_package.json",
15:     "01_validation_report.json",
16:     "02_canonical_case_context.json",
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
```

### `collect_oversee_evidence.py` line 20

```text
16:     "01_enterprise_api_calls.json",
17:     "01_output_layer1_aggregated_evidence_package.json",
18:     "01_validation_report.json",
19:     "02_canonical_case_context.json",
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
```

### `collect_oversee_meeting_evidence.py` line 40

```text
36:     "01_enterprise_api_calls.json",
37:     "01_output_layer1_aggregated_evidence_package.json",
38:     "01_validation_report.json",
39:     "02_canonical_case_context.json",
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 25

```text
21:         "01_validation_report.json",
22:     ],
23:     "layer2": [
24:         "02_canonical_case_context.json",
25:         "02_contextualization_rule_trace.json",
26:         "02_output_layer2_contextualization_result.json",
27:     ],
28:     "layer3": [
29:         "03_case_lifecycle_trace.json",
```

### `demo\interactive_walkthrough\DEMO_MANUAL.md` line 426

```text
422: ```
423: 
424: ---
425: 
426: ### Layer 2 - Contextualization
427: 
428: Layer 2 interprets the evidence in its operational context.
429: 
430: It asks:
```

### `demo\interactive_walkthrough\presenters\layer_presenter.py` line 16

```text
12: 
13: 
14: LAYER_TITLES = {
15:     "layer1": "Layer 1 - Evidence intake, aggregation and validation",
16:     "layer2": "Layer 2 - Contextualization",
17:     "layer3": "Layer 3 - Case lifecycle",
18:     "layer4": "Layer 4 - Decision logic",
19:     "layer5": "Layer 5 - Governed packaging and traceability",
20: }
```

### `demo\interactive_walkthrough\walkthrough.py` line 150

```text
146:             "",
147:             "## Interpretation",
148:             "",
149:             "The final recommendation is not produced directly from the predictive alert.",
150:             "It is built through evidence validation, contextualization, case lifecycle management, decision logic, governed packaging, traceability, and human review preparation.",
151:             "",
152:             "## Output directory",
153:             "",
154:             f"`{state.output_dir}`",
```

## `case lifecycle`

### `collect_oversee_deep_dive_evidence.py` line 163

```text
159:                         f"| `{r.get('rule_id')}` | {r.get('rule_name')} | `{r.get('condition')}` | "
160:                         f"`{r.get('triggered')}` | `{r.get('output_field')}` | `{r.get('output_value')}` | {r.get('rationale')} |\n"
161:                     )
162: 
163:             out.write("\n## E. Layer 3 case lifecycle tables\n\n")
164:             case_state = data.get("03_output_layer3_case_management_state.json", {})
165:             out.write("### Case state summary\n\n")
166:             for key in ["case_status", "lifecycle_stage", "human_review_required", "maintenance_planning_required", "decision_ready", "event_count", "task_count", "milestone_count", "blockers"]:
167:                 out.write(f"- `{key}`: `{case_state.get(key)}`\n")
```

### `collect_oversee_meeting_evidence.py` line 73

```text
69:     "scenario_execution_summary",
70:     "build_canonical",
71:     "canonical context",
72:     "contextualization",
73:     "case lifecycle",
74:     "DMN",
75:     "governed recommendation",
76:     "controlled_planning",
77:     "constrained_execution",
```

### `demo\interactive_walkthrough\DEMO_MANUAL.md` line 454

```text
450: ```
451: 
452: ---
453: 
454: ### Layer 3 - Case lifecycle
455: 
456: Layer 3 manages the case state.
457: 
458: It identifies:
```

### `demo\interactive_walkthrough\presenters\intro_presenter.py` line 50

```text
46:         [
47:             "Enterprise sources provide information through the API access layer.",
48:             "Layer 1 validates and aggregates evidence.",
49:             "Layer 2 contextualizes the evidence through DMN-like rules.",
50:             "Layer 3 manages the case lifecycle using CMMN-inspired concepts.",
51:             "Layer 4 formulates the decision record through DMN-like decision logic.",
52:             "Layer 5 packages the result for review, workflow handoff, and audit.",
53:         ]
54:     )
```

### `demo\interactive_walkthrough\presenters\layer_presenter.py` line 17

```text
13: 
14: LAYER_TITLES = {
15:     "layer1": "Layer 1 - Evidence intake, aggregation and validation",
16:     "layer2": "Layer 2 - Contextualization",
17:     "layer3": "Layer 3 - Case lifecycle",
18:     "layer4": "Layer 4 - Decision logic",
19:     "layer5": "Layer 5 - Governed packaging and traceability",
20: }
21: 
```

### `demo\interactive_walkthrough\README.md` line 18

```text
14: Enterprise sources
15: -> API access layer
16: -> Layer 1: validated evidence package
17: -> Layer 2: contextualized decision profile
18: -> Layer 3: case lifecycle state
19: -> Layer 4: decision evaluation and recommendation record
20: -> Layer 5: governed recommendation package
21: ```
22: 
```

### `demo\interactive_walkthrough\walkthrough.py` line 150

```text
146:             "",
147:             "## Interpretation",
148:             "",
149:             "The final recommendation is not produced directly from the predictive alert.",
150:             "It is built through evidence validation, contextualization, case lifecycle management, decision logic, governed packaging, traceability, and human review preparation.",
151:             "",
152:             "## Output directory",
153:             "",
154:             f"`{state.output_dir}`",
```

### `docs\01_artifact_overview.md` line 41

```text
37: - REQUIRES_HUMAN_REVIEW
38: - RELEASED_FOR_REVIEW
39: - AUDIT_ARCHIVED
40: 
41: This makes the case lifecycle visible, inspectable, and easy to map to the paper.
42: 
43: ## DMN-like scope
44: 
45: The implementation uses DMN-like executable decision tables.
```

## `DMN`

### `CHANGELOG.md` line 46

```text
42:   - asset registry service
43:   - inventory and resource service
44:   - policy service
45: - Implemented CMMN-inspired case-state tracker and lifecycle trace builder.
46: - Implemented generic DMN-like decision table engine.
47: - Added contextualization, action eligibility, action ranking, and governance validation decision tables.
48: - Added bounded action catalogue.
49: - Implemented Layer 1: evidence ingestion and normalization.
50: - Implemented Layer 2: contextualization.
```

### `collect_oversee_deep_dive_evidence.py` line 21

```text
17:     "02_contextualization_rule_trace.json",
18:     "02_output_layer2_contextualization_result.json",
19:     "03_case_lifecycle_trace.json",
20:     "03_output_layer3_case_management_state.json",
21:     "04_output_layer4_dmn_decision_evaluation.json",
22:     "04_output_layer4_recommendation_path_outputs.json",
23:     "05_final_governed_recommendation_package.json",
24:     "05_traceability_index.json",
25:     "05_execution_manifest.json",
```

### `collect_oversee_evidence.py` line 24

```text
20:     "02_contextualization_rule_trace.json",
21:     "02_output_layer2_contextualization_result.json",
22:     "03_case_lifecycle_trace.json",
23:     "03_output_layer3_case_management_state.json",
24:     "04_output_layer4_dmn_decision_evaluation.json",
25:     "04_output_layer4_recommendation_path_outputs.json",
26:     "05_final_governed_recommendation_package.json",
27:     "05_traceability_index.json",
28:     "05_execution_manifest.json",
```

### `collect_oversee_meeting_evidence.py` line 44

```text
40:     "02_contextualization_rule_trace.json",
41:     "02_output_layer2_contextualization_result.json",
42:     "03_case_lifecycle_trace.json",
43:     "03_output_layer3_case_management_state.json",
44:     "04_output_layer4_dmn_decision_evaluation.json",
45:     "04_output_layer4_recommendation_path_outputs.json",
46:     "05_final_governed_recommendation_package.json",
47:     "05_traceability_index.json",
48:     "05_execution_manifest.json",
```

### `demo\interactive_walkthrough\adapters\scenario_all_layers_adapter.py` line 33

```text
29:         "03_case_lifecycle_trace.json",
30:         "03_output_layer3_case_management_state.json",
31:     ],
32:     "layer4": [
33:         "04_output_layer4_dmn_decision_evaluation.json",
34:         "04_output_layer4_recommendation_path_outputs.json",
35:     ],
36:     "layer5": [
37:         "05_final_governed_recommendation_package.json",
```

### `demo\interactive_walkthrough\DEMO_MANUAL.md` line 484

```text
480: ---
481: 
482: ### Layer 4 - Decision logic
483: 
484: Layer 4 applies explicit DMN-like rules.
485: 
486: It decides:
487: 
488: ```text
```

### `demo\interactive_walkthrough\presenters\intro_presenter.py` line 49

```text
45:     print_bullets(
46:         [
47:             "Enterprise sources provide information through the API access layer.",
48:             "Layer 1 validates and aggregates evidence.",
49:             "Layer 2 contextualizes the evidence through DMN-like rules.",
50:             "Layer 3 manages the case lifecycle using CMMN-inspired concepts.",
51:             "Layer 4 formulates the decision record through DMN-like decision logic.",
52:             "Layer 5 packages the result for review, workflow handoff, and audit.",
53:         ]
```

### `demo\interactive_walkthrough\presenters\layer_presenter.py` line 33

```text
29:     "layer2": [
30:         "Operational contextualization",
31:         "Feasibility assessment",
32:         "Policy interpretation",
33:         "DMN-like contextualization rules",
34:     ],
35:     "layer3": [
36:         "CMMN-inspired lifecycle management",
37:         "Task activation",
```

## `governed recommendation`

### `collect_oversee_deep_dive_evidence.py` line 201

```text
197:             paths = data.get("04_output_layer4_recommendation_path_outputs.json", {})
198:             out.write(markdown_code(paths))
199:             out.write("\n\n")
200: 
201:             out.write("## H. Layer 5 governed recommendation package\n\n")
202:             package = data.get("05_final_governed_recommendation_package.json", {})
203:             final_rec = package.get("final_recommendation", {}) if isinstance(package, dict) else {}
204:             governance = package.get("governance_summary", {}) if isinstance(package, dict) else {}
205: 
```

### `collect_oversee_meeting_evidence.py` line 75

```text
71:     "canonical context",
72:     "contextualization",
73:     "case lifecycle",
74:     "DMN",
75:     "governed recommendation",
76:     "controlled_planning",
77:     "constrained_execution",
78:     "intervention_not_feasible",
79:     "case_not_decision_ready",
```

### `data\case_model\case_milestones.json` line 39

```text
35:     "description": "The preliminary recommendation has been validated against governance checks."
36:   },
37:   {
38:     "milestone_id": "M08",
39:     "name": "Governed recommendation package released",
40:     "description": "A governed recommendation package has been prepared for human review."
41:   },
42:   {
43:     "milestone_id": "M09",
```

### `demo\interactive_walkthrough\DEMO_MANUAL.md` line 12

```text
8: ## 1. Purpose
9: 
10: This manual explains how to run and explain the interactive OVERSEE walkthrough demo.
11: 
12: The walkthrough helps a non-programmer reviewer understand how OVERSEE transforms industrial maintenance evidence into a governed recommendation package.
13: 
14: The key idea is simple:
15: 
16: ```text
```

### `demo\interactive_walkthrough\presenters\intro_presenter.py` line 18

```text
14:     print_title("OVERSEE interactive walkthrough")
15: 
16:     print(
17:         "\nThis walkthrough uses Figure 3 as the guide. "
18:         "The aim is to see how enterprise information becomes a governed recommendation package."
19:     )
20:     print(
21:         "\nThe demo code is only a presentation layer. "
22:         "It does not modify the OVERSEE core."
```

### `demo\interactive_walkthrough\README.md` line 5

```text
1: # OVERSEE Interactive Walkthrough
2: 
3: This folder contains an isolated demonstration layer for explaining the OVERSEE architecture step by step.
4: 
5: The walkthrough is designed for live explanation. It helps a reviewer understand how enterprise evidence becomes a governed recommendation package through the OVERSEE five-layer architecture.
6: 
7: ---
8: 
9: ## Purpose
```

### `demo\interactive_walkthrough\scenarios\agv_001_battery_degradation.json` line 81

```text
77:     "layer1": "Validated evidence package: battery degradation alert, fleet context, asset redundancy, and maintenance history",
78:     "layer2": "Contextualized decision profile: medium urgency, redundant capacity, feasible planned replacement",
79:     "layer3": "Decision-ready case: open, replacement planning task active, no blockers",
80:     "layer4": "Decision record: medium priority, planned replacement recommended",
81:     "layer5": "Governed recommendation package: fleet summary, traceability index, and replacement proposal"
82:   },
83:   "executable_inputs": {
84:     "alert": {
85:       "alert_id": "ALERT-AGV-001-20260603",
```

### `demo\interactive_walkthrough\scenarios\boiler_001_pressure_instability.json` line 81

```text
77:     "layer1": "Validated evidence package: pressure instability alert, condition trends, regulated asset context, and maintenance history",
78:     "layer2": "Contextualized decision profile: critical urgency, safety/compliance review required, intervention conditional",
79:     "layer3": "Decision-ready case: open, compliance escalation active, permit requirement visible",
80:     "layer4": "Decision record: critical priority, compliance escalation recommended",
81:     "layer5": "Governed recommendation package: compliance summary, traceability index, and safety inspection proposal"
82:   },
83:   "executable_inputs": {
84:     "alert": {
85:       "alert_id": "ALERT-BOILER-001-20260603",
```

## `controlled_planning`

### `collect_oversee_meeting_evidence.py` line 76

```text
72:     "contextualization",
73:     "case lifecycle",
74:     "DMN",
75:     "governed recommendation",
76:     "controlled_planning",
77:     "constrained_execution",
78:     "intervention_not_feasible",
79:     "case_not_decision_ready",
80:     "spare_part_not_available",
```

### `demo\interactive_walkthrough\DEMO_MANUAL.md` line 499

```text
495: Possible execution modes include:
496: 
497: ```text
498: standard_planning
499: controlled_planning
500: constrained_execution
501: diagnostic_review
502: ```
503: 
```

### `demo\interactive_walkthrough\scenarios\comp_001_default.json` line 11

```text
7:   "failure_mode": "bearing_degradation",
8:   "paper_aligned": true,
9:   "master_case": true,
10:   "master_case_role": "main_paper_case",
11:   "decision_pattern": "critical_but_feasible_controlled_planning",
12:   "layer_inputs": {
13:     "layer1": [
14:       {
15:         "source": "PdM analytics service",
```

### `demo\interactive_walkthrough\scenarios\comp_001_paper.json` line 11

```text
7:   "failure_mode": "bearing_degradation",
8:   "paper_aligned": true,
9:   "master_case": true,
10:   "master_case_role": "main_paper_case",
11:   "decision_pattern": "critical_but_feasible_controlled_planning",
12:   "layer_inputs": {
13:     "layer1": [
14:       {
15:         "source": "PdM analytics service",
```

### `docs\code_review_demo_script.md` line 424

```text
420: layer1_evidence_package_valid = true
421: layer2_decision_ready = true
422: case_lifecycle_stage = decision_ready
423: dmn_decision_final_priority = high
424: recommended_execution_mode = controlled_planning
425: intervention_feasible = true
426: human_review_required = true
427: generated_file_count = 17
428: ```
```

### `docs\master_cases_demo_guide.md` line 127

```text
123: ### Expected result
124: 
125: ```text
126: priority: high
127: execution_mode: controlled_planning
128: intervention_feasible: true
129: human_review_required: true
130: ```
131: 
```

### `docs\master_cases_results_comparison.md` line 16

```text
12: ## Comparative table
13: 
14: | Scenario | Role | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle |
15: |---|---|---:|---|---|---:|---:|---|
16: | `COMP-001` | Main controlled-planning case | True | high | controlled_planning | True | True | decision_ready |
17: | `COMP-002` | Early-warning proportional-response case | True | medium | standard_planning | True | True | evidence_review |
18: | `PUMP-001` | Resource-constrained execution case | True | high | constrained_execution | False | True | evidence_review |
19: | `CONV-001` | Production-maintenance conflict case | True | high | controlled_planning | True | True | decision_ready |
20: | `DATA-001` | Evidence-quality stop and diagnostic-review case | False | medium | diagnostic_review | True | True | evidence_review |
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 568

```text
564: For `COMP-001`, the expected result is:
565: 
566: ```text
567: priority = high
568: execution_mode = controlled_planning
569: human_review_required = true
570: ```
571: 
572: Why it matters:
```

## `constrained_execution`

### `collect_oversee_meeting_evidence.py` line 77

```text
73:     "case lifecycle",
74:     "DMN",
75:     "governed recommendation",
76:     "controlled_planning",
77:     "constrained_execution",
78:     "intervention_not_feasible",
79:     "case_not_decision_ready",
80:     "spare_part_not_available",
81:     "specialist_technician_not_available",
```

### `demo\interactive_walkthrough\DEMO_MANUAL.md` line 500

```text
496: 
497: ```text
498: standard_planning
499: controlled_planning
500: constrained_execution
501: diagnostic_review
502: ```
503: 
504: Output:
```

### `docs\master_cases_demo_guide.md` line 207

```text
203: ### Expected result
204: 
205: ```text
206: priority: high
207: execution_mode: constrained_execution
208: intervention_feasible: false
209: human_review_required: true
210: ```
211: 
```

### `docs\master_cases_results_comparison.md` line 18

```text
14: | Scenario | Role | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle |
15: |---|---|---:|---|---|---:|---:|---|
16: | `COMP-001` | Main controlled-planning case | True | high | controlled_planning | True | True | decision_ready |
17: | `COMP-002` | Early-warning proportional-response case | True | medium | standard_planning | True | True | evidence_review |
18: | `PUMP-001` | Resource-constrained execution case | True | high | constrained_execution | False | True | evidence_review |
19: | `CONV-001` | Production-maintenance conflict case | True | high | controlled_planning | True | True | decision_ready |
20: | `DATA-001` | Evidence-quality stop and diagnostic-review case | False | medium | diagnostic_review | True | True | evidence_review |
21: 
22: ## Detailed case-by-case explanation
```

### `docs\oversee_architecture_comp001_deep_dive_manual.md` line 764

```text
760: 
761: ```text
762: controlled_planning
763: standard_planning
764: constrained_execution
765: diagnostic_review
766: ```
767: 
768: ---
```

### `docs\reports\consistency_benchmark\oversee_consistency_benchmark_report.md` line 104

```text
100: **Conclusion:** The stable governed decision remained identical across repeated executions.
101: 
102: | Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
103: |---:|---|---:|---|---|---:|---:|---|---|---|
104: | 1 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
105: | 2 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
106: | 3 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
107: | 4 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
108: | 5 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
```

### `docs\reports\consistency_benchmark\oversee_consistency_benchmark_results.json` line 393

```text
389:       "layer1_valid": true,
390:       "layer2_decision_ready": true,
391:       "case_lifecycle_stage": "evidence_review",
392:       "priority": "high",
393:       "execution_mode": "constrained_execution",
394:       "intervention_feasible": false,
395:       "human_review_required": true,
396:       "generated_file_count": 17,
397:       "governed_signature": "7a4bc2c9c65b09999ad16b2555231dada3656ee961d96e68c4f58f7415ec189b",
```

### `docs\reports\v0_6_2_scenario_results_summary.json` line 68

```text
64:     "failure_mode": "seal_degradation",
65:     "decision_pattern": "high_risk_resource_constrained_escalation",
66:     "layer1_valid": true,
67:     "priority": "high",
68:     "execution_mode": "constrained_execution",
69:     "intervention_feasible": false,
70:     "human_review_required": true,
71:     "case_lifecycle_stage": "evidence_review",
72:     "data_quality_flags": "",
```

## `intervention_not_feasible`

### `collect_oversee_meeting_evidence.py` line 78

```text
74:     "DMN",
75:     "governed recommendation",
76:     "controlled_planning",
77:     "constrained_execution",
78:     "intervention_not_feasible",
79:     "case_not_decision_ready",
80:     "spare_part_not_available",
81:     "specialist_technician_not_available",
82: ]
```

### `src\oversee\decision_rules\recommendation_path_runner.py` line 140

```text
136:             "Obtain accountable human review before execution."
137:         )
138: 
139:     if not intervention_feasible:
140:         transformation_reasons.append("intervention_not_feasible")
141:         preconditions.append(
142:             "Restore intervention feasibility before executing physical maintenance."
143:         )
144: 
```

## `case_not_decision_ready`

### `collect_oversee_meeting_evidence.py` line 79

```text
75:     "governed recommendation",
76:     "controlled_planning",
77:     "constrained_execution",
78:     "intervention_not_feasible",
79:     "case_not_decision_ready",
80:     "spare_part_not_available",
81:     "specialist_technician_not_available",
82: ]
83: 
```

### `src\oversee\decision_rules\recommendation_path_runner.py` line 146

```text
142:             "Restore intervention feasibility before executing physical maintenance."
143:         )
144: 
145:     if not decision_ready:
146:         transformation_reasons.append("case_not_decision_ready")
147:         preconditions.append(
148:             "Resolve open case blockers before approving execution."
149:         )
150: 
```

## `spare_part_not_available`

### `collect_oversee_meeting_evidence.py` line 80

```text
76:     "controlled_planning",
77:     "constrained_execution",
78:     "intervention_not_feasible",
79:     "case_not_decision_ready",
80:     "spare_part_not_available",
81:     "specialist_technician_not_available",
82: ]
83: 
84: 
```

### `src\oversee\case_management\case_lifecycle_builder.py` line 400

```text
396: 
397:     blockers.extend(context.data_quality_flags)
398: 
399:     if not context.maintenance_resources.spare_part_available:
400:         blockers.append("spare_part_not_available")
401:     if not context.maintenance_resources.specialist_technician_available_next_shift:
402:         blockers.append("specialist_technician_not_available")
403:     if context.predictive_evidence.confidence_score < 0.5:
404:         blockers.append("low_predictive_confidence")
```

## `specialist_technician_not_available`

### `collect_oversee_meeting_evidence.py` line 81

```text
77:     "constrained_execution",
78:     "intervention_not_feasible",
79:     "case_not_decision_ready",
80:     "spare_part_not_available",
81:     "specialist_technician_not_available",
82: ]
83: 
84: 
85: @dataclass
```

### `src\oversee\case_management\case_lifecycle_builder.py` line 402

```text
398: 
399:     if not context.maintenance_resources.spare_part_available:
400:         blockers.append("spare_part_not_available")
401:     if not context.maintenance_resources.specialist_technician_available_next_shift:
402:         blockers.append("specialist_technician_not_available")
403:     if context.predictive_evidence.confidence_score < 0.5:
404:         blockers.append("low_predictive_confidence")
405: 
406:     return blockers
```

# Meeting walkthrough with Fernando

## Selected runs

Show the two selected paper-facing output folders.

## Scenario files

Open 00_scenario.json and show comparable predictions plus diverging resource/governance context.

## Layer 1

Open the aggregated evidence package and validation report. Show 7 payloads, valid=true, no quality flags.

## Canonical Context

Open 02_canonical_case_context.json. Show how independent payloads become asset, predictive_evidence, operational_context, maintenance_resources and governance_policy.

## Layer 2

Open 02_contextualization_rule_trace.json. Show rule conditions, triggered status, output fields and rationales.

## Layer 3

Open 03_output_layer3_case_management_state.json. Compare decision_ready vs evidence_review and blockers.

## Layer 4

Open 04_output_layer4_dmn_decision_evaluation.json and recommendation_path_outputs. Show controlled_planning vs constrained_execution.

## Layer 5

Open the governed package and traceability index. Show final recommendation, governance summary and traceability_count=6.

