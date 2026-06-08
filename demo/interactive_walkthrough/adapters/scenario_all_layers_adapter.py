"""Adapter from the interactive walkthrough to the executable scenario runner."""

from __future__ import annotations

import shutil
from pathlib import Path

from demo.interactive_walkthrough.adapters.placeholder_adapter import (
    record_expected_layer_output,
)
from demo.interactive_walkthrough.demo_state import DemoRunState
from scripts.run_scenario_all_layers_demo import run_scenario_all_layers


LAYER_ARTIFACTS = {
    "layer1": [
        "00_predictive_alert_request.json",
        "01_received_predictive_alert.json",
        "01_enterprise_api_calls.json",
        "01_output_layer1_aggregated_evidence_package.json",
        "01_validation_report.json",
    ],
    "layer2": [
        "02_canonical_case_context.json",
        "02_contextualization_rule_trace.json",
        "02_output_layer2_contextualization_result.json",
    ],
    "layer3": [
        "03_case_lifecycle_trace.json",
        "03_output_layer3_case_management_state.json",
    ],
    "layer4": [
        "04_output_layer4_dmn_decision_evaluation.json",
        "04_output_layer4_recommendation_path_outputs.json",
    ],
    "layer5": [
        "05_final_governed_recommendation_package.json",
        "05_traceability_index.json",
        "05_execution_manifest.json",
        "05_scenario_execution_summary.md",
    ],
}


def run_real_scenario_layer(state: DemoRunState, layer_id: str) -> dict[str, object]:
    """Return the real scenario execution artifact summary for one layer."""

    if "executable_inputs" not in state.scenario.raw:
        return record_expected_layer_output(state, layer_id)

    _ensure_real_scenario_execution(state)

    expected_output = state.scenario.expected_layer_outputs[layer_id]
    state.record_layer_output(layer_id, expected_output)

    return {
        "mode": "real_oversee_scenario_all_layers_runner",
        "expected_output_summary": expected_output,
        "source_output_dir": str(state.scenario_source_output_dir),
        "source_output_dir_cleaned": True,
        "copied_files": state.scenario_layer_artifacts.get(layer_id, []),
        "scenario_execution_result": state.scenario_execution_result or {},
    }


def _ensure_real_scenario_execution(state: DemoRunState) -> None:
    """Execute the all-layers scenario runner once and copy artifacts."""

    if state.scenario_execution_result is not None:
        return

    result = run_scenario_all_layers(state.scenario.scenario_id)
    source_output_dir = Path(result["output_dir"])

    state.scenario_execution_result = result
    state.scenario_source_output_dir = source_output_dir

    _copy_scenario_runner_artifacts(state, source_output_dir)

    if source_output_dir.exists():
        shutil.rmtree(source_output_dir)


def _copy_scenario_runner_artifacts(
    state: DemoRunState,
    source_output_dir: Path,
) -> None:
    """Copy the scenario runner artifacts into the interactive demo output folder."""

    for layer_id, filenames in LAYER_ARTIFACTS.items():
        copied_paths: list[Path] = []

        for filename in filenames:
            source_path = source_output_dir / filename

            if not source_path.exists():
                continue

            destination_path = state.output_dir / f"real_{filename}"
            shutil.copy2(source_path, destination_path)

            artifact_key = f"real_{Path(filename).stem}"
            state.record_artifact(artifact_key, destination_path)
            copied_paths.append(destination_path)

        state.scenario_layer_artifacts[layer_id] = copied_paths