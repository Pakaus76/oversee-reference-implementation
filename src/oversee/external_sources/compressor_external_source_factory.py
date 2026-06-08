"""Build external source payloads for the compressor case.

The Digital Factory remains the synthetic origin of the case, but this module
exposes the information as if it had been obtained from separate industrial
systems: asset registry, historian, predictive maintenance, maintenance history,
production planning, inventory and governance policy.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from oversee.digital_factory import generate_compressor_scenarios
from oversee.external_sources.external_source_contracts import (
    ExternalSourcePackage,
    ExternalSourcePayload,
)


def build_compressor_external_source_package(
    source_case_id: str | None = None,
) -> ExternalSourcePackage:
    """Build Layer 1 external source payloads for one compressor case."""

    scenario = _select_scenario(source_case_id=source_case_id)
    scenario_dict = _to_dict(scenario)

    case_id = _extract_text(
        scenario_dict,
        "case_id",
        "source_case_id",
        "scenario_id",
        default="DF_COMPRESSOR_CASE",
    )
    asset_id = _extract_text(
        scenario_dict,
        "asset_id",
        "protected_facts.asset_id",
        "asset.asset_id",
        default="COMP-001",
    )
    line_id = _extract_optional_text(
        scenario_dict,
        "line_id",
        "protected_facts.line_id",
        "asset.line_id",
        "industrial_context.line_id",
    ) or "PKG-LINE-01"
    created_at = _utc_now()

    payloads = [
        _asset_registry_payload(scenario_dict, case_id, asset_id, line_id, created_at),
        _sensor_historian_payload(scenario_dict, case_id, asset_id, line_id, created_at),
        _predictive_maintenance_payload(scenario_dict, case_id, asset_id, line_id, created_at),
        _maintenance_history_payload(scenario_dict, case_id, asset_id, line_id, created_at),
        _production_planning_payload(scenario_dict, case_id, asset_id, line_id, created_at),
        _inventory_payload(scenario_dict, case_id, asset_id, line_id, created_at),
        _policy_payload(scenario_dict, case_id, asset_id, line_id, created_at),
    ]

    return ExternalSourcePackage(
        package_id=f"external_sources_{case_id}",
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        created_at=created_at,
        payloads=payloads,
    )


def _select_scenario(source_case_id: str | None) -> Any:
    """Select one Digital Factory scenario by case id or return the first one."""

    scenarios = generate_compressor_scenarios()

    if not scenarios:
        raise ValueError("Digital Factory did not generate any compressor scenarios.")

    if source_case_id is None:
        return scenarios[0]

    for scenario in scenarios:
        scenario_dict = _to_dict(scenario)
        candidate_ids = {
            str(scenario_dict.get("case_id", "")),
            str(scenario_dict.get("source_case_id", "")),
            str(scenario_dict.get("scenario_id", "")),
        }
        if source_case_id in candidate_ids:
            return scenario

    available = [_to_dict(scenario).get("case_id") for scenario in scenarios]
    raise ValueError(
        f"Requested source_case_id '{source_case_id}' was not found. "
        f"Available case ids: {available}"
    )


def _asset_registry_payload(
    scenario: dict[str, Any],
    case_id: str,
    asset_id: str,
    line_id: str | None,
    generated_at: str,
) -> ExternalSourcePayload:
    """Build the simulated Asset Registry response."""

    asset_criticality = _extract_text(
        scenario,
        "asset_criticality",
        "protected_facts.asset_criticality",
        "expected_decision_behavior.expected_priority",
        default="high",
    )

    raw_payload = {
        "asset_id": asset_id,
        "asset_name": _extract_optional_text(scenario, "asset_name"),
        "asset_type": _extract_text(scenario, "asset_type", default="industrial_air_compressor"),
        "line_id": line_id,
        "site_id": _extract_optional_text(scenario, "site_id"),
        "criticality": asset_criticality,
        "process_role": _extract_optional_text(scenario, "industrial_context.process_role"),
        "operational_dependency": _extract_optional_text(
            scenario,
            "industrial_context.operational_dependency",
        ),
    }

    return _payload(
        source_name="asset_registry",
        source_system="enterprise_asset_registry",
        source_type="master_data",
        endpoint=f"GET /assets/{asset_id}",
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields={
            "asset_id": asset_id,
            "line_id": line_id,
            "asset_type": raw_payload["asset_type"],
            "asset_criticality": asset_criticality,
            "criticality_score": _criticality_score(asset_criticality),
        },
    )


def _sensor_historian_payload(
    scenario: dict[str, Any],
    case_id: str,
    asset_id: str,
    line_id: str | None,
    generated_at: str,
) -> ExternalSourcePayload:
    """Build the simulated sensor historian response."""

    severity = _extract_text(
        scenario,
        "predictive_alert.severity",
        "severity",
        default="high",
    )

    raw_payload = {
        "asset_id": asset_id,
        "window_hours": 24,
        "vibration_trend": _extract_text(scenario, "sensor_summary.vibration_trend", default="increasing"),
        "temperature_trend": _extract_text(scenario, "sensor_summary.temperature_trend", default="stable"),
        "severity": severity,
        "source_note": "Digital Factory generated sensor summary.",
    }

    return _payload(
        source_name="sensor_historian",
        source_system="industrial_data_historian",
        source_type="time_series_summary",
        endpoint=f"GET /historian/assets/{asset_id}/windows/latest",
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields={
            "vibration_trend": raw_payload["vibration_trend"],
            "temperature_trend": raw_payload["temperature_trend"],
            "sensor_severity": severity,
        },
    )


def _predictive_maintenance_payload(
    scenario: dict[str, Any],
    case_id: str,
    asset_id: str,
    line_id: str | None,
    generated_at: str,
) -> ExternalSourcePayload:
    """Build the simulated predictive maintenance alert response."""

    time_to_failure = _extract_number(
        scenario,
        "estimated_time_to_failure_hours",
        "predictive_alert.estimated_time_to_failure_hours",
        "protected_facts.estimated_time_to_failure_hours",
        "alert_row.estimated_rul_hours",
        default=72.0,
    )
    confidence = _extract_number(
        scenario,
        "confidence_score",
        "predictive_alert.confidence_score",
        "protected_facts.confidence_score",
        "alert_row.confidence_score",
        default=0.86,
    )
    alert_type = _extract_text(
        scenario,
        "predictive_alert.alert_type",
        "alert_type",
        default="bearing_degradation_or_vibration_anomaly",
    )

    raw_payload = {
        "alert_id": _extract_text(
            scenario,
            "predictive_alert.alert_id",
            default=f"ALERT-{asset_id}-{case_id}",
        ),
        "asset_id": asset_id,
        "alert_type": alert_type,
        "estimated_time_to_failure_hours": time_to_failure,
        "confidence_score": confidence,
        "severity": _extract_text(scenario, "predictive_alert.severity", default="high"),
        "model_name": _extract_optional_text(scenario, "predictive_alert.model_name"),
        "model_version": _extract_optional_text(scenario, "predictive_alert.model_version"),
    }

    return _payload(
        source_name="predictive_maintenance",
        source_system="predictive_maintenance_service",
        source_type="predictive_alert",
        endpoint=f"GET /predictive-alerts/assets/{asset_id}/latest",
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields={
            "alert_type": alert_type,
            "estimated_time_to_failure_hours": time_to_failure,
            "confidence_score": confidence,
            "alert_severity": raw_payload["severity"],
        },
    )


def _maintenance_history_payload(
    scenario: dict[str, Any],
    case_id: str,
    asset_id: str,
    line_id: str | None,
    generated_at: str,
) -> ExternalSourcePayload:
    """Build the simulated maintenance history response."""

    repeated_failures = _extract_bool(
        scenario,
        "expected_operational_situation.recent_repeated_failures",
        "recent_repeated_failures",
        default=True,
    )

    raw_payload = {
        "asset_id": asset_id,
        "lookback_days": 90,
        "recent_repeated_failures": repeated_failures,
        "last_intervention_type": _extract_text(scenario, "maintenance_history.last_intervention_type", default="inspection"),
        "source_note": "Digital Factory generated maintenance history summary.",
    }

    return _payload(
        source_name="maintenance_history",
        source_system="cmms_maintenance_history",
        source_type="maintenance_history_summary",
        endpoint=f"GET /maintenance-history/assets/{asset_id}?lookback_days=90",
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields={
            "recent_repeated_failures": repeated_failures,
            "lookback_days": 90,
        },
    )


def _production_planning_payload(
    scenario: dict[str, Any],
    case_id: str,
    asset_id: str,
    line_id: str | None,
    generated_at: str,
) -> ExternalSourcePayload:
    """Build the simulated production planning response."""

    production_load = _extract_number(
        scenario,
        "expected_operational_situation.production_load_pct",
        "production_load_pct",
        default=92.0,
    )
    downtime_window = _extract_number(
        scenario,
        "expected_operational_situation.next_planned_downtime_hours",
        "next_planned_downtime_hours",
        default=36.0,
    )

    raw_payload = {
        "line_id": line_id,
        "asset_id": asset_id,
        "production_load_pct": production_load,
        "next_planned_downtime_hours": downtime_window,
        "business_impact_if_unavailable": _extract_optional_text(
            scenario,
            "industrial_context.business_impact_if_unavailable",
        ),
    }

    return _payload(
        source_name="production_planning",
        source_system="production_planning_system",
        source_type="operational_context",
        endpoint=f"GET /production-plan/lines/{line_id or 'unknown_line'}/latest",
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields={
            "production_load_pct": production_load,
            "next_planned_downtime_hours": downtime_window,
            "production_pressure": _production_pressure(production_load),
        },
    )


def _inventory_payload(
    scenario: dict[str, Any],
    case_id: str,
    asset_id: str,
    line_id: str | None,
    generated_at: str,
) -> ExternalSourcePayload:
    """Build the simulated inventory and resource response."""

    spare_part_available = _extract_bool(
        scenario,
        "expected_operational_situation.spare_part_available",
        "spare_part_available",
        default=True,
    )
    technician_available = _extract_bool(
        scenario,
        "expected_operational_situation.specialist_technician_available_next_shift",
        "specialist_technician_available_next_shift",
        default=True,
    )

    raw_payload = {
        "asset_id": asset_id,
        "spare_part_available": spare_part_available,
        "specialist_technician_available_next_shift": technician_available,
    }

    return _payload(
        source_name="inventory_and_resources",
        source_system="inventory_and_workforce_system",
        source_type="resource_availability",
        endpoint=f"GET /inventory/assets/{asset_id}/availability",
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields={
            "spare_part_available": spare_part_available,
            "specialist_technician_available_next_shift": technician_available,
            "intervention_feasible": spare_part_available and technician_available,
        },
    )


def _policy_payload(
    scenario: dict[str, Any],
    case_id: str,
    asset_id: str,
    line_id: str | None,
    generated_at: str,
) -> ExternalSourcePayload:
    """Build the simulated policy and governance response."""

    expected_human_review = _extract_bool(
        scenario,
        "expected_decision_behavior.human_review_required",
        "human_review_required",
        default=True,
    )

    raw_payload = {
        "asset_id": asset_id,
        "mandatory_human_review_for_high_criticality": True,
        "expected_human_review_required": expected_human_review,
        "policy_basis": "High-criticality maintenance decisions require accountable human review.",
    }

    return _payload(
        source_name="policy_governance",
        source_system="maintenance_governance_policy_service",
        source_type="policy_constraints",
        endpoint=f"GET /policies/assets/{asset_id}/maintenance-decision",
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields={
            "mandatory_human_review_for_high_criticality": True,
            "expected_human_review_required": expected_human_review,
        },
    )


def _payload(
    *,
    source_name: str,
    source_system: str,
    source_type: str,
    endpoint: str,
    generated_at: str,
    case_id: str,
    asset_id: str,
    line_id: str | None,
    raw_payload: dict[str, Any],
    normalized_fields: dict[str, Any],
) -> ExternalSourcePayload:
    """Create one external source payload with basic data-quality flags."""

    flags: list[str] = []

    if asset_id in {"", "unknown_asset"}:
        flags.append("missing_asset_id")
    if line_id is None:
        flags.append("missing_line_id")

    return ExternalSourcePayload(
        source_name=source_name,
        source_system=source_system,
        source_type=source_type,
        endpoint=endpoint,
        generated_at=generated_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields=normalized_fields,
        data_quality_flags=flags,
    )


def _to_dict(value: Any) -> dict[str, Any]:
    """Convert a Digital Factory scenario object to a dictionary."""

    if isinstance(value, dict):
        return value

    if hasattr(value, "to_dict") and callable(value.to_dict):
        result = value.to_dict()
        if isinstance(result, dict):
            return result

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    raise TypeError(f"Cannot convert scenario object to dict: {type(value)!r}")


def _utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


def _extract_optional_text(source: dict[str, Any], *paths: str) -> str | None:
    """Extract an optional text value from nested dictionaries."""

    value = _first_present(source, *paths)
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _extract_text(source: dict[str, Any], *paths: str, default: str) -> str:
    """Extract a text value from nested dictionaries."""

    value = _first_present(source, *paths)
    if value is None:
        return default

    text = str(value).strip()
    return text or default


def _extract_number(source: dict[str, Any], *paths: str, default: float) -> float:
    """Extract a numeric value from nested dictionaries."""

    value = _first_present(source, *paths)

    if value is None:
        return float(default)

    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _extract_bool(source: dict[str, Any], *paths: str, default: bool) -> bool:
    """Extract a boolean value from nested dictionaries."""

    value = _first_present(source, *paths)

    if value is None:
        return bool(default)

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "y"}

    return bool(value)


def _first_present(source: dict[str, Any], *paths: str) -> Any:
    """Return the first non-empty value found in a dictionary."""

    for path in paths:
        value = _get_path(source, path)

        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue

        return value

    return None


def _get_path(source: dict[str, Any], path: str) -> Any:
    """Read a dotted path from a dictionary."""

    current: Any = source

    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)

    return current


def _criticality_score(value: Any) -> int:
    """Map criticality labels to a simple numeric score."""

    text = str(value).strip().lower()

    if text in {"critical", "very_high", "very high"}:
        return 5
    if text == "high":
        return 5
    if text == "medium":
        return 3
    if text == "low":
        return 1

    try:
        return int(float(text))
    except ValueError:
        return 3


def _production_pressure(production_load_pct: float) -> str:
    """Classify production pressure from load percentage."""

    if production_load_pct >= 90:
        return "high"
    if production_load_pct >= 70:
        return "medium"
    return "low"

