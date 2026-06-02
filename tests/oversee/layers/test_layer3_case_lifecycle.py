"""Tests for OVERSEE Layer 3 CMMN-inspired case lifecycle."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_management import build_case_management_state
from oversee.external_sources import build_compressor_external_source_package


def test_layer3_case_lifecycle_builds_expected_state() -> None:
    """Layer 3 should build an inspectable case-management state."""

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)

    assert case_state.case_id == canonical_context.case_id
    assert case_state.asset_id == canonical_context.asset.asset_id
    assert case_state.case_status == "open"
    assert case_state.lifecycle_stage == "decision_ready"
    assert case_state.human_review_required is True
    assert case_state.maintenance_planning_required is True
    assert case_state.decision_ready is True
    assert case_state.event_count == 7
    assert case_state.task_count >= 2
    assert case_state.milestone_count == 5


def test_layer3_lifecycle_trace_preserves_layer_progression() -> None:
    """Layer 3 trace should explicitly reference Layer 1 and Layer 2 evidence."""

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)

    event_types = [event.event_type for event in case_state.events]
    source_layers = {event.source_layer for event in case_state.events}

    assert event_types == [
        "case_opened",
        "external_evidence_received",
        "canonical_context_built",
        "risk_assessment_completed",
        "human_review_requirement_identified",
        "maintenance_planning_task_created",
        "decision_milestone_reached",
    ]
    assert "Layer 1" in source_layers
    assert "Layer 2" in source_layers
    assert "Layer 3" in source_layers


def test_layer3_case_tasks_include_human_review_and_planning() -> None:
    """Layer 3 should create tasks for human review and maintenance planning."""

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)

    task_types = {task.task_type for task in case_state.tasks}

    assert "human_review" in task_types
    assert "maintenance_planning" in task_types


def test_layer3_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 3 outputs should not expose old bridge terminology."""

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)

    serialized = json.dumps(case_state.to_dict(), ensure_ascii=False).lower()

    forbidden_terms = [
        "do_bridge",
        "bridgepayload",
        "bridge payload",
        "decision orchestrator bridge",
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
