"""Tests for the OVERSEE deterministic-versus-generative comparison."""

from __future__ import annotations

import json
import os
from pathlib import Path

from oversee.comparison.deterministic_generative_comparison import (
    run_deterministic_generative_comparison,
)


def test_deterministic_generative_comparison_offline_outputs(tmp_path: Path) -> None:
    """The offline comparison should generate complete reviewer-facing outputs."""

    os.environ.pop("OPENAI_API_KEY", None)

    result = run_deterministic_generative_comparison(outputs_root=tmp_path)

    summary = result["summary"]
    rows = result["comparison_rows"]
    paths = result["paths"]

    assert summary["case_count"] == 3
    assert summary["live_generative_fallback_count"] == 3
    assert summary["live_generative_model_response_count"] == 0
    assert len(rows) == 3

    expected_files = [
        "scenarios",
        "oversee_inputs",
        "deterministic_results",
        "live_generative_results",
        "comparison_json",
        "comparison_csv",
        "summary",
    ]

    for key in expected_files:
        assert paths[key].exists()
        assert paths[key].stat().st_size > 0


def test_deterministic_generative_comparison_uses_public_terminology(tmp_path: Path) -> None:
    """The comparison output should avoid legacy experiment terminology."""

    os.environ.pop("OPENAI_API_KEY", None)

    result = run_deterministic_generative_comparison(outputs_root=tmp_path)
    serialized_output = json.dumps(
        {
            "summary": result["summary"],
            "comparison_rows": result["comparison_rows"],
            "deterministic_results": result["deterministic_results"],
            "live_generative_results": result["live_generative_results"],
        },
        ensure_ascii=False,
    ).lower()

    forbidden_terms = [
        "decision orchestrator",
        "decision_orchestrator",
        "dual_generative_do",
        "condition c",
        "condition_c",
        "run_condition_c",
        "condition d",
        "condition_d",
        "run_condition_d",
        "condition e",
        "condition_e",
        "run_condition_e",
        "condition f",
        "condition_f",
        "run_condition_f",
        "c-vs-f",
        "c_vs_f",
        "orch_input",
    ]

    for term in forbidden_terms:
        assert term not in serialized_output
