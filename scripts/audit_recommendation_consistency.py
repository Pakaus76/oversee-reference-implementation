"""Recommendation consistency audit for OVERSEE.

Purpose:
    Run all executable scenarios and check whether final governed
    recommendations are coherent with feasibility, readiness, execution mode,
    blockers, and human review signals.

Output:
    A timestamped audit folder under outputs/ with JSON and Markdown reports.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from demo.interactive_walkthrough.scenario_catalog import list_scenarios  # noqa: E402
from scripts.run_scenario_all_layers_demo import run_scenario_all_layers  # noqa: E402


OUTPUT_ROOT = PROJECT_ROOT / "outputs"
AUDIT_PREFIX = "recommendation_consistency_audit_"


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    """Write a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    """Write a Markdown file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def find_output_dir(result: dict[str, Any]) -> Path:
    """Return the output directory from a scenario execution result."""
    output_dir = Path(str(result["output_dir"]))
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")
    return output_dir


def audit_package(package: dict[str, Any]) -> list[str]:
    """Return consistency issues detected in one governed package."""
    issues: list[str] = []

    recommendation = package.get("final_recommendation", {})
    action = str(recommendation.get("recommended_action", "")).lower()

    intervention_feasible = bool(recommendation.get("intervention_feasible"))
    decision_ready = bool(recommendation.get("decision_ready"))
    human_review_required = bool(recommendation.get("human_review_required"))
    execution_mode = str(recommendation.get("recommended_execution_mode", ""))
    transformation_applied = bool(recommendation.get("transformation_applied", False))

    blockers = recommendation.get("blockers", [])
    preconditions = recommendation.get("preconditions", [])
    required_reviews = recommendation.get("required_reviews", [])
    escalations = recommendation.get("escalations", [])
    contingency_actions = recommendation.get("contingency_actions", [])

    immediate_terms = ["immediate", "execute now", "uncontrolled stop"]
    constraint_terms = ["constrain", "escalate", "monitor", "contingency", "defer", "blocker"]

    if not intervention_feasible and any(term in action for term in immediate_terms):
        issues.append(
            "Intervention is not feasible, but the recommendation contains unqualified immediate-execution wording."
        )

    if not decision_ready and not blockers and not preconditions:
        issues.append(
            "Case is not decision-ready, but no blockers or preconditions are preserved in the final package."
        )

    if execution_mode == "constrained_execution":
        if not transformation_applied:
            issues.append(
                "Execution mode is constrained_execution, but transformation_applied is false."
            )

        if not any(term in action for term in constraint_terms):
            issues.append(
                "Execution mode is constrained_execution, but the recommended action does not mention constraint handling."
            )

        if not escalations and not contingency_actions:
            issues.append(
                "Execution mode is constrained_execution, but no escalation or contingency actions are preserved."
            )

    if human_review_required and not required_reviews:
        issues.append(
            "Human review is required, but required_reviews is empty."
        )

    return issues


def build_markdown_report(results: list[dict[str, Any]]) -> str:
    """Build a compact Markdown audit report."""
    lines: list[str] = [
        "# OVERSEE Recommendation Consistency Audit",
        "",
        "| Scenario | Asset | Status | Issues |",
        "|---|---|---|---|",
    ]

    for item in results:
        issue_text = "<br>".join(item["issues"]) if item["issues"] else "-"
        lines.append(
            f"| {item['scenario_id']} | {item['asset_id']} | {item['status']} | {issue_text} |"
        )

    passed = sum(1 for item in results if item["status"] == "PASS")
    total = len(results)

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Scenarios audited: {total}",
            f"- Passed: {passed}",
            f"- Failed: {total - passed}",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    """Run the recommendation consistency audit."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audit_dir = OUTPUT_ROOT / f"{AUDIT_PREFIX}{timestamp}"
    audit_dir.mkdir(parents=True, exist_ok=False)

    audit_results: list[dict[str, Any]] = []

    scenarios = [
        scenario
        for scenario in list_scenarios()
        if "executable_inputs" in scenario.raw
    ]

    seen_ids: set[str] = set()

    for scenario in scenarios:
        if scenario.scenario_id in seen_ids:
            continue

        seen_ids.add(scenario.scenario_id)

        try:
            result = run_scenario_all_layers(scenario.scenario_id)
            output_dir = find_output_dir(result)
            package_path = output_dir / "05_final_governed_recommendation_package.json"
            package = read_json(package_path)
            issues = audit_package(package)

            audit_results.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "asset_id": scenario.asset_id,
                    "output_dir": str(output_dir),
                    "status": "PASS" if not issues else "FAIL",
                    "issues": issues,
                }
            )

        except Exception as exc:  # noqa: BLE001
            audit_results.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "asset_id": scenario.asset_id,
                    "output_dir": None,
                    "status": "ERROR",
                    "issues": [str(exc)],
                }
            )

    write_json(audit_dir / "recommendation_consistency_audit.json", audit_results)
    write_markdown(
        audit_dir / "recommendation_consistency_audit.md",
        build_markdown_report(audit_results),
    )

    print("Recommendation consistency audit completed.")
    print(f"Audit directory: {audit_dir}")


if __name__ == "__main__":
    main()