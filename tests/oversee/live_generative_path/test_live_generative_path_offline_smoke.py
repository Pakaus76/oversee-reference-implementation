"""Offline fallback tests for the OVERSEE live generative path."""

from __future__ import annotations

import os

from oversee.domain import Asset, DecisionCase, PredictiveAlert, Recommendation
from oversee.live_generative_path import run_live_generative_path


def build_smoke_decision_case() -> DecisionCase:
    """Build a minimal compressor decision case for offline fallback validation."""

    asset = Asset(
        asset_id="COMP-001",
        asset_type="compressor",
        criticality=5,
        location="Packaging line utilities area",
    )

    alert = PredictiveAlert(
        alert_id="ALERT-COMP-001-LIVE-GEN-OFFLINE",
        asset_id="COMP-001",
        predicted_issue="bearing wear progression",
        time_to_failure_hours=24.0,
        confidence_score=0.86,
    )

    return DecisionCase(
        case_id="CASE-COMP-001-LIVE-GEN-OFFLINE",
        asset=asset,
        alert=alert,
        context_note=(
            "High production dependency. Spare part available. Technician available. "
            "Planned intervention window possible within the next shift."
        ),
    )


def test_live_generative_path_returns_fallback_recommendation_without_api_key() -> None:
    """The live generative path should return a valid fallback recommendation offline."""

    os.environ.pop("OPENAI_API_KEY", None)

    recommendation = run_live_generative_path(build_smoke_decision_case())

    assert isinstance(recommendation, Recommendation)
    assert recommendation.asset_id == "COMP-001"
    assert recommendation.recommendation_id.startswith("live_gen_")
    assert recommendation.action
    assert recommendation.rationale
    assert recommendation.priority in {"low", "medium", "high", "critical"}


def test_live_generative_path_output_uses_public_terminology_without_api_key() -> None:
    """The live generative path output should avoid legacy terminology."""

    os.environ.pop("OPENAI_API_KEY", None)

    recommendation = run_live_generative_path(build_smoke_decision_case())
    output_text = " ".join(
        [
            recommendation.recommendation_id,
            recommendation.action,
            recommendation.rationale,
            recommendation.priority,
        ]
    ).lower()

    forbidden_terms = [
        "condition c",
        "condition d",
        "condition e",
        "condition f",
        "condition_c",
        "condition_d",
        "condition_e",
        "condition_f",
        "run_condition",
        "c-vs-f",
        "decision orchestrator",
        "dual_generative_do",
    ]

    for term in forbidden_terms:
        assert term not in output_text
