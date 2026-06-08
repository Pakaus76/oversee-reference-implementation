"""Run paper-aligned OVERSEE Layer 4 demo.

This script reuses:
- Layer 1 evidence intake and validation.
- Layer 2 DMN-like contextualization.
- Layer 3 CMMN-inspired case lifecycle.
- Layer 4 DMN-like decision rules, deterministic path and live generative path.

It does not build the final Layer 5 governed package yet.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


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
    compare_deterministic_and_generative_outputs,
)


def main() -> None:
    """Run Layers 1-4 demo and persist inspectable outputs."""

    load_powershell_env_file(PROJECT_ROOT / ".env")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"paper_aligned_layer4_demo_{timestamp}"
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

    paths = {
        "predictive_alert_request": output_dir / "00_predictive_alert_request.json",
        "received_predictive_alert": output_dir / "01_received_predictive_alert.json",
        "enterprise_api_calls": output_dir / "01_enterprise_api_calls.json",
        "aggregated_evidence_package": output_dir / "01_output_layer1_aggregated_evidence_package.json",
        "validation_report": output_dir / "01_validation_report.json",
        "canonical_case_context": output_dir / "02_canonical_case_context.json",
        "contextualization_rule_trace": output_dir / "02_contextualization_rule_trace.json",
        "context_enrichment_summary": output_dir / "02_context_enrichment_summary.md",
        "layer2_contextualization_result": output_dir / "02_output_layer2_contextualization_result.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_output_layer3_case_management_state.json",
        "layer3_case_lifecycle_summary": output_dir / "03_layer3_case_lifecycle_summary.md",
        "dmn_decision_evaluation": output_dir / "04_output_layer4_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_output_layer4_recommendation_path_outputs.json",
        "live_generative_recommendation": output_dir / "04_live_generative_recommendation.json",
        "deterministic_vs_generative_comparison": output_dir / "04_deterministic_vs_generative_comparison.json",
        "layer4_decision_summary": output_dir / "04_layer4_decision_summary.md",
    }

    paths["predictive_alert_request"].write_text(
        json.dumps(alert_request, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["received_predictive_alert"].write_text(
        json.dumps(layer1_result.received_alert.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["enterprise_api_calls"].write_text(
        json.dumps(layer1_result.enterprise_api_calls, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["aggregated_evidence_package"].write_text(
        json.dumps(layer1_result.evidence_package.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["validation_report"].write_text(
        json.dumps(layer1_result.validation_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["canonical_case_context"].write_text(
        json.dumps(canonical_context.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["contextualization_rule_trace"].write_text(
        json.dumps(
            [rule.to_dict() for rule in layer2_result.rule_trace],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    paths["layer2_contextualization_result"].write_text(
        json.dumps(layer2_result.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["context_enrichment_summary"].write_text(
        _build_context_enrichment_summary(layer2_result.to_dict()),
        encoding="utf-8",
    )
    paths["case_lifecycle_trace"].write_text(
        json.dumps(case_state.lifecycle_trace(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["case_management_state"].write_text(
        json.dumps(case_state.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["layer3_case_lifecycle_summary"].write_text(
        _build_layer3_summary(case_state.to_dict(), layer2_result.to_dict()),
        encoding="utf-8",
    )
    paths["dmn_decision_evaluation"].write_text(
        json.dumps(rule_evaluation.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["recommendation_path_outputs"].write_text(
        json.dumps(recommendation_bundle.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["live_generative_recommendation"].write_text(
        json.dumps(live_result.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["deterministic_vs_generative_comparison"].write_text(
        json.dumps(comparison.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["layer4_decision_summary"].write_text(
        _build_layer4_summary(
            rule_evaluation=rule_evaluation.to_dict(),
            recommendation_bundle=recommendation_bundle.to_dict(),
            live_result=live_result.to_dict(),
            comparison=comparison.to_dict(),
        ),
        encoding="utf-8",
    )

    print("Paper-aligned Layer 4 demo completed.")
    print()
    print(
        json.dumps(
            {
                "layer1_evidence_package_valid": layer1_result.validation_report["valid"],
                "layer2_decision_ready": layer2_result.layer2_ready,
                "case_lifecycle_stage": case_state.lifecycle_stage,
                "dmn_decision_final_priority": rule_evaluation.final_priority,
                "recommended_execution_mode": rule_evaluation.recommended_execution_mode,
                "deterministic_path_available": _recommendation_path_count(recommendation_bundle.to_dict()) > 0,
                "recommendation_path_count": _recommendation_path_count(recommendation_bundle.to_dict()),
                "oversee_model_call_attempted": live_result.model_call_attempted,
                "oversee_model_call_successful": live_result.model_call_successful,
                "oversee_fallback_used": live_result.fallback_used,
                "priority_alignment": comparison.priority_alignment,
                "action_alignment": comparison.action_alignment,
                "output_dir": str(output_dir),
            },
            indent=2,
            ensure_ascii=False,
        )
    )



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
        f"- Protected fact violations: {comparison.get('protected_fact_violation_count', live_result.get('protected_fact_violation_count', 'not_recorded_in_comparison'))}\n\n"
        "## Interpretation\n\n"
        "The generative recommendation is not treated as an uncontrolled final "
        "answer. It is compared against a deterministic anchor and checked against "
        "protected facts and governance constraints.\n"
    )


if __name__ == "__main__":
    main()
