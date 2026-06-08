"""Layer 1 evidence intake, aggregation and validation pipeline.

Purpose:
    Receive the predictive alert, retrieve the required scenario-backed
    enterprise evidence, harmonize source payloads and validate the resulting
    evidence package.

Architectural role:
    Layer 1 is the only implemented point where the executable demo interacts
    with the scenario-backed enterprise API boundary. Downstream layers consume
    the aggregated evidence package and derived context instead of calling
    external sources directly.

Main output:
    01_output_layer1_aggregated_evidence_package.json
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from oversee.external_sources import ExternalSourcePackage, ExternalSourcePayload
from oversee.integration.predictive_alert_api import (
    PredictiveAlertReceipt,
    receive_predictive_alert,
)
from oversee.integration.simulated_enterprise_apis import SimulatedEnterpriseApiClient


@dataclass(slots=True)
class Layer1EvidencePipelineResult:
    """Result object produced by the Layer 1 evidence pipeline.
    
    It groups the received alert, enterprise API call trace, aggregated evidence
    package and validation report so the runner can persist each part as a
    reviewable artifact.
    """

    received_alert: PredictiveAlertReceipt
    enterprise_api_calls: list[dict[str, Any]]
    evidence_package: ExternalSourcePackage
    validation_report: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "received_alert": self.received_alert.to_dict(),
            "enterprise_api_calls": self.enterprise_api_calls,
            "evidence_package": self.evidence_package.to_dict(),
            "validation_report": self.validation_report,
        }


def run_layer1_evidence_pipeline(
    alert_request: dict[str, Any],
    *,
    api_client: Any | None = None,
    case_id_prefix: str = "PAPER_ALIGNED",
) -> Layer1EvidencePipelineResult:
    """Run Layer 1 intake, enterprise lookup, aggregation and validation.
    
    The function receives the predictive alert request, calls the scenario-backed
    enterprise API client, builds the aggregated evidence package and validates
    whether the evidence is complete enough for downstream reasoning.
    
    The main inter-layer output is the aggregated evidence package consumed by
    Layer 2 contextualization.
    """

    receipt = receive_predictive_alert(alert_request)

    if not receipt.accepted:
        empty_package = ExternalSourcePackage(
            package_id="invalid_layer1_evidence_package",
            case_id="INVALID",
            asset_id="UNKNOWN",
            line_id="UNKNOWN",
            created_at=datetime.now(timezone.utc).isoformat(),
            payloads=[],
            package_version="0.1.0",
        )
        return Layer1EvidencePipelineResult(
            received_alert=receipt,
            enterprise_api_calls=[],
            evidence_package=empty_package,
            validation_report={
                "valid": False,
                "errors": receipt.validation_errors,
                "payload_count": 0,
            },
        )

    alert = alert_request["alert"]
    raw_sensor_context = alert_request["raw_sensor_context"]
    requested_context = alert_request["requested_context"]

    asset_id = str(alert["asset_id"])
    asset_type = str(alert["asset_type"])
    line_id = str(alert["line_id"])
    lookback_days = int(requested_context["maintenance_history_lookback_days"])
    horizon_hours = int(requested_context["production_context_horizon_hours"])

    if api_client is None:
        api_client = SimulatedEnterpriseApiClient()

    asset_metadata = api_client.get_asset_metadata(asset_id=asset_id)
    maintenance_history = api_client.get_maintenance_history(
        asset_id=asset_id,
        lookback_days=lookback_days,
    )
    operational_context = api_client.get_operational_context(
        asset_id=asset_id,
        line_id=line_id,
        horizon_hours=horizon_hours,
    )
    inventory_and_resources = api_client.get_inventory_and_resources(asset_id=asset_id)
    policy_governance = api_client.get_policy_governance(
        asset_type=asset_type,
        criticality_score=int(asset_metadata["criticality_score"]),
    )

    created_at = datetime.now(timezone.utc).isoformat()
    normalized_case_id_prefix = case_id_prefix.strip() if case_id_prefix else "CASE"
    case_id = f"{normalized_case_id_prefix}_{alert['alert_id']}"
    payloads = [
        _payload(
            source_name="asset_registry",
            source_system="enterprise_asset_registry_api",
            source_type="master_data",
            endpoint="/enterprise/asset-registry/assets/{asset_id}",
            created_at=created_at,
            case_id=case_id,
            asset_id=asset_id,
            line_id=line_id,
            raw_payload=asset_metadata,
            normalized_fields={
                "asset_type": asset_metadata["asset_type"],
                "asset_criticality": asset_metadata["asset_criticality"],
                "criticality_score": asset_metadata["criticality_score"],
            },
        ),
        _payload(
            source_name="sensor_historian",
            source_system="predictive_agent_payload",
            source_type="raw_sensor_context",
            endpoint="embedded_in_predictive_alert_request",
            created_at=created_at,
            case_id=case_id,
            asset_id=asset_id,
            line_id=line_id,
            raw_payload=raw_sensor_context,
            normalized_fields={
                "vibration_trend": _trend(raw_sensor_context["vibration_mms"]),
                "temperature_trend": _trend(raw_sensor_context["temperature_celsius"]),
                "sensor_severity": "high"
                if raw_sensor_context.get("alarm_count", 0) >= 1
                else "medium",
            },
            data_quality_flags=_as_text_list(
                raw_sensor_context.get("data_quality_flags", [])
            ),
        ),
        _payload(
            source_name="predictive_maintenance",
            source_system="predictive_maintenance_agent",
            source_type="model_inference",
            endpoint="POST /oversee/api/v1/predictive-alerts",
            created_at=created_at,
            case_id=case_id,
            asset_id=asset_id,
            line_id=line_id,
            raw_payload=alert,
            normalized_fields={
                "alert_type": alert.get("alert_type", "predictive_degradation_alert"),
                "estimated_time_to_failure_hours": float(alert["predictive_horizon_hours"]),
                "confidence_score": float(alert["confidence_score"]),
                "alert_severity": "high",
            },
        ),
        _payload(
            source_name="maintenance_history",
            source_system="enterprise_cmms_api",
            source_type="work_order_history",
            endpoint="/enterprise/cmms/assets/{asset_id}/work-orders",
            created_at=created_at,
            case_id=case_id,
            asset_id=asset_id,
            line_id=line_id,
            raw_payload=maintenance_history,
            normalized_fields={
                "recent_repeated_failures": maintenance_history["recent_repeated_failures"],
            },
        ),
        _payload(
            source_name="production_planning",
            source_system="enterprise_mes_api",
            source_type="operational_context",
            endpoint="/enterprise/mes/lines/{line_id}/operational-context",
            created_at=created_at,
            case_id=case_id,
            asset_id=asset_id,
            line_id=line_id,
            raw_payload=operational_context,
            normalized_fields={
                "production_load_pct": operational_context["production_load_pct"],
                "next_planned_downtime_hours": operational_context[
                    "next_planned_downtime_hours"
                ],
                "production_pressure": operational_context["production_pressure"],
            },
        ),
        _payload(
            source_name="inventory_and_resources",
            source_system="enterprise_inventory_api",
            source_type="resource_availability",
            endpoint="/enterprise/inventory/assets/{asset_id}/resources",
            created_at=created_at,
            case_id=case_id,
            asset_id=asset_id,
            line_id=line_id,
            raw_payload=inventory_and_resources,
            normalized_fields={
                "spare_part_available": inventory_and_resources["spare_part_available"],
                "specialist_technician_available_next_shift": inventory_and_resources[
                    "specialist_technician_available_next_shift"
                ],
                "intervention_feasible": inventory_and_resources["intervention_feasible"],
            },
        ),
        _payload(
            source_name="policy_governance",
            source_system="enterprise_policy_governance_api",
            source_type="governance_policy",
            endpoint="/enterprise/policy-governance/assets/{asset_type}",
            created_at=created_at,
            case_id=case_id,
            asset_id=asset_id,
            line_id=line_id,
            raw_payload=policy_governance,
            normalized_fields={
                "mandatory_human_review_for_high_criticality": policy_governance[
                    "mandatory_human_review_for_high_criticality"
                ],
                "expected_human_review_required": policy_governance[
                    "expected_human_review_required"
                ],
            },
        ),
    ]

    package = ExternalSourcePackage(
        package_id=f"layer1_evidence_package_{case_id}",
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        created_at=created_at,
        payloads=payloads,
        package_version="0.1.0",
    )

    return Layer1EvidencePipelineResult(
        received_alert=receipt,
        enterprise_api_calls=api_client.call_trace(),
        evidence_package=package,
        validation_report=_validate_evidence_package(package=package),
    )


def _payload(
    *,
    source_name: str,
    source_system: str,
    source_type: str,
    endpoint: str,
    created_at: str,
    case_id: str,
    asset_id: str,
    line_id: str,
    raw_payload: dict[str, Any],
    normalized_fields: dict[str, Any],
    data_quality_flags: list[str] | None = None,
) -> ExternalSourcePayload:
    """Create an external source payload."""

    return ExternalSourcePayload(
        source_name=source_name,
        source_system=source_system,
        source_type=source_type,
        endpoint=endpoint,
        generated_at=created_at,
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        raw_payload=raw_payload,
        normalized_fields=normalized_fields,
        data_quality_flags=list(data_quality_flags or []),
    )


def _validate_evidence_package(package: ExternalSourcePackage) -> dict[str, Any]:
    """Validate the aggregated evidence package."""

    required_sources = {
        "asset_registry",
        "sensor_historian",
        "predictive_maintenance",
        "maintenance_history",
        "production_planning",
        "inventory_and_resources",
        "policy_governance",
    }
    present_sources = {payload.source_name for payload in package.payloads}
    missing_sources = sorted(required_sources - present_sources)
    payloads_with_quality_flags = [
        payload.source_name for payload in package.payloads if payload.data_quality_flags
    ]

    return {
        "valid": not missing_sources and not payloads_with_quality_flags,
        "missing_sources": missing_sources,
        "payloads_with_quality_flags": payloads_with_quality_flags,
        "payload_count": len(package.payloads),
        "required_source_count": len(required_sources),
    }




def _as_text_list(value: Any) -> list[str]:
    """Return a defensive list of non-empty text flags."""

    if value is None:
        return []

    if isinstance(value, str):
        return [value] if value.strip() else []

    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]

    return [str(value)] if str(value).strip() else []


def _trend(values: list[float]) -> str:
    """Calculate a simple trend."""

    if len(values) < 2:
        return "unknown"

    if float(values[-1]) > float(values[0]):
        return "increasing"

    if float(values[-1]) < float(values[0]):
        return "decreasing"

    return "stable"
