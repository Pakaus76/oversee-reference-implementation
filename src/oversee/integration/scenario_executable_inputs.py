"""Executable scenario input utilities for the OVERSEE workbench.

Purpose:
    Convert controlled scenario JSON inputs into the predictive alert request
    consumed by Layer 1.

Architectural role:
    This module belongs to the scenario preparation and integration boundary.
    It validates that every executable scenario contains the minimum structure
    needed to run through the same OVERSEE Layer 1 to Layer 5 path.

Inputs:
    The executable_inputs section of a scenario JSON file.

Outputs:
    A validated predictive alert request and a stable case identifier prefix.
"""

from __future__ import annotations

import copy
import re
from typing import Any

#2.0--------------------------------------------------------------------------------------------------------------------------------->

REQUIRED_EXECUTABLE_INPUT_SECTIONS = {
    "alert",
    "raw_sensor_context",
    "requested_context",
    "enterprise_sources",
}

#2.0--------------------------------------------------------------------------------------------------------------------------------

REQUIRED_ALERT_FIELDS = {
    "alert_id",
    "asset_id",
    "asset_type",
    "line_id",
    "suspected_failure_mode",
    "predictive_horizon_hours",
    "confidence_score",
}

#2.0<--------------------------------------------------------------------------------------------------------------------------------

REQUIRED_RAW_SENSOR_FIELDS = {
    "vibration_mms",
    "temperature_celsius",
    "pressure_bar",
}

REQUIRED_REQUESTED_CONTEXT_FIELDS = {
    "maintenance_history_lookback_days",
    "production_context_horizon_hours",
    "include_inventory_and_resources",
    "include_policy_governance",
}

REQUIRED_ENTERPRISE_SOURCES = {
    "asset_metadata",
    "maintenance_history",
    "operational_context",
    "inventory_and_resources",
    "policy_governance",
}

#2.1--------------------------------------------------------------------------------------------------------------------------------->

def build_alert_request_from_executable_inputs(
    executable_inputs: dict[str, Any],
) -> dict[str, Any]:
    """Build the Layer 1 predictive alert request from executable inputs.
    
    The function extracts the controlled alert payload from a scenario and adds the
    case identifier expected by the Layer 1 pipeline. It is the bridge between
    scenario data and the operational alert intake contract.

    - I separated the alert from the enterprise sources. The alert comes in as a Layer 1 request, 
    while the enterprise sources remain behind the ScenarioBackedEnterpriseApiClient, which simulates the external APIs.
    """

    validate_executable_inputs(executable_inputs)

    return {
        "alert": copy.deepcopy(executable_inputs["alert"]),
        "raw_sensor_context": copy.deepcopy(executable_inputs["raw_sensor_context"]),
        "requested_context": copy.deepcopy(executable_inputs["requested_context"]),
    } # enterprise resources are not included in the alert here.

#2.1<--------------------------------------------------------------------------------------------------------------------------------

def validate_executable_inputs(executable_inputs: dict[str, Any]) -> None:
    """Validate the minimal structure required for executable scenarios.
    
    The validation checks that the scenario can support the all-layers execution:
    alert data, raw sensor context, requested context and enterprise source payloads
    must be present before Layer 1 is allowed to run.
    """

    if not isinstance(executable_inputs, dict):
        raise TypeError("executable_inputs must be a dictionary")

    _require_keys(
        container=executable_inputs,
        required_keys=REQUIRED_EXECUTABLE_INPUT_SECTIONS,
        context_name="executable_inputs",
    )

    _require_mapping(executable_inputs["alert"], "executable_inputs.alert")
    _require_mapping(
        executable_inputs["raw_sensor_context"],
        "executable_inputs.raw_sensor_context",
    )
    _require_mapping(
        executable_inputs["requested_context"],
        "executable_inputs.requested_context",
    )
    _require_mapping(
        executable_inputs["enterprise_sources"],
        "executable_inputs.enterprise_sources",
    )

    _require_keys(
        container=executable_inputs["alert"],
        required_keys=REQUIRED_ALERT_FIELDS,
        context_name="executable_inputs.alert",
    )
    _require_keys(
        container=executable_inputs["raw_sensor_context"],
        required_keys=REQUIRED_RAW_SENSOR_FIELDS,
        context_name="executable_inputs.raw_sensor_context",
    )
    _require_keys(
        container=executable_inputs["requested_context"],
        required_keys=REQUIRED_REQUESTED_CONTEXT_FIELDS,
        context_name="executable_inputs.requested_context",
    )
    _require_keys(
        container=executable_inputs["enterprise_sources"],
        required_keys=REQUIRED_ENTERPRISE_SOURCES,
        context_name="executable_inputs.enterprise_sources",
    )


def build_case_id_prefix_from_scenario_id(scenario_id: str) -> str:
    """Build a stable, readable case ID prefix from a scenario identifier.
    
    The prefix is used to create deterministic case identifiers for scenario-based
    runs, making generated artifacts easier to compare across executions.
    """

    if not scenario_id or not scenario_id.strip():
        raise ValueError("scenario_id cannot be empty")

    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", scenario_id.strip().upper()).strip("_")

    if not cleaned:
        raise ValueError("scenario_id does not contain usable characters")

    return f"SCENARIO_{cleaned}"


def _require_mapping(value: Any, context_name: str) -> None:
    """Require a value to be a dictionary."""

    if not isinstance(value, dict):
        raise TypeError(f"{context_name} must be a dictionary")


def _require_keys(
    *,
    container: dict[str, Any],
    required_keys: set[str],
    context_name: str,
) -> None:
    """Require a dictionary to include a set of keys."""

    missing = sorted(required_keys - set(container))

    if missing:
        raise ValueError(f"{context_name} missing required fields: {', '.join(missing)}")
