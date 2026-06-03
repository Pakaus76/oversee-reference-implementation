"""Comparison utilities for deterministic and generative OVERSEE outputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from oversee.decision_rules import LiveGenerativeRecommendationResult, RecommendationPathBundle
from oversee.reporting.governed_recommendation_package import GovernedRecommendationPackage


@dataclass(slots=True)
class DeterministicGenerativeComparison:
    """Comparison between deterministic and live generative recommendation paths."""

    comparison_id: str
    case_id: str
    asset_id: str
    deterministic_priority: str | None
    generative_priority: str | None
    priority_alignment: bool
    deterministic_action: str | None
    generative_action: str | None
    action_alignment: str
    human_review_alignment: bool
    model_call_successful: bool
    fallback_used: bool
    protected_fact_violation_count: int
    rationale_difference: bool
    comparison_version: str = "0.1.0"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


def compare_deterministic_and_generative_outputs(
    *,
    recommendation_bundle: RecommendationPathBundle,
    live_result: LiveGenerativeRecommendationResult,
) -> DeterministicGenerativeComparison:
    """Compare deterministic and generative recommendation outputs."""

    deterministic = _find_path_recommendation(
        recommendation_bundle,
        path_name="deterministic_anchor",
    )
    generative = live_result.parsed_recommendation

    deterministic_priority = _safe_lower(deterministic.get("priority"))
    generative_priority = _safe_lower(generative.get("priority"))
    deterministic_action = _safe_text(deterministic.get("action"))
    generative_action = _safe_text(generative.get("recommended_action"))

    return DeterministicGenerativeComparison(
        comparison_id=f"det_vs_gen_{live_result.case_id}",
        case_id=live_result.case_id,
        asset_id=live_result.asset_id,
        deterministic_priority=deterministic_priority,
        generative_priority=generative_priority,
        priority_alignment=deterministic_priority == generative_priority,
        deterministic_action=deterministic_action,
        generative_action=generative_action,
        action_alignment=_action_alignment(deterministic_action, generative_action),
        human_review_alignment=bool(
            generative.get("human_review_required")
        ) == bool(live_result.protected_facts["human_review_required"]),
        model_call_successful=live_result.model_call_successful,
        fallback_used=live_result.fallback_used,
        protected_fact_violation_count=len(live_result.protected_fact_violations),
        rationale_difference=_safe_text(deterministic.get("rationale")) != _safe_text(
            generative.get("rationale")
        ),
    )


def build_advanced_governed_package_dict(
    *,
    base_package: GovernedRecommendationPackage,
    live_result: LiveGenerativeRecommendationResult,
    comparison: DeterministicGenerativeComparison,
) -> dict[str, Any]:
    """Return the Layer 5 package enriched with generative evidence."""

    package_dict = base_package.to_dict()

    package_dict["generative_ai_summary"] = {
        "live_generative_result_id": live_result.result_id,
        "model_call_attempted": live_result.model_call_attempted,
        "model_call_successful": live_result.model_call_successful,
        "fallback_used": live_result.fallback_used,
        "fallback_reason": live_result.fallback_reason,
        "model_name": live_result.model_name,
        "response_id": live_result.response_id,
        "prompt_hash": live_result.prompt_hash,
        "validation_error_count": len(live_result.validation_errors),
        "protected_fact_violation_count": len(live_result.protected_fact_violations),
    }
    package_dict["deterministic_vs_generative_comparison"] = comparison.to_dict()
    package_dict["final_recommendation"]["live_generative_priority"] = (
        live_result.parsed_recommendation.get("priority")
    )
    package_dict["final_recommendation"]["live_generative_action"] = (
        live_result.parsed_recommendation.get("recommended_action")
    )
    package_dict["final_recommendation"]["generative_path_fallback_used"] = (
        live_result.fallback_used
    )

    package_dict["reviewer_notes"].append(
        "Layer 4 includes a live generative recommendation path compared against the deterministic anchor."
    )
    package_dict["reviewer_notes"].append(
        "Layer 5 preserves model-call metadata, fallback status and protected-fact validation."
    )

    return package_dict


def build_advanced_reviewer_summary_markdown(
    *,
    package_dict: dict[str, Any],
) -> str:
    """Build reviewer summary for the advanced generative package."""

    final = package_dict["final_recommendation"]
    generative = package_dict["generative_ai_summary"]
    comparison = package_dict["deterministic_vs_generative_comparison"]

    lines = [
        "# OVERSEE advanced governed recommendation package",
        "",
        f"Package ID: `{package_dict['package_id']}`",
        f"Case ID: `{package_dict['case_id']}`",
        f"Asset ID: `{package_dict['asset_id']}`",
        "",
        "## Final governed recommendation",
        "",
        f"- Recommended action: {final.get('recommended_action')}",
        f"- Priority: {final.get('priority')}",
        f"- Execution mode: {final.get('recommended_execution_mode')}",
        f"- Human review required: {final.get('human_review_required')}",
        f"- Decision ready: {final.get('decision_ready')}",
        "",
        "## Live generative path",
        "",
        f"- Model: {generative.get('model_name')}",
        f"- Model call attempted: {generative.get('model_call_attempted')}",
        f"- Model call successful: {generative.get('model_call_successful')}",
        f"- Fallback used: {generative.get('fallback_used')}",
        f"- Fallback reason: {generative.get('fallback_reason')}",
        f"- Protected fact violations: {generative.get('protected_fact_violation_count')}",
        "",
        "## Deterministic vs generative comparison",
        "",
        f"- Priority alignment: {comparison.get('priority_alignment')}",
        f"- Action alignment: {comparison.get('action_alignment')}",
        f"- Human review alignment: {comparison.get('human_review_alignment')}",
        f"- Rationale difference: {comparison.get('rationale_difference')}",
        "",
        "## Traceability",
        "",
        f"- Traceability entries: {package_dict.get('traceability_count')}",
        f"- Prompt hash: {generative.get('prompt_hash')}",
        "",
        "## Reviewer notes",
        "",
    ]

    for note in package_dict["reviewer_notes"]:
        lines.append(f"- {note}")

    return "\n".join(lines)


def _find_path_recommendation(
    recommendation_bundle: RecommendationPathBundle,
    *,
    path_name: str,
) -> dict[str, Any]:
    """Return recommendation for one path."""

    for output in recommendation_bundle.path_outputs:
        if output.path_name == path_name:
            return dict(output.recommendation)

    return {}


def _safe_lower(value: Any) -> str | None:
    """Return lowercase string or None."""

    if value is None:
        return None

    return str(value).strip().lower()


def _safe_text(value: Any) -> str | None:
    """Return normalized text or None."""

    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _action_alignment(
    deterministic_action: str | None,
    generative_action: str | None,
) -> str:
    """Classify action alignment with a simple token-overlap heuristic."""

    if not deterministic_action or not generative_action:
        return "missing"

    det_tokens = _content_tokens(deterministic_action)
    gen_tokens = _content_tokens(generative_action)

    if not det_tokens or not gen_tokens:
        return "missing"

    overlap = len(det_tokens.intersection(gen_tokens))
    ratio = overlap / max(len(det_tokens), len(gen_tokens))

    if ratio >= 0.7:
        return "strong"
    if ratio >= 0.35:
        return "partial"
    return "different"


def _content_tokens(text: str) -> set[str]:
    """Return rough content tokens for comparison."""

    stop_words = {
        "and",
        "or",
        "the",
        "a",
        "an",
        "to",
        "of",
        "for",
        "in",
        "on",
        "with",
        "is",
        "are",
    }

    return {
        token
        for token in text.lower().replace(".", " ").replace(",", " ").split()
        if token and token not in stop_words
    }
