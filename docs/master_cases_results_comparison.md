# OVERSEE Master Cases Results Comparison

Version baseline: `v0.6.2`  
Scope: detailed comparison of the 5 paradigmatic master cases

## Purpose

This document explains the result of the five paradigmatic OVERSEE cases in enough detail for a reviewer to compare them comfortably.

The objective is to make clear that the demo is not repeating the same answer with different names. Each master case follows the same architecture, but the reasoning changes because the evidence, context, resource situation and governance conditions are different.

## Comparative table

| Scenario | Role | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle |
|---|---|---:|---|---|---:|---:|---|
| `COMP-001` | Main controlled-planning case | True | high | controlled_planning | True | True | decision_ready |
| `COMP-002` | Early-warning proportional-response case | True | medium | standard_planning | True | True | evidence_review |
| `PUMP-001` | Resource-constrained execution case | True | high | constrained_execution | False | True | evidence_review |
| `CONV-001` | Production-maintenance conflict case | True | high | controlled_planning | True | True | decision_ready |
| `DATA-001` | Evidence-quality stop and diagnostic-review case | False | medium | diagnostic_review | True | True | evidence_review |

## Detailed case-by-case explanation

### COMP-001 - Paper compressor case

**Role:** Main controlled-planning case

**Asset type:** `industrial_air_compressor`  
**Failure mode:** `bearing_degradation`  
**Decision pattern:** `critical_but_feasible_controlled_planning`

#### Input situation

- Layer 1 output: Validated evidence package: alert, condition trends, asset criticality, and maintenance history
- Layer 2 output: Contextualized decision profile: high urgency, near downtime window, intervention feasible, review required
- Layer 3 output: Decision-ready case: open, 2 tasks active, 5 milestones reached, no blockers
- Layer 4 output: Decision record: high priority, controlled planning, human review retained
- Layer 5 output: Governed recommendation package: reviewer summary, traceability index, and work-order proposal

#### Result

```text
layer1_valid: True
priority: high
execution_mode: controlled_planning
intervention_feasible: True
human_review_required: True
case_lifecycle_stage: decision_ready
```

#### Why this result is different

This is the standard high-value path. The predictive alert is strong, the evidence is valid, the compressor is critical, resources are available, and a near downtime window exists. OVERSEE therefore recommends controlled planning rather than blind emergency action.

#### Business interpretation

A predictive maintenance alert becomes useful only after it is enriched with asset criticality, maintenance history, production context, resource availability and governance rules.

### COMP-002 - Lower urgency compressor case

**Role:** Early-warning proportional-response case

**Asset type:** `industrial_air_compressor`  
**Failure mode:** `early_vibration_anomaly`  
**Decision pattern:** `medium_urgency_planned_inspection`

#### Input situation

- Layer 1 output: Validated evidence package: early anomaly, condition trend, asset context, and maintenance history
- Layer 2 output: Contextualized decision profile: medium urgency, distant downtime window, intervention feasible, review recommended
- Layer 3 output: Decision-ready case: open, monitoring task active, no blockers
- Layer 4 output: Decision record: medium priority, planned inspection recommended
- Layer 5 output: Governed recommendation package: monitoring summary, traceability index, and inspection proposal

#### Result

```text
layer1_valid: True
priority: medium
execution_mode: standard_planning
intervention_feasible: True
human_review_required: True
case_lifecycle_stage: evidence_review
```

#### Why this result is different

This case shows that OVERSEE does not overreact. The alert exists, but the horizon is longer, operational pressure is moderate, and intervention can be planned. The result is standard planning rather than high-priority escalation.

#### Business interpretation

The system can distinguish between a real alert and an urgent alert. This prevents unnecessary disruption.

### PUMP-001 - Resource-constrained pump case

**Role:** Resource-constrained execution case

**Asset type:** `industrial_pump`  
**Failure mode:** `seal_degradation`  
**Decision pattern:** `high_risk_resource_constrained_escalation`

#### Input situation

