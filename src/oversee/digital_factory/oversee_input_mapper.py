"""
Read-only mapper from Digital Factory payloads to OVERSEE input candidates.

This module prepares candidate input dictionaries for a future controlled
OVERSEE evaluation runner.

It intentionally does not:
- import or modify deterministic anchor;
- import or modify live generative path;
- invoke the OVERSEE;
- call generative AI;
- modify priority logic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


MAPPER_NAME = "digital_factory_read_only_oversee_mapper"
MAPPER_VERSION = "0.1.0"

TARGET_CONTRACTS = {
    "asset_contract": "Asset",
    "alert_contract": "PredictiveAlert",
    "case_contract": "DecisionCase",
}


@dataclass(frozen=True)
class OverseeInputCandidate:
    """Read-only candidate input for a future OVERSEE evaluation."""

    candidate_id: str
    source_payload_id: str
    source_case_id: str
    target_contracts: dict[str, str]
    asset_candidate: dict[str, Any]
    predictive_alert_candidate: dict[str, Any]
    decision_case_candidate: dict[str, Any]
    expected_decision: dict[str, Any]
    mapping_metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


def map_bridge_ready_payload_to_oversee_input(
    payload: dict[str, Any],
) -> OverseeInputCandidate:
    """
    Map one bridge-ready Digital Factory payload into a read-only OVERSEE input candidate.

    The mapping preserves source traceability and expected decision labels for later evaluation.
    """
    asset = payload["asset"]
    evidence = payload["evidence"]
    context = payload["context"]
    expected_decision = payload["expected_decision"]
    generation_metadata = payload["generation_metadata"]
    adapter_metadata = payload["adapter_metadata"]

    sensor_evidence = evidence["sensor_evidence"]
    predictive_alert = evidence["predictive_alert"]

    asset_candidate = {
        "asset_id": asset.get("asset_id"),
        "asset_name": asset.get("asset_name"),
        "asset_type": asset.get("asset_type"),
        "criticality": asset.get("criticality"),
        "location": asset.get("location"),
        "source_section": "asset",
    }

    alert_id = predictive_alert.get("alert_id") or f"ALERT_{payload['source_case_id']}"

    predictive_alert_candidate = {
        "alert_id": alert_id,
        "alert_type": predictive_alert.get("alert_type"),
        "failure_mode": predictive_alert.get("failure_mode"),
        "time_to_failure_hours": predictive_alert.get("time_to_failure_hours"),
        "confidence_score": predictive_alert.get("confidence_score"),
        "sensor_evidence": sensor_evidence,
        "source_section": "evidence",
        "alert_id_source": (
            "predictive_alert.alert_id"
            if predictive_alert.get("alert_id")
            else "derived_from_source_case_id"
        ),
    }

    decision_case_candidate = {
        "case_id": payload["source_case_id"],
        "scenario_family": payload["scenario_family"],
        "asset_id": asset_candidate["asset_id"],
        "alert_id": predictive_alert_candidate["alert_id"],
        "operational_context": context["operational_context"],
        "maintenance_context": context["maintenance_context"],
        "uncertainty_context": context["uncertainty_context"],
        "narrative_context": payload["narrative"],
        "expected_decision_posture": expected_decision["expected_decision_posture"],
        "expected_review_focus": expected_decision["expected_review_focus"],
        "expected_human_review_required": expected_decision["expected_human_review_required"],
        "source_section": "assembled_candidate",
    }

    return OverseeInputCandidate(
        candidate_id=f"OVERSEE_INPUT_{payload['source_case_id']}",
        source_payload_id=payload["payload_id"],
        source_case_id=payload["source_case_id"],
        target_contracts=dict(TARGET_CONTRACTS),
        asset_candidate=asset_candidate,
        predictive_alert_candidate=predictive_alert_candidate,
        decision_case_candidate=decision_case_candidate,
        expected_decision=expected_decision,
        mapping_metadata={
            "mapper_name": MAPPER_NAME,
            "mapper_version": MAPPER_VERSION,
            "source_adapter_name": adapter_metadata.get("adapter_name"),
            "source_adapter_version": adapter_metadata.get("adapter_version"),
            "source_generator": generation_metadata.get("generator_name"),
            "source_generator_version": generation_metadata.get("generator_version"),
            "read_only_mapping": True,
            "oversee_invoked": False,
            "uses_generative_ai": False,
            "deterministic_anchor_modified": False,
            "live_generative_path_modified": False,
        },
    )


def map_bridge_ready_payloads_to_oversee_inputs(
    payloads: list[dict[str, Any]],
) -> list[OverseeInputCandidate]:
    """Map bridge-ready payloads into read-only OVERSEE input candidates."""
    return [
        map_bridge_ready_payload_to_oversee_input(payload)
        for payload in payloads
    ]



