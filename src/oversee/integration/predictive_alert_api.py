"""Simulated predictive alert ingestion API for OVERSEE Layer 1.

This module makes the Layer 1 entry point explicit. In a production deployment,
this would be exposed as an HTTP endpoint. In this reference implementation,
it is a deterministic Python function so the demo remains locally executable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


API_ENDPOINT = "POST /oversee/api/v1/predictive-alerts"


@dataclass(slots=True)
class PredictiveAlertReceipt:
    """Validated receipt returned by the simulated Layer 1 API."""

    endpoint: str
    received_at: str
    accepted: bool
    validation_errors: list[str]
    request_payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


def build_sample_predictive_alert_request() -> dict[str, Any]:
    """Build a concrete predictive alert request with raw sensor context."""

    return {
        "alert": {
            "alert_id": "ALERT-COMP-001-20260603",
            "asset_id": "COMP-001",
            "asset_type": "industrial_air_compressor",
            "line_id": "PKG-LINE-01",
            "suspected_failure_mode": "bearing_degradation",
            "alert_type": "predictive_degradation_alert",
            "predictive_horizon_hours": 48,
            "confidence_score": 0.88,
            "model_name": "compressor_failure_risk_model",
            "model_version": "v1.0-reference",
            "triggered_at": "2026-06-03T08:30:00Z",
        },
        "raw_sensor_context": {
            "sampling_window_hours": 24,
            "vibration_mms": [1.4, 1.7, 2.1, 2.6, 2.9],
            "temperature_celsius": [74.0, 77.5, 81.2, 85.0, 88.5],
            "pressure_bar": [7.8, 7.6, 7.4, 7.1, 6.9],
            "alarm_count": 3,
            "last_sensor_timestamp": "2026-06-03T08:25:00Z",
        },
        "requested_context": {
            "maintenance_history_lookback_days": 180,
            "production_context_horizon_hours": 72,
            "include_inventory_and_resources": True,
            "include_policy_governance": True,
        },
    }


def receive_predictive_alert(request_payload: dict[str, Any]) -> PredictiveAlertReceipt:
    """Receive and validate one predictive alert request."""

    validation_errors = _validate_predictive_alert_request(request_payload)

    return PredictiveAlertReceipt(
        endpoint=API_ENDPOINT,
        received_at=datetime.now(timezone.utc).isoformat(),
        accepted=not validation_errors,
        validation_errors=validation_errors,
        request_payload=request_payload,
    )


def _validate_predictive_alert_request(request_payload: dict[str, Any]) -> list[str]:
    """Validate the minimal request structure expected by the ingestion API."""

    errors: list[str] = []

    if not isinstance(request_payload, dict):
        return ["request_payload_must_be_object"]

    alert = request_payload.get("alert")
    raw_sensor_context = request_payload.get("raw_sensor_context")
    requested_context = request_payload.get("requested_context")

    if not isinstance(alert, dict):
        errors.append("missing_or_invalid_alert_object")
    if not isinstance(raw_sensor_context, dict):
        errors.append("missing_or_invalid_raw_sensor_context_object")
    if not isinstance(requested_context, dict):
        errors.append("missing_or_invalid_requested_context_object")

    if isinstance(alert, dict):
        required_alert_fields = [
            "alert_id",
            "asset_id",
            "asset_type",
            "line_id",
            "suspected_failure_mode",
            "predictive_horizon_hours",
            "confidence_score",
        ]
        for field_name in required_alert_fields:
            if field_name not in alert:
                errors.append(f"missing_alert_field:{field_name}")

    if isinstance(raw_sensor_context, dict):
        for field_name in ["vibration_mms", "temperature_celsius", "pressure_bar"]:
            if field_name not in raw_sensor_context:
                errors.append(f"missing_raw_sensor_field:{field_name}")

    return errors
