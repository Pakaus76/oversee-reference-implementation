"""Tests for OVERSEE Layer 4 DMN-like rules and recommendation paths."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_management import build_case_management_state
from oversee.decision_rules import evaluate_dmn_like_rules, run_recommendation_paths
from oversee.external_sources import build_compressor_external_source_package


def _build_layer4_objects():
    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)
    rule_evaluation = evaluate_dmn_like_rules(canonical_context, case_state)
    recommendation_bundle = run_recommendation_paths(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )
    return canonical_context, case_state, rule_evaluation, recommendation_bundle


def test_layer4_dmn_like_rules_produce_expected_governance_outputs() -> None:
    """Layer 4 should produce explicit decision-rule outputs."""

    canonical_context, case_state, rule_evaluation, _ = _build_layer4_objects()

    assert rule_evaluation.case_id == canonical_context.case_id
    assert rule_evaluation.asset_id == canonical_context.asset.asset_id
    assert rule_evaluation.source_case_state == case_state.lifecycle_stage
    assert len(rule_evaluation.rules) == 6
    assert rule_evaluation.final_priority == "high"
    assert rule_evaluation.recommended_execution_mode == "controlled_planning"
    assert rule_evaluation.human_review_required is True
    assert rule_evaluation.intervention_feasible is True
    assert rule_evaluation.triggered_rule_count >= 4


def test_layer4_recommendation_paths_include_deterministic_anchor() -> None:
    """Layer 4 should connect rule outputs with recommendation paths."""

    _, _, rule_evaluation, recommendation_bundle = _build_layer4_objects()

    path_names = {output.path_name for output in recommendation_bundle.path_outputs}

    assert recommendation_bundle.decision_rule_evaluation_id == rule_evaluation.evaluation_id
    assert recommendation_bundle.path_count == 2
    assert "deterministic_anchor" in path_names
    assert "dmn_like_governance_summary" in path_names


def test_layer4_recommendation_path_preserves_rule_context() -> None:
    """Recommendation path output should preserve governance context."""

    _, _, _, recommendation_bundle = _build_layer4_objects()

    deterministic_output = next(
        output
        for output in recommendation_bundle.path_outputs
        if output.path_name == "deterministic_anchor"
    )

    assert deterministic_output.status == "completed"
    assert deterministic_output.recommendation["dmn_like_final_priority"] == "high"
    assert deterministic_output.recommendation["recommended_execution_mode"] == "controlled_planning"
    assert deterministic_output.recommendation["human_review_required"] is True


def test_layer4_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 4 outputs should not expose old bridge terminology."""

    _, _, rule_evaluation, recommendation_bundle = _build_layer4_objects()

    serialized = json.dumps(
        {
            "rule_evaluation": rule_evaluation.to_dict(),
            "recommendation_bundle": recommendation_bundle.to_dict(),
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
