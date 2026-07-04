"""Layer 4 DMN-like decision rules for OVERSEE.

Purpose:
    Evaluate explicit decision rules that convert context and case state into
    governed decision fields.

Architectural role:
    Layer 4 assigns priority, execution mode, intervention feasibility and
    human-review requirements. These outputs constrain any recommendation
    formulation and are later packaged by Layer 5.

Main output:
    04_output_layer4_dmn_decision_evaluation.json
"""

from __future__ import annotations

from oversee.case_context import CanonicalCaseContext
from oversee.case_management import CaseManagementState
from oversee.decision_rules.decision_rule_contracts import (
    DecisionRuleEvaluation,
    RuleEvaluation,
)

#8.0 >-------------------------------------------------------------------------------------------------------------------------------

def evaluate_dmn_like_rules(
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
) -> DecisionRuleEvaluation:
    """Evaluate explicit DMN-like rules for one OVERSEE case.
    
    The function receives the canonical context and Layer 3 case state. It returns
    a decision-rule evaluation bundle containing triggered rules and final decision
    fields such as priority, execution mode and review requirement.
    """

    urgency_rule = _evaluate_urgency_rule(canonical_context)
    criticality_rule = _evaluate_criticality_rule(canonical_context)
    feasibility_rule = _evaluate_intervention_feasibility_rule(canonical_context)
    human_review_rule = _evaluate_human_review_rule(canonical_context, case_state)
    execution_constraint_rule = _evaluate_execution_constraint_rule(canonical_context)
    final_priority_rule = _evaluate_final_priority_rule(
        urgency_rule=urgency_rule,
        criticality_rule=criticality_rule,
        feasibility_rule=feasibility_rule,
        human_review_rule=human_review_rule,
        execution_constraint_rule=execution_constraint_rule,
    )

    rules = [
        urgency_rule,
        criticality_rule,
        feasibility_rule,
        human_review_rule,
        execution_constraint_rule,
        final_priority_rule,
    ]

    return DecisionRuleEvaluation(
        evaluation_id=f"dmn_like_eval_{canonical_context.case_id}",
        case_id=canonical_context.case_id,
        asset_id=canonical_context.asset.asset_id,
        source_context_id=canonical_context.context_id,
        source_case_state=case_state.lifecycle_stage,
        rules=rules,
        final_priority=str(final_priority_rule.output_fields["final_priority"]),
        recommended_execution_mode=str(
            execution_constraint_rule.output_fields["recommended_execution_mode"]
        ),
        human_review_required=bool(human_review_rule.output_fields["human_review_required"]),
        intervention_feasible=bool(feasibility_rule.output_fields["intervention_feasible"]),
    )


def _evaluate_urgency_rule(context: CanonicalCaseContext) -> RuleEvaluation:
    """Evaluate failure-horizon urgency."""

    hours = context.predictive_evidence.estimated_time_to_failure_hours

    if hours <= 24:
        urgency = "critical"
        triggered = True
        rationale = "Estimated failure horizon is within 24 hours."
    elif hours <= 72:
        urgency = "high"
        triggered = True
        rationale = "Estimated failure horizon is within 72 hours."
    elif hours <= 168:
        urgency = "medium"
        triggered = False
        rationale = "Estimated failure horizon is within one week."
    else:
        urgency = "low"
        triggered = False
        rationale = "Estimated failure horizon is beyond one week."

    return RuleEvaluation(
        rule_id="DMN_R001",
        rule_name="Failure horizon urgency",
        decision_table="compressor_urgency_assessment",
        status="evaluated",
        input_fields={
            "estimated_time_to_failure_hours": hours,
            "alert_severity": context.predictive_evidence.alert_severity,
        },
        output_fields={
            "urgency": urgency,
        },
        triggered=triggered,
        rationale=rationale,
    )


def _evaluate_criticality_rule(context: CanonicalCaseContext) -> RuleEvaluation:
    """Evaluate asset criticality."""

    score = context.asset.criticality_score
    label = context.asset.criticality_label

    if score >= 5:
        criticality_band = "high"
        triggered = True
        rationale = "Asset criticality score is high."
    elif score >= 3:
        criticality_band = "medium"
        triggered = False
        rationale = "Asset criticality score is medium."
    else:
        criticality_band = "low"
        triggered = False
        rationale = "Asset criticality score is low."

    return RuleEvaluation(
        rule_id="DMN_R002",
        rule_name="Asset criticality classification",
        decision_table="compressor_criticality_assessment",
        status="evaluated",
        input_fields={
            "asset_criticality_label": label,
            "asset_criticality_score": score,
        },
        output_fields={
            "criticality_band": criticality_band,
        },
        triggered=triggered,
        rationale=rationale,
    )


