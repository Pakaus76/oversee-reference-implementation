"""Run paper-aligned OVERSEE Layer 5 demo.

This script closes the paper-aligned five-layer flow:
- Layer 1: evidence intake and validation.
- Layer 2: DMN-like contextualization.
- Layer 3: CMMN-inspired case lifecycle.
- Layer 4: DMN-like decision rules, deterministic path, live generative path and comparison.
- Layer 5: governed recommendation package, traceability, manifest and reviewer summary.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.case_context import build_canonical_case_context  # noqa: E402
from oversee.case_context.contextualization_rules import (  # noqa: E402
    run_layer2_contextualization,
)
from oversee.case_management import build_case_management_state  # noqa: E402
from oversee.decision_rules import (  # noqa: E402
    evaluate_dmn_like_rules,
    run_live_generative_recommendation,
    run_recommendation_paths,
)
from oversee.integration import (  # noqa: E402
    build_sample_predictive_alert_request,
    run_layer1_evidence_pipeline,
)
from oversee.reporting.generative_comparison import (  # noqa: E402
    build_advanced_governed_package_dict,
    build_advanced_reviewer_summary_markdown,
    compare_deterministic_and_generative_outputs,
)
from oversee.reporting.governed_recommendation_package import (  # noqa: E402
    build_execution_manifest,
    build_governed_recommendation_package,
)


def main() -> None:
    """Run Layers 1-5 demo and persist inspectable outputs."""

    load_powershell_env_file(PROJECT_ROOT / ".env")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"paper_aligned_layer5_demo_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

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
        allow_live_call=True,
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

    paths = {
        "predictive_alert_request": output_dir / "00_predictive_alert_request.json",
        "received_predictive_alert": output_dir / "01_received_predictive_alert.json",
        "enterprise_api_calls": output_dir / "01_enterprise_api_calls.json",
        "aggregated_evidence_package": output_dir / "01_aggregated_evidence_package.json",
        "validation_report": output_dir / "01_validation_report.json",
        "canonical_case_context": output_dir / "02_canonical_case_context.json",
        "contextualization_rule_trace": output_dir / "02_contextualization_rule_trace.json",
        "context_enrichment_summary": output_dir / "02_context_enrichment_summary.md",
        "layer2_contextualization_result": output_dir / "02_layer2_contextualization_result.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_case_management_state.json",
        "layer3_case_lifecycle_summary": output_dir / "03_layer3_case_lifecycle_summary.md",
        "dmn_decision_evaluation": output_dir / "04_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_recommendation_path_outputs.json",
        "live_generative_recommendation": output_dir / "04_live_generative_recommendation.json",
        "deterministic_vs_generative_comparison": output_dir / "04_deterministic_vs_generative_comparison.json",
        "layer4_decision_summary": output_dir / "04_layer4_decision_summary.md",
        "governed_recommendation_package": output_dir / "05_governed_recommendation_package.json",
        "traceability_index": output_dir / "05_traceability_index.json",
        "execution_manifest": output_dir / "05_execution_manifest.json",
        "reviewer_summary": output_dir / "05_reviewer_summary.md",
        "full_layer_trace_summary": output_dir / "05_full_layer_trace_summary.md",
    }

    _write_json(paths["predictive_alert_request"], alert_request)
    _write_json(paths["received_predictive_alert"], layer1_result.received_alert.to_dict())
    _write_json(paths["enterprise_api_calls"], layer1_result.enterprise_api_calls)
    _write_json(paths["aggregated_evidence_package"], layer1_result.evidence_package.to_dict())
    _write_json(paths["validation_report"], layer1_result.validation_report)
    _write_json(paths["canonical_case_context"], canonical_context.to_dict())
    _write_json(
        paths["contextualization_rule_trace"],
        [rule.to_dict() for rule in layer2_result.rule_trace],
    )
    _write_json(paths["layer2_contextualization_result"], layer2_result.to_dict())
    paths["context_enrichment_summary"].write_text(
        _build_context_enrichment_summary(layer2_result.to_dict()),
        encoding="utf-8",
    )
    _write_json(paths["case_lifecycle_trace"], case_state.lifecycle_trace())
    _write_json(paths["case_management_state"], case_state.to_dict())
    paths["layer3_case_lifecycle_summary"].write_text(
        _build_layer3_summary(case_state.to_dict(), layer2_result.to_dict()),
        encoding="utf-8",
    )
    _write_json(paths["dmn_decision_evaluation"], rule_evaluation.to_dict())
    _write_json(paths["recommendation_path_outputs"], recommendation_bundle.to_dict())
    _write_json(paths["live_generative_recommendation"], live_result.to_dict())
    _write_json(paths["deterministic_vs_generative_comparison"], comparison.to_dict())
    paths["layer4_decision_summary"].write_text(
        _build_layer4_summary(
            rule_evaluation=rule_evaluation.to_dict(),
            recommendation_bundle=recommendation_bundle.to_dict(),
            live_result=live_result.to_dict(),
            comparison=comparison.to_dict(),
        ),
        encoding="utf-8",
    )
    _write_json(paths["governed_recommendation_package"], advanced_package)
    _write_json(paths["traceability_index"], advanced_package.get("traceability_index", {}))
    paths["reviewer_summary"].write_text(
        build_advanced_reviewer_summary_markdown(package_dict=advanced_package),
        encoding="utf-8",
    )

    generated_files = [path.name for path in paths.values()]
    manifest = build_execution_manifest(
        output_dir=str(output_dir),
        package=base_package,
        generated_files=generated_files,
    )
    manifest["paper_alignment"] = {
        "layer1_predictive_alert_api": True,
        "layer1_enterprise_api_calls": True,
        "layer1_aggregation_and_validation": True,
        "layer2_contextualization_rules": True,
        "layer3_cmmn_inspired_lifecycle": True,
        "layer4_dmn_like_decision_rules": True,
        "layer4_deterministic_path": _recommendation_path_count(recommendation_bundle.to_dict()) > 0,
        "layer4_live_generative_path": live_result.model_call_successful,
        "layer4_deterministic_vs_generative_comparison": True,
        "layer5_governed_package": True,
    }
    manifest["live_generative_result_id"] = live_result.result_id
    manifest["model_call_attempted"] = live_result.model_call_attempted
    manifest["model_call_successful"] = live_result.model_call_successful
    manifest["fallback_used"] = live_result.fallback_used
    manifest["comparison_id"] = comparison.comparison_id
    _write_json(paths["execution_manifest"], manifest)

    paths["full_layer_trace_summary"].write_text(
        _build_full_layer_trace_summary(
            layer1_result=layer1_result.to_dict(),
            layer2_result=layer2_result.to_dict(),
            case_state=case_state.to_dict(),
            rule_evaluation=rule_evaluation.to_dict(),
            recommendation_bundle=recommendation_bundle.to_dict(),
            live_result=live_result.to_dict(),
            comparison=comparison.to_dict(),
            advanced_package=advanced_package,
        ),
        encoding="utf-8",
    )

    traceability_index = advanced_package.get("traceability_index", {})
    traceability_count = advanced_package.get(
        "traceability_count",
        len(traceability_index) if isinstance(traceability_index, dict) else 0,
    )

    print("Paper-aligned Layer 5 demo completed.")
    print()
    print(
        json.dumps(
            {
                "layer1_evidence_package_valid": layer1_result.validation_report["valid"],
                "layer2_decision_ready": layer2_result.layer2_ready,
                "case_lifecycle_stage": case_state.lifecycle_stage,
                "dmn_decision_final_priority": rule_evaluation.final_priority,
                "recommended_execution_mode": rule_evaluation.recommended_execution_mode,
                "oversee_model_call_attempted": live_result.model_call_attempted,
                "oversee_model_call_successful": live_result.model_call_successful,
                "oversee_fallback_used": live_result.fallback_used,
                "priority_alignment": comparison.priority_alignment,
                "action_alignment": comparison.action_alignment,
                "governed_package_created": bool(advanced_package),
                "traceability_count": traceability_count,
                "generated_file_count": len(generated_files),
                "output_dir": str(output_dir),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def load_powershell_env_file(path: Path) -> None:
    """Load a local PowerShell-style .env file if present."""

    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("$env:") and "=" in line:
            left, right = line.split("=", 1)
            name = left.replace("$env:", "").strip()
            value = right.strip().strip('"').strip("'")
            if name:
                os.environ[name] = value
            continue

        if "=" in line and not line.startswith("$"):
            name, value = line.split("=", 1)
            name = name.strip()
            value = value.strip().strip('"').strip("'")
            if name:
                os.environ[name] = value


def _write_json(path: Path, payload: Any) -> None:
    """Write a JSON file with consistent formatting."""

    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _recommendation_path_count(bundle_dict: dict[str, object]) -> int:
    """Return recommendation path count from a flexible bundle dictionary."""

    for key in ("recommendation_path_count", "path_count"):
        value = bundle_dict.get(key)
        if isinstance(value, int):
            return value

    for key in ("recommendation_paths", "paths", "path_outputs", "outputs"):
        value = bundle_dict.get(key)
        if isinstance(value, list):
            return len(value)

    return 0


def _protected_fact_violation_count(
    *,
    comparison: dict[str, object],
    live_result: dict[str, object],
) -> object:
    """Return protected fact violation count from the available metadata."""

    return comparison.get(
        "protected_fact_violation_count",
        live_result.get("protected_fact_violation_count", "not_recorded_in_comparison"),
    )


def _build_context_enrichment_summary(layer2_result: dict[str, object]) -> str:
    """Build a compact markdown summary for Layer 2."""

    derived = layer2_result["derived_context"]

    return (
        "# Paper-aligned Layer 2 contextualization summary\n\n"
        "## Purpose\n\n"
        "Layer 2 converts the validated evidence package from Layer 1 into "
        "contextual decision factors using explicit DMN-like rules. These rules "
        "do not produce the final recommendation; they explain what the evidence "
        "means in decision context.\n\n"
        "## Derived context\n\n"
        f"- Technical urgency: {derived['technical_urgency']}\n"
        f"- Asset escalation: {derived['asset_escalation']}\n"
        f"- Operational constraint: {derived['operational_constraint']}\n"
        f"- Downtime window: {derived['downtime_window']}\n"
        f"- Intervention feasible: {derived['intervention_feasible']}\n"
        f"- Recurrence risk: {derived['recurrence_risk']}\n"
        f"- Human review required: {derived['human_review_required']}\n"
        f"- Layer 2 decision ready: {derived['layer2_decision_ready']}\n\n"
        "## Interpretation\n\n"
        "The layer has transformed technical, operational, maintenance and "
        "governance evidence into explicit decision factors that can be consumed "
        "by the downstream case lifecycle and decision logic.\n"
    )


def _build_layer3_summary(
    case_state: dict[str, object],
    layer2_result: dict[str, object],
) -> str:
    """Build a compact markdown summary for Layer 3."""

    return (
        "# Paper-aligned Layer 3 case lifecycle summary\n\n"
        "## Purpose\n\n"
        "Layer 3 turns the contextualized compressor evidence into a managed "
        "decision case. This is CMMN-inspired, but it is not a full CMMN engine. "
        "The purpose is to make the case lifecycle inspectable and executable "
        "inside the reference implementation.\n\n"
        "## Input from Layer 2\n\n"
        f"- Layer 2 ready: {layer2_result['layer2_ready']}\n"
        f"- Technical urgency: {layer2_result['derived_context']['technical_urgency']}\n"
        f"- Human review required: {layer2_result['derived_context']['human_review_required']}\n\n"
        "## Case state\n\n"
        f"- Case status: {case_state['case_status']}\n"
        f"- Lifecycle stage: {case_state['lifecycle_stage']}\n"
        f"- Human review required: {case_state['human_review_required']}\n"
        f"- Maintenance planning required: {case_state['maintenance_planning_required']}\n"
        f"- Decision ready: {case_state['decision_ready']}\n"
        f"- Events: {len(case_state['events'])}\n"
        f"- Tasks: {len(case_state['tasks'])}\n"
        f"- Milestones: {len(case_state['milestones'])}\n"
        f"- Blockers: {len(case_state['blockers'])}\n\n"
        "## Interpretation\n\n"
        "The alert is no longer only a technical model output. It is now a "
        "structured decision case with events, tasks, milestones and readiness "
        "status for downstream decision logic.\n"
    )


def _build_layer4_summary(
    *,
    rule_evaluation: dict[str, object],
    recommendation_bundle: dict[str, object],
    live_result: dict[str, object],
    comparison: dict[str, object],
) -> str:
    """Build a compact markdown summary for Layer 4."""

    protected_fact_violation_count = _protected_fact_violation_count(
        comparison=comparison,
        live_result=live_result,
    )

    return (
        "# Paper-aligned Layer 4 decision and recommendation summary\n\n"
        "## Purpose\n\n"
        "Layer 4 consolidates the contextualized case into decision and "
        "recommendation logic. This layer uses DMN-like decision rules, a "
        "deterministic anchor path and a live generative recommendation path.\n\n"
        "## Difference from Layer 2\n\n"
        "- Layer 2 DMN-like rules derive contextual decision factors from evidence.\n"
        "- Layer 4 DMN-like rules consolidate priority, constraints and recommendation logic.\n\n"
        "## Decision result\n\n"
        f"- Final priority: {rule_evaluation['final_priority']}\n"
        f"- Recommended execution mode: {rule_evaluation['recommended_execution_mode']}\n"
        f"- Recommendation paths: {_recommendation_path_count(recommendation_bundle)}\n\n"
        "## Generative path\n\n"
        f"- Model call attempted: {live_result['model_call_attempted']}\n"
        f"- Model call successful: {live_result['model_call_successful']}\n"
        f"- Fallback used: {live_result['fallback_used']}\n\n"
        "## Deterministic vs generative comparison\n\n"
        f"- Priority alignment: {comparison['priority_alignment']}\n"
        f"- Action alignment: {comparison['action_alignment']}\n"
        f"- Protected fact violations: {protected_fact_violation_count}\n\n"
        "## Interpretation\n\n"
        "The generative recommendation is not treated as an uncontrolled final "
        "answer. It is compared against a deterministic anchor and checked against "
        "protected facts and governance constraints.\n"
    )


def _build_full_layer_trace_summary(
    *,
    layer1_result: dict[str, object],
    layer2_result: dict[str, object],
    case_state: dict[str, object],
    rule_evaluation: dict[str, object],
    recommendation_bundle: dict[str, object],
    live_result: dict[str, object],
    comparison: dict[str, object],
    advanced_package: dict[str, object],
) -> str:
    """Build a compact all-layer trace summary."""

    traceability_index = advanced_package.get("traceability_index", {})
    traceability_count = advanced_package.get(
        "traceability_count",
        len(traceability_index) if isinstance(traceability_index, dict) else 0,
    )

    return (
        "# Paper-aligned full five-layer OVERSEE trace summary\n\n"
        "## Layer 1 - Integration, aggregation and validation\n\n"
        "- Receives a predictive alert through a simulated API endpoint.\n"
        "- Receives raw sensor context together with the alert.\n"
        "- Calls simulated enterprise APIs for asset metadata, CMMS history, MES context, inventory/resources and policy governance.\n"
        f"- Evidence package valid: {layer1_result['validation_report']['valid']}\n\n"
        "## Layer 2 - DMN-like contextualization\n\n"
        "- Applies explicit if-then rules to derive contextual decision factors.\n"
        f"- Layer 2 ready: {layer2_result['layer2_ready']}\n"
        f"- Derived technical urgency: {layer2_result['derived_context']['technical_urgency']}\n\n"
        "## Layer 3 - CMMN-inspired lifecycle\n\n"
        f"- Lifecycle stage: {case_state['lifecycle_stage']}\n"
        f"- Decision ready: {case_state['decision_ready']}\n\n"
        "## Layer 4 - Decision and recommendation logic\n\n"
        f"- Final priority: {rule_evaluation['final_priority']}\n"
        f"- Recommended execution mode: {rule_evaluation['recommended_execution_mode']}\n"
        f"- Recommendation path count: {_recommendation_path_count(recommendation_bundle)}\n"
        f"- Live generative model call successful: {live_result['model_call_successful']}\n"
        f"- Priority alignment: {comparison['priority_alignment']}\n"
        f"- Action alignment: {comparison['action_alignment']}\n\n"
        "## Layer 5 - Governed package\n\n"
        f"- Package ID: {advanced_package.get('package_id', 'not_recorded')}\n"
        f"- Traceability count: {traceability_count}\n"
        "- Final output is a governed package, not an uncontrolled model answer.\n"
    )


if __name__ == "__main__":
    main()
