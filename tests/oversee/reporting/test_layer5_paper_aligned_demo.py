"""Tests for paper-aligned Layer 5 governed package demo."""

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
from oversee.reporting.generative_comparison import (
    build_advanced_governed_package_dict,
    compare_deterministic_and_generative_outputs,
)
from oversee.reporting.governed_recommendation_package import build_governed_recommendation_package


def _build_layer5_flow():
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
    base_package = build_governed_recommendation_package(
        source_package=layer1_result.evidence_package,
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        recommendation_bundle=recommendation_bundle,
    )
    advanced_package = build_advanced_governed_package_dict(
        base_package=base_package,
        live_result=live_result,
        comparison=comparison,
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
        "base_package": base_package,
        "advanced_package": advanced_package,
    }


def test_layer5_builds_governed_package_from_layers_1_to_4() -> None:
    """Layer 5 should build a governed package from the full prior flow."""

    flow = _build_layer5_flow()
    advanced_package = flow["advanced_package"]

    assert flow["layer1_result"].validation_report["valid"] is True
    assert flow["layer2_result"].layer2_ready is True
    assert flow["case_state"].decision_ready is True
    assert flow["rule_evaluation"].final_priority == "high"
    assert flow["comparison"].priority_alignment is True
    assert bool(advanced_package) is True
    assert advanced_package["layer_completion"]["layer_5_governed_package"] is True


def test_layer5_preserves_generative_comparison_metadata() -> None:
    """Layer 5 should preserve generative comparison and fallback metadata."""

    flow = _build_layer5_flow()
    advanced_package = flow["advanced_package"]
    serialized = json.dumps(advanced_package, ensure_ascii=False).lower()

    assert flow["live_result"].fallback_used is True
    assert "generative" in serialized
    assert "comparison" in serialized
    assert "fallback" in serialized
    assert "traceability" in serialized


def test_layer5_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 5 outputs should not expose old bridge terminology."""

    flow = _build_layer5_flow()

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
            "advanced_package": flow["advanced_package"],
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