- Layer 1 output: Validated evidence package: seal degradation alert, condition trends, criticality, and maintenance history
- Layer 2 output: Contextualized decision profile: high urgency, no near downtime window, intervention not feasible, review required
- Layer 3 output: Decision-ready case: open, escalation task active, planning blocker visible
- Layer 4 output: Decision record: high priority, escalation planning recommended, human review retained
- Layer 5 output: Governed recommendation package: escalation summary, traceability index, and constrained work-order proposal

#### Result

```text
layer1_valid: True
priority: high
execution_mode: constrained_execution
intervention_feasible: False
human_review_required: True
case_lifecycle_stage: evidence_review
```

#### Why this result is different

This case separates risk from readiness. The pump risk is high, but resources are not ready for normal execution. OVERSEE keeps the high priority visible while changing the execution mode to constrained execution.

#### Business interpretation

A correct decision must consider whether the organization can execute safely and realistically, not only whether the asset is at risk.

### CONV-001 - Production-constrained conveyor case

**Role:** Production-maintenance conflict case

**Asset type:** `conveyor_system`  
**Failure mode:** `belt_drive_degradation`  
**Decision pattern:** `high_risk_production_maintenance_conflict`

#### Input situation

- Layer 1 output: Validated evidence package: conveyor degradation alert, condition trends, bottleneck criticality, and maintenance history
- Layer 2 output: Contextualized decision profile: high urgency, no near downtime window, intervention technically feasible, review required
- Layer 3 output: Decision-ready case: open, escalation task active, production slot blocker visible
- Layer 4 output: Decision record: high priority, escalation planning recommended, human review retained
- Layer 5 output: Governed recommendation package: escalation summary, traceability index, and conditional work-order proposal

#### Result

```text
layer1_valid: True
priority: high
execution_mode: controlled_planning
intervention_feasible: True
human_review_required: True
case_lifecycle_stage: decision_ready
```

#### Why this result is different

This case shows that a technically feasible intervention can still be operationally difficult. The conveyor risk is real and resources are available, but production pressure and downtime-window limitations create a conflict that must be made visible.

#### Business interpretation

Maintenance decisions are not purely technical. OVERSEE makes production constraints visible before action is recommended.

### DATA-001 - Evidence-quality stop case

**Role:** Evidence-quality stop and diagnostic-review case

**Asset type:** `electric_motor`  
**Failure mode:** `contradictory_thermal_vibration_evidence`  
**Decision pattern:** `evidence_quality_review_before_action`

#### Input situation

- Layer 1 output: Validated evidence package: moderate anomaly, contradictory condition indicators, asset context, and maintenance history
- Layer 2 output: Contextualized decision profile: medium urgency, evidence quality concern, diagnostic review recommended
- Layer 3 output: Decision-ready case: open, evidence review task active, diagnostic clarification required
- Layer 4 output: Decision record: medium priority, diagnostic review before intervention
- Layer 5 output: Governed recommendation package: evidence-quality summary, traceability index, and diagnostic inspection proposal

#### Result

```text
layer1_valid: False
priority: medium
execution_mode: diagnostic_review
intervention_feasible: True
human_review_required: True
case_lifecycle_stage: evidence_review
```

#### Why this result is different

This case proves that OVERSEE does not automate blindly. The evidence contains contradictory signals: temperature rises while vibration and current remain stable. Layer 1 marks the evidence package as not valid, Layer 3 keeps the case in evidence review, and Layer 4 recommends diagnostic review.

#### Business interpretation

When evidence quality is questionable, the correct governed behaviour is not to force an intervention, but to request diagnostic clarification and preserve traceability.

## Main conclusion

The five master cases demonstrate five different decision behaviours:

```text
COMP-001 -> act through controlled planning
COMP-002 -> plan proportionally without overreacting
PUMP-001 -> preserve urgency but constrain execution
CONV-001 -> expose the production-maintenance conflict
DATA-001 -> stop normal execution and request diagnostic review
```

This is exactly the intended value of OVERSEE: the same architecture does not produce a generic answer. It builds a context-specific, governed and traceable recommendation.
