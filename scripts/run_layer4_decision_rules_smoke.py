"""Run Layer 1 to Layer 4 smoke test for the compressor case.

The script persists:
- 01_external_source_payloads.json
- 02_canonical_case_context.json
- 03_case_lifecycle_trace.json
- 03_output_layer3_case_management_state.json
- 04_output_layer4_dmn_decision_evaluation.json
- 04_output_layer4_recommendation_path_outputs.json
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
from oversee.case_management import build_case_management_state  # noqa: E402
from oversee.decision_rules import evaluate_dmn_like_rules, run_recommendation_paths  # noqa: E402
from oversee.external_sources import build_compressor_external_source_package  # noqa: E402


def main() -> None:
    """Run the Layer 4 compressor decision rules smoke test."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"five_layer_layer4_decision_rules_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)
    rule_evaluation = evaluate_dmn_like_rules(canonical_context, case_state)
    recommendation_bundle = run_recommendation_paths(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )

    paths = {
        "external_sources": output_dir / "01_external_source_payloads.json",
        "canonical_context": output_dir / "02_canonical_case_context.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_output_layer3_case_management_state.json",
        "dmn_decision_evaluation": output_dir / "04_output_layer4_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_output_layer4_recommendation_path_outputs.json",
    }

    paths["external_sources"].write_text(
        json.dumps(source_package.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["canonical_context"].write_text(
        json.dumps(canonical_context.to_dict(), indent=2, ensure_ascii=False),
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
    paths["dmn_decision_evaluation"].write_text(
        json.dumps(rule_evaluation.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["recommendation_path_outputs"].write_text(
        json.dumps(recommendation_bundle.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OVERSEE Layer 4 decision rules smoke completed.")
    print()
    print(json.dumps(
        {
            "case_id": rule_evaluation.case_id,
            "asset_id": rule_evaluation.asset_id,
            "final_priority": rule_evaluation.final_priority,
            "recommended_execution_mode": rule_evaluation.recommended_execution_mode,
            "human_review_required": rule_evaluation.human_review_required,
            "intervention_feasible": rule_evaluation.intervention_feasible,
            "triggered_rule_count": rule_evaluation.triggered_rule_count,
            "recommendation_path_count": recommendation_bundle.path_count,
            "recommendation_paths": [
                output.path_name for output in recommendation_bundle.path_outputs
            ],
            "output_dir": str(output_dir),
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
