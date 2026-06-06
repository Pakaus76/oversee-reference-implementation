"""Simulated enterprise APIs used by the paper-aligned Layer 1 demo.

These deterministic functions represent external enterprise systems:
asset registry, CMMS, MES/ERP, inventory/resources and governance policy services.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class EnterpriseApiCall:
    """Trace of one simulated enterprise API call."""

    api_name: str
    endpoint: str
    method: str
    request_parameters: dict[str, Any]
    response_payload: dict[str, Any]
    called_at: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


class SimulatedEnterpriseApiClient:
    """Deterministic simulator for enterprise-side APIs."""

    def __init__(self) -> None:
        """Create an API client with an empty call trace."""

        self.calls: list[EnterpriseApiCall] = []

    def get_asset_metadata(self, *, asset_id: str) -> dict[str, Any]:
        """Simulate an asset registry lookup."""

        response = {
            "asset_id": asset_id,
            "asset_type": "industrial_air_compressor",
            "line_id": "PKG-LINE-01",
            "asset_criticality": "high",
            "criticality_score": 5,
            "manufacturer": "Reference Compressor Systems",
            "model": "RC-5500",
            "location": "Packaging area - line 1",
        }
        self._record(
            api_name="asset_registry_api",
            endpoint="/enterprise/asset-registry/assets/{asset_id}",
            method="GET",
            request_parameters={"asset_id": asset_id},
            response_payload=response,
        )
        return response

    def get_maintenance_history(self, *, asset_id: str, lookback_days: int) -> dict[str, Any]:
        """Simulate a CMMS maintenance history lookup."""

        response = {
            "asset_id": asset_id,
            "lookback_days": lookback_days,
            "recent_repeated_failures": True,
            "work_orders": [
                {
                    "work_order_id": "WO-2026-0418",
                    "type": "corrective",
                    "failure_mode": "vibration_anomaly",
                    "duration_hours": 2.0,
                },
                {
                    "work_order_id": "WO-2026-0522",
                    "type": "corrective",
                    "failure_mode": "bearing_noise",
                    "duration_hours": 3.5,
                },
            ],
        }
        self._record(
            api_name="cmms_maintenance_history_api",
            endpoint="/enterprise/cmms/assets/{asset_id}/work-orders",
            method="GET",
            request_parameters={"asset_id": asset_id, "lookback_days": lookback_days},
            response_payload=response,
        )
        return response

    def get_operational_context(
        self,
        *,
        asset_id: str,
        line_id: str,
        horizon_hours: int,
    ) -> dict[str, Any]:
        """Simulate MES/ERP operational context retrieval."""

        response = {
            "asset_id": asset_id,
            "line_id": line_id,
            "horizon_hours": horizon_hours,
            "production_pressure": "high",
            "production_load_pct": 92.0,
            "next_planned_downtime_hours": 36.0,
            "customer_impact": "medium",
            "shift_demand": "high",
        }
        self._record(
            api_name="mes_operational_context_api",
            endpoint="/enterprise/mes/lines/{line_id}/operational-context",
            method="GET",
            request_parameters={
                "asset_id": asset_id,
                "line_id": line_id,
                "horizon_hours": horizon_hours,
            },
            response_payload=response,
        )
        return response

    def get_inventory_and_resources(self, *, asset_id: str) -> dict[str, Any]:
        """Simulate spare-parts and specialist-resource lookup."""

        response = {
            "asset_id": asset_id,
            "spare_part_available": True,
            "spare_part_id": "SP-COMP-BEARING-KIT",
            "specialist_technician_available_next_shift": True,
            "intervention_feasible": True,
        }
        self._record(
            api_name="inventory_and_resources_api",
            endpoint="/enterprise/inventory/assets/{asset_id}/resources",
            method="GET",
            request_parameters={"asset_id": asset_id},
            response_payload=response,
        )
        return response

    def get_policy_governance(self, *, asset_type: str, criticality_score: int) -> dict[str, Any]:
        """Simulate governance policy lookup."""

        response = {
            "asset_type": asset_type,
            "criticality_score": criticality_score,
            "mandatory_human_review_for_high_criticality": True,
            "expected_human_review_required": criticality_score >= 5,
            "policy_id": "POL-COMP-HIGH-CRIT-001",
        }
        self._record(
            api_name="policy_governance_api",
            endpoint="/enterprise/policy-governance/assets/{asset_type}",
            method="GET",
            request_parameters={
                "asset_type": asset_type,
                "criticality_score": criticality_score,
            },
            response_payload=response,
        )
        return response

    def call_trace(self) -> list[dict[str, Any]]:
        """Return all simulated API calls as dictionaries."""

        return [call.to_dict() for call in self.calls]

    def _record(
        self,
        *,
        api_name: str,
        endpoint: str,
        method: str,
        request_parameters: dict[str, Any],
        response_payload: dict[str, Any],
    ) -> None:
        """Record one simulated API call."""

        self.calls.append(
            EnterpriseApiCall(
                api_name=api_name,
                endpoint=endpoint,
                method=method,
                request_parameters=request_parameters,
                response_payload=response_payload,
                called_at=datetime.now(timezone.utc).isoformat(),
            )
        )
