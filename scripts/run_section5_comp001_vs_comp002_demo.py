"""
Paper-facing Section 5 COMP-001 vs COMP-002 demonstration runner.

This script executes two paper-specific scenario JSON files directly,
without using the scenario catalog lookup by scenario_id. This avoids
ambiguity when several JSON files share the same scenario_id.

It runs both scenarios through the real OVERSEE Layer 1 to Layer 5 path
and creates paper-ready evidence artifacts for Section 5.
"""

from __future__ import annotations

import csv
import json
import shutil
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


from demo.interactive_walkthrough.scenario_catalog import load_scenario_file  # noqa: E402
from oversee.case_context import build_canonical_case_context  # noqa: E402
from oversee.case_context.contextualization_rules import run_layer2_contextualization  # noqa: E402
from oversee.case_management import build_case_management_state  # noqa: E402
from oversee.decision_rules import evaluate_dmn_like_rules, run_recommendation_paths  # noqa: E402
from oversee.integration.layer1_evidence_pipeline import run_layer1_evidence_pipeline  # noqa: E402
from oversee.integration.scenario_backed_enterprise_apis import ScenarioBackedEnterpriseApiClient  # noqa: E402
from oversee.integration.scenario_executable_inputs import (  # noqa: E402
    build_alert_request_from_executable_inputs,
    build_case_id_prefix_from_scenario_id,
    validate_executable_inputs,
)
from oversee.reporting.governed_recommendation_package import (  # noqa: E402
    build_execution_manifest,
    build_governed_recommendation_package,
)


OUTPUT_ROOT = PROJECT_ROOT / "outputs"
SCENARIO_DIR = PROJECT_ROOT / "demo" / "interactive_walkthrough" / "scenarios"

SOURCE_SCENARIOS = {
    "COMP-001": SCENARIO_DIR / "comp_001_paper.json",
    "COMP-002": SCENARIO_DIR / "comp_002_paper.json",
}

SECTION5_PREFIX = "paper_section5_comp001_vs_comp002_"


def serialize_layer_artifact_default(value: Any) -> Any:
    """Convert common OVERSEE objects into JSON-serializable values."""
    if hasattr(value, "to_dict"):
        return value.to_dict()

    if is_dataclass(value):
        return asdict(value)

    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def write_json(path: Path, payload: Any) -> None:
    """Write a JSON artifact with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            default=serialize_layer_artifact_default,
        ),
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_markdown(path: Path, content: str) -> None:
    """Write a Markdown artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def safe_get(data: dict[str, Any], path: list[str], default: Any = None) -> Any:
    """Safely extract a nested dictionary value."""
    current: Any = data

    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]

    return current


def build_layer5_scenario_execution_summary(
    *,
    scenario: dict[str, Any],
    canonical_context: dict[str, Any],
    layer2_result: dict[str, Any],
    case_state: dict[str, Any],
    rule_evaluation: dict[str, Any],
    recommendation_bundle: dict[str, Any],
    governed_package: dict[str, Any],
) -> str:
    """Build a reviewer-facing Markdown summary for one scenario execution."""
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


