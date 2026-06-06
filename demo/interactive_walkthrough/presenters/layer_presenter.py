"""Layer presenters for the interactive OVERSEE walkthrough."""

from __future__ import annotations

from demo.interactive_walkthrough.adapters.placeholder_adapter import record_expected_layer_output
from demo.interactive_walkthrough.adapters.scenario_all_layers_adapter import (
    run_real_scenario_layer,
)
from demo.interactive_walkthrough.demo_state import DemoRunState
from demo.interactive_walkthrough.display import print_bullets, print_key_values, print_section
from demo.interactive_walkthrough.presenters.common import maybe_pause, present_layer_inputs


LAYER_TITLES = {
    "layer1": "Layer 1 - Evidence intake, aggregation and validation",
    "layer2": "Layer 2 - Contextualization",
    "layer3": "Layer 3 - Case lifecycle",
    "layer4": "Layer 4 - Decision logic",
    "layer5": "Layer 5 - Governed packaging and traceability",
}

LAYER_MECHANISMS = {
    "layer1": [
        "Input validation",
        "Source harmonization",
        "Evidence aggregation",
        "Provenance capture",
    ],
    "layer2": [
        "Operational contextualization",
        "Feasibility assessment",
        "Policy interpretation",
        "DMN-like contextualization rules",
    ],
    "layer3": [
        "CMMN-inspired lifecycle management",
        "Task activation",
        "Milestone and blocker tracking",
        "Decision-readiness assessment",
    ],
    "layer4": [
        "DMN-like decision evaluation",
        "Priority assignment",
        "Execution-mode selection",
        "Policy checks",
        "Recommendation formulation",
    ],
    "layer5": [
        "Traceability assembly",
        "Reviewer summary generation",
        "Audit-ready serialization",
        "Workflow handoff",
    ],
}


def present_layer(
    state: DemoRunState,
    layer_id: str,
    pause_enabled: bool,
    show_artifacts: bool = False,
) -> None:
    """Present one layer and record its output."""

    title = LAYER_TITLES[layer_id]
    inputs = state.scenario.layer_inputs[layer_id]

    present_layer_inputs(title, inputs)

    print("\nProcessing mechanism:")
    print_bullets(LAYER_MECHANISMS[layer_id])

    artifact = _execute_layer(state, layer_id)

    print("\nLayer output:")
    print(artifact["expected_output_summary"])

    print("\nExecution mode:")
    print(artifact["mode"])

    if artifact["mode"].startswith("real_oversee_"):
        _present_real_artifact_summary(state, layer_id, artifact, show_artifacts)
    else:
        print("\nGenerated demo artifact:")
        artifact_key = f"{layer_id}_placeholder"
        print_key_values({"path": state.generated_artifacts[artifact_key]})

    maybe_pause(pause_enabled)


def _present_real_artifact_summary(
    state: DemoRunState,
    layer_id: str,
    artifact: dict[str, object],
    show_artifacts: bool,
) -> None:
    """Present a concise summary of copied real artifacts."""

    copied_files = artifact.get("copied_files", [])
    execution_result = artifact.get("scenario_execution_result", {})

    print("\nReal OVERSEE scenario execution:")
    if isinstance(execution_result, dict):
        print_key_values(
            {
                "case_id": execution_result.get("case_id"),
                "priority": execution_result.get("dmn_decision_final_priority"),
                "execution_mode": execution_result.get("recommended_execution_mode"),
                "intervention_feasible": execution_result.get("intervention_feasible"),
                "human_review_required": execution_result.get("human_review_required"),
            }
        )

    print("\nInteractive demo capture:")
    print(f"- Copied real artifacts for this layer: {len(copied_files)}")
    print("- Temporary scenario runner output copied into this demo folder and cleaned.")

    if show_artifacts:
        print("\nCopied real artifacts for this layer:")
        for file_path in copied_files:
            print(f"- {file_path}")
    else:
        print("- Detailed artifact list hidden. Use --show-artifacts for expert inspection.")


def _execute_layer(state: DemoRunState, layer_id: str) -> dict[str, object]:
    """Execute one walkthrough layer using the real scenario runner when possible."""

    if layer_id in {"layer1", "layer2", "layer3", "layer4", "layer5"}:
        if "executable_inputs" in state.scenario.raw:
            if state.scenario_execution_result is None:
                print("\nExecuting real OVERSEE multi-scenario path...")
            else:
                print("\nReusing real OVERSEE scenario execution artifacts...")
            return run_real_scenario_layer(state, layer_id)

        print(
            f"\n{layer_id} has no executable_inputs section. "
            "This scenario uses a presentation placeholder."
        )

    return record_expected_layer_output(state, layer_id)


def present_final_summary(
    state: DemoRunState,
    show_artifacts: bool = False,
) -> None:
    """Present the final walkthrough summary."""

    print_section("End-to-end walkthrough summary")

    print("Layer outputs:")
    for layer_id, output in state.layer_outputs.items():
        print(f"- {layer_id}: {output}")

    if state.scenario_execution_result is not None:
        print("\nScenario execution result:")
        print_key_values(
            {
                "case_id": state.scenario_execution_result.get("case_id"),
                "priority": state.scenario_execution_result.get(
                    "dmn_decision_final_priority"
                ),
                "execution_mode": state.scenario_execution_result.get(
                    "recommended_execution_mode"
                ),
                "intervention_feasible": state.scenario_execution_result.get(
                    "intervention_feasible"
                ),
                "human_review_required": state.scenario_execution_result.get(
                    "human_review_required"
                ),
            }
        )

    print("\nDemo output folder:")
    print(state.output_dir)

    summary_path = state.generated_artifacts.get("demo_walkthrough_summary")
    manifest_path = state.generated_artifacts.get("demo_run_manifest")

    if summary_path is not None:
        print(f"\nConcise walkthrough summary: {summary_path}")

    if manifest_path is not None:
        print(f"Run manifest: {manifest_path}")

    if show_artifacts:
        print("\nGenerated artifacts:")
        for key, path in state.generated_artifacts.items():
            print(f"- {key}: {path}")
    else:
        print("\nDetailed artifact list hidden. Use --show-artifacts for expert inspection.")

    print(
        "\nCurrent integration status: executable scenarios are connected to the "
        "real OVERSEE multi-scenario all-layers runner. Scenarios without "
        "executable_inputs remain available in presentation mode."
    )