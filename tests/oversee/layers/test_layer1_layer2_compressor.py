"""Tests for OVERSEE Layer 1 external sources and Layer 2 canonical context."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.external_sources import build_compressor_external_source_package


def test_layer1_external_source_package_contains_expected_sources() -> None:
    """Layer 1 should expose the compressor case as external source payloads."""

    source_package = build_compressor_external_source_package()
    source_names = {payload.source_name for payload in source_package.payloads}

    assert source_package.source_count == 7
    assert source_package.asset_id
    assert "asset_registry" in source_names
    assert "sensor_historian" in source_names
    assert "predictive_maintenance" in source_names
    assert "maintenance_history" in source_names
    assert "production_planning" in source_names
    assert "inventory_and_resources" in source_names
    assert "policy_governance" in source_names


def test_layer2_canonical_context_contains_decision_relevant_fields() -> None:
    """Layer 2 should build a canonical compressor context from Layer 1."""

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)

    assert canonical_context.case_id == source_package.case_id
    assert canonical_context.asset.asset_id == source_package.asset_id
    assert canonical_context.asset.criticality_score >= 3
    assert canonical_context.predictive_evidence.estimated_time_to_failure_hours > 0
    assert 0 <= canonical_context.predictive_evidence.confidence_score <= 1
    assert canonical_context.operational_context.production_load_pct >= 0
    assert canonical_context.source_payload_count == 7
    assert canonical_context.governance_policy.computed_human_review_required is True
    assert "human_review_required" in canonical_context.key_risk_drivers


def test_layer1_layer2_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 1 and Layer 2 outputs should not expose old bridge terminology."""

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)

    serialized = json.dumps(
        {
            "source_package": source_package.to_dict(),
            "canonical_context": canonical_context.to_dict(),
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
