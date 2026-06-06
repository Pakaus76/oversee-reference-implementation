"""Tests for scenario-backed Layer 1 enterprise API injection."""

from __future__ import annotations

from typing import Any

from oversee.integration import build_sample_predictive_alert_request, run_layer1_evidence_pipeline


class FakeScenarioEnterpriseApiClient:
    """Small scenario-backed enterprise API client used to verify injection."""

    def __init__(self) -> None:
        """Create an empty call trace."""

        self._calls: list[dict[str, Any]] = []

    def get_asset_metadata(self, *, asset_id: str) -> dict[str, Any]:
        """Return scenario-specific asset metadata."""

        response = {
            "asset_id": asset_id,
            "asset_type": "industrial_pump",
            "line_id": "WATER-LINE-02",
            "asset_criticality": "medium",
            "criticality_score": 3,
            "manufacturer": "Reference Pump Systems",
            "model": "RP-2200",
            "location": "Utilities area - water loop",
        }
        self._record("fake_asset_registry_api", response)
        return response

    def get_maintenance_history(self, *, asset_id: str, lookback_days: int) -> dict[str, Any]:
        """Return scenario-specific maintenance history."""

        response = {
            "asset_id": asset_id,
            "lookback_days": lookback_days,
            "recent_repeated_failures": False,
            "work_orders": [],
        }
        self._record("fake_cmms_maintenance_history_api", response)
        return response

    def get_operational_context(
        self,
        *,
        asset_id: str,
        line_id: str,
        horizon_hours: int,
    ) -> dict[str, Any]:
        """Return scenario-specific operational context."""

        response = {
            "asset_id": asset_id,
            "line_id": line_id,
            "horizon_hours": horizon_hours,
            "production_pressure": "medium",
            "production_load_pct": 67.0,
            "next_planned_downtime_hours": 96.0,
            "customer_impact": "low",
            "shift_demand": "medium",
        }
        self._record("fake_mes_operational_context_api", response)
        return response

    def get_inventory_and_resources(self, *, asset_id: str) -> dict[str, Any]:
        """Return scenario-specific inventory and resource context."""

        response = {
            "asset_id": asset_id,
            "spare_part_available": True,
            "spare_part_id": "SP-PUMP-SEAL-KIT",
            "specialist_technician_available_next_shift": False,
            "intervention_feasible": False,
        }
        self._record("fake_inventory_and_resources_api", response)
        return response

    def get_policy_governance(self, *, asset_type: str, criticality_score: int) -> dict[str, Any]:
        """Return scenario-specific governance policy."""

        response = {
            "asset_type": asset_type,
            "criticality_score": criticality_score,
            "mandatory_human_review_for_high_criticality": True,
            "expected_human_review_required": False,
            "policy_id": "POL-GENERIC-MEDIUM-CRIT-001",
        }
        self._record("fake_policy_governance_api", response)
        return response

    def call_trace(self) -> list[dict[str, Any]]:
        """Return the fake enterprise API call trace."""

        return self._calls

    def _record(self, api_name: str, response_payload: dict[str, Any]) -> None:
        """Record one fake enterprise API call."""

        self._calls.append(
            {
                "api_name": api_name,
                "method": "GET",
                "request_parameters": {},
                "response_payload": response_payload,
            }
        )


def test_layer1_pipeline_accepts_scenario_backed_api_client() -> None:
    """Layer 1 should use the provided API client instead of fixed demo data."""

    alert_request = build_sample_predictive_alert_request()
    alert_request["alert"]["alert_id"] = "ALERT-PUMP-TST-001"
    alert_request["alert"]["asset_id"] = "PUMP-TST"
    alert_request["alert"]["asset_type"] = "industrial_pump"
    alert_request["alert"]["line_id"] = "WATER-LINE-02"
    alert_request["alert"]["suspected_failure_mode"] = "seal_degradation"
    alert_request["alert"]["predictive_horizon_hours"] = 168
    alert_request["alert"]["confidence_score"] = 0.73

    result = run_layer1_evidence_pipeline(
        alert_request,
        api_client=FakeScenarioEnterpriseApiClient(),
        case_id_prefix="SCENARIO_TEST",
    )

    assert result.validation_report["valid"] is True
    assert result.evidence_package.case_id == "SCENARIO_TEST_ALERT-PUMP-TST-001"
    assert result.evidence_package.asset_id == "PUMP-TST"

    asset_payload = next(
        payload
        for payload in result.evidence_package.payloads
        if payload.source_name == "asset_registry"
    )
    assert asset_payload.normalized_fields["asset_type"] == "industrial_pump"
    assert asset_payload.normalized_fields["criticality_score"] == 3

    resource_payload = next(
        payload
        for payload in result.evidence_package.payloads
        if payload.source_name == "inventory_and_resources"
    )
    assert resource_payload.normalized_fields["intervention_feasible"] is False

    api_names = {call["api_name"] for call in result.enterprise_api_calls}
    assert "fake_asset_registry_api" in api_names
    assert "fake_inventory_and_resources_api" in api_names