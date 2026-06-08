"""CMMN-inspired case lifecycle contracts for OVERSEE Layer 3."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CaseLifecycleEvent:
    """One event in the case lifecycle trace."""

    event_id: str
    sequence: int
    event_type: str
    event_name: str
    status: str
    source_layer: str
    occurred_at: str
    evidence_refs: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class CaseTask:
    """One case-management task derived from the case context."""

    task_id: str
    task_type: str
    task_name: str
    status: str
    required_role: str
    trigger: str
    source_layer: str
    evidence_refs: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class CaseMilestone:
    """One lifecycle milestone for the case."""

    milestone_id: str
    milestone_name: str
    status: str
    source_layer: str
    reached_at: str | None
    criteria: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class CaseManagementState:
    """Layer 3 case-management state for one OVERSEE case."""

    case_id: str
    asset_id: str
    case_status: str
    lifecycle_stage: str
    current_layer: str
    opened_at: str
    human_review_required: bool
    maintenance_planning_required: bool
    decision_ready: bool
    events: list[CaseLifecycleEvent]
    tasks: list[CaseTask]
    milestones: list[CaseMilestone]
    blockers: list[str] = field(default_factory=list)
    lifecycle_version: str = "0.1.0"

    @property
    def event_count(self) -> int:
        """Return the number of lifecycle events."""

        return len(self.events)

    @property
    def task_count(self) -> int:
        """Return the number of case tasks."""

        return len(self.tasks)

    @property
    def milestone_count(self) -> int:
        """Return the number of milestones."""

        return len(self.milestones)

    def lifecycle_trace(self) -> list[dict[str, Any]]:
        """Return only the ordered lifecycle trace."""

        return [event.to_dict() for event in self.events]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        data = asdict(self)
        data["event_count"] = self.event_count
        data["task_count"] = self.task_count
        data["milestone_count"] = self.milestone_count
        return data
