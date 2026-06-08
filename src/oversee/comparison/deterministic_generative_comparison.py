"""
Deterministic-versus-generative comparison for OVERSEE.

This module runs the Digital Factory scenarios through two OVERSEE paths:

1. deterministic anchor
2. live generative path

The objective is not to prove that one path is universally better. The objective
is to expose comparable recommendation outputs, governance signals, fallback
status, and traceability fields for reviewer-facing inspection.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from oversee.digital_factory import (
    build_bridge_ready_payloads,
    evaluate_deterministic_anchor_candidates,
    evaluate_live_generative_path_candidates,
    generate_compressor_scenarios,
    map_bridge_ready_payloads_to_oversee_inputs,
)


def to_dict(value: Any) -> Any:
    """Convert dataclass-like objects into dictionaries."""

    if is_dataclass(value):
        return asdict(value)

    if hasattr(value, "to_dict"):
        return value.to_dict()

    if isinstance(value, list):
        return [to_dict(item) for item in value]

    if isinstance(value, dict):
        return {key: to_dict(item) for key, item in value.items()}

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def build_comparison_rows(
    deterministic_results: list[Any],
    live_generative_results: list[Any],
) -> list[dict[str, Any]]:
    """Build comparison rows keyed by source case ID."""

    deterministic_by_case = {
        to_dict(result)["source_case_id"]: to_dict(result)
        for result in deterministic_results
    }

    live_by_case = {
        to_dict(result)["source_case_id"]: to_dict(result)
        for result in live_generative_results
    }

    rows: list[dict[str, Any]] = []

    for source_case_id in sorted(deterministic_by_case):
        deterministic = deterministic_by_case[source_case_id]
        live = live_by_case[source_case_id]

        deterministic_action = deterministic.get("action")
        live_action = live.get("action")

        deterministic_priority = deterministic.get("priority")
        live_priority = live.get("priority")

        deterministic_rationale = deterministic.get("rationale", "")
        live_rationale = live.get("rationale", "")

        row = {
            "source_case_id": source_case_id,
            "candidate_id": deterministic.get("candidate_id"),
            "expected_decision_posture": deterministic.get("expected_decision_posture"),
            "expected_human_review_required": deterministic.get("expected_human_review_required"),
            "deterministic_recommendation_id": deterministic.get("recommendation_id"),
            "live_generative_recommendation_id": live.get("recommendation_id"),
            "deterministic_priority": deterministic_priority,
            "live_generative_priority": live_priority,
            "priority_changed": deterministic_priority != live_priority,
            "deterministic_action": deterministic_action,
            "live_generative_action": live_action,
            "action_changed": deterministic_action != live_action,
            "deterministic_rationale": deterministic_rationale,
            "live_generative_rationale": live_rationale,
            "rationale_changed": deterministic_rationale != live_rationale,
            "live_generative_fallback_detected": live.get("fallback_detected"),
            "live_generative_fallback_anchor": live.get("fallback_anchor"),
            "live_generative_model_response_id_present": live.get("model_response_id_present"),
            "live_generative_evidence_reference_detected": live.get("evidence_reference_detected"),
            "live_generative_priority_governance_detected": live.get("priority_governance_detected"),
            "deterministic_path_invoked": deterministic.get("deterministic_anchor_invoked"),
            "live_generative_path_invoked": live.get("live_generative_path_invoked"),
        }

        rows.append(row)

    return rows


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a compact comparison summary."""

    return {
        "case_count": len(rows),
        "action_differences": sum(1 for row in rows if row["action_changed"]),
        "priority_differences": sum(1 for row in rows if row["priority_changed"]),
        "rationale_differences": sum(1 for row in rows if row["rationale_changed"]),
        "live_generative_fallback_count": sum(
            1 for row in rows if row["live_generative_fallback_detected"]
        ),
        "live_generative_model_response_count": sum(
            1 for row in rows if row["live_generative_model_response_id_present"]
        ),
        "live_generative_evidence_reference_count": sum(
            1 for row in rows if row["live_generative_evidence_reference_detected"]
        ),
        "live_generative_priority_governance_count": sum(
            1 for row in rows if row["live_generative_priority_governance_detected"]
        ),
    }


def write_json(path: Path, payload: Any) -> None:
    """Write JSON output."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write comparison rows as CSV."""

    path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_comparison_run_folder(outputs_root: str | Path = "outputs") -> Path:
    """Create a timestamped comparison output folder."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = Path(outputs_root) / f"deterministic_generative_comparison_{timestamp}"
    run_folder.mkdir(parents=True, exist_ok=True)
    return run_folder


def run_deterministic_generative_comparison(
    outputs_root: str | Path = "outputs",
) -> dict[str, Any]:
    """
    Run Digital Factory scenarios through deterministic and live generative paths.

    Returns a dictionary containing scenarios, inputs, recommendations,
    comparison rows, summary metrics, and output paths.
    """

    run_folder = create_comparison_run_folder(outputs_root)

    scenarios = generate_compressor_scenarios()
    scenario_dicts = [scenario.to_dict() for scenario in scenarios]

    bridge_payloads = build_bridge_ready_payloads(scenario_dicts)
    bridge_payload_dicts = [payload.to_dict() for payload in bridge_payloads]

    oversee_inputs = map_bridge_ready_payloads_to_oversee_inputs(bridge_payload_dicts)
    oversee_input_dicts = [candidate.to_dict() for candidate in oversee_inputs]

    deterministic_results = evaluate_deterministic_anchor_candidates(oversee_input_dicts)
    live_generative_results = evaluate_live_generative_path_candidates(oversee_input_dicts)

    deterministic_dicts = [to_dict(result) for result in deterministic_results]
    live_generative_dicts = [to_dict(result) for result in live_generative_results]

    rows = build_comparison_rows(
        deterministic_results=deterministic_results,
        live_generative_results=live_generative_results,
    )

    summary = build_summary(rows)

    paths = {
        "scenarios": run_folder / "01_digital_factory_scenarios.json",
        "oversee_inputs": run_folder / "02_oversee_input_candidates.json",
        "deterministic_results": run_folder / "03_deterministic_anchor_results.json",
        "live_generative_results": run_folder / "04_live_generative_path_results.json",
        "comparison_json": run_folder / "05_deterministic_generative_comparison.json",
        "comparison_csv": run_folder / "05_deterministic_generative_comparison.csv",
        "summary": run_folder / "06_comparison_summary.json",
    }

    write_json(paths["scenarios"], scenario_dicts)
    write_json(paths["oversee_inputs"], oversee_input_dicts)
    write_json(paths["deterministic_results"], deterministic_dicts)
    write_json(paths["live_generative_results"], live_generative_dicts)
    write_json(paths["comparison_json"], rows)
    write_csv(paths["comparison_csv"], rows)
    write_json(paths["summary"], summary)

    return {
        "run_folder": run_folder,
        "scenarios": scenario_dicts,
        "oversee_inputs": oversee_input_dicts,
        "deterministic_results": deterministic_dicts,
        "live_generative_results": live_generative_dicts,
        "comparison_rows": rows,
        "summary": summary,
        "paths": paths,
    }
