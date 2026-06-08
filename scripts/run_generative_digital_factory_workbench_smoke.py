"""Run the advanced OVERSEE workbench with Generative Digital Factory.

This script runs:
- Generative Digital Factory source generation
- Full five-layer OVERSEE execution
- Live generative recommendation inside OVERSEE
- Deterministic-vs-generative comparison
- Advanced governed package
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
from oversee.case_management import build_case_management_state  # noqa: E402
from oversee.decision_rules import (  # noqa: E402
    evaluate_dmn_like_rules,
    run_live_generative_recommendation,
    run_recommendation_paths,
)
from oversee.digital_factory import run_generative_digital_factory_source_generation  # noqa: E402
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
    """Run the advanced generative workbench smoke test."""

    load_powershell_env_file(PROJECT_ROOT / ".env")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"generative_digital_factory_workbench_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    factory_result = run_generative_digital_factory_source_generation(allow_live_call=True)
    source_package = factory_result.source_package
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
        "factory_result": output_dir / "00_generative_factory_result.json",
        "factory_prompt": output_dir / "00_generative_factory_prompt.txt",
        "factory_raw_response": output_dir / "00_generative_factory_raw_response.txt",
        "factory_parsed_sources": output_dir / "00_generative_factory_parsed_sources.json",
        "external_sources": output_dir / "01_external_source_payloads.json",
        "canonical_context": output_dir / "02_canonical_case_context.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_output_layer3_case_management_state.json",
        "dmn_decision_evaluation": output_dir / "04_output_layer4_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_output_layer4_recommendation_path_outputs.json",
        "live_generative_recommendation": output_dir / "04_live_generative_recommendation.json",
        "deterministic_vs_generative_comparison": output_dir / "04_deterministic_vs_generative_comparison.json",
        "governed_recommendation_package": output_dir / "05_final_governed_recommendation_package.json",
        "traceability_index": output_dir / "05_traceability_index.json",
        "reviewer_summary": output_dir / "05_reviewer_summary.md",
        "execution_manifest": output_dir / "05_execution_manifest.json",
    }

    paths["factory_result"].write_text(json.dumps(factory_result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["factory_prompt"].write_text(factory_result.prompt, encoding="utf-8")
    paths["factory_raw_response"].write_text(factory_result.raw_response or "", encoding="utf-8")
    paths["factory_parsed_sources"].write_text(json.dumps(source_package.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["external_sources"].write_text(json.dumps(source_package.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["canonical_context"].write_text(json.dumps(canonical_context.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["case_lifecycle_trace"].write_text(json.dumps(case_state.lifecycle_trace(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["case_management_state"].write_text(json.dumps(case_state.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["dmn_decision_evaluation"].write_text(json.dumps(rule_evaluation.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["recommendation_path_outputs"].write_text(json.dumps(recommendation_bundle.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["live_generative_recommendation"].write_text(json.dumps(live_result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["deterministic_vs_generative_comparison"].write_text(json.dumps(comparison.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths["governed_recommendation_package"].write_text(json.dumps(advanced_package, indent=2, ensure_ascii=False), encoding="utf-8")
    paths["traceability_index"].write_text(json.dumps(advanced_package["traceability_index"], indent=2, ensure_ascii=False), encoding="utf-8")
    paths["reviewer_summary"].write_text(build_advanced_reviewer_summary_markdown(package_dict=advanced_package), encoding="utf-8")

    generated_files = [path.name for path in paths.values()]
    manifest = build_execution_manifest(output_dir=str(output_dir), package=base_package, generated_files=generated_files)
    manifest["generative_digital_factory_result_id"] = factory_result.result_id
    manifest["factory_model_call_successful"] = factory_result.model_call_successful
    manifest["factory_fallback_used"] = factory_result.fallback_used
    manifest["oversee_live_generative_result_id"] = live_result.result_id
    manifest["oversee_model_call_successful"] = live_result.model_call_successful
    manifest["oversee_fallback_used"] = live_result.fallback_used
    manifest["comparison_id"] = comparison.comparison_id

    paths["execution_manifest"].write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print("OVERSEE Generative Digital Factory workbench smoke completed.")
    print()
    print(json.dumps(
        {
            "case_id": canonical_context.case_id,
            "asset_id": canonical_context.asset.asset_id,
            "factory_model_name": factory_result.model_name,
            "factory_model_call_attempted": factory_result.model_call_attempted,
            "factory_model_call_successful": factory_result.model_call_successful,
            "factory_fallback_used": factory_result.fallback_used,
            "factory_fallback_reason": factory_result.fallback_reason,
            "oversee_model_name": live_result.model_name,
            "oversee_model_call_attempted": live_result.model_call_attempted,
            "oversee_model_call_successful": live_result.model_call_successful,
            "oversee_fallback_used": live_result.fallback_used,
            "oversee_fallback_reason": live_result.fallback_reason,
            "final_priority": advanced_package["final_recommendation"]["priority"],
            "generative_priority": live_result.parsed_recommendation.get("priority"),
            "priority_alignment": comparison.priority_alignment,
            "action_alignment": comparison.action_alignment,
            "generated_file_count": len(generated_files),
            "output_dir": str(output_dir),
        },
        indent=2,
        ensure_ascii=False,
    ))


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


if __name__ == "__main__":
    main()
