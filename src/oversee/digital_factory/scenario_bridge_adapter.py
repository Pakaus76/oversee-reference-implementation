"""
Bridge-ready adapter for Digital Factory synthetic scenarios.

This module converts validated Digital Factory synthetic scenarios into a
stable bridge-ready evaluation payload. It does not invoke the Decision
oversee yet.

Purpose:
- keep Digital Factory generation separate from OVERSEE execution;
- prepare a clean payload shape for later bridge/OVERSEE evaluation;
- preserve expected decision information for evaluation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from oversee.digital_factory.synthetic_scenario_loader import (
    load_synthetic_scenarios,
)


ADAPTER_NAME = "digital_factory_synthetic_scenario_bridge_adapter"
ADAPTER_VERSION = "0.1.0"


@dataclass(frozen=True)
class BridgeReadyScenarioPayload:
    """Bridge-ready representation of one synthetic scenario."""

    payload_id: str
    source_case_id: str
    scenario_family: str
    asset: dict[str, Any]
    evidence: dict[str, Any]
    context: dict[str, Any]
    narrative: dict[str, Any]
    expected_decision: dict[str, Any]
    generation_metadata: dict[str, Any]
    adapter_metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        return asdict(self)


def build_bridge_ready_payload(scenario: dict[str, Any]) -> BridgeReadyScenarioPayload:
    """
    Build one bridge-ready payload from a validated synthetic scenario.

    The payload keeps enough information for future OVERSEE evaluation
    without calling the oversee here.
    """
    case_id = scenario["case_id"]
    generation_metadata = scenario["generation_metadata"]

    return BridgeReadyScenarioPayload(
        payload_id=f"BRIDGE_READY_{case_id}",
        source_case_id=case_id,
        scenario_family=scenario["scenario_family"],
        asset=scenario["asset_context"],
        evidence={
            "sensor_evidence": scenario["sensor_evidence"],
            "predictive_alert": scenario["predictive_alert"],
        },
        context={
            "operational_context": scenario["operational_context"],
            "maintenance_context": scenario["maintenance_context"],
            "uncertainty_context": scenario["uncertainty_context"],
        },
        narrative=scenario["narrative_context"],
        expected_decision=scenario["expected_decision"],
        generation_metadata=generation_metadata,
        adapter_metadata={
            "adapter_name": ADAPTER_NAME,
            "adapter_version": ADAPTER_VERSION,
            "source_generator": generation_metadata["generator_name"],
            "source_generator_version": generation_metadata["generator_version"],
            "oversee_invoked": False,
            "bridge_ready": True,
        },
    )


def build_bridge_ready_payloads(scenarios: list[dict[str, Any]]) -> list[BridgeReadyScenarioPayload]:
    """Build bridge-ready payloads from validated synthetic scenarios."""
    return [build_bridge_ready_payload(scenario) for scenario in scenarios]


def load_bridge_ready_payloads(path: Path) -> list[BridgeReadyScenarioPayload]:
    """Load synthetic scenarios from JSON and return bridge-ready payloads."""
    scenarios = load_synthetic_scenarios(path)
    return build_bridge_ready_payloads(scenarios)


