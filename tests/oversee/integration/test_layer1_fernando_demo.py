"""Tests for the Fernando-aligned OVERSEE Layer 1 demo."""

from __future__ import annotations

import json

from oversee.integration import (
    build_sample_predictive_alert_request,
    receive_predictive_alert,
    run_layer1_evidence_pipeline,
)


def test_layer1_receives_predictive_alert_request() -> None:
    """Layer 1 should receive and validate a predictive alert request."""

    alert_request = build_sample_predictive_alert_request()
    receipt = receive_predictive_alert(alert_request)

    assert receipt.accepted is True
    assert receipt.endpoint == "POST /oversee/api/v1/predictive-alerts"
    assert receipt.validation_errors == []
    assert "raw_sensor_context" in receipt.request_payload


def test_layer1_calls_required_enterprise_apis_and_aggregates_evidence() -> None:
    """Layer 1 should call simulated enterprise APIs and aggregate evidence."""

    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)

    api_names = {call["api_name"] for call in layer1_result.enterprise_api_calls}
    source_names = {payload.source_name for payload in layer1_result.evidence_package.payloads}

    assert api_names == {
        "asset_registry_api",
        "cmms_maintenance_history_api",
        "mes_operational_context_api",
        "inventory_and_resources_api",
        "policy_governance_api",
    }
    assert source_names == {
        "asset_registry",
        "sensor_historian",
        "predictive_maintenance",
        "maintenance_history",
        "production_planning",
        "inventory_and_resources",
        "policy_governance",
    }
    assert layer1_result.validation_report["valid"] is True
    assert layer1_result.validation_report["payload_count"] == 7


def test_layer1_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 1 outputs should not expose old bridge terminology."""

    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)

    serialized = json.dumps(
        {
            "alert_request": alert_request,
            "layer1_result": layer1_result.to_dict(),
        },
        ensure_ascii=False,
    ).lower()

    forbidden_terms = [
        "do_bridge",
        "bridgepayload",
        "bridge payload",
        "condition a",
        "condition b",
        "condition c",
        "condition d",
        "condition e",
        "condition f",
        "target_condition",
        "matrix_runner",
        "condition_registry",
    ]

    for term in forbidden_terms:
        assert term not in serialized