def _evaluate_intervention_feasibility_rule(context: CanonicalCaseContext) -> RuleEvaluation:
    """Evaluate whether a controlled intervention is feasible."""

    resources = context.maintenance_resources
    feasible = resources.intervention_feasible

    if feasible:
        rationale = "Spare part and specialist support are available."
    else:
        rationale = "At least one required intervention resource is unavailable."

    return RuleEvaluation(
        rule_id="DMN_R003",
        rule_name="Intervention feasibility",
        decision_table="compressor_intervention_feasibility",
        status="evaluated",
        input_fields={
            "spare_part_available": resources.spare_part_available,
            "specialist_technician_available_next_shift": (
                resources.specialist_technician_available_next_shift
            ),
        },
        output_fields={
            "intervention_feasible": feasible,
        },
        triggered=feasible,
        rationale=rationale,
    )


def _evaluate_human_review_rule(
    context: CanonicalCaseContext,
    case_state: CaseManagementState,
) -> RuleEvaluation:
    """Evaluate accountable human review requirement."""

    required = (
        context.governance_policy.computed_human_review_required
        or case_state.human_review_required
    )

    if required:
        rationale = "High criticality or high-severity evidence requires accountable review."
    else:
        rationale = "No mandatory human review trigger is active."

    return RuleEvaluation(
        rule_id="DMN_R004",
        rule_name="Accountable human review requirement",
        decision_table="compressor_human_review_policy",
        status="evaluated",
        input_fields={
            "computed_human_review_required": (
                context.governance_policy.computed_human_review_required
            ),
            "case_state_human_review_required": case_state.human_review_required,
        },
        output_fields={
            "human_review_required": required,
        },
        triggered=required,
        rationale=rationale,
    )


def _evaluate_execution_constraint_rule(context: CanonicalCaseContext) -> RuleEvaluation:
    """Evaluate execution constraint and recommended execution mode."""

    production_pressure = context.operational_context.production_pressure
    downtime_hours = context.operational_context.next_planned_downtime_hours
    intervention_feasible = context.maintenance_resources.intervention_feasible
    data_quality_flags = context.data_quality_flags

    if data_quality_flags:
        execution_mode = "diagnostic_review"
        triggered = True
        rationale = (
            "Data quality flags are present. The case should remain in diagnostic "
            "review before releasing an execution recommendation."
        )
    elif production_pressure == "high" and intervention_feasible:
        execution_mode = "controlled_planning"
        triggered = True
        rationale = (
            "Production pressure is high, but resources are available. "
            "Controlled planning is preferred over uncontrolled stop."
        )
    elif not intervention_feasible:
        execution_mode = "constrained_execution"
        triggered = True
        rationale = "Execution is constrained because intervention resources are incomplete."
    else:
        execution_mode = "standard_planning"
        triggered = False
        rationale = "No severe execution constraint is active."

    return RuleEvaluation(
        rule_id="DMN_R005",
        rule_name="Execution constraint assessment",
        decision_table="compressor_execution_mode",
        status="evaluated",
        input_fields={
            "production_pressure": production_pressure,
            "next_planned_downtime_hours": downtime_hours,
            "intervention_feasible": intervention_feasible,
            "data_quality_flags": data_quality_flags,
        },
        output_fields={
            "recommended_execution_mode": execution_mode,
        },
        triggered=triggered,
        rationale=rationale,
    )

def _evaluate_final_priority_rule(
    *,
    urgency_rule: RuleEvaluation,
    criticality_rule: RuleEvaluation,
    feasibility_rule: RuleEvaluation,
    human_review_rule: RuleEvaluation,
    execution_constraint_rule: RuleEvaluation,
) -> RuleEvaluation:
    """Consolidate final priority from upstream rule outputs."""

    urgency = str(urgency_rule.output_fields["urgency"])
    criticality = str(criticality_rule.output_fields["criticality_band"])
    feasible = bool(feasibility_rule.output_fields["intervention_feasible"])
    human_review = bool(human_review_rule.output_fields["human_review_required"])
    execution_mode = str(execution_constraint_rule.output_fields["recommended_execution_mode"])

    if urgency == "critical":
        final_priority = "critical"
    elif urgency == "high" and criticality == "high":
        final_priority = "high"
    elif urgency in {"high", "medium"} and criticality in {"high", "medium"}:
        final_priority = "medium"
    else:
        final_priority = "low"

    if not feasible and final_priority in {"critical", "high"}:
        escalation_required = True
    else:
        escalation_required = False

    rationale_parts = [
        f"urgency={urgency}",
        f"criticality={criticality}",
        f"intervention_feasible={feasible}",
        f"human_review_required={human_review}",
        f"execution_mode={execution_mode}",
    ]

    return RuleEvaluation(
        rule_id="DMN_R006",
        rule_name="Final priority consolidation",
        decision_table="compressor_final_priority",
        status="evaluated",
        input_fields={
            "urgency": urgency,
            "criticality_band": criticality,
            "intervention_feasible": feasible,
            "human_review_required": human_review,
            "recommended_execution_mode": execution_mode,
        },
        output_fields={
            "final_priority": final_priority,
            "escalation_required": escalation_required,
        },
        triggered=True,
        rationale="Final priority consolidated from " + ", ".join(rationale_parts) + ".",
    )
