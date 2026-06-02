"""
Deterministic deterministic anchor adapter for Digital Factory input candidates.

This module translates Digital Factory OVERSEE input candidates into the
typed OVERSEE domain contracts required by deterministic anchor.

The adapter is intentionally narrow:
- no generative AI;
- no deterministic anchor modification;
- no live generative path modification;
- no prompt modification;
- no Digital Factory scenario expansion.

It exists to evaluate the already implemented deterministic deterministic anchor policy
against the current Digital Factory candidate JSON.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from oversee.deterministic_anchor import run_deterministic_anchor
from oversee.domain import (
    Asset,
    DecisionCase,
    PredictiveAlert,
    validate_decision_case,
)


ADAPTER_NAME = "digital_factory_deterministic_anchor_adapter"
ADAPTER_VERSION = "0.1.0"

CRITICALITY_LABEL_TO_INT: dict[str, int] = {
    "low": 1,
    "medium": 3,
    "high": 5,
}


@dataclass(frozen=True)
class DigitalFactoryDeterministicAnchorResult:
    """Deterministic deterministic anchor result for one Digital Factory candidate."""

    candidate_id: str
    source_case_id: str
    recommendation_id: str
    asset_id: str
    priority: str
    action: str
    rationale: str
    expected_decision_posture: str
    expected_human_review_required: bool
    normalized_criticality: int
    predicted_issue_source: str
    deterministic_anchor_invoked: bool
    adapter_metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


def _normalize_criticality(raw_criticality: Any) -> int:
    """Convert Digital Factory criticality labels into Asset criticality integers."""
    if isinstance(raw_criticality, bool):
        raise ValueError("criticality must not be a boolean value.")

    if isinstance(raw_criticality, int):
        if raw_criticality < 0:
            raise ValueError("criticality must be zero or positive.")
        return raw_criticality

    if isinstance(raw_criticality, str):
        normalized = raw_criticality.strip().lower()
        if normalized in CRITICALITY_LABEL_TO_INT:
            return CRITICALITY_LABEL_TO_INT[normalized]

    raise ValueError(f"Unsupported criticality value: {raw_criticality!r}")


def _derive_predicted_issue(alert_candidate: dict[str, Any]) -> tuple[str, str]:
    """Derive the required PredictiveAlert.predicted_issue field."""
    failure_mode = alert_candidate.get("failure_mode")
    if isinstance(failure_mode, str) and failure_mode.strip():
        return failure_mode.strip(), "failure_mode"

    alert_type = alert_candidate.get("alert_type")
    if isinstance(alert_type, str) and alert_type.strip():
        return alert_type.strip(), "alert_type_fallback"

    raise ValueError(
        "Cannot derive predicted_issue: both failure_mode and alert_type are empty."
    )


def _build_context_note(candidate: dict[str, Any]) -> str:
    """Build a compact traceability note without using expected decision labels."""
    case_candidate = candidate["decision_case_candidate"]
    operational_context = case_candidate.get("operational_context", {})
    maintenance_context = case_candidate.get("maintenance_context", {})
    uncertainty_context = case_candidate.get("uncertainty_context", {})
    narrative_context = case_candidate.get("narrative_context", {})

    note_parts = [
        f"scenario_family={case_candidate.get('scenario_family')}",
        f"production_pressure={operational_context.get('production_pressure')}",
        f"downtime_window={operational_context.get('downtime_window')}",
        f"spare_part_status={maintenance_context.get('spare_part_status')}",
        f"technician_available={maintenance_context.get('technician_available')}",
        f"data_quality={uncertainty_context.get('data_quality')}",
        f"diagnosis_clarity={uncertainty_context.get('diagnosis_clarity')}",
        f"technician_note={narrative_context.get('technician_note')}",
    ]

    return "; ".join(str(part) for part in note_parts)


def build_decision_case_from_candidate(candidate: dict[str, Any]) -> tuple[DecisionCase, int, str]:
    """
    Translate one Digital Factory candidate dictionary into a typed DecisionCase.

    Returns:
        tuple: DecisionCase, normalized criticality, predicted issue source.
    """
    asset_candidate = candidate["asset_candidate"]
    alert_candidate = candidate["predictive_alert_candidate"]
    case_candidate = candidate["decision_case_candidate"]

    asset_id = asset_candidate["asset_id"]
    case_asset_id = case_candidate["asset_id"]

    if asset_id != case_asset_id:
        raise ValueError(
            "Asset identity mismatch between asset_candidate and decision_case_candidate."
        )

    normalized_criticality = _normalize_criticality(asset_candidate["criticality"])
    predicted_issue, predicted_issue_source = _derive_predicted_issue(alert_candidate)

    asset = Asset(
        asset_id=asset_id,
        asset_type=asset_candidate["asset_type"],
        criticality=normalized_criticality,
        location=asset_candidate.get("location"),
    )

    alert = PredictiveAlert(
        alert_id=alert_candidate["alert_id"],
        asset_id=case_asset_id,
        predicted_issue=predicted_issue,
        time_to_failure_hours=alert_candidate.get("time_to_failure_hours"),
        confidence_score=alert_candidate.get("confidence_score"),
    )

    decision_case = DecisionCase(
        case_id=case_candidate["case_id"],
        asset=asset,
        alert=alert,
        context_note=_build_context_note(candidate),
    )

    validate_decision_case(decision_case)

    return decision_case, normalized_criticality, predicted_issue_source


def evaluate_deterministic_anchor_candidate(candidate: dict[str, Any]) -> DigitalFactoryDeterministicAnchorResult:
    """Evaluate one Digital Factory candidate through deterministic deterministic anchor."""
    decision_case, normalized_criticality, predicted_issue_source = (
        build_decision_case_from_candidate(candidate)
    )

    recommendation = run_deterministic_anchor(decision_case)
    expected_decision = candidate["expected_decision"]

    return DigitalFactoryDeterministicAnchorResult(
        candidate_id=candidate["candidate_id"],
        source_case_id=candidate["source_case_id"],
        recommendation_id=recommendation.recommendation_id,
        asset_id=recommendation.asset_id,
        priority=recommendation.priority,
        action=recommendation.action,
        rationale=recommendation.rationale,
        expected_decision_posture=expected_decision["expected_decision_posture"],
        expected_human_review_required=expected_decision[
            "expected_human_review_required"
        ],
        normalized_criticality=normalized_criticality,
        predicted_issue_source=predicted_issue_source,
        deterministic_anchor_invoked=True,
        adapter_metadata={
            "adapter_name": ADAPTER_NAME,
            "adapter_version": ADAPTER_VERSION,
            "deterministic": True,
            "uses_generative_ai": False,
            "deterministic_anchor_adapter_invoked": True,
            "deterministic_anchor_modified": False,
            "live_generative_path_modified": False,
            "prompt_modified": False,
            "criticality_mapping": CRITICALITY_LABEL_TO_INT,
            "predicted_issue_fallback_allowed": True,
        },
    )


def evaluate_deterministic_anchor_candidates(
    candidates: list[dict[str, Any]],
) -> list[DigitalFactoryDeterministicAnchorResult]:
    """Evaluate multiple Digital Factory candidates through deterministic deterministic anchor."""
    return [evaluate_deterministic_anchor_candidate(candidate) for candidate in candidates]



