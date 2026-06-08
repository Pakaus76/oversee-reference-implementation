"""Tests for DATA-001 diagnostic/evidence-quality behaviour."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.run_scenario_all_layers_demo import run_scenario_all_layers


def test_data001_triggers_diagnostic_review_from_data_quality_flags() -> None:
    """DATA-001 should not look like a standard planning case."""

    output_dir: Path | None = None

    try:
        result = run_scenario_all_layers("DATA-001")
        output_dir = Path(result["output_dir"])

        assert result["scenario_id"] == "DATA-001"
        assert result["layer1_evidence_package_valid"] is False
        assert result["case_lifecycle_stage"] == "evidence_review"
        assert result["recommended_execution_mode"] == "diagnostic_review"
        assert result["human_review_required"] is True

        validation_report = json.loads(
            (output_dir / "01_validation_report.json").read_text(encoding="utf-8")
        )
        canonical_context = json.loads(
            (output_dir / "02_canonical_case_context.json").read_text(encoding="utf-8")
        )
        dmn_evaluation = json.loads(
            (output_dir / "04_output_layer4_dmn_decision_evaluation.json").read_text(encoding="utf-8")
        )

        assert validation_report["valid"] is False
        assert "sensor_historian" in validation_report["payloads_with_quality_flags"]

        assert "sensor_historian:contradictory_temperature_vibration_evidence" in (
            canonical_context["data_quality_flags"]
        )
        assert "sensor_historian:thermal_channel_requires_review" in (
            canonical_context["data_quality_flags"]
        )

        execution_rule = next(
            rule for rule in dmn_evaluation["rules"] if rule["rule_id"] == "DMN_R005"
        )

        assert execution_rule["output_fields"]["recommended_execution_mode"] == (
            "diagnostic_review"
        )
        assert execution_rule["triggered"] is True
        assert execution_rule["input_fields"]["data_quality_flags"]

    finally:
        if output_dir is not None and output_dir.exists():
            shutil.rmtree(output_dir)
