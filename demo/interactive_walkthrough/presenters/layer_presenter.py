"""Layer presenters for the interactive OVERSEE walkthrough."""

from __future__ import annotations

from demo.interactive_walkthrough.adapters.placeholder_adapter import record_expected_layer_output
from demo.interactive_walkthrough.adapters.real_layer1_adapter import run_real_layer1
from demo.interactive_walkthrough.adapters.real_layer2_adapter import run_real_layer2
from demo.interactive_walkthrough.adapters.real_layer3_adapter import run_real_layer3
from demo.interactive_walkthrough.adapters.real_layer4_adapter import run_real_layer4
from demo.interactive_walkthrough.adapters.real_layer5_adapter import run_real_layer5
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
    manifest_key = f"{layer_id}_real_execution_manifest"
    manifest_path = state.generated_artifacts.get(manifest_key)

    print("\nReal OVERSEE source output directory:")
    print(artifact["source_output_dir"])

    print("\nInteractive demo capture:")
    print(f"- Copied real artifacts: {len(copied_files)}")
    if manifest_path is not None:
        print(f"- Layer execution manifest: {manifest_path}")

    if show_artifacts:
        print("\nCopied real artifacts:")
        for file_path in copied_files:
            print(f"- {file_path}")
    else:
        print("- Detailed artifact list hidden. Use --show-artifacts for expert inspection.")


def _execute_layer(state: DemoRunState, layer_id: str) -> dict[str, object]:
    """Execute one walkthrough layer.

    Layers 1 to 5 use existing OVERSEE execution paths for the paper-aligned
    COMP-001 scenario. Alternative scenarios remain in presentation mode.
    """
    if state.scenario.scenario_id == "COMP-001":
        if layer_id == "layer1":
            print("\nExecuting existing OVERSEE Layer 1 path...")
            return run_real_layer1(state)

        if layer_id == "layer2":
            print("\nExecuting existing OVERSEE Layer 2 path...")
            return run_real_layer2(state)

        if layer_id == "layer3":
            print("\nExecuting existing OVERSEE Layer 3 path...")
            return run_real_layer3(state)

        if layer_id == "layer4":
            print("\nExecuting existing OVERSEE Layer 4 path...")
            return run_real_layer4(state)

        if layer_id == "layer5":
            print("\nExecuting existing OVERSEE Layer 5 path...")
            return run_real_layer5(state)

    if layer_id in {"layer1", "layer2", "layer3", "layer4", "layer5"}:
        print(
            f"\n{layer_id} real execution is currently enabled only for the "
            "paper-aligned COMP-001 scenario. This scenario uses a presentation placeholder."
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
        "\nCurrent integration status: Layers 1 to 5 are connected to existing "
        "OVERSEE execution paths for the paper-aligned COMP-001 scenario. "
        "Alternative scenarios remain available in presentation mode."
    )
