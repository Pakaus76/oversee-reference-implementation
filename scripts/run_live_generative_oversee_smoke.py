"""Run live generative OVERSEE smoke test.

This script runs the full five-layer pipeline and adds:
- live generative recommendation output
- deterministic-vs-generative comparison
- advanced governed package with generative evidence

If the API call fails, the script still completes with governed fallback metadata.
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
from oversee.decision_rules import (  # noqa: E402
    evaluate_dmn_like_rules,
    run_live_generative_recommendation,
    run_recommendation_paths,
)
from oversee.external_sources import build_compressor_external_source_package  # noqa: E402
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
    """Run the live generative OVERSEE smoke test."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"live_generative_oversee_{timestamp}"
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
        source_package=source_package,
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
        "external_sources": output_dir / "01_external_source_payloads.json",
        "canonical_context": output_dir / "02_canonical_case_context.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_case_management_state.json",
        "dmn_decision_evaluation": output_dir / "04_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_recommendation_path_outputs.json",
        "live_generative_recommendation": output_dir / "04_live_generative_recommendation.json",
        "deterministic_vs_generative_comparison": output_dir / "04_deterministic_vs_generative_comparison.json",
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
    paths["live_generative_recommendation"].write_text(
        json.dumps(live_result.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["deterministic_vs_generative_comparison"].write_text(
        json.dumps(comparison.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["governed_recommendation_package"].write_text(
        json.dumps(advanced_package, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["traceability_index"].write_text(
        json.dumps(advanced_package["traceability_index"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
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
    manifest["live_generative_result_id"] = live_result.result_id
    manifest["model_call_attempted"] = live_result.model_call_attempted
    manifest["model_call_successful"] = live_result.model_call_successful
    manifest["fallback_used"] = live_result.fallback_used
    manifest["comparison_id"] = comparison.comparison_id

    paths["execution_manifest"].write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OVERSEE live generative recommendation smoke completed.")
    print()
    print(json.dumps(
        {
            "case_id": live_result.case_id,
            "asset_id": live_result.asset_id,
            "model_name": live_result.model_name,
            "model_call_attempted": live_result.model_call_attempted,
            "model_call_successful": live_result.model_call_successful,
            "fallback_used": live_result.fallback_used,
            "fallback_reason": live_result.fallback_reason,
            "generative_priority": live_result.parsed_recommendation.get("priority"),
            "generative_action": live_result.parsed_recommendation.get("recommended_action"),
            "priority_alignment": comparison.priority_alignment,
            "action_alignment": comparison.action_alignment,
            "protected_fact_violation_count": comparison.protected_fact_violation_count,
            "generated_file_count": len(generated_files),
            "output_dir": str(output_dir),
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
