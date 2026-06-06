"""Scenario catalog for the interactive OVERSEE walkthrough."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCENARIO_DIR = Path(__file__).resolve().parent / "scenarios"


@dataclass(frozen=True)
class DemoScenario:
    """Scenario metadata and paper-facing walkthrough data."""

    scenario_id: str
    title: str
    description: str
    asset_id: str
    asset_type: str
    failure_mode: str
    paper_aligned: bool
    layer_inputs: dict[str, list[dict[str, str]]]
    expected_layer_outputs: dict[str, str]
    raw: dict[str, Any]


def load_scenario_file(path: Path) -> DemoScenario:
    """Load one scenario JSON file."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))

    return DemoScenario(
        scenario_id=data["scenario_id"],
        title=data["title"],
        description=data["description"],
        asset_id=data["asset_id"],
        asset_type=data["asset_type"],
        failure_mode=data["failure_mode"],
        paper_aligned=bool(data.get("paper_aligned", False)),
        layer_inputs=data["layer_inputs"],
        expected_layer_outputs=data["expected_layer_outputs"],
        raw=data,
    )


def list_scenarios() -> list[DemoScenario]:
    """Return all available demo scenarios."""
    scenario_files = sorted(SCENARIO_DIR.glob("*.json"))
    scenarios = [load_scenario_file(path) for path in scenario_files]

    return sorted(scenarios, key=lambda item: item.scenario_id)


def get_scenario(scenario_id: str) -> DemoScenario:
    """Return a scenario by identifier."""
    normalized = scenario_id.strip().upper()

    for scenario in list_scenarios():
        if scenario.scenario_id.upper() == normalized:
            return scenario

    available = ", ".join(scenario.scenario_id for scenario in list_scenarios())
    raise ValueError(f"Unknown scenario '{scenario_id}'. Available scenarios: {available}")


def get_default_scenario() -> DemoScenario:
    """Return the default scenario for the reviewer-facing walkthrough."""
    return get_scenario("COMP-001")

