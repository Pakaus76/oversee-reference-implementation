"""Scenario-backed enterprise API simulator for executable walkthrough scenarios.

This module provides the same enterprise API surface used by Layer 1, but it
returns data from a scenario's executable_inputs section instead of returning a
single fixed reference case.

The goal is to make OVERSEE executable across multiple industrial scenarios
while keeping the external API metaphor explicit and traceable.
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any

from oversee.integration.simulated_enterprise_apis import EnterpriseApiCall


class ScenarioBackedEnterpriseApiClient:
    """Enterprise API client backed by one scenario's executable inputs."""

    REQUIRED_ENTERPRISE_SOURCES = {
        "asset_metadata",
        "maintenance_history",
        "operational_context",
        "inventory_and_resources",
        "policy_governance",
    }

    def __init__(self, executable_inputs: dict[str, Any]) -> None:
        """Create a scenario-backed client.

        Parameters
        ----------
        executable_inputs:
            The executable_inputs dictionary from one walkthrough scenario.
        """

        self.executable_inputs = copy.deepcopy(executable_inputs)
        self.enterprise_sources = self._extract_enterprise_sources(executable_inputs)
        self.calls: list[EnterpriseApiCall] = []

    def get_asset_metadata(self, *, asset_id: str) -> dict[str, Any]:
        """Return scenario asset registry data."""

        response = self._copy_source_payload("asset_metadata")
        self._assert_asset_match(response=response, asset_id=asset_id, source_name="asset_metadata")

        self._record(
            api_name="scenario_asset_registry_api",
            endpoint="/enterprise/asset-registry/assets/{asset_id}",
            method="GET",
            request_parameters={"asset_id": asset_id},
            response_payload=response,
        )

        return response

    def get_maintenance_history(self, *, asset_id: str, lookback_days: int) -> dict[str, Any]:
        """Return scenario CMMS/EAM maintenance history data."""

        response = self._copy_source_payload("maintenance_history")
        self._assert_asset_match(
            response=response,
            asset_id=asset_id,
            source_name="maintenance_history",
        )

        if "lookback_days" not in response:
            response["lookback_days"] = lookback_days

        self._record(
            api_name="scenario_cmms_maintenance_history_api",
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
        """Return scenario MES/ERP operational context data."""

        response = self._copy_source_payload("operational_context")
        self._assert_asset_match(
            response=response,
            asset_id=asset_id,
            source_name="operational_context",
        )

        if response.get("line_id") != line_id:
            raise ValueError(
                "Scenario operational_context line_id does not match request: "
                f"expected {line_id}, got {response.get('line_id')}"
            )

        if "horizon_hours" not in response:
            response["horizon_hours"] = horizon_hours

        self._record(
            api_name="scenario_mes_operational_context_api",
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
        """Return scenario inventory and resource availability data."""

        response = self._copy_source_payload("inventory_and_resources")
        self._assert_asset_match(
            response=response,
            asset_id=asset_id,
            source_name="inventory_and_resources",
        )

        self._record(
            api_name="scenario_inventory_and_resources_api",
            endpoint="/enterprise/inventory/assets/{asset_id}/resources",
            method="GET",
            request_parameters={"asset_id": asset_id},
            response_payload=response,
        )

        return response

    def get_policy_governance(self, *, asset_type: str, criticality_score: int) -> dict[str, Any]:
        """Return scenario governance policy data."""

        response = self._copy_source_payload("policy_governance")

        if response.get("asset_type") != asset_type:
            raise ValueError(
                "Scenario policy_governance asset_type does not match request: "
                f"expected {asset_type}, got {response.get('asset_type')}"
            )

        if int(response.get("criticality_score", -1)) != int(criticality_score):
            raise ValueError(
                "Scenario policy_governance criticality_score does not match request: "
                f"expected {criticality_score}, got {response.get('criticality_score')}"
            )

        self._record(
            api_name="scenario_policy_governance_api",
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
        """Return all scenario-backed API calls as dictionaries."""

        return [call.to_dict() for call in self.calls]

    def _copy_source_payload(self, source_name: str) -> dict[str, Any]:
        """Return one enterprise source payload as a defensive copy."""

        if source_name not in self.enterprise_sources:
            raise KeyError(f"Missing enterprise source: {source_name}")

        payload = self.enterprise_sources[source_name]

        if not isinstance(payload, dict):
            raise TypeError(f"Enterprise source must be a dictionary: {source_name}")

        return copy.deepcopy(payload)

    def _record(
        self,
        *,
        api_name: str,
        endpoint: str,
        method: str,
        request_parameters: dict[str, Any],
        response_payload: dict[str, Any],
    ) -> None:
        """Record one scenario-backed enterprise API call."""

        self.calls.append(
            EnterpriseApiCall(
                api_name=api_name,
                endpoint=endpoint,
                method=method,
                request_parameters=request_parameters,
                response_payload=copy.deepcopy(response_payload),
                called_at=datetime.now(timezone.utc).isoformat(),
            )
        )

    @classmethod
    def _extract_enterprise_sources(
        cls,
        executable_inputs: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract and validate the enterprise source section."""

        if not isinstance(executable_inputs, dict):
            raise TypeError("executable_inputs must be a dictionary")

        enterprise_sources = executable_inputs.get("enterprise_sources")

        if not isinstance(enterprise_sources, dict):
            raise ValueError("executable_inputs.enterprise_sources must be a dictionary")

        missing_sources = sorted(cls.REQUIRED_ENTERPRISE_SOURCES - set(enterprise_sources))

        if missing_sources:
            raise ValueError(
                "Missing required enterprise source payloads: "
                + ", ".join(missing_sources)
            )

        return copy.deepcopy(enterprise_sources)

    @staticmethod
    def _assert_asset_match(
        *,
        response: dict[str, Any],
        asset_id: str,
        source_name: str,
    ) -> None:
        """Raise an error when a scenario source does not match the requested asset."""

        if response.get("asset_id") != asset_id:
            raise ValueError(
                f"Scenario {source_name} asset_id does not match request: "
                f"expected {asset_id}, got {response.get('asset_id')}"
            )