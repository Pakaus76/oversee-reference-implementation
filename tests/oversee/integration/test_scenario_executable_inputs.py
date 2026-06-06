"""Tests for executable scenario input builders."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from oversee.integration.predictive_alert_api import receive_predictive_alert
from oversee.integration.scenario_executable_inputs import (
    build_alert_request_from_executable_inputs,
    build_case_id_prefix_from_scenario_id,
    validate_executable_inputs,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCENARIO_DIR = PROJECT_ROOT / "demo" / "interactive_walkthrough" / "scenarios"


def _load_scenario(filename: str) -> dict[str, object]:
    """Load one walkthrough scenario from disk."""

    return json.loads((SCENARIO_DIR / filename).read_text(encoding="utf-8-sig"))


@pytest.mark.parametrize(
    "filename",
    [
        "comp_001_default.json",
        "comp_002_lower_urgency.json",
        "pump_001_resource_constrained.json",
    ],
)
def test_scenario_executable_inputs_build_valid_layer1_alert_request(
    filename: str,
) -> None:
    """All current executable scenarios should build valid Layer 1 requests."""

    scenario = _load_scenario(filename)
    executable_inputs = scenario["executable_inputs"]

    alert_request = build_alert_request_from_executable_inputs(executable_inputs)
    receipt = receive_predictive_alert(alert_request)

    assert receipt.accepted is True
    assert receipt.validation_errors == []
    assert alert_request["alert"]["asset_id"] == scenario["asset_id"]
    assert alert_request["alert"]["asset_type"] == scenario["asset_type"]
    assert alert_request["alert"]["suspected_failure_mode"] == scenario["failure_mode"]


def test_builder_returns_defensive_copy() -> None:
    """Mutating a built request should not mutate the original scenario dictionary."""

    scenario = _load_scenario("comp_002_lower_urgency.json")
    executable_inputs = scenario["executable_inputs"]

    alert_request = build_alert_request_from_executable_inputs(executable_inputs)
    alert_request["alert"]["asset_id"] = "CHANGED"

    assert executable_inputs["alert"]["asset_id"] == "COMP-002"


def test_validate_executable_inputs_rejects_missing_section() -> None:
    """Invalid executable inputs should fail with a clear validation error."""

    with pytest.raises(ValueError, match="missing required fields"):
        validate_executable_inputs({"alert": {}})


def test_build_case_id_prefix_from_scenario_id() -> None:
    """Scenario IDs should produce stable case ID prefixes."""

    assert build_case_id_prefix_from_scenario_id("COMP-001") == "SCENARIO_COMP_001"
    assert build_case_id_prefix_from_scenario_id("pump 001") == "SCENARIO_PUMP_001"

    with pytest.raises(ValueError, match="scenario_id cannot be empty"):
        build_case_id_prefix_from_scenario_id("")