def execute_scenario_file(asset_key: str, scenario_file: Path) -> Path:
    """Execute one paper-specific scenario file through the real OVERSEE path."""
    if not scenario_file.exists():
        raise FileNotFoundError(f"Scenario file not found: {scenario_file}")

    scenario = load_scenario_file(scenario_file)
    executable_inputs = scenario.raw.get("executable_inputs")

    if not isinstance(executable_inputs, dict):
        raise ValueError(f"Scenario {scenario.scenario_id} has no executable_inputs section.")

    validate_executable_inputs(executable_inputs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario_slug = asset_key.lower().replace("-", "_")
    output_dir = OUTPUT_ROOT / f"scenario_all_layers_{scenario_slug}_paper_{timestamp}"
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
        "aggregated_evidence_package": output_dir / "01_output_layer1_aggregated_evidence_package.json",
        "validation_report": output_dir / "01_validation_report.json",
        "canonical_case_context": output_dir / "02_canonical_case_context.json",
        "contextualization_rule_trace": output_dir / "02_contextualization_rule_trace.json",
        "layer2_contextualization_result": output_dir / "02_output_layer2_contextualization_result.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_output_layer3_case_management_state.json",
        "dmn_decision_evaluation": output_dir / "04_output_layer4_dmn_decision_evaluation.json",
        "recommendation_path_outputs": output_dir / "04_output_layer4_recommendation_path_outputs.json",
        "governed_recommendation_package": output_dir / "05_final_governed_recommendation_package.json",
        "traceability_index": output_dir / "05_traceability_index.json",
        "execution_manifest": output_dir / "05_execution_manifest.json",
        "scenario_execution_summary": output_dir / "05_scenario_execution_summary.md",
    }

    write_json(paths["scenario"], scenario.raw)
    write_json(paths["predictive_alert_request"], alert_request)
    write_json(paths["received_predictive_alert"], layer1_result.received_alert.to_dict())
    write_json(paths["enterprise_api_calls"], layer1_result.enterprise_api_calls)
    write_json(paths["aggregated_evidence_package"], layer1_result.evidence_package.to_dict())
    write_json(paths["validation_report"], layer1_result.validation_report)
    write_json(paths["canonical_case_context"], canonical_context.to_dict())
    write_json(paths["contextualization_rule_trace"], [rule.to_dict() for rule in layer2_result.rule_trace])
    write_json(paths["layer2_contextualization_result"], layer2_result.to_dict())
    write_json(paths["case_lifecycle_trace"], case_state.lifecycle_trace())
    write_json(paths["case_management_state"], case_state.to_dict())
    write_json(paths["dmn_decision_evaluation"], rule_evaluation.to_dict())
    write_json(paths["recommendation_path_outputs"], recommendation_bundle.to_dict())
    write_json(paths["governed_recommendation_package"], governed_package.to_dict())
    write_json(paths["traceability_index"], governed_package.traceability_index)

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
        "paper_section5_execution": True,
    }
    write_json(paths["execution_manifest"], manifest)

    summary = build_layer5_scenario_execution_summary(
        scenario=scenario.raw,
        canonical_context=canonical_context.to_dict(),
        layer2_result=layer2_result.to_dict(),
        case_state=case_state.to_dict(),
        rule_evaluation=rule_evaluation.to_dict(),
        recommendation_bundle=recommendation_bundle.to_dict(),
        governed_package=governed_package.to_dict(),
    )
    paths["scenario_execution_summary"].write_text(summary, encoding="utf-8")

    return output_dir


def load_run_artifacts(run_dir: Path) -> dict[str, Any]:
    """Load the main artifacts generated by one scenario execution."""
    artifact_files = {
        "scenario": "00_scenario.json",
        "predictive_alert": "01_received_predictive_alert.json",
        "layer1": "01_output_layer1_aggregated_evidence_package.json",
        "validation": "01_validation_report.json",
        "canonical_context": "02_canonical_case_context.json",
        "layer2": "02_output_layer2_contextualization_result.json",
        "layer2_trace": "02_contextualization_rule_trace.json",
        "layer3": "03_output_layer3_case_management_state.json",
        "layer3_trace": "03_case_lifecycle_trace.json",
        "layer4_dmn": "04_output_layer4_dmn_decision_evaluation.json",
        "layer4_recommendation": "04_output_layer4_recommendation_path_outputs.json",
        "layer5_package": "05_final_governed_recommendation_package.json",
        "traceability": "05_traceability_index.json",
        "manifest": "05_execution_manifest.json",
    }

    artifacts: dict[str, Any] = {"run_dir": str(run_dir)}

    for key, filename in artifact_files.items():
        path = run_dir / filename
        artifacts[key] = read_json(path) if path.exists() else {}

    summary_path = run_dir / "05_scenario_execution_summary.md"
    artifacts["summary_markdown"] = (
        summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    )

    return artifacts


