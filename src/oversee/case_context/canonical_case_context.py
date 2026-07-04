"""Canonical compressor case context contracts for OVERSEE Layer 2."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

#5.1 >-------------------------------------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class CanonicalAssetContext:
    """Normalized asset context."""

    asset_id: str
    asset_type: str
    line_id: str | None
    criticality_label: str
    criticality_score: int
    process_role: str | None = None


@dataclass(slots=True)
class PredictiveEvidenceContext:
    """Normalized predictive evidence context."""

    alert_type: str
    estimated_time_to_failure_hours: float
    confidence_score: float
    alert_severity: str
    vibration_trend: str | None = None
    temperature_trend: str | None = None


@dataclass(slots=True)
class OperationalContext:
    """Normalized operational and production context."""

    production_load_pct: float
    next_planned_downtime_hours: float
    production_pressure: str
    business_impact_if_unavailable: str | None = None


@dataclass(slots=True)
class MaintenanceResourceContext:
    """Normalized maintenance history and resource context."""

    recent_repeated_failures: bool
    spare_part_available: bool
    specialist_technician_available_next_shift: bool
    intervention_feasible: bool


@dataclass(slots=True)
class GovernancePolicyContext:
    """Normalized policy and governance context."""

    mandatory_human_review_for_high_criticality: bool
    expected_human_review_required: bool
    computed_human_review_required: bool


@dataclass(slots=True)
class CanonicalCaseContext:
    """Layer 2 canonical case context built from Layer 1 payloads."""

    context_id: str
    case_id: str
    asset: CanonicalAssetContext
    predictive_evidence: PredictiveEvidenceContext
    operational_context: OperationalContext
    maintenance_resources: MaintenanceResourceContext
    governance_policy: GovernancePolicyContext
    source_payload_count: int
    source_names: list[str]
    data_quality_flags: list[str] = field(default_factory=list)
    key_risk_drivers: list[str] = field(default_factory=list)
    context_version: str = "0.1.0"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)
