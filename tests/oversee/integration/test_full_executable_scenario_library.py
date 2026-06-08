"""Regression tests for the full executable scenario library."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from demo.interactive_walkthrough.scenario_catalog import get_scenario, list_scenarios
from scripts.run_scenario_all_layers_demo import run_scenario_all_layers


EXPECTED_SCENARIOS = [
    "COMP-001",
    "COMP-002",
    "PUMP-001",
    "CONV-001",
    "DATA-001",
    "FAN-001",
    "MOTOR-001",
    "GEAR-001",
    "ROBOT-001",
    "CHILLER-001",
    "BOILER-001",
    "VALVE-001",
    "AGV-001",
    "PACK-001",
    "CIP-001",
    "HVAC-001",
    "PUMP-002",
    "COMP-003",
    "SENSOR-001",
    "MIXER-001",
]

MASTER_SCENARIOS = {
    "COMP-001",
    "COMP-002",
    "PUMP-001",
    "CONV-001",
    "DATA-001",
}

DIAGNOSTIC_REVIEW_SCENARIOS = {
    "DATA-001",
    "VALVE-001",
    "SENSOR-001",
}

CONSTRAINED_EXECUTION_SCENARIOS = {
    "PUMP-001",
    "PUMP-002",
    "COMP-003",
}

ALLOWED_PRIORITIES = {"low", "medium", "high", "critical"}

ALLOWED_EXECUTION_MODES = {
    "standard_planning",
    "controlled_planning",
    "constrained_execution",
    "diagnostic_review",
}


def test_catalog_contains_exactly_the_expected_executable_scenarios() -> None:
    """The scenario catalog should expose the full 20-scenario library."""

    scenarios = list_scenarios()
    scenario_ids = [scenario.scenario_id for scenario in scenarios]

    assert sorted(scenario_ids) == sorted(EXPECTED_SCENARIOS)
    assert len(scenario_ids) == 20
    assert len(set(scenario_ids)) == 20

    for scenario_id in EXPECTED_SCENARIOS:
        scenario = get_scenario(scenario_id)

        assert "executable_inputs" in scenario.raw
        assert set(scenario.raw["executable_inputs"]) == {
            "alert",
            "raw_sensor_context",
            "requested_context",
            "enterprise_sources",
        }

        assert scenario.raw["master_case"] is (scenario_id in MASTER_SCENARIOS)


@pytest.mark.parametrize("scenario_id", EXPECTED_SCENARIOS)
def test_every_executable_scenario_runs_through_real_all_layers_path(
    scenario_id: str,
) -> None:
    """Every scenario should execute through the real Layer 1 to Layer 5 runner."""

    output_dir: Path | None = None

    try:
        result = run_scenario_all_layers(scenario_id)
        output_dir = Path(result["output_dir"])

        assert result["scenario_id"] == scenario_id
        assert result["layer2_decision_ready"] is True
        assert result["generated_file_count"] >= 10

        assert result["dmn_decision_final_priority"] in ALLOWED_PRIORITIES
        assert result["recommended_execution_mode"] in ALLOWED_EXECUTION_MODES
        assert isinstance(result["intervention_feasible"], bool)
        assert isinstance(result["human_review_required"], bool)

        if scenario_id in DIAGNOSTIC_REVIEW_SCENARIOS:
            assert result["layer1_evidence_package_valid"] is False
            assert result["case_lifecycle_stage"] == "evidence_review"
            assert result["recommended_execution_mode"] == "diagnostic_review"
        else:
            assert result["layer1_evidence_package_valid"] is True

        if scenario_id in CONSTRAINED_EXECUTION_SCENARIOS:
            assert result["intervention_feasible"] is False
            assert result["recommended_execution_mode"] == "constrained_execution"

        assert output_dir.exists()
        assert (output_dir / "00_scenario.json").exists()
        assert (output_dir / "00_predictive_alert_request.json").exists()
        assert (output_dir / "01_output_layer1_aggregated_evidence_package.json").exists()
        assert (output_dir / "01_validation_report.json").exists()
        assert (output_dir / "02_canonical_case_context.json").exists()
        assert (output_dir / "02_output_layer2_contextualization_result.json").exists()
        assert (output_dir / "03_output_layer3_case_management_state.json").exists()
        assert (output_dir / "04_output_layer4_dmn_decision_evaluation.json").exists()
        assert (output_dir / "05_final_governed_recommendation_package.json").exists()
        assert (output_dir / "05_scenario_execution_summary.md").exists()

    finally:
        if output_dir is not None and output_dir.exists():
            shutil.rmtree(output_dir)
