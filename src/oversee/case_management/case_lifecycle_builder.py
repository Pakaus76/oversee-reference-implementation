"""Build a CMMN-inspired lifecycle from the canonical compressor context."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from oversee.case_context import CanonicalCaseContext
from oversee.case_management.case_lifecycle import (
    CaseLifecycleEvent,
    CaseManagementState,
    CaseMilestone,
    CaseTask,
)


def build_case_management_state(
    canonical_context: CanonicalCaseContext,
) -> CaseManagementState:
    """Build Layer 3 case-management state from Layer 2 canonical context."""

    timestamp = _utc_now()
    case_id = canonical_context.case_id
    asset_id = canonical_context.asset.asset_id

    human_review_required = canonical_context.governance_policy.computed_human_review_required
    maintenance_planning_required = _requires_maintenance_planning(canonical_context)
    blockers = _build_blockers(canonical_context)
    decision_ready = human_review_required and maintenance_planning_required and not blockers

    events = _build_events(
        canonical_context=canonical_context,
        timestamp=timestamp,
        human_review_required=human_review_required,
        maintenance_planning_required=maintenance_planning_required,
        decision_ready=decision_ready,
        blockers=blockers,
    )
    tasks = _build_tasks(
        canonical_context=canonical_context,
        timestamp=timestamp,
        human_review_required=human_review_required,
        maintenance_planning_required=maintenance_planning_required,
        blockers=blockers,
    )
    milestones = _build_milestones(
        canonical_context=canonical_context,
        timestamp=timestamp,
        human_review_required=human_review_required,
        maintenance_planning_required=maintenance_planning_required,
        decision_ready=decision_ready,
        blockers=blockers,
    )

    return CaseManagementState(
        case_id=case_id,
        asset_id=asset_id,
        case_status="open",
        lifecycle_stage="decision_ready" if decision_ready else "evidence_review",
        current_layer="Layer 3 - CMMN-inspired case lifecycle",
        opened_at=timestamp,
        human_review_required=human_review_required,
        maintenance_planning_required=maintenance_planning_required,
        decision_ready=decision_ready,
        events=events,
        tasks=tasks,
        milestones=milestones,
        blockers=blockers,
    )


def _build_events(
    *,
    canonical_context: CanonicalCaseContext,
    timestamp: str,
    human_review_required: bool,
    maintenance_planning_required: bool,
    decision_ready: bool,
    blockers: list[str],
) -> list[CaseLifecycleEvent]:
    """Build the ordered case lifecycle events."""

    case_id = canonical_context.case_id
    events = [
        CaseLifecycleEvent(
            event_id=f"{case_id}_evt_001_case_opened",
            sequence=1,
            event_type="case_opened",
            event_name="Compressor decision case opened",
            status="completed",
            source_layer="Layer 3",
            occurred_at=timestamp,
            evidence_refs=[canonical_context.context_id],
            details={
                "asset_id": canonical_context.asset.asset_id,
                "line_id": canonical_context.asset.line_id,
            },
        ),
        CaseLifecycleEvent(
            event_id=f"{case_id}_evt_002_external_evidence_received",
            sequence=2,
            event_type="external_evidence_received",
            event_name="External source evidence received",
            status="completed",
            source_layer="Layer 1",
            occurred_at=timestamp,
            evidence_refs=canonical_context.source_names,
            details={
                "source_payload_count": canonical_context.source_payload_count,
                "source_names": canonical_context.source_names,
            },
        ),
        CaseLifecycleEvent(
            event_id=f"{case_id}_evt_003_canonical_context_built",
            sequence=3,
            event_type="canonical_context_built",
            event_name="Canonical case context built",
            status="completed",
            source_layer="Layer 2",
            occurred_at=timestamp,
            evidence_refs=[canonical_context.context_id],
            details={
                "criticality_score": canonical_context.asset.criticality_score,
                "estimated_time_to_failure_hours": (
                    canonical_context.predictive_evidence.estimated_time_to_failure_hours
                ),
                "confidence_score": canonical_context.predictive_evidence.confidence_score,
            },
        ),
        CaseLifecycleEvent(
            event_id=f"{case_id}_evt_004_risk_assessment_completed",
            sequence=4,
            event_type="risk_assessment_completed",
            event_name="Risk drivers identified from canonical context",
            status="completed",
            source_layer="Layer 3",
            occurred_at=timestamp,
            evidence_refs=[canonical_context.context_id],
            details={
                "key_risk_drivers": canonical_context.key_risk_drivers,
                "data_quality_flags": canonical_context.data_quality_flags,
            },
        ),
        CaseLifecycleEvent(
            event_id=f"{case_id}_evt_005_human_review_requirement_identified",
            sequence=5,
            event_type="human_review_requirement_identified",
            event_name="Accountable human review requirement identified",
            status="completed" if human_review_required else "not_required",
            source_layer="Layer 3",
            occurred_at=timestamp,
            evidence_refs=["policy_governance", canonical_context.context_id],
            details={
                "human_review_required": human_review_required,
                "criticality_score": canonical_context.asset.criticality_score,
                "alert_severity": canonical_context.predictive_evidence.alert_severity,
            },
        ),
        CaseLifecycleEvent(
            event_id=f"{case_id}_evt_006_maintenance_planning_task_created",
            sequence=6,
            event_type="maintenance_planning_task_created",
            event_name="Maintenance planning task created",
            status="completed" if maintenance_planning_required else "not_required",
            source_layer="Layer 3",
            occurred_at=timestamp,
            evidence_refs=["inventory_and_resources", "production_planning"],
            details={
                "maintenance_planning_required": maintenance_planning_required,
                "intervention_feasible": (
                    canonical_context.maintenance_resources.intervention_feasible
                ),
                "next_planned_downtime_hours": (
                    canonical_context.operational_context.next_planned_downtime_hours
                ),
            },
        ),
        CaseLifecycleEvent(
            event_id=f"{case_id}_evt_007_decision_milestone_reached",
            sequence=7,
            event_type="decision_milestone_reached",
            event_name="Case is ready for decision rule evaluation",
            status="completed" if decision_ready else "blocked",
            source_layer="Layer 3",
            occurred_at=timestamp,
            evidence_refs=[canonical_context.context_id],
            details={
                "decision_ready": decision_ready,
                "blockers": blockers,
            },
        ),
    ]

    return events


def _build_tasks(
    *,
    canonical_context: CanonicalCaseContext,
    timestamp: str,
    human_review_required: bool,
    maintenance_planning_required: bool,
    blockers: list[str],
) -> list[CaseTask]:
    """Build human and operational tasks for the case."""

    case_id = canonical_context.case_id
    tasks: list[CaseTask] = []

    if human_review_required:
        tasks.append(
            CaseTask(
                task_id=f"{case_id}_task_human_review",
                task_type="human_review",
                task_name="Review compressor risk and approve decision path",
                status="open",
                required_role="maintenance_decision_owner",
                trigger="high criticality or high-severity predictive alert",
                source_layer="Layer 3",
                evidence_refs=["policy_governance", canonical_context.context_id],
                details={
                    "criticality_score": canonical_context.asset.criticality_score,
                    "alert_severity": canonical_context.predictive_evidence.alert_severity,
                    "created_at": timestamp,
                },
            )
        )

    if maintenance_planning_required:
        tasks.append(
            CaseTask(
                task_id=f"{case_id}_task_maintenance_planning",
                task_type="maintenance_planning",
                task_name="Prepare controlled compressor inspection or intervention",
                status="open",
                required_role="maintenance_planner",
                trigger="short failure horizon with intervention resources available",
                source_layer="Layer 3",
                evidence_refs=["predictive_maintenance", "inventory_and_resources"],
                details={
                    "estimated_time_to_failure_hours": (
                        canonical_context.predictive_evidence.estimated_time_to_failure_hours
                    ),
                    "spare_part_available": (
                        canonical_context.maintenance_resources.spare_part_available
                    ),
                    "specialist_available": (
                        canonical_context.maintenance_resources.specialist_technician_available_next_shift
                    ),
                    "created_at": timestamp,
                },
            )
        )

    if blockers:
        tasks.append(
            CaseTask(
                task_id=f"{case_id}_task_blocker_resolution",
                task_type="blocker_resolution",
                task_name="Resolve missing evidence or resource blockers",
                status="open",
                required_role="case_owner",
                trigger="case has blockers before decision readiness",
                source_layer="Layer 3",
                evidence_refs=[canonical_context.context_id],
                details={
                    "blockers": blockers,
                    "created_at": timestamp,
                },
            )
        )

    return tasks


def _build_milestones(
    *,
    canonical_context: CanonicalCaseContext,
    timestamp: str,
    human_review_required: bool,
    maintenance_planning_required: bool,
    decision_ready: bool,
    blockers: list[str],
) -> list[CaseMilestone]:
    """Build lifecycle milestones for the case."""

    case_id = canonical_context.case_id

    return [
        CaseMilestone(
            milestone_id=f"{case_id}_ms_external_evidence_complete",
            milestone_name="External evidence complete",
            status="reached",
            source_layer="Layer 1",
            reached_at=timestamp,
            criteria=[
                "asset registry payload present",
                "predictive maintenance payload present",
                "production planning payload present",
                "policy payload present",
            ],
            evidence_refs=canonical_context.source_names,
        ),
        CaseMilestone(
            milestone_id=f"{case_id}_ms_canonical_context_available",
            milestone_name="Canonical context available",
            status="reached",
            source_layer="Layer 2",
            reached_at=timestamp,
            criteria=[
                "canonical asset context built",
                "predictive evidence normalized",
                "operational context normalized",
                "governance policy normalized",
            ],
            evidence_refs=[canonical_context.context_id],
        ),
        CaseMilestone(
            milestone_id=f"{case_id}_ms_human_review_identified",
            milestone_name="Human review identified",
            status="reached" if human_review_required else "not_required",
            source_layer="Layer 3",
            reached_at=timestamp if human_review_required else None,
            criteria=[
                "high criticality or high severity",
                "policy requires accountable human review",
            ],
            evidence_refs=["policy_governance", canonical_context.context_id],
        ),
        CaseMilestone(
            milestone_id=f"{case_id}_ms_maintenance_planning_required",
            milestone_name="Maintenance planning required",
            status="reached" if maintenance_planning_required else "not_required",
            source_layer="Layer 3",
            reached_at=timestamp if maintenance_planning_required else None,
            criteria=[
                "short failure horizon",
                "resources support controlled planning",
            ],
            evidence_refs=["predictive_maintenance", "inventory_and_resources"],
        ),
        CaseMilestone(
            milestone_id=f"{case_id}_ms_decision_ready",
            milestone_name="Decision-ready case package",
            status="reached" if decision_ready else "blocked",
            source_layer="Layer 3",
            reached_at=timestamp if decision_ready else None,
            criteria=[
                "external evidence received",
                "canonical context built",
                "human review requirement evaluated",
                "maintenance planning requirement evaluated",
                "no unresolved blockers",
            ],
            evidence_refs=[canonical_context.context_id],
        ),
    ]


def _requires_maintenance_planning(context: CanonicalCaseContext) -> bool:
    """Return whether a maintenance planning task should be opened."""

    short_failure_horizon = (
        context.predictive_evidence.estimated_time_to_failure_hours <= 72
    )
    high_confidence = context.predictive_evidence.confidence_score >= 0.75
    resources_available = context.maintenance_resources.intervention_feasible

    return short_failure_horizon and high_confidence and resources_available


def _build_blockers(context: CanonicalCaseContext) -> list[str]:
    """Build case blockers from data quality and resource constraints."""

    blockers: list[str] = []

    blockers.extend(context.data_quality_flags)

    if not context.maintenance_resources.spare_part_available:
        blockers.append("spare_part_not_available")
    if not context.maintenance_resources.specialist_technician_available_next_shift:
        blockers.append("specialist_technician_not_available")
    if context.predictive_evidence.confidence_score < 0.5:
        blockers.append("low_predictive_confidence")

    return blockers


def _utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()
