"""Intro presenter for the interactive OVERSEE walkthrough."""

from __future__ import annotations

from demo.interactive_walkthrough.demo_state import DemoRunState
from demo.interactive_walkthrough.display import print_bullets, print_key_values, print_section, print_title
from demo.interactive_walkthrough.presenters.common import maybe_pause


def present_intro(state: DemoRunState, pause_enabled: bool) -> None:
    """Present the demo introduction and selected scenario."""
    scenario = state.scenario

    print_title("OVERSEE interactive walkthrough")

    print(
        "\nThis walkthrough uses Figure 3 as the guide. "
        "The aim is to see how enterprise information becomes a governed recommendation package."
    )
    print(
        "\nThe demo code is only a presentation layer. "
        "It does not modify the OVERSEE core."
    )

    print_section("Selected scenario")
    print_key_values(
        {
            "Scenario": scenario.scenario_id,
            "Title": scenario.title,
            "Asset": scenario.asset_id,
            "Asset type": scenario.asset_type,
            "Failure mode": scenario.failure_mode,
            "Paper aligned": scenario.paper_aligned,
            "Output folder": state.output_dir,
        }
    )
    print(f"Description: {scenario.description}")

    maybe_pause(pause_enabled)


def present_architecture_path(pause_enabled: bool) -> None:
    """Present the architecture path from Figure 3."""
    print_section("Figure 3 walkthrough path")
    print_bullets(
        [
            "Enterprise sources provide information through the API access layer.",
            "Layer 1 validates and aggregates evidence.",
            "Layer 2 contextualizes the evidence through DMN-like rules.",
            "Layer 3 manages the case lifecycle using CMMN-inspired concepts.",
            "Layer 4 formulates the decision record through DMN-like decision logic.",
            "Layer 5 packages the result for review, workflow handoff, and audit.",
        ]
    )

    maybe_pause(pause_enabled)
