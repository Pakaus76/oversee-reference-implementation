"""Tests for Fernando-aligned Layer 3 case lifecycle demo."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_context.contextualization_rules import run_layer2_contextualization
from oversee.case_management import build_case_management_state
from oversee.integration import build_sample_predictive_alert_request, run_layer1_evidence_pipeline


def _build_layer3_flow():
    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)
    canonical_context = build_canonical_case_context(layer1_result.evidence_package)
    layer2_result = run_layer2_contextualization(canonical_context)
    case_state = build_case_management_state(canonical_context)

    return {
        "alert_request": alert_request,
        "layer1_result": layer1_result,
        "canonical_context": canonical_context,
        "layer2_result": layer2_result,
        "case_state": case_state,
    }


def test_layer3_builds_cmmn_inspired_case_lifecycle_from_layer2_context() -> None:
    """Layer 3 should build a case lifecycle from contextualized evidence."""

    flow = _build_layer3_flow()
    layer1_result = flow["layer1_result"]
    layer2_result = flow["layer2_result"]
    case_state = flow["case_state"]

    assert layer1_result.validation_report["valid"] is True
    assert layer2_result.layer2_ready is True
    assert case_state.case_status == "open"
    assert case_state.lifecycle_stage == "decision_ready"
    assert case_state.human_review_required is True
    assert case_state.maintenance_planning_required is True
    assert case_state.decision_ready is True
    assert len(case_state.events) >= 5
    assert len(case_state.tasks) >= 2
    assert len(case_state.milestones) >= 5
    assert case_state.blockers == []


def test_layer3_lifecycle_trace_is_inspectable() -> None:
    """Layer 3 should expose an inspectable lifecycle trace."""

    flow = _build_layer3_flow()
    case_state = flow["case_state"]

    lifecycle_trace = case_state.lifecycle_trace()
    serialized = json.dumps(lifecycle_trace, ensure_ascii=False).lower()

    assert isinstance(lifecycle_trace, list)
    assert len(lifecycle_trace) >= 5
    assert "evidence" in serialized
    assert "decision" in serialized


def test_layer3_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 3 outputs should not expose old bridge terminology."""

    flow = _build_layer3_flow()

    serialized = json.dumps(
        {
            "alert_request": flow["alert_request"],
            "layer1_result": flow["layer1_result"].to_dict(),
            "canonical_context": flow["canonical_context"].to_dict(),
            "layer2_result": flow["layer2_result"].to_dict(),
            "case_state": flow["case_state"].to_dict(),
            "case_lifecycle_trace": flow["case_state"].lifecycle_trace(),
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
