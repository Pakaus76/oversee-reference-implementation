"""Tests for paper-aligned Layer 2 contextualization rules."""

from __future__ import annotations

import json

from oversee.case_context import build_canonical_case_context
from oversee.case_context.contextualization_rules import run_layer2_contextualization
from oversee.integration import build_sample_predictive_alert_request, run_layer1_evidence_pipeline


def test_layer2_builds_contextualization_rule_trace() -> None:
    """Layer 2 should produce a transparent DMN-like rule trace."""

    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)
    canonical_context = build_canonical_case_context(layer1_result.evidence_package)
    layer2_result = run_layer2_contextualization(canonical_context)

    assert layer2_result.case_id == canonical_context.case_id
    assert layer2_result.asset_id == "COMP-001"
    assert len(layer2_result.rule_trace) == 8
    assert all(rule.rule_id.startswith("L2_R") for rule in layer2_result.rule_trace)
    assert all(rule.condition.startswith("IF ") for rule in layer2_result.rule_trace)


def test_layer2_derived_context_contains_expected_decision_factors() -> None:
    """Layer 2 should derive expected contextual decision factors."""

    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)
    canonical_context = build_canonical_case_context(layer1_result.evidence_package)
    layer2_result = run_layer2_contextualization(canonical_context)
    derived = layer2_result.derived_context

    assert derived["technical_urgency"] == "high"
    assert derived["asset_escalation"] == "required"
    assert derived["operational_constraint"] == "high"
    assert derived["downtime_window"] == "near"
    assert derived["intervention_feasible"] is True
    assert derived["recurrence_risk"] == "high"
    assert derived["human_review_required"] is True
    assert derived["layer2_decision_ready"] is True
    assert layer2_result.layer2_ready is True


def test_layer2_outputs_avoid_old_bridge_terminology() -> None:
    """Layer 2 outputs should not expose old bridge terminology."""

    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)
    canonical_context = build_canonical_case_context(layer1_result.evidence_package)
    layer2_result = run_layer2_contextualization(canonical_context)

    serialized = json.dumps(layer2_result.to_dict(), ensure_ascii=False).lower()

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
