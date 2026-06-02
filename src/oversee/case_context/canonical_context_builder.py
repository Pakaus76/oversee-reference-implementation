"""Build canonical compressor case context from external source payloads."""

from __future__ import annotations

from typing import Any

from oversee.case_context.canonical_case_context import (
    CanonicalAssetContext,
    CanonicalCaseContext,
    GovernancePolicyContext,
    MaintenanceResourceContext,
    OperationalContext,
    PredictiveEvidenceContext,
)
from oversee.external_sources import ExternalSourcePackage, ExternalSourcePayload


def build_canonical_case_context(
    source_package: ExternalSourcePackage,
) -> CanonicalCaseContext:
    """Build a Layer 2 canonical context from Layer 1 external payloads."""

    by_source = {payload.source_name: payload for payload in source_package.payloads}

    asset_registry = _require_source(by_source, "asset_registry")
    sensor_historian = _require_source(by_source, "sensor_historian")
    predictive_maintenance = _require_source(by_source, "predictive_maintenance")
    maintenance_history = _require_source(by_source, "maintenance_history")
    production_planning = _require_source(by_source, "production_planning")
    inventory = _require_source(by_source, "inventory_and_resources")
    policy = _require_source(by_source, "policy_governance")

    asset = CanonicalAssetContext(
        asset_id=source_package.asset_id,
        asset_type=_text(asset_registry.normalized_fields, "asset_type", "industrial_air_compressor"),
        line_id=source_package.line_id,
        criticality_label=_text(asset_registry.normalized_fields, "asset_criticality", "high"),
        criticality_score=_integer(asset_registry.normalized_fields, "criticality_score", 5),
        process_role=_optional_text(asset_registry.raw_payload, "process_role"),
    )

    predictive_evidence = PredictiveEvidenceContext(
        alert_type=_text(
            predictive_maintenance.normalized_fields,
            "alert_type",
            "bearing_degradation_or_vibration_anomaly",
        ),
        estimated_time_to_failure_hours=_number(
            predictive_maintenance.normalized_fields,
            "estimated_time_to_failure_hours",
            72.0,
        ),
        confidence_score=_number(
            predictive_maintenance.normalized_fields,
            "confidence_score",
            0.86,
        ),
        alert_severity=_text(
            predictive_maintenance.normalized_fields,
            "alert_severity",
            "high",
        ),
        vibration_trend=_optional_text(sensor_historian.normalized_fields, "vibration_trend"),
        temperature_trend=_optional_text(sensor_historian.normalized_fields, "temperature_trend"),
    )

    operational_context = OperationalContext(
        production_load_pct=_number(
            production_planning.normalized_fields,
            "production_load_pct",
            92.0,
        ),
        next_planned_downtime_hours=_number(
            production_planning.normalized_fields,
            "next_planned_downtime_hours",
            36.0,
        ),
        production_pressure=_text(
            production_planning.normalized_fields,
            "production_pressure",
            "high",
        ),
        business_impact_if_unavailable=_optional_text(
            production_planning.raw_payload,
            "business_impact_if_unavailable",
        ),
    )

    maintenance_resources = MaintenanceResourceContext(
        recent_repeated_failures=_boolean(
            maintenance_history.normalized_fields,
            "recent_repeated_failures",
            True,
        ),
        spare_part_available=_boolean(
            inventory.normalized_fields,
            "spare_part_available",
            True,
        ),
        specialist_technician_available_next_shift=_boolean(
            inventory.normalized_fields,
            "specialist_technician_available_next_shift",
            True,
        ),
        intervention_feasible=_boolean(
            inventory.normalized_fields,
            "intervention_feasible",
            True,
        ),
    )

    computed_human_review_required = _compute_human_review_required(
        asset=asset,
        predictive_evidence=predictive_evidence,
        policy=policy,
    )

    governance_policy = GovernancePolicyContext(
        mandatory_human_review_for_high_criticality=_boolean(
            policy.normalized_fields,
            "mandatory_human_review_for_high_criticality",
            True,
        ),
        expected_human_review_required=_boolean(
            policy.normalized_fields,
            "expected_human_review_required",
            True,
        ),
        computed_human_review_required=computed_human_review_required,
    )

    data_quality_flags = _collect_data_quality_flags(source_package.payloads)
    key_risk_drivers = _build_key_risk_drivers(
        asset=asset,
        predictive_evidence=predictive_evidence,
        operational_context=operational_context,
        maintenance_resources=maintenance_resources,
        governance_policy=governance_policy,
    )

    return CanonicalCaseContext(
        context_id=f"canonical_context_{source_package.case_id}",
        case_id=source_package.case_id,
        asset=asset,
        predictive_evidence=predictive_evidence,
        operational_context=operational_context,
        maintenance_resources=maintenance_resources,
        governance_policy=governance_policy,
        source_payload_count=source_package.source_count,
        source_names=[payload.source_name for payload in source_package.payloads],
        data_quality_flags=data_quality_flags,
        key_risk_drivers=key_risk_drivers,
    )


