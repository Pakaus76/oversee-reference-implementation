"""Run an executable OVERSEE scenario through all five layers.

This runner executes the real OVERSEE Layer 1 to Layer 5 path from a scenario
JSON file. It is intentionally separate from the paper-aligned runner so the
reference paper case remains stable while the workbench evolves toward
multi-scenario execution.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from demo.interactive_walkthrough.scenario_catalog import get_scenario, list_scenarios  # noqa: E402
from oversee.case_context import build_canonical_case_context  # noqa: E402
from oversee.case_context.contextualization_rules import run_layer2_contextualization  # noqa: E402
from oversee.case_management import build_case_management_state  # noqa: E402
from oversee.decision_rules import evaluate_dmn_like_rules, run_recommendation_paths  # noqa: E402
from oversee.integration.layer1_evidence_pipeline import run_layer1_evidence_pipeline  # noqa: E402
from oversee.integration.scenario_backed_enterprise_apis import (  # noqa: E402
    ScenarioBackedEnterpriseApiClient,
)
from oversee.integration.scenario_executable_inputs import (  # noqa: E402
    build_alert_request_from_executable_inputs,
    build_case_id_prefix_from_scenario_id,
    validate_executable_inputs,
)
from oversee.reporting.governed_recommendation_package import (  # noqa: E402
    build_execution_manifest,
    build_governed_recommendation_package,
)


def main() -> None:
    """Run one executable scenario through the real OVERSEE pipeline."""

    parser = argparse.ArgumentParser(
        description="Run one executable OVERSEE scenario through Layers 1 to 5.",
    )
    parser.add_argument(
        "--scenario",
        default="COMP-001",
        help="Scenario ID to execute. Example: COMP-001, COMP-002, PUMP-001.",
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List available scenarios and exit.",
    )
    args = parser.parse_args()

    if args.list_scenarios:
        _print_available_scenarios()
        return

    result = run_scenario_all_layers(scenario_id=args.scenario)

    print("Executable OVERSEE scenario completed.")
    print()
    print(
        json.dumps(
            {
                "scenario_id": result["scenario_id"],
                "case_id": result["case_id"],
                "asset_id": result["asset_id"],
                "asset_type": result["asset_type"],
                "failure_mode": result["failure_mode"],
                "layer1_evidence_package_valid": result["layer1_evidence_package_valid"],
                "layer2_decision_ready": result["layer2_decision_ready"],
                "case_lifecycle_stage": result["case_lifecycle_stage"],
                "dmn_decision_final_priority": result["dmn_decision_final_priority"],
                "recommended_execution_mode": result["recommended_execution_mode"],
                "intervention_feasible": result["intervention_feasible"],
                "human_review_required": result["human_review_required"],
                "generated_file_count": result["generated_file_count"],
                "output_dir": result["output_dir"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def run_scenario_all_layers(scenario_id: str) -> dict[str, Any]:
    """Execute one scenario through the real Layer 1 to Layer 5 path."""

    scenario = get_scenario(scenario_id)
    executable_inputs = scenario.raw.get("executable_inputs")

    if not isinstance(executable_inputs, dict):
        raise ValueError(f"Scenario {scenario.scenario_id} has no executable_inputs section.")

    validate_executable_inputs(executable_inputs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario_slug = scenario.scenario_id.lower().replace("-", "_")
    output_dir = PROJECT_ROOT / "outputs" / f"scenario_all_layers_{scenario_slug}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    alert_request = build_alert_request_from_executable_inputs(executable_inputs)
    api_client = ScenarioBackedEnterpriseApiClient(executable_inputs)
    case_id_prefix = build_case_id_prefix_from_scenario_id(scenario.scenario_id)

    layer1_result = run_layer1_evidence_pipeline(
        alert_request,
        api_client=api_client,
        case_id_prefix=case_id_prefix,
    )
    canonical_context = build_canonical_case_context(layer1_result.evidence_package)
    layer2_result = run_layer2_contextualization(canonical_context)
    case_state = build_case_management_state(canonical_context)
    rule_evaluation = evaluate_dmn_like_rules(canonical_context, case_state)
    recommendation_bundle = run_recommendation_paths(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )
    governed_package = build_governed_recommendation_package(
        source_package=layer1_result.evidence_package,
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        recommendation_bundle=recommendation_bundle,
    )

    paths = {
        "scenario": output_dir / "00_scenario.json",
        "predictive_alert_request": output_dir / "00_predictive_alert_request.json",
        "received_predictive_alert": output_dir / "01_received_predictive_alert.json",
        "enterprise_api_calls": output_dir / "01_enterprise_api_calls.json",
        "aggregated_evidence_package": output_dir / "01_aggregated_evidence_package.json",
        "validation_report": output_dir / "01_validation_report.json",
        "canonical_case_context": output_dir / "02_canonical_case_context.json",
        "contextualization_rule_trace": output_dir / "02_contextualization_rule_trace.json",
        "layer2_contextualization_result": output_dir / "02_layer2_contextualization_result.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_case_management_state.json",
        "dmn_decision_evaluation": output_dir / "04_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_recommendation_path_outputs.json",
        "governed_recommendation_package": output_dir / "05_governed_recommendation_package.json",
        "traceability_index": output_dir / "05_traceability_index.json",
        "execution_manifest": output_dir / "05_execution_manifest.json",
        "scenario_execution_summary": output_dir / "05_scenario_execution_summary.md",
    }

    _write_json(paths["scenario"], scenario.raw)
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
    _write_json(paths["case_lifecycle_trace"], case_state.lifecycle_trace())
    _write_json(paths["case_management_state"], case_state.to_dict())
    _write_json(paths["dmn_decision_evaluation"], rule_evaluation.to_dict())
    _write_json(paths["recommendation_path_outputs"], recommendation_bundle.to_dict())
    _write_json(paths["governed_recommendation_package"], governed_package.to_dict())
    _write_json(paths["traceability_index"], governed_package.traceability_index)

    generated_files = [path.name for path in paths.values()]
    manifest = build_execution_manifest(
        output_dir=str(output_dir),
        package=governed_package,
        generated_files=generated_files,
    )
    manifest["scenario_execution"] = {
        "scenario_id": scenario.scenario_id,
        "scenario_title": scenario.title,
        "asset_id": scenario.asset_id,
        "asset_type": scenario.asset_type,
        "failure_mode": scenario.failure_mode,
        "decision_pattern": scenario.raw.get("decision_pattern"),
        "master_case": bool(scenario.raw.get("master_case", False)),
        "case_id_prefix": case_id_prefix,
        "scenario_backed_enterprise_api_client": True,
    }
    _write_json(paths["execution_manifest"], manifest)

    summary = _build_scenario_execution_summary(
        scenario=scenario.raw,
        canonical_context=canonical_context.to_dict(),
        layer2_result=layer2_result.to_dict(),
        case_state=case_state.to_dict(),
        rule_evaluation=rule_evaluation.to_dict(),
        recommendation_bundle=recommendation_bundle.to_dict(),
        governed_package=governed_package.to_dict(),
    )
    paths["scenario_execution_summary"].write_text(summary, encoding="utf-8")

    result = {
        "scenario_id": scenario.scenario_id,
        "case_id": canonical_context.case_id,
        "asset_id": canonical_context.asset.asset_id,
        "asset_type": canonical_context.asset.asset_type,
        "failure_mode": scenario.failure_mode,
        "layer1_evidence_package_valid": layer1_result.validation_report["valid"],
        "layer2_decision_ready": layer2_result.layer2_ready,
        "case_lifecycle_stage": case_state.lifecycle_stage,
        "dmn_decision_final_priority": rule_evaluation.final_priority,
        "recommended_execution_mode": rule_evaluation.recommended_execution_mode,
        "intervention_feasible": rule_evaluation.intervention_feasible,
        "human_review_required": rule_evaluation.human_review_required,
        "generated_file_count": len(generated_files),
        "output_dir": str(output_dir),
    }

    return result


def _print_available_scenarios() -> None:
    """Print all scenarios available to the runner."""

    print("Available executable OVERSEE scenarios")
    print("======================================")
    print()

    for scenario in list_scenarios():
        executable = "yes" if "executable_inputs" in scenario.raw else "no"
        print(
            f"{scenario.scenario_id} - {scenario.title} "
            f"| asset={scenario.asset_id} | executable={executable}"
        )


def _write_json(path: Path, payload: Any) -> None:
    """Write a JSON payload to disk."""

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            default=_json_default,
        ),
        encoding="utf-8",
    )


def _json_default(value: Any) -> Any:
    """Convert common OVERSEE objects into JSON-serializable dictionaries."""

    if hasattr(value, "to_dict"):
        return value.to_dict()

    if is_dataclass(value):
        return asdict(value)

    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def _build_scenario_execution_summary(
    *,
    scenario: dict[str, Any],
    canonical_context: dict[str, Any],
    layer2_result: dict[str, Any],
    case_state: dict[str, Any],
    rule_evaluation: dict[str, Any],
    recommendation_bundle: dict[str, Any],
    governed_package: dict[str, Any],
) -> str:
    """Build a concise Markdown summary for one executed scenario."""

    scenario_id = scenario["scenario_id"]
    title = scenario["title"]
    asset_id = scenario["asset_id"]
    asset_type = scenario["asset_type"]
    failure_mode = scenario["failure_mode"]
    decision_pattern = scenario.get("decision_pattern", "not_specified")

    derived_context = layer2_result.get("derived_context", {})
    recommended_actions = recommendation_bundle.get("recommendations", [])
    action_count = len(recommended_actions) if isinstance(recommended_actions, list) else 0

    return f"""# OVERSEE Scenario Execution Summary

