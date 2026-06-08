"""Layer 5 governed packaging and traceability for OVERSEE.

Purpose:
    Assemble the final governed recommendation package from the evidence,
    context, case lifecycle, decision-rule evaluation and recommendation-path
    outputs.

Architectural role:
    Layer 5 does not decide the case again. It packages the already-governed
    decision into a reviewer-facing and audit-ready structure, including
    traceability entries, execution metadata and final recommendation fields.

Final output:
    05_final_governed_recommendation_package.json
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from oversee.case_context import CanonicalCaseContext
from oversee.case_management import CaseManagementState
from oversee.decision_rules import DecisionRuleEvaluation, RecommendationPathBundle
from oversee.external_sources import ExternalSourcePackage


@dataclass(slots=True)
class TraceabilityEntry:
    """One traceability entry linking sources, layers and generated artifacts.
    
    Traceability entries make it possible to see which layer produced which piece
    of evidence or reasoning and where that information is persisted.
    """

    trace_id: str
    layer: str
    artifact_name: str
    artifact_type: str
    source_refs: list[str]
    summary: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class GovernedRecommendationPackage:
    """Complete Layer 5 governed package for one OVERSEE case.
    
    The package combines the final recommendation, governance summary,
    traceability index, reviewer summary and supporting references needed for
    human review and workflow handoff.
    """

    package_id: str
    case_id: str
    asset_id: str
    generated_at: str
    final_recommendation: dict[str, Any]
    governance_summary: dict[str, Any]
    traceability_index: list[TraceabilityEntry]
    layer_completion: dict[str, bool]
    reviewer_notes: list[str] = field(default_factory=list)
    package_version: str = "0.1.0"

    @property
    def traceability_count(self) -> int:
        """Return number of traceability entries."""

        return len(self.traceability_index)

    def traceability_dicts(self) -> list[dict[str, Any]]:
        """Return traceability entries as dictionaries."""

        return [entry.to_dict() for entry in self.traceability_index]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        data = asdict(self)
        data["traceability_index"] = self.traceability_dicts()
        data["traceability_count"] = self.traceability_count
        return data


def build_governed_recommendation_package(
    *,
    source_package: ExternalSourcePackage,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
    recommendation_bundle: RecommendationPathBundle,
) -> GovernedRecommendationPackage:
    """Build the Layer 5 governed recommendation package.
    
    The function receives all upstream layer outputs and assembles the final
    reviewable package. It does not overwrite Layer 4 decisions; it preserves them
    with traceability and reviewer-facing explanation.
    """

    generated_at = _utc_now()
    deterministic_recommendation = _find_path_recommendation(
        recommendation_bundle,
        path_name="deterministic_anchor",
    )
    governance_summary = _build_governance_summary(
        source_package=source_package,
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        recommendation_bundle=recommendation_bundle,
    )
    final_recommendation = _build_final_recommendation(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        deterministic_recommendation=deterministic_recommendation,
    )
    traceability_index = _build_traceability_index(
        source_package=source_package,
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        recommendation_bundle=recommendation_bundle,
    )

    return GovernedRecommendationPackage(
        package_id=f"governed_package_{canonical_context.case_id}",
        case_id=canonical_context.case_id,
        asset_id=canonical_context.asset.asset_id,
        generated_at=generated_at,
        final_recommendation=final_recommendation,
        governance_summary=governance_summary,
        traceability_index=traceability_index,
        layer_completion={
            "layer_1_external_sources": source_package.source_count > 0,
            "layer_2_canonical_context": canonical_context.source_payload_count > 0,
            "layer_3_case_lifecycle": case_state.event_count > 0,
            "layer_4_decision_rules": len(rule_evaluation.rules) > 0,
            "layer_5_governed_package": True,
        },
        reviewer_notes=[
            "This package is generated from an end-to-end five-layer OVERSEE execution.",
            "The package is inspectable and preserves source-to-recommendation traceability.",
            "The current recommendation path uses the migrated deterministic anchor plus explicit DMN-like governance context.",
        ],
    )


def build_reviewer_summary_markdown(package: GovernedRecommendationPackage) -> str:
    """Build a compact reviewer-facing Markdown summary.
    
    The summary translates the governed package into a human-readable view for
    maintenance, operations or review stakeholders.
    """

    recommendation = package.final_recommendation
    governance = package.governance_summary

    lines = [
        "# OVERSEE governed recommendation package",
        "",
        f"Package ID: `{package.package_id}`",
        f"Case ID: `{package.case_id}`",
        f"Asset ID: `{package.asset_id}`",
        f"Generated at: `{package.generated_at}`",
        "",
        "## Final recommendation",
        "",
        f"- Recommended action: {recommendation.get('recommended_action')}",
        f"- Priority: {recommendation.get('priority')}",
        f"- Execution mode: {recommendation.get('recommended_execution_mode')}",
        f"- Human review required: {recommendation.get('human_review_required')}",
        f"- Decision ready: {recommendation.get('decision_ready')}",
        "",
        "## Governance summary",
        "",
        f"- Source payloads: {governance.get('source_payload_count')}",
        f"- Triggered rules: {governance.get('triggered_rule_count')}",
        f"- Recommendation paths: {governance.get('recommendation_path_count')}",
        f"- Traceability entries: {package.traceability_count}",
        "",
        "## Layer completion",
        "",
        "| Layer | Complete |",
        "|---|---:|",
    ]

    for layer_name, complete in package.layer_completion.items():
        lines.append(f"| {layer_name} | {complete} |")

    lines.extend(
        [
            "",
            "## Reviewer notes",
            "",
        ]
    )

    for note in package.reviewer_notes:
        lines.append(f"- {note}")

    lines.extend(
        [
            "",
            "## Traceability overview",
            "",
            "| Layer | Artifact | Summary |",
            "|---|---|---|",
        ]
    )

    for entry in package.traceability_index:
        lines.append(f"| {entry.layer} | {entry.artifact_name} | {entry.summary} |")

    return "\n".join(lines)


def build_execution_manifest(
    *,
    output_dir: str,
    package: GovernedRecommendationPackage,
    generated_files: list[str],
) -> dict[str, Any]:
    """Build an execution manifest for the output directory.
    
    The manifest records generated files, scenario metadata and execution context
    so reviewers can audit what was produced in one run.
    """

    return {
        "manifest_version": "0.1.0",
        "created_at": _utc_now(),
        "output_dir": output_dir,
        "case_id": package.case_id,
        "asset_id": package.asset_id,
        "package_id": package.package_id,
        "generated_files": generated_files,
        "layer_completion": package.layer_completion,
        "traceability_count": package.traceability_count,
        "status": "completed",
    }


def _build_final_recommendation(
    *,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
    deterministic_recommendation: dict[str, Any],
) -> dict[str, Any]:
    """Build the final governed recommendation view."""

    action = deterministic_recommendation.get(
        "action",
        "Prepare controlled compressor inspection or intervention.",
    )
    anchor_priority = deterministic_recommendation.get("priority")

    return {
        "case_id": canonical_context.case_id,
        "asset_id": canonical_context.asset.asset_id,
        "recommended_action": action,
        "priority": rule_evaluation.final_priority,
        "deterministic_anchor_priority": anchor_priority,
        "recommended_execution_mode": rule_evaluation.recommended_execution_mode,
        "human_review_required": rule_evaluation.human_review_required,
        "intervention_feasible": rule_evaluation.intervention_feasible,
        "decision_ready": case_state.decision_ready,
        "key_risk_drivers": canonical_context.key_risk_drivers,
        "rationale": (
            "Final recommendation combines explicit DMN-like governance outputs, "
            "case lifecycle readiness and the migrated deterministic anchor recommendation."
        ),
    }


def _build_governance_summary(
    *,
    source_package: ExternalSourcePackage,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
    recommendation_bundle: RecommendationPathBundle,
) -> dict[str, Any]:
    """Build compact governance summary for Layer 5."""

    return {
        "source_payload_count": source_package.source_count,
        "source_names": [payload.source_name for payload in source_package.payloads],
        "canonical_context_id": canonical_context.context_id,
        "case_lifecycle_stage": case_state.lifecycle_stage,
        "case_event_count": case_state.event_count,
        "case_task_count": case_state.task_count,
        "case_milestone_count": case_state.milestone_count,
        "triggered_rule_count": rule_evaluation.triggered_rule_count,
        "decision_rule_evaluation_id": rule_evaluation.evaluation_id,
        "recommendation_path_count": recommendation_bundle.path_count,
        "human_review_required": rule_evaluation.human_review_required,
        "decision_ready": case_state.decision_ready,
    }


def _build_traceability_index(
    *,
    source_package: ExternalSourcePackage,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
    recommendation_bundle: RecommendationPathBundle,
) -> list[TraceabilityEntry]:
    """Build traceability entries across the five layers."""

    source_names = [payload.source_name for payload in source_package.payloads]

    return [
        TraceabilityEntry(
            trace_id=f"{source_package.case_id}_trace_001_layer_1",
            layer="Layer 1",
            artifact_name="external_source_payloads",
            artifact_type="external_source_package",
            source_refs=source_names,
            summary="Industrial information is exposed as external source payloads.",
        ),
        TraceabilityEntry(
            trace_id=f"{source_package.case_id}_trace_002_layer_2",
            layer="Layer 2",
            artifact_name="canonical_case_context",
            artifact_type="canonical_context",
            source_refs=source_names,
            summary="External payloads are normalized into a canonical compressor case context.",
        ),
        TraceabilityEntry(
            trace_id=f"{source_package.case_id}_trace_003_layer_3",
            layer="Layer 3",
            artifact_name="case_management_state",
            artifact_type="case_lifecycle",
            source_refs=[canonical_context.context_id],
            summary="The compressor case is managed through events, tasks and milestones.",
        ),
        TraceabilityEntry(
            trace_id=f"{source_package.case_id}_trace_004_layer_4_rules",
            layer="Layer 4",
            artifact_name="dmn_like_decision_evaluation",
            artifact_type="decision_rules",
            source_refs=[canonical_context.context_id, case_state.case_id],
            summary="Explicit DMN-like rules evaluate urgency, criticality, feasibility, review and priority.",
        ),
        TraceabilityEntry(
            trace_id=f"{source_package.case_id}_trace_005_layer_4_paths",
            layer="Layer 4",
            artifact_name="recommendation_path_outputs",
            artifact_type="recommendation_paths",
            source_refs=[rule_evaluation.evaluation_id],
            summary="Recommendation paths produce decision outputs under governance context.",
        ),
        TraceabilityEntry(
            trace_id=f"{source_package.case_id}_trace_006_layer_5",
            layer="Layer 5",
            artifact_name="governed_recommendation_package",
            artifact_type="governed_package",
            source_refs=[
                canonical_context.context_id,
                case_state.case_id,
                rule_evaluation.evaluation_id,
                recommendation_bundle.bundle_id,
            ],
            summary="All evidence is packaged into a governed recommendation with traceability.",
        ),
    ]


def _find_path_recommendation(
    recommendation_bundle: RecommendationPathBundle,
    *,
    path_name: str,
) -> dict[str, Any]:
    """Return the recommendation dictionary for one path."""

    for output in recommendation_bundle.path_outputs:
        if output.path_name == path_name:
            return dict(output.recommendation)

    return {}


def _utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()
