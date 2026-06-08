"""
Digital Factory adapter for the OVERSEE live generative path.

This module translates Digital Factory OVERSEE input candidates into the
typed DecisionCase contract already used by deterministic anchor, then delegates execution
to the existing live generative path implementation.

The adapter is intentionally narrow:
- it does not modify live generative path;
- it does not modify model-backed anchor, grounded model path, or deterministic anchor;
- it does not modify prompts;
- it does not modify retrieval or model provider infrastructure;
- it does not expand Digital Factory scenarios.

It only provides a traceable Digital Factory-facing wrapper around the existing
live generative path input contract.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from oversee.live_generative_path import run_live_generative_path

from oversee.digital_factory.deterministic_anchor_adapter import (
    build_decision_case_from_candidate,
)


ADAPTER_NAME = "digital_factory_live_generative_path_adapter"
ADAPTER_VERSION = "0.1.0"

FALLBACK_MARKERS = (
    "live generative path fell back to the grounded model path",
    "fell back to the grounded model path",
    "fallback to grounded model path",
)

MODEL_PROVIDER_RESPONSE_ID_MARKER = "model response id:"
EVIDENCE_REFERENCE_MARKERS = ("[g1]", "[g2]", "[g3]")
PRIORITY_GOVERNANCE_MARKER = "priority governance:"


@dataclass(frozen=True)
class DigitalFactoryLiveGenerativePathResult:
    """live generative path result for one Digital Factory candidate."""

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
    fallback_detected: bool
    fallback_anchor: str | None
    model_response_id_present: bool
    evidence_reference_detected: bool
    priority_governance_detected: bool
    live_generative_path_invoked: bool
    adapter_metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


def detect_live_generative_path_fallback(rationale: str) -> bool:
    """
    Detect whether the returned live generative path rationale indicates fallback.

    Args:
        rationale: Recommendation rationale returned by live generative path.

    Returns:
        bool: True when a known live-generative-path-to-E fallback marker is present.
    """
    normalized_rationale = rationale.lower()
    return any(marker in normalized_rationale for marker in FALLBACK_MARKERS)


def detect_model_response_id(rationale: str) -> bool:
    """
    Detect whether the final rationale exposes a provider response id marker.
    """
    return MODEL_PROVIDER_RESPONSE_ID_MARKER in rationale.lower()


def detect_evidence_reference(rationale: str) -> bool:
    """
    Detect whether the final rationale references known bounded evidence snippets.
    """
    normalized_rationale = rationale.lower()
    return any(marker in normalized_rationale for marker in EVIDENCE_REFERENCE_MARKERS)


def detect_priority_governance(rationale: str) -> bool:
    """
    Detect whether the final rationale exposes live generative path priority governance.
    """
    return PRIORITY_GOVERNANCE_MARKER in rationale.lower()


def evaluate_live_generative_path_candidate(candidate: dict[str, Any]) -> DigitalFactoryLiveGenerativePathResult:
    """
    Evaluate one Digital Factory candidate through the existing live generative path.

    The candidate-to-DecisionCase translation is reused from the tested
    deterministic anchor adapter because live generative path also receives a DecisionCase.

    Args:
        candidate: Digital Factory OVERSEE input candidate.

    Returns:
        DigitalFactoryLiveGenerativePathResult: Traceable adapter-level result.
    """
    decision_case, normalized_criticality, predicted_issue_source = (
        build_decision_case_from_candidate(candidate)
    )

    recommendation = run_live_generative_path(decision_case)
    expected_decision = candidate["expected_decision"]

    fallback_detected = detect_live_generative_path_fallback(recommendation.rationale)

    return DigitalFactoryLiveGenerativePathResult(
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
        fallback_detected=fallback_detected,
        fallback_anchor="grounded_model_path" if fallback_detected else None,
        model_response_id_present=detect_model_response_id(recommendation.rationale),
        evidence_reference_detected=detect_evidence_reference(recommendation.rationale),
        priority_governance_detected=detect_priority_governance(recommendation.rationale),
        live_generative_path_invoked=True,
        adapter_metadata={
            "adapter_name": ADAPTER_NAME,
            "adapter_version": ADAPTER_VERSION,
            "uses_existing_live_generative_path": True,
            "reuses_deterministic_anchor_candidate_mapping": True,
            "live_generative_path_adapter_invoked": True,
            "live_generative_path_modified": False,
            "grounded_model_path_modified": False,
            "model_backed_anchor_modified": False,
            "deterministic_anchor_modified": False,
            "prompt_modified": False,
            "retrieval_modified": False,
            "model_client_modified": False,
            "live_model_call_observable_from_adapter": False,
            "fallback_detection_markers": FALLBACK_MARKERS,
        },
    )


def evaluate_live_generative_path_candidates(
    candidates: list[dict[str, Any]],
) -> list[DigitalFactoryLiveGenerativePathResult]:
    """Evaluate multiple Digital Factory candidates through live generative path."""
    return [evaluate_live_generative_path_candidate(candidate) for candidate in candidates]