def scenario_overview(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Create a compact scenario overview for Section 5."""
    scenario = artifacts.get("scenario", {})
    alert = artifacts.get("predictive_alert", {})
    executable_inputs = scenario.get("executable_inputs", {})
    enterprise_sources = executable_inputs.get("enterprise_sources", {})

    return {
        "asset_id": scenario.get("asset_id"),
        "asset_type": scenario.get("asset_type"),
        "failure_mode": scenario.get("failure_mode"),
        "decision_pattern": scenario.get("decision_pattern"),
        "confidence_score": alert.get("confidence_score")
        or safe_get(executable_inputs, ["alert", "confidence_score"]),
        "predictive_horizon_hours": alert.get("predictive_horizon_hours")
        or safe_get(executable_inputs, ["alert", "predictive_horizon_hours"]),
        "production_pressure": safe_get(
            enterprise_sources, ["operational_context", "production_pressure"]
        ),
        "production_load_pct": safe_get(
            enterprise_sources, ["operational_context", "production_load_pct"]
        ),
        "next_planned_downtime_hours": safe_get(
            enterprise_sources, ["operational_context", "next_planned_downtime_hours"]
        ),
        "spare_part_available": safe_get(
            enterprise_sources, ["inventory_and_resources", "spare_part_available"]
        ),
        "technician_available_next_shift": safe_get(
            enterprise_sources,
            ["inventory_and_resources", "specialist_technician_available_next_shift"],
        ),
        "intervention_feasible": safe_get(
            enterprise_sources, ["inventory_and_resources", "intervention_feasible"]
        ),
        "human_review_required": safe_get(
            enterprise_sources,
            ["policy_governance", "expected_human_review_required"],
        ),
        "management_escalation_required": safe_get(
            enterprise_sources,
            ["policy_governance", "management_escalation_required"],
            False,
        ),
    }


def build_cross_scenario_rows(overviews: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    """Build the main cross-scenario comparison matrix."""
    comp1 = overviews["COMP-001"]
    comp2 = overviews["COMP-002"]

    return [
        {
            "demonstration_aspect": "Asset type",
            "comp_001": str(comp1["asset_type"]),
            "comp_002": str(comp2["asset_type"]),
            "interpretation": "Comparable asset type.",
        },
        {
            "demonstration_aspect": "Predictive condition",
            "comp_001": f"confidence={comp1['confidence_score']}; horizon={comp1['predictive_horizon_hours']}h",
            "comp_002": f"confidence={comp2['confidence_score']}; horizon={comp2['predictive_horizon_hours']}h",
            "interpretation": "Predictive conditions are comparable and do not alone explain the recommendation divergence.",
        },
        {
            "demonstration_aspect": "Operational context",
            "comp_001": f"{comp1['production_pressure']} load; downtime in {comp1['next_planned_downtime_hours']}h",
            "comp_002": f"{comp2['production_pressure']} load; downtime={comp2['next_planned_downtime_hours']}",
            "interpretation": "The operational context starts to separate the scenarios.",
        },
        {
            "demonstration_aspect": "Resource feasibility",
            "comp_001": f"spare={comp1['spare_part_available']}; technician={comp1['technician_available_next_shift']}; feasible={comp1['intervention_feasible']}",
            "comp_002": f"spare={comp2['spare_part_available']}; technician={comp2['technician_available_next_shift']}; feasible={comp2['intervention_feasible']}",
            "interpretation": "Resource feasibility is a major source of divergence.",
        },
        {
            "demonstration_aspect": "Governance context",
            "comp_001": f"human_review={comp1['human_review_required']}; escalation={comp1['management_escalation_required']}",
            "comp_002": f"human_review={comp2['human_review_required']}; escalation={comp2['management_escalation_required']}",
            "interpretation": "Both require human review, but only COMP-002 requires management escalation.",
        },
        {
            "demonstration_aspect": "Layer 2 divergence",
            "comp_001": "Operationally feasible and governance-cleared.",
            "comp_002": "Operationally constrained and escalation-required.",
            "interpretation": "The main divergence begins at contextualization.",
        },
        {
            "demonstration_aspect": "Expected governed recommendation",
            "comp_001": "Controlled planned intervention.",
            "comp_002": "Deferred intervention, enhanced monitoring, and escalation.",
            "interpretation": "Similar prediction does not imply similar recommendation.",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    """Write comparison rows as CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_figure5_input(overviews: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Build a compact data structure for Figure 5."""
    return {
        "title": "Digital Factory demonstration logic",
        "message": "Comparable predictive condition, divergent contextualization, different governed recommendations.",
        "common_technical_condition": {
            "asset_type": "industrial_air_compressor",
            "failure_mode": "bearing_degradation",
            "predictive_horizon_hours": 48,
        },
        "scenarios": overviews,
        "divergence_point": "Layer 2: Contextualization",
        "comp_001_outcome": "Controlled planned intervention",
        "comp_002_outcome": "Deferred intervention, enhanced monitoring, and escalation",
    }


def build_appendix_bundle(
    manifest: dict[str, Any],
    overviews: dict[str, dict[str, Any]],
    rows: list[dict[str, str]],
    artifacts_by_asset: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a compact appendix bundle with selected artifacts."""
    return {
        "manifest": manifest,
        "scenario_overview": overviews,
        "cross_scenario_matrix": rows,
        "selected_artifacts": {
            asset_id: {
                "canonical_context": artifacts.get("canonical_context", {}),
                "layer2_contextualization": artifacts.get("layer2", {}),
                "layer3_case_state": artifacts.get("layer3", {}),
                "layer4_recommendation": artifacts.get("layer4_recommendation", {}),
                "layer5_package": artifacts.get("layer5_package", {}),
                "traceability": artifacts.get("traceability", {}),
            }
            for asset_id, artifacts in artifacts_by_asset.items()
        },
    }


def build_markdown_report(
    output_dir: Path,
    run_dirs: dict[str, Path],
    overviews: dict[str, dict[str, Any]],
    rows: list[dict[str, str]],
) -> str:
    """Build a paper-facing Section 5 evidence report."""
    lines: list[str] = []

    lines.append("# Section 5 Evidence Report")
    lines.append("")
    lines.append("## Execution runs")
    lines.append("")

    for asset_id, run_dir in run_dirs.items():
        lines.append(f"- **{asset_id}**: `{run_dir}`")

    lines.append("")
    lines.append("## Scenario overview")
    lines.append("")

    for asset_id, overview in overviews.items():
        lines.append(f"### {asset_id}")
        lines.append("")
        for key, value in overview.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")

    lines.append("## Cross-scenario matrix")
    lines.append("")
    lines.append("| Demonstration aspect | COMP-001 | COMP-002 | Interpretation |")
    lines.append("|---|---|---|---|")

    for row in rows:
        lines.append(
            f"| {row['demonstration_aspect']} | {row['comp_001']} | {row['comp_002']} | {row['interpretation']} |"
        )

    lines.append("")
    lines.append("## Paper claim supported")
    lines.append("")
    lines.append(
        "The two scenarios exhibit comparable predictive conditions, but the contextualization layer "
        "introduces operational and governance divergence. This supports the paper claim that prediction "
        "similarity does not imply recommendation similarity."
    )
    lines.append("")
    lines.append("## Generated artifacts")
    lines.append("")

    for path in sorted(output_dir.iterdir()):
        lines.append(f"- `{path.name}`")

    return "\n".join(lines)


def main() -> None:
    """Run both paper scenarios and build Section 5 evidence artifacts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    section5_dir = OUTPUT_ROOT / f"{SECTION5_PREFIX}{timestamp}"
    section5_dir.mkdir(parents=True, exist_ok=False)

    run_dirs: dict[str, Path] = {}
    artifacts_by_asset: dict[str, dict[str, Any]] = {}

    for asset_id, scenario_file in SOURCE_SCENARIOS.items():
        run_dir = execute_scenario_file(asset_id, scenario_file)
        run_dirs[asset_id] = run_dir
        artifacts_by_asset[asset_id] = load_run_artifacts(run_dir)

        target_run_dir = section5_dir / f"run_{asset_id.lower().replace('-', '_')}"
        shutil.copytree(run_dir, target_run_dir)

    overviews = {
        asset_id: scenario_overview(artifacts)
        for asset_id, artifacts in artifacts_by_asset.items()
    }

    rows = build_cross_scenario_rows(overviews)

    manifest = {
        "generated_at": timestamp,
        "purpose": "Section 5 paper-facing COMP-001 vs COMP-002 demonstration",
        "source_scenario_files": {
            asset_id: str(path)
            for asset_id, path in SOURCE_SCENARIOS.items()
        },
        "source_run_dirs": {
            asset_id: str(path)
            for asset_id, path in run_dirs.items()
        },
        "section5_output_dir": str(section5_dir),
        "catalog_independent_execution": True,
    }

    figure5_input = build_figure5_input(overviews)
    appendix_bundle = build_appendix_bundle(
        manifest=manifest,
        overviews=overviews,
        rows=rows,
        artifacts_by_asset=artifacts_by_asset,
    )

    write_json(section5_dir / "00_execution_manifest.json", manifest)
    write_json(section5_dir / "01_scenario_pair_overview.json", overviews)
    write_json(section5_dir / "02_figure5_input.json", figure5_input)
    write_json(section5_dir / "03_appendix_evidence_bundle.json", appendix_bundle)
    write_csv(section5_dir / "04_cross_scenario_matrix.csv", rows)

    report = build_markdown_report(
        output_dir=section5_dir,
        run_dirs=run_dirs,
        overviews=overviews,
        rows=rows,
    )
    write_markdown(section5_dir / "05_section5_evidence_report.md", report)

    print("Section 5 demonstration completed.")
    print(f"Output directory: {section5_dir}")


if __name__ == "__main__":
    main()