def _require_source(
    by_source: dict[str, ExternalSourcePayload],
    source_name: str,
) -> ExternalSourcePayload:
    """Return one required source payload."""

    payload = by_source.get(source_name)

    if payload is None:
        raise ValueError(f"Missing required external source payload: {source_name}")

    return payload


def _collect_data_quality_flags(payloads: list[ExternalSourcePayload]) -> list[str]:
    """Collect source-level data quality flags."""

    flags: list[str] = []

    for payload in payloads:
        for flag in payload.data_quality_flags:
            flags.append(f"{payload.source_name}:{flag}")

    return flags


def _build_key_risk_drivers(
    *,
    asset: CanonicalAssetContext,
    predictive_evidence: PredictiveEvidenceContext,
    operational_context: OperationalContext,
    maintenance_resources: MaintenanceResourceContext,
    governance_policy: GovernancePolicyContext,
) -> list[str]:
    """Build a compact list of risk drivers for downstream layers."""

    drivers: list[str] = []

    if asset.criticality_score >= 5:
        drivers.append("high_asset_criticality")
    if predictive_evidence.estimated_time_to_failure_hours <= 72:
        drivers.append("short_failure_horizon")
    if predictive_evidence.confidence_score >= 0.8:
        drivers.append("high_model_confidence")
    if operational_context.production_pressure == "high":
        drivers.append("high_production_pressure")
    if maintenance_resources.recent_repeated_failures:
        drivers.append("recent_repeated_failures")
    if maintenance_resources.intervention_feasible:
        drivers.append("intervention_resources_available")
    if governance_policy.computed_human_review_required:
        drivers.append("human_review_required")

    return drivers


def _compute_human_review_required(
    *,
    asset: CanonicalAssetContext,
    predictive_evidence: PredictiveEvidenceContext,
    policy: ExternalSourcePayload,
) -> bool:
    """Compute whether accountable human review is required."""

    policy_requires_review = _boolean(
        policy.normalized_fields,
        "mandatory_human_review_for_high_criticality",
        True,
    )

    high_criticality = asset.criticality_score >= 5
    high_severity = predictive_evidence.alert_severity.lower() in {"high", "critical"}

    return (policy_requires_review and high_criticality) or high_severity


def _text(source: dict[str, Any], key: str, default: str) -> str:
    """Read a text field with fallback."""

    value = source.get(key)

    if value is None:
        return default

    text = str(value).strip()
    return text or default


def _optional_text(source: dict[str, Any], key: str) -> str | None:
    """Read an optional text field."""

    value = source.get(key)

    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _number(source: dict[str, Any], key: str, default: float) -> float:
    """Read a numeric field with fallback."""

    value = source.get(key)

    if value is None:
        return float(default)

    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _integer(source: dict[str, Any], key: str, default: int) -> int:
    """Read an integer field with fallback."""

    return int(_number(source, key, float(default)))


def _boolean(source: dict[str, Any], key: str, default: bool) -> bool:
    """Read a boolean field with fallback."""

    value = source.get(key)

    if value is None:
        return bool(default)

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "y"}

    return bool(value)
