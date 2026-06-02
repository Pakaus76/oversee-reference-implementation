"""Run Layer 1 to Layer 5 smoke test for the compressor case.

The script persists:
- 01_external_source_payloads.json
- 02_canonical_case_context.json
- 03_case_lifecycle_trace.json
- 03_case_management_state.json
- 04_dmn_decision_evaluation.json
- 04_recommendation_path_outputs.json
- 05_governed_recommendation_package.json
- 05_traceability_index.json
- 05_reviewer_summary.md
- 05_execution_manifest.json
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
from oversee.reporting.governed_recommendation_package import (  # noqa: E402
    build_execution_manifest,
    build_governed_recommendation_package,
    build_reviewer_summary_markdown,
)


def main() -> None:
    """Run the complete Layer 5 governed package smoke test."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"five_layer_layer5_governed_package_{timestamp}"
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
    governed_package = build_governed_recommendation_package(
        source_package=source_package,
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        recommendation_bundle=recommendation_bundle,
    )

    paths = {
        "external_sources": output_dir / "01_external_source_payloads.json",
        "canonical_context": output_dir / "02_canonical_case_context.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_case_management_state.json",
        "dmn_decision_evaluation": output_dir / "04_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_recommendation_path_outputs.json",
        "governed_recommendation_package": output_dir / "05_governed_recommendation_package.json",
        "traceability_index": output_dir / "05_traceability_index.json",
        "reviewer_summary": output_dir / "05_reviewer_summary.md",
        "execution_manifest": output_dir / "05_execution_manifest.json",
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
    paths["governed_recommendation_package"].write_text(
        json.dumps(governed_package.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["traceability_index"].write_text(
        json.dumps(governed_package.traceability_dicts(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["reviewer_summary"].write_text(
        build_reviewer_summary_markdown(governed_package),
        encoding="utf-8",
    )

    generated_files = [path.name for path in paths.values()]
    manifest = build_execution_manifest(
        output_dir=str(output_dir),
        package=governed_package,
        generated_files=generated_files,
    )
    paths["execution_manifest"].write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OVERSEE Layer 5 governed package smoke completed.")
    print()
    print(json.dumps(
        {
            "case_id": governed_package.case_id,
            "asset_id": governed_package.asset_id,
            "package_id": governed_package.package_id,
            "priority": governed_package.final_recommendation["priority"],
            "recommended_action": governed_package.final_recommendation["recommended_action"],
            "recommended_execution_mode": governed_package.final_recommendation["recommended_execution_mode"],
            "human_review_required": governed_package.final_recommendation["human_review_required"],
            "decision_ready": governed_package.final_recommendation["decision_ready"],
            "traceability_count": governed_package.traceability_count,
            "generated_file_count": len(generated_files),
            "output_dir": str(output_dir),
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
