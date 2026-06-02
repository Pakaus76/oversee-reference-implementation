"""Smoke tests for the OVERSEE deterministic anchor."""

from oversee.deterministic_anchor import run_deterministic_anchor
from oversee.domain import Asset, DecisionCase, PredictiveAlert, Recommendation


def build_smoke_decision_case() -> DecisionCase:
    """Build a minimal high-criticality compressor decision case."""

    asset = Asset(
        asset_id="COMP-001",
        asset_type="compressor",
        criticality=5,
        location="Packaging line utilities area",
    )

    alert = PredictiveAlert(
        alert_id="ALERT-COMP-001-SMOKE",
        asset_id="COMP-001",
        predicted_issue="bearing wear progression",
        time_to_failure_hours=24.0,
        confidence_score=0.86,
    )

    return DecisionCase(
        case_id="CASE-COMP-001-SMOKE",
        asset=asset,
        alert=alert,
        context_note=(
            "High production dependency. Spare part available. Technician available. "
            "Planned intervention window possible within the next shift."
        ),
    )


def test_deterministic_anchor_returns_recommendation() -> None:
    """The deterministic anchor should return a valid recommendation."""

    decision_case = build_smoke_decision_case()
    recommendation = run_deterministic_anchor(decision_case)

    assert isinstance(recommendation, Recommendation)
    assert recommendation.asset_id == "COMP-001"
    assert recommendation.recommendation_id
    assert recommendation.action
    assert recommendation.rationale
    assert recommendation.priority in {"low", "medium", "high", "critical"}


def test_deterministic_anchor_preserves_asset_identity() -> None:
    """The recommendation should preserve the asset identity from the decision case."""

    decision_case = build_smoke_decision_case()
    recommendation = run_deterministic_anchor(decision_case)

    assert recommendation.asset_id == decision_case.asset.asset_id
