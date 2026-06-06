"""Tests for the five executable master scenarios."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from demo.interactive_walkthrough.scenario_catalog import get_scenario, list_scenarios
from scripts.run_scenario_all_layers_demo import run_scenario_all_layers


MASTER_SCENARIOS = ["COMP-001", "COMP-002", "PUMP-001", "CONV-001", "DATA-001"]

EXPECTED_LAYER1_VALIDITY = {
    "COMP-001": True,
    "COMP-002": True,
    "PUMP-001": True,
    "CONV-001": True,
    "DATA-001": False,
}


def test_master_scenario_catalog_contains_five_master_cases() -> None:
    """The scenario catalog should expose the five master scenarios."""

    scenario_ids = {scenario.scenario_id for scenario in list_scenarios()}

    assert set(MASTER_SCENARIOS).issubset(scenario_ids)

    for scenario_id in MASTER_SCENARIOS:
        scenario = get_scenario(scenario_id)
        assert scenario.raw["master_case"] is True
        assert "executable_inputs" in scenario.raw


@pytest.mark.parametrize("scenario_id", MASTER_SCENARIOS)
def test_master_scenarios_execute_real_all_layers_path(scenario_id: str) -> None:
    """Each master scenario should execute through the real all-layers path."""

    output_dir: Path | None = None

    try:
        result = run_scenario_all_layers(scenario_id)

        assert result["scenario_id"] == scenario_id
        assert result["layer1_evidence_package_valid"] is EXPECTED_LAYER1_VALIDITY[scenario_id]
        assert result["layer2_decision_ready"] is True
        assert result["generated_file_count"] >= 10

        output_dir = Path(result["output_dir"])

        assert output_dir.exists()
        assert (output_dir / "01_aggregated_evidence_package.json").exists()
        assert (output_dir / "02_layer2_contextualization_result.json").exists()
        assert (output_dir / "03_case_management_state.json").exists()
        assert (output_dir / "04_dmn_decision_evaluation.json").exists()
        assert (output_dir / "05_governed_recommendation_package.json").exists()
        assert (output_dir / "05_scenario_execution_summary.md").exists()

    finally:
        if output_dir is not None and output_dir.exists():
            shutil.rmtree(output_dir)
