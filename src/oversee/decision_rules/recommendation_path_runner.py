"""Run OVERSEE recommendation paths from Layer 4 inputs."""

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
    """Run currently available recommendation paths for the compressor case."""

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
    """Run the migrated deterministic anchor using the canonical context."""

    decision_case = _build_decision_case(canonical_context, case_state)
    recommendation = run_deterministic_anchor(decision_case)

    recommendation_dict = _jsonable(recommendation)
    recommendation_dict["dmn_like_final_priority"] = rule_evaluation.final_priority
    recommendation_dict["recommended_execution_mode"] = (
        rule_evaluation.recommended_execution_mode
    )
    recommendation_dict["human_review_required"] = rule_evaluation.human_review_required

    return RecommendationPathOutput(
        path_name="deterministic_anchor",
        path_type="existing_recommendation_path",
        status="completed",
        recommendation=recommendation_dict,
        input_refs=[
            canonical_context.context_id,
            case_state.case_id,
            rule_evaluation.evaluation_id,
        ],
        governance_refs=[
            "compressor_human_review_policy",
            "compressor_final_priority",
        ],
        notes=[
            "The deterministic anchor is executed after explicit DMN-like rule evaluation.",
            "DMN-like rule outputs are preserved as governance context; they do not overwrite the anchor recommendation.",
        ],
    )


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
