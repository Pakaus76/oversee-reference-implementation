"""Offline-safe tests for the live generative OVERSEE integration."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_management import build_case_management_state
from oversee.decision_rules import (
    evaluate_dmn_like_rules,
    run_live_generative_recommendation,
    run_recommendation_paths,
)
from oversee.external_sources import build_compressor_external_source_package
from oversee.reporting.generative_comparison import (
    build_advanced_governed_package_dict,
    compare_deterministic_and_generative_outputs,
)
from oversee.reporting.governed_recommendation_package import (
    build_governed_recommendation_package,
)


def _build_objects():
    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
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
        source_package=source_package,
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
    return live_result, comparison, advanced_package


def test_live_generative_path_has_governed_offline_fallback() -> None:
    """Offline test should not require API access."""

    live_result, _, _ = _build_objects()

    assert live_result.model_call_attempted is False
    assert live_result.model_call_successful is False
    assert live_result.fallback_used is True
    assert live_result.fallback_reason == "live_call_not_allowed"
    assert live_result.parsed_recommendation["priority"] == "high"
    assert live_result.parsed_recommendation["human_review_required"] is True


def test_deterministic_vs_generative_comparison_is_available() -> None:
    """Comparison should exist even when the generative path uses fallback."""

    _, comparison, _ = _build_objects()

    assert comparison.case_id == "DF_COMP_001_CONTROLLED_MONITORING"
    assert comparison.deterministic_priority == "high"
    assert comparison.generative_priority == "high"
    assert comparison.priority_alignment is True
    assert comparison.protected_fact_violation_count == 0


def test_advanced_governed_package_contains_generative_metadata() -> None:
    """Layer 5 package should be enrichable with generative evidence."""

    live_result, comparison, advanced_package = _build_objects()

    assert advanced_package["generative_ai_summary"]["live_generative_result_id"] == (
        live_result.result_id
    )
    assert advanced_package["generative_ai_summary"]["fallback_used"] is True
    assert advanced_package["deterministic_vs_generative_comparison"]["comparison_id"] == (
        comparison.comparison_id
    )
    assert "live_generative_priority" in advanced_package["final_recommendation"]
    assert "generative_path_fallback_used" in advanced_package["final_recommendation"]


def test_live_generative_outputs_avoid_old_bridge_terminology() -> None:
    """Advanced outputs should not expose old bridge terminology."""

    live_result, comparison, advanced_package = _build_objects()

    serialized = json.dumps(
        {
            "live_result": live_result.to_dict(),
            "comparison": comparison.to_dict(),
            "advanced_package": advanced_package,
        },
        ensure_ascii=False,
    ).lower()

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
