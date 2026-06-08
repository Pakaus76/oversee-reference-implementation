"""Tests for the interactive walkthrough scenario runner adapter."""

from __future__ import annotations

from pathlib import Path

from demo.interactive_walkthrough.adapters.scenario_all_layers_adapter import (
    run_real_scenario_layer,
)
from demo.interactive_walkthrough.demo_state import DemoRunState
from demo.interactive_walkthrough.scenario_catalog import get_scenario


def test_interactive_adapter_runs_pump_scenario_with_real_artifacts(
    tmp_path: Path,
) -> None:
    """The interactive adapter should execute non-COMP scenarios through the real runner."""

    state = DemoRunState(
        scenario=get_scenario("PUMP-001"),
        output_dir=tmp_path,
    )

    layer1_artifact = run_real_scenario_layer(state, "layer1")
    layer5_artifact = run_real_scenario_layer(state, "layer5")

    assert layer1_artifact["mode"] == "real_oversee_scenario_all_layers_runner"
    assert layer5_artifact["mode"] == "real_oversee_scenario_all_layers_runner"

    assert state.scenario_execution_result is not None
    assert state.scenario_execution_result["scenario_id"] == "PUMP-001"
    assert state.scenario_execution_result["intervention_feasible"] is False
    assert state.scenario_execution_result["recommended_execution_mode"] == "constrained_execution"

    assert state.scenario_source_output_dir is not None
    assert not state.scenario_source_output_dir.exists()

    assert (tmp_path / "real_01_output_layer1_aggregated_evidence_package.json").exists()
    assert (tmp_path / "real_05_final_governed_recommendation_package.json").exists()
    assert len(state.scenario_layer_artifacts["layer1"]) >= 1
    assert len(state.scenario_layer_artifacts["layer5"]) >= 1