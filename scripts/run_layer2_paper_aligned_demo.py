"""Run paper-aligned OVERSEE Layer 2 demo.

This script reuses the Layer 1 evidence intake pipeline and then demonstrates
Layer 2 contextualization through explicit DMN-like rules.
"""

from __future__ import annotations

import json
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
from oversee.integration import (  # noqa: E402
    build_sample_predictive_alert_request,
    run_layer1_evidence_pipeline,
)


def main() -> None:
    """Run Layer 1 and Layer 2 demo and persist inspectable outputs."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"paper_aligned_layer2_demo_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)
    canonical_context = build_canonical_case_context(layer1_result.evidence_package)
    layer2_result = run_layer2_contextualization(canonical_context)

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

    derived = layer2_result.derived_context

    print("Paper-aligned Layer 2 demo completed.")
    print()
    print(
        json.dumps(
            {
                "layer1_evidence_package_valid": layer1_result.validation_report["valid"],
                "canonical_context_built": canonical_context.case_id == layer1_result.evidence_package.case_id,
                "contextualization_rules_applied": len(layer2_result.rule_trace),
                "contextualization_rules_triggered": sum(
                    1 for rule in layer2_result.rule_trace if rule.triggered
                ),
                "technical_urgency": derived.get("technical_urgency"),
                "asset_escalation": derived.get("asset_escalation"),
                "operational_constraint": derived.get("operational_constraint"),
                "downtime_window": derived.get("downtime_window"),
                "intervention_feasible": derived.get("intervention_feasible"),
                "recurrence_risk": derived.get("recurrence_risk"),
                "human_review_required": derived.get("human_review_required"),
                "layer2_decision_ready": derived.get("layer2_decision_ready"),
                "output_dir": str(output_dir),
            },
            indent=2,
            ensure_ascii=False,
        )
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


if __name__ == "__main__":
    main()
