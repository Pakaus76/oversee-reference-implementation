"""Tests for OVERSEE Layer 5 governed recommendation package."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_management import build_case_management_state
from oversee.decision_rules import evaluate_dmn_like_rules, run_recommendation_paths
from oversee.external_sources import build_compressor_external_source_package
from oversee.reporting.governed_recommendation_package import (
    build_execution_manifest,
    build_governed_recommendation_package,
    build_reviewer_summary_markdown,
)


def _build_layer5_package():
    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)
    rule_evaluation = evaluate_dmn_like_rules(canonical_context, case_state)
    recommendation_bundle = run_recommendation_paths(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )
    governed_package = build_governed_recommendation_package(
        source_package=source_package,
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        recommendation_bundle=recommendation_bundle,
    )
    return governed_package


def test_layer5_governed_package_contains_complete_layer_chain() -> None:
    """Layer 5 should package all five layers."""

    package = _build_layer5_package()

    assert package.case_id == "DF_COMP_001_CONTROLLED_MONITORING"
    assert package.asset_id == "COMP-001"
    assert package.layer_completion["layer_1_external_sources"] is True
    assert package.layer_completion["layer_2_canonical_context"] is True
    assert package.layer_completion["layer_3_case_lifecycle"] is True
    assert package.layer_completion["layer_4_decision_rules"] is True
    assert package.layer_completion["layer_5_governed_package"] is True
    assert package.traceability_count == 6


def test_layer5_final_recommendation_preserves_governance_fields() -> None:
    """Final recommendation should preserve governance-relevant fields."""

    package = _build_layer5_package()
    recommendation = package.final_recommendation

    assert recommendation["priority"] == "high"
    assert recommendation["recommended_execution_mode"] == "controlled_planning"
    assert recommendation["human_review_required"] is True
    assert recommendation["intervention_feasible"] is True
    assert recommendation["decision_ready"] is True
    assert "recommended_action" in recommendation
    assert "rationale" in recommendation


def test_layer5_reviewer_summary_and_manifest_are_generated() -> None:
    """Reviewer summary and manifest should be generated from package metadata."""

    package = _build_layer5_package()
    summary = build_reviewer_summary_markdown(package)
    manifest = build_execution_manifest(
        output_dir="outputs/example",
        package=package,
        generated_files=[
            "01_external_source_payloads.json",
            "02_canonical_case_context.json",
            "03_case_lifecycle_trace.json",
            "03_output_layer3_case_management_state.json",
            "04_output_layer4_dmn_decision_evaluation.json",
            "04_output_layer4_recommendation_path_outputs.json",
            "05_final_governed_recommendation_package.json",
            "05_traceability_index.json",
            "05_reviewer_summary.md",
            "05_execution_manifest.json",
        ],
    )

    assert "# OVERSEE governed recommendation package" in summary
    assert "Final recommendation" in summary
    assert manifest["status"] == "completed"
    assert manifest["generated_files"][-1] == "05_execution_manifest.json"


def test_layer5_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 5 outputs should not expose old bridge terminology."""

    package = _build_layer5_package()

    serialized = json.dumps(package.to_dict(), ensure_ascii=False).lower()

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
