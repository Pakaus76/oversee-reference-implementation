"""Layer 4 recommendation path runner for OVERSEE.

Purpose:
    Execute recommendation paths after DMN-like rule evaluation.

Architectural role:
    This module complements the Layer 4 decision-rule output with governed
    recommendation formulation. The deterministic anchor provides an initial
    recommendation, but OVERSEE may preserve, constrain, transform, or escalate
    that recommendation according to feasibility, readiness, execution mode,
    and governance requirements.

Main output:
    04_output_layer4_recommendation_path_outputs.json
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from oversee.case_context import CanonicalCaseContext
from oversee.case_management import CaseManagementState
from oversee.decision_rules.decision_rule_contracts import (
    DecisionRuleEvaluation,
    RecommendationPathBundle,
    RecommendationPathOutput,
)
from oversee.deterministic_anchor import run_deterministic_anchor
from oversee.domain import Asset, DecisionCase, PredictiveAlert


def run_recommendation_paths(
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
) -> RecommendationPathBundle:
    """Run available recommendation paths for one OVERSEE case."""

    deterministic_output = _run_deterministic_anchor_path(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )

    governance_summary_output = _build_rule_governance_summary_path(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )

    return RecommendationPathBundle(
        bundle_id=f"recommendation_paths_{canonical_context.case_id}",
        case_id=canonical_context.case_id,
        asset_id=canonical_context.asset.asset_id,
        decision_rule_evaluation_id=rule_evaluation.evaluation_id,
        path_outputs=[
            deterministic_output,
            governance_summary_output,
        ],
    )


def _run_deterministic_anchor_path(
    *,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
) -> RecommendationPathOutput:
    """Run the deterministic anchor and transform it into a governed recommendation."""

    decision_case = _build_decision_case(canonical_context, case_state)
    anchor_recommendation = run_deterministic_anchor(decision_case)
    anchor_dict = _jsonable(anchor_recommendation)

    governed_recommendation = _build_governed_recommendation(
        anchor_recommendation=anchor_dict,
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )

    return RecommendationPathOutput(
        path_name="governed_recommendation_formulation",
        path_type="governed_recommendation_path",
        status="completed",
        recommendation=governed_recommendation,
        input_refs=[
            canonical_context.context_id,
            case_state.case_id,
            rule_evaluation.evaluation_id,
        ],
        governance_refs=[
            "compressor_human_review_policy",
            "compressor_final_priority",
            "compressor_execution_mode",
            "recommendation_consistency_constraints",
        ],
        notes=[
            "The deterministic anchor is used as an initial recommendation.",
            "Layer 4 formulates a governed recommendation by preserving, constraining, transforming, or escalating the anchor according to feasibility, readiness, execution mode, and governance signals.",
        ],
    )


def _build_governed_recommendation(
    *,
    anchor_recommendation: dict[str, Any],
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
) -> dict[str, Any]:
    """Build a governed recommendation consistent with contextual constraints."""

    anchor_action = str(
        anchor_recommendation.get(
            "action",
            "Plan inspection and maintenance preparation.",
        )
    )
    anchor_priority = str(anchor_recommendation.get("priority", "medium"))
    execution_mode = rule_evaluation.recommended_execution_mode
    intervention_feasible = bool(rule_evaluation.intervention_feasible)
    human_review_required = bool(rule_evaluation.human_review_required)
    decision_ready = bool(case_state.decision_ready)
    blockers = list(getattr(case_state, "blockers", []) or [])

    transformation_reasons: list[str] = []
    preconditions: list[str] = []
    required_reviews: list[str] = []
    escalations: list[str] = []
    contingency_actions: list[str] = []

    if human_review_required:
        required_reviews.append(
            "Obtain accountable human review before execution."
        )

    if not intervention_feasible:
        transformation_reasons.append("intervention_not_feasible")
        preconditions.append(
            "Restore intervention feasibility before executing physical maintenance."
        )

    if not decision_ready:
        transformation_reasons.append("case_not_decision_ready")
        preconditions.append(
            "Resolve open case blockers before approving execution."
        )

    if execution_mode == "constrained_execution":
        transformation_reasons.append("constrained_execution_mode")
        escalations.append(
            "Escalate the constrained execution case to the accountable maintenance and operations owners."
        )
        contingency_actions.append(
            "Increase monitoring and prepare a contingency plan until resources and approval are available."
        )

    if blockers:
        preconditions.append(
            "Resolve listed blockers: " + ", ".join(str(item) for item in blockers) + "."
        )

    transformation_applied = bool(transformation_reasons)

    if transformation_applied:
        primary_action = (
            "Escalate the constrained maintenance case, resolve execution blockers, "
            "increase monitoring, and prepare intervention once feasibility is restored."
        )
        recommended_action = primary_action
    else:
        primary_action = anchor_action
        recommended_action = anchor_action

    rationale_parts = [
        f"Deterministic anchor proposed: {anchor_action}",
        f"DMN-like final priority: {rule_evaluation.final_priority}",
        f"Execution mode: {execution_mode}",
        f"Intervention feasible: {intervention_feasible}",
        f"Decision ready: {decision_ready}",
        f"Human review required: {human_review_required}",
    ]

    if transformation_reasons:
        rationale_parts.append(
            "The anchor was transformed because: "
            + ", ".join(transformation_reasons)
            + "."
        )
    else:
        rationale_parts.append(
            "The anchor was preserved because the case is feasible and decision-ready."
        )

    return {
        "recommendation_id": f"governed_rec_{canonical_context.case_id}",
        "asset_id": canonical_context.asset.asset_id,
        "action": recommended_action,
        "primary_action": primary_action,
        "anchor_action": anchor_action,
        "priority": rule_evaluation.final_priority,
        "deterministic_anchor_priority": anchor_priority,
        "dmn_like_final_priority": rule_evaluation.final_priority,
        "recommended_execution_mode": execution_mode,
        "human_review_required": human_review_required,
        "intervention_feasible": intervention_feasible,
        "decision_ready": decision_ready,
        "transformation_applied": transformation_applied,
        "transformation_reasons": transformation_reasons,
        "preconditions": preconditions,
        "blockers": blockers,
        "required_reviews": required_reviews,
        "escalations": escalations,
        "contingency_actions": contingency_actions,
        "rationale": " ".join(rationale_parts),
    }


def _build_rule_governance_summary_path(
    *,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
) -> RecommendationPathOutput:
    """Build a rule-governance summary output for Layer 4 traceability."""

    recommendation = {
        "case_id": canonical_context.case_id,
        "asset_id": canonical_context.asset.asset_id,
        "final_priority": rule_evaluation.final_priority,
        "recommended_execution_mode": rule_evaluation.recommended_execution_mode,
        "human_review_required": rule_evaluation.human_review_required,
        "intervention_feasible": rule_evaluation.intervention_feasible,
        "decision_ready": case_state.decision_ready,
        "triggered_rule_count": rule_evaluation.triggered_rule_count,
    }

    return RecommendationPathOutput(
        path_name="dmn_like_governance_summary",
        path_type="rule_governance_summary",
        status="completed",
        recommendation=recommendation,
        input_refs=[
            canonical_context.context_id,
            case_state.case_id,
            rule_evaluation.evaluation_id,
        ],
        governance_refs=[
            rule.rule_id for rule in rule_evaluation.rules if rule.triggered
        ],
        notes=[
            "This output summarizes explicit rule evaluation before final governed packaging.",
        ],
    )


def _build_decision_case(
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
) -> DecisionCase:
    """Convert canonical context into the current domain DecisionCase."""

    asset = Asset(
        asset_id=canonical_context.asset.asset_id,
        asset_type=canonical_context.asset.asset_type,
        criticality=canonical_context.asset.criticality_score,
        location=canonical_context.asset.line_id,
    )
    alert = PredictiveAlert(
        alert_id=f"ALERT-{canonical_context.case_id}",
        asset_id=canonical_context.asset.asset_id,
        predicted_issue=canonical_context.predictive_evidence.alert_type,
        time_to_failure_hours=(
            canonical_context.predictive_evidence.estimated_time_to_failure_hours
        ),
        confidence_score=canonical_context.predictive_evidence.confidence_score,
    )
    context_note = (
        "Risk drivers: "
        + ", ".join(canonical_context.key_risk_drivers)
        + f". Case lifecycle stage: {case_state.lifecycle_stage}."
    )

    return DecisionCase(
        case_id=canonical_context.case_id,
        asset=asset,
        alert=alert,
        context_note=context_note,
    )


def _jsonable(value: Any) -> dict[str, Any]:
    """Convert a recommendation object into a JSON-serializable dictionary."""

    if isinstance(value, dict):
        return dict(value)

    if is_dataclass(value):
        return asdict(value)

    if hasattr(value, "model_dump") and callable(value.model_dump):
        return value.model_dump()

    if hasattr(value, "dict") and callable(value.dict):
        return value.dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return {"value": str(value)}