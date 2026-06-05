"""Common presenter helpers for the interactive walkthrough."""

from __future__ import annotations

from demo.interactive_walkthrough.display import print_section, print_source_inputs
from demo.interactive_walkthrough.pause import wait_for_user


def maybe_pause(enabled: bool) -> None:
    """Pause only when guided mode is enabled."""
    if enabled:
        wait_for_user()


def present_layer_inputs(layer_title: str, inputs: list[dict[str, str]]) -> None:
    """Present the enterprise/API inputs for a layer."""
    print_section(layer_title)
    print("Enterprise/API inputs aligned with Figure 3:")
    print_source_inputs(inputs)
