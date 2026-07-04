"""Scenario-backed enterprise API boundary for the OVERSEE workbench.

Purpose:
    Simulate calls to enterprise information sources without connecting to real
    ERP, MES, CMMS, MRO, workforce planning or policy systems.

Architectural role:
    This module represents the external-source access boundary used by the
    executable demo. In a production deployment these methods could be replaced
    by real connectors. In the reference implementation they return controlled
    scenario-backed payloads so that runs are reproducible and testable.

Important note:
    The goal is not to build complex enterprise integrations. The goal is to
    make clear which external information would be retrieved and how it enters
    the OVERSEE evidence package.
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any

from oversee.integration.simulated_enterprise_apis import EnterpriseApiCall

#3.0 --------------------------------------------------------------------------------------------------------------------------------->

class ScenarioBackedEnterpriseApiClient:
    """Enterprise API client backed by one scenario's executable inputs.
    
    The class exposes simple methods that look like enterprise API calls from the
    perspective of Layer 1. Each call returns a defensive copy of the corresponding
    scenario source payload and records a trace entry for auditability.
    """

    REQUIRED_ENTERPRISE_SOURCES = {
        "asset_metadata",
        "maintenance_history",
        "operational_context",
        "inventory_and_resources",
        "policy_governance",
    }

#3.1 --------------------------------------------------------------------------------------------------------------------------------->

    def __init__(self, executable_inputs: dict[str, Any]) -> None:
        """Create a scenario-backed enterprise API client.
        
        The client receives the executable_inputs section of one scenario and extracts
        its enterprise_sources block. All later source lookups are served from that
        controlled source set.
        """

        self.executable_inputs = copy.deepcopy(executable_inputs)
        self.enterprise_sources = self._extract_enterprise_sources(executable_inputs)
        self.calls: list[EnterpriseApiCall] = []

#3.2 -------------------------------------------------------------------------------------------------------------------------------->

    def get_asset_metadata(self, *, asset_id: str) -> dict[str, Any]:
        """Return Asset Registry and engineering master-data evidence.
        
        In a real implementation this method could query an asset registry or
        engineering master-data system. In the demo it returns the scenario-backed
        payload used by Layer 1 evidence aggregation.

        - It helps us to know what type of asset we are dealing with and what its criticality is.
        This simulated API would be equivalent to querying an asset registry or engineering master system.
        For COMP-001, it returns the asset data: asset type, criticality, and role in the process.
        """

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
    
#3.2 --------------------------------------------------------------------------------------------------------------------------------

    def get_maintenance_history(self, *, asset_id: str, lookback_days: int) -> dict[str, Any]:
        """Return CMMS/EAM maintenance-history evidence.
        
        The method supplies historical work orders, repeated interventions and related maintenance context for the requested asset.

        - It helps to determine if this asset has already had repeated problems, recent interventions, or historical signs of failure.
        This API simulates a query to the CMMS. I pass it the asset_id and a window back,
        for example 90 days, and it returns the relevant maintenance history.
        """

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

#3.2 --------------------------------------------------------------------------------------------------------------------------------

    def get_operational_context(
        self,
        *,
        asset_id: str,
        line_id: str,
        horizon_hours: int,
    ) -> dict[str, Any]:
        """Return ERP/MES production and operational-context evidence.
        
        The method supplies production pressure, downtime-window and planning context needed for downstream contextualization and decision readiness.

        -It helps determine if there's production pressure, when the next shutdown window is, and what the impact of losing the asset would be.
        This API simulates a query to the MES/ERP. It's not enough to know that the compressor is degrading;
        I need to know if the line is loaded, if there's an upcoming shutdown window, and what the impact of inaction would be.
        """

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

#3.2 --------------------------------------------------------------------------------------------------------------------------------

    def get_inventory_and_resources(self, *, asset_id: str) -> dict[str, Any]:
        """Return MRO inventory and workforce-availability evidence.
        
        The method supplies spare-part availability, technician availability and other
        resource constraints used later by contextualization and decision logic.

        - It helps determine if the intervention is feasible.
        This API answers a very practical question: even if the case is urgent, do I have a spare part and a technician available to intervene?
        """

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

#3.2 --------------------------------------------------------------------------------------------------------------------------------

    def get_policy_governance(self, *, asset_type: str, criticality_score: int) -> dict[str, Any]:
        """Return policy-governance and compliance evidence.
        
        The method supplies review rules, criticality constraints and policy checks
        that become part of the evidence package and downstream governed decision.

        - This API helps determine whether, due to criticality or internal policy, a decision requires human review.
        This API simulates governance rules. If the asset is critical, policy may mandate human review before implementing the recommendation.
        """

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

#3.2 --------------------------------------------------------------------------------------------------------------------------------

    def call_trace(self) -> list[dict[str, Any]]:
        """Return all scenario-backed enterprise API calls as dictionaries.
        
        The trace shows which simulated source methods were called and what payload was
        returned. It helps reviewers distinguish source access from internal OVERSEE
        reasoning.

        -It serves to audit which sources were consulted.
        This allows us to demonstrate that Layer 1 did not invent the data. 
        It called specific methods of the boundary API, and that trace is then saved in 01_enterprise_api_calls.json.
        """

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
