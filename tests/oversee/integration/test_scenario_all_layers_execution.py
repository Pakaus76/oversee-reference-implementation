"""Tests for executable multi-scenario all-layers runner."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from scripts.run_scenario_all_layers_demo import run_scenario_all_layers


EXPECTED_SCENARIO_OUTCOMES = {
    "COMP-001": {
        "case_lifecycle_stage": "decision_ready",
        "dmn_decision_final_priority": "high",
        "recommended_execution_mode": "controlled_planning",
        "intervention_feasible": True,
        "human_review_required": True,
    },
    "COMP-002": {
        "case_lifecycle_stage": "evidence_review",
        "dmn_decision_final_priority": "medium",
        "recommended_execution_mode": "standard_planning",
        "intervention_feasible": True,
        "human_review_required": True,
    },
    "PUMP-001": {
        "case_lifecycle_stage": "evidence_review",
        "dmn_decision_final_priority": "high",
        "recommended_execution_mode": "constrained_execution",
        "intervention_feasible": False,
        "human_review_required": True,
    },
}


@pytest.mark.parametrize("scenario_id", ["COMP-001", "COMP-002", "PUMP-001"])
def test_scenario_all_layers_runner_executes_current_master_scenarios(
    scenario_id: str,
) -> None:
    """Current master scenarios should execute through the real all-layers path."""

    output_dir: Path | None = None

    try:
        expected = EXPECTED_SCENARIO_OUTCOMES[scenario_id]
        result = run_scenario_all_layers(scenario_id)

        assert result["scenario_id"] == scenario_id
        assert result["layer1_evidence_package_valid"] is True
        assert result["layer2_decision_ready"] is True

        assert result["case_lifecycle_stage"] == expected["case_lifecycle_stage"]
        assert result["dmn_decision_final_priority"] == expected["dmn_decision_final_priority"]
        assert result["recommended_execution_mode"] == expected["recommended_execution_mode"]
        assert result["intervention_feasible"] is expected["intervention_feasible"]
        assert result["human_review_required"] is expected["human_review_required"]

        assert result["generated_file_count"] >= 10

        output_dir = Path(result["output_dir"])

        assert output_dir.exists()
        assert (output_dir / "01_output_layer1_aggregated_evidence_package.json").exists()
        assert (output_dir / "02_output_layer2_contextualization_result.json").exists()
        assert (output_dir / "03_output_layer3_case_management_state.json").exists()
        assert (output_dir / "04_output_layer4_dmn_decision_evaluation.json").exists()
        assert (output_dir / "05_final_governed_recommendation_package.json").exists()
        assert (output_dir / "05_scenario_execution_summary.md").exists()

    finally:
        if output_dir is not None and output_dir.exists():
            shutil.rmtree(output_dir)