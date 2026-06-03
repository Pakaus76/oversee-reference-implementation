"""Offline-safe tests for the Generative Digital Factory workbench."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_management import build_case_management_state
from oversee.decision_rules import (
    evaluate_dmn_like_rules,
    run_live_generative_recommendation,
    run_recommendation_paths,
)
from oversee.digital_factory import run_generative_digital_factory_source_generation
from oversee.reporting.generative_comparison import (
    build_advanced_governed_package_dict,
    compare_deterministic_and_generative_outputs,
)
from oversee.reporting.governed_recommendation_package import build_governed_recommendation_package


def _build_offline_workbench():
    factory_result = run_generative_digital_factory_source_generation(allow_live_call=False)
    source_package = factory_result.source_package
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
    return factory_result, canonical_context, case_state, rule_evaluation, live_result, comparison, advanced_package


def test_generative_digital_factory_has_offline_fallback_source_package() -> None:
    """Generative Digital Factory should be offline-safe for CI."""

    factory_result, canonical_context, _, _, _, _, _ = _build_offline_workbench()

    assert factory_result.model_call_attempted is False
    assert factory_result.model_call_successful is False
    assert factory_result.fallback_used is True
    assert factory_result.fallback_reason == "live_call_not_allowed"
    assert factory_result.source_package.source_count == 7
    assert canonical_context.asset.asset_id == factory_result.source_package.asset_id


def test_generative_digital_factory_output_flows_through_all_layers() -> None:
    """Fallback or live source package should flow through all five layers."""

    _, canonical_context, case_state, rule_evaluation, live_result, comparison, advanced_package = _build_offline_workbench()

    assert canonical_context.source_payload_count == 7
    assert case_state.decision_ready is True
    assert rule_evaluation.final_priority == "high"
    assert live_result.fallback_used is True
    assert comparison.priority_alignment is True
    assert advanced_package["layer_completion"]["layer_5_governed_package"] is True


def test_generative_digital_factory_outputs_avoid_old_bridge_terminology() -> None:
    """Advanced workbench outputs should not expose old bridge terminology."""

    factory_result, canonical_context, case_state, rule_evaluation, live_result, comparison, advanced_package = _build_offline_workbench()

    serialized = json.dumps(
        {
            "factory_result": factory_result.to_dict(),
            "canonical_context": canonical_context.to_dict(),
            "case_state": case_state.to_dict(),
            "rule_evaluation": rule_evaluation.to_dict(),
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