## Scenario

- Scenario ID: `{scenario_id}`
- Title: {title}
- Asset: `{asset_id}`
- Asset type: `{asset_type}`
- Failure mode: `{failure_mode}`
- Decision pattern: `{decision_pattern}`

## Layer 1 - Evidence package

- Case ID: `{canonical_context.get("case_id")}`
- Source payload count: `{canonical_context.get("source_payload_count")}`
- Data quality flags: `{canonical_context.get("data_quality_flags")}`

## Layer 2 - Contextualization

- Layer 2 ready: `{layer2_result.get("layer2_ready")}`
- Derived context: `{derived_context}`

## Layer 3 - Case lifecycle

- Case status: `{case_state.get("case_status")}`
- Lifecycle stage: `{case_state.get("lifecycle_stage")}`
- Event count: `{case_state.get("event_count")}`
- Task count: `{case_state.get("task_count")}`
- Milestone count: `{case_state.get("milestone_count")}`
- Blockers: `{case_state.get("blockers")}`

## Layer 4 - Decision logic

- Final priority: `{rule_evaluation.get("final_priority")}`
- Recommended execution mode: `{rule_evaluation.get("recommended_execution_mode")}`
- Intervention feasible: `{rule_evaluation.get("intervention_feasible")}`
- Human review required: `{rule_evaluation.get("human_review_required")}`
- Triggered rule count: `{rule_evaluation.get("triggered_rule_count")}`

## Layer 5 - Governed package

- Package ID: `{governed_package.get("package_id")}`
- Traceability count: `{governed_package.get("traceability_count")}`
- Recommendation count: `{action_count}`

## Interpretation

This scenario was executed through the real OVERSEE Layer 1 to Layer 5 path using
scenario-backed enterprise API data. The result is therefore not only a
presentation placeholder: it is a generated governed recommendation package.
"""


if __name__ == "__main__":
    main()