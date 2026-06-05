"""Interactive OVERSEE walkthrough.

This module is a presentation layer.
It does not implement OVERSEE logic and does not modify the OVERSEE core.
"""

from __future__ import annotations

import argparse

from demo.interactive_walkthrough.demo_state import DemoRunState
from demo.interactive_walkthrough.output_manager import (
    create_demo_output_dir,
    write_json,
    write_text,
)
from demo.interactive_walkthrough.presenters.intro_presenter import (
    present_architecture_path,
    present_intro,
)
from demo.interactive_walkthrough.presenters.layer_presenter import (
    present_final_summary,
    present_layer,
)
from demo.interactive_walkthrough.scenario_catalog import (
    DemoScenario,
    get_default_scenario,
    get_scenario,
    list_scenarios,
)


def main() -> None:
    """Run the interactive walkthrough."""
    args = _parse_args()

    if args.list_scenarios:
        _print_available_scenarios()
        return

    scenario = get_scenario(args.scenario) if args.scenario else get_default_scenario()
    pause_enabled = not args.no_pause

    state = DemoRunState(
        scenario=scenario,
        output_dir=create_demo_output_dir(),
    )

    present_intro(state, pause_enabled)
    present_architecture_path(pause_enabled)

    for layer_id in ["layer1", "layer2", "layer3", "layer4", "layer5"]:
        present_layer(
            state=state,
            layer_id=layer_id,
            pause_enabled=pause_enabled,
            show_artifacts=args.show_artifacts,
        )

    _write_run_outputs(state)
    present_final_summary(state, show_artifacts=args.show_artifacts)


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Interactive walkthrough for the OVERSEE architecture."
    )
    parser.add_argument(
        "--scenario",
        default="COMP-001",
        help="Scenario identifier to use. Default: COMP-001.",
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List available demo scenarios and exit.",
    )
    parser.add_argument(
        "--no-pause",
        action="store_true",
        help="Run the walkthrough without waiting for Enter between sections.",
    )
    parser.add_argument(
        "--show-artifacts",
        action="store_true",
        help="Show the full generated artifact list during the walkthrough.",
    )
    return parser.parse_args()


def _print_available_scenarios() -> None:
    """Print available demo scenarios."""
    from demo.interactive_walkthrough.display import print_title

    print_title("Available OVERSEE walkthrough scenarios")

    for scenario in list_scenarios():
        marker = "paper default" if scenario.paper_aligned else "alternative"
        print(f"\n{scenario.scenario_id} - {scenario.title} ({marker})")
        print(f"Asset: {scenario.asset_id} | Type: {scenario.asset_type}")
        print(f"Failure mode: {scenario.failure_mode}")
        print(f"Description: {scenario.description}")


def _write_run_outputs(state: DemoRunState) -> None:
    """Write the demo summary and manifest."""
    summary_path = state.output_dir / "demo_walkthrough_summary.md"
    write_text(summary_path, _build_summary_markdown(state))
    state.record_artifact("demo_walkthrough_summary", summary_path)

    manifest_path = state.output_dir / "demo_run_manifest.json"
    write_json(manifest_path, state.to_manifest())
    state.record_artifact("demo_run_manifest", manifest_path)


def _build_summary_markdown(state: DemoRunState) -> str:
    """Build a concise walkthrough summary for live review."""
    scenario = state.scenario

    lines = [
        "# OVERSEE Interactive Walkthrough Summary",
        "",
        "## Scenario",
        "",
        f"- Scenario ID: `{scenario.scenario_id}`",
        f"- Title: {scenario.title}",
        f"- Asset: `{scenario.asset_id}`",
        f"- Asset type: `{scenario.asset_type}`",
        f"- Failure mode: `{scenario.failure_mode}`",
        f"- Paper aligned: `{scenario.paper_aligned}`",
        "",
        "## Figure 3 path",
        "",
        "The walkthrough follows the same evidence-to-recommendation path represented in Figure 3.",
        "",
        "## Layer outputs",
        "",
    ]

    for layer_id, output in state.layer_outputs.items():
        lines.append(f"- `{layer_id}`: {output}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The final recommendation is not produced directly from the predictive alert.",
            "It is built through evidence validation, contextualization, case lifecycle management, decision logic, governed packaging, traceability, and human review preparation.",
            "",
            "## Output directory",
            "",
            f"`{state.output_dir}`",
            "",
        ]
    )

    return "\n".join(lines)


if __name__ == "__main__":
    main()
