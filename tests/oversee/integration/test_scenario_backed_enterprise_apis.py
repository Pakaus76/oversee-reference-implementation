"""Tests for scenario-backed enterprise API simulation."""

from __future__ import annotations

import pytest

from oversee.integration.scenario_backed_enterprise_apis import (
    ScenarioBackedEnterpriseApiClient,
)


def _sample_executable_inputs() -> dict[str, object]:
    """Return a compact executable scenario payload for testing."""

    return {
        "enterprise_sources": {
            "asset_metadata": {
                "asset_id": "PUMP-001",
                "asset_type": "industrial_pump",
                "line_id": "WATER-LINE-01",
                "asset_criticality": "high",
                "criticality_score": 5,
                "manufacturer": "Reference Pump Systems",
                "model": "RP-4100",
                "location": "Process area - water circulation loop",
            },
            "maintenance_history": {
                "asset_id": "PUMP-001",
                "lookback_days": 180,
                "recent_repeated_failures": True,
                "work_orders": [],
            },
            "operational_context": {
                "asset_id": "PUMP-001",
                "line_id": "WATER-LINE-01",
                "horizon_hours": 72,
                "production_pressure": "high",
                "production_load_pct": 88.0,
                "next_planned_downtime_hours": 120.0,
                "customer_impact": "high",
                "shift_demand": "high",
            },
            "inventory_and_resources": {
                "asset_id": "PUMP-001",
                "spare_part_available": False,
                "spare_part_id": "SP-PUMP-SEAL-KIT",
                "specialist_technician_available_next_shift": False,
                "intervention_feasible": False,
            },
            "policy_governance": {
                "asset_type": "industrial_pump",
                "criticality_score": 5,
                "mandatory_human_review_for_high_criticality": True,
                "expected_human_review_required": True,
                "policy_id": "POL-PUMP-HIGH-CRIT-001",
            },
        }
    }


def test_scenario_backed_client_returns_enterprise_source_payloads() -> None:
    """The scenario-backed client should expose all enterprise source payloads."""

    client = ScenarioBackedEnterpriseApiClient(_sample_executable_inputs())

    asset = client.get_asset_metadata(asset_id="PUMP-001")
    maintenance = client.get_maintenance_history(asset_id="PUMP-001", lookback_days=180)
    operations = client.get_operational_context(
        asset_id="PUMP-001",
        line_id="WATER-LINE-01",
        horizon_hours=72,
    )
    resources = client.get_inventory_and_resources(asset_id="PUMP-001")
    policy = client.get_policy_governance(
        asset_type="industrial_pump",
        criticality_score=5,
    )

    assert asset["asset_type"] == "industrial_pump"
    assert maintenance["recent_repeated_failures"] is True
    assert operations["next_planned_downtime_hours"] == 120.0
    assert resources["intervention_feasible"] is False
    assert policy["expected_human_review_required"] is True

    trace = client.call_trace()
    assert len(trace) == 5
    assert {call["api_name"] for call in trace} == {
        "scenario_asset_registry_api",
        "scenario_cmms_maintenance_history_api",
        "scenario_mes_operational_context_api",
        "scenario_inventory_and_resources_api",
        "scenario_policy_governance_api",
    }


def test_scenario_backed_client_rejects_missing_enterprise_sources() -> None:
    """The client should fail fast when required scenario sources are missing."""

    with pytest.raises(ValueError, match="Missing required enterprise source payloads"):
        ScenarioBackedEnterpriseApiClient({"enterprise_sources": {}})


def test_scenario_backed_client_rejects_asset_mismatch() -> None:
    """The client should protect against inconsistent scenario asset identifiers."""

    client = ScenarioBackedEnterpriseApiClient(_sample_executable_inputs())

    with pytest.raises(ValueError, match="asset_id does not match request"):
        client.get_asset_metadata(asset_id="OTHER-ASSET")