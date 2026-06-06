"""Tests for paper-aligned Layer 4 decision and recommendation demo."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_context.contextualization_rules import run_layer2_contextualization
from oversee.case_management import build_case_management_state
from oversee.decision_rules import (
    evaluate_dmn_like_rules,
    run_live_generative_recommendation,
    run_recommendation_paths,
)
from oversee.integration import build_sample_predictive_alert_request, run_layer1_evidence_pipeline
from oversee.reporting.generative_comparison import compare_deterministic_and_generative_outputs



def _recommendation_path_count(recommendation_bundle) -> int:
    """Return recommendation path count from the bundle to keep the test implementation-tolerant."""

    bundle_dict = recommendation_bundle.to_dict()

    for key in ("recommendation_path_count", "path_count"):
        value = bundle_dict.get(key)
        if isinstance(value, int):
            return value

    for key in ("recommendation_paths", "paths", "path_outputs", "outputs"):
        value = bundle_dict.get(key)
        if isinstance(value, list):
            return len(value)

    return 0


def _build_layer4_flow():
    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)
    canonical_context = build_canonical_case_context(layer1_result.evidence_package)
    layer2_result = run_layer2_contextualization(canonical_context)
    case_state = build_case_management_state(canonical_context)
    rule_evaluation = evaluate_dmn_like_rules(canonical_context, case_state)
    recommendation_bundle = run_recommendation_paths(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )
    live_result = run_live_generative_recommendation(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        allow_live_call=False,
    )
    comparison = compare_deterministic_and_generative_outputs(
        recommendation_bundle=recommendation_bundle,
        live_result=live_result,
    )

    return {
        "alert_request": alert_request,
        "layer1_result": layer1_result,
        "canonical_context": canonical_context,
        "layer2_result": layer2_result,
        "case_state": case_state,
        "rule_evaluation": rule_evaluation,
        "recommendation_bundle": recommendation_bundle,
        "live_result": live_result,
        "comparison": comparison,
    }


def test_layer4_evaluates_dmn_like_rules_and_recommendation_paths() -> None:
    """Layer 4 should evaluate decision rules and deterministic paths."""

    flow = _build_layer4_flow()
    rule_evaluation = flow["rule_evaluation"]
    recommendation_bundle = flow["recommendation_bundle"]

    assert flow["layer1_result"].validation_report["valid"] is True
    assert flow["layer2_result"].layer2_ready is True
    assert flow["case_state"].decision_ready is True
    assert rule_evaluation.final_priority == "high"
    assert rule_evaluation.recommended_execution_mode == "controlled_planning"
    assert rule_evaluation.triggered_rule_count >= 1
    assert _recommendation_path_count(recommendation_bundle) >= 1


def test_layer4_offline_generative_path_uses_fallback_and_comparison() -> None:
    """Layer 4 tests should remain offline-safe while preserving comparison."""

    flow = _build_layer4_flow()
    live_result = flow["live_result"]
    comparison = flow["comparison"]

    assert live_result.model_call_attempted is False
    assert live_result.model_call_successful is False
    assert live_result.fallback_used is True
    assert comparison.priority_alignment is True
    assert comparison.protected_fact_violation_count == 0


def test_layer4_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 4 outputs should not expose old bridge terminology."""

    flow = _build_layer4_flow()

    serialized = json.dumps(
        {
            "alert_request": flow["alert_request"],
            "layer1_result": flow["layer1_result"].to_dict(),
            "canonical_context": flow["canonical_context"].to_dict(),
            "layer2_result": flow["layer2_result"].to_dict(),
            "case_state": flow["case_state"].to_dict(),
            "rule_evaluation": flow["rule_evaluation"].to_dict(),
            "recommendation_bundle": flow["recommendation_bundle"].to_dict(),
            "live_result": flow["live_result"].to_dict(),
            "comparison": flow["comparison"].to_dict(),
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
