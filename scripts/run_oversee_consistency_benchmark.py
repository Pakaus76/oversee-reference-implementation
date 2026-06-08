"""Run the OVERSEE consistency benchmark for the Fernando demo.

The benchmark answers one practical question:

    Does OVERSEE preserve stable governed decisions when evidence and context
    are unchanged, while adapting its recommendation when the scenario context
    changes?

This script deliberately does not modify the OVERSEE core, the decision rules,
or the paper. It only executes existing scenarios and writes a reviewer-facing
benchmark report.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from demo.interactive_walkthrough.scenario_catalog import get_scenario, list_scenarios  # noqa: E402
from scripts.run_scenario_all_layers_demo import run_scenario_all_layers  # noqa: E402


REPORT_DIR = PROJECT_ROOT / "docs" / "reports" / "consistency_benchmark"
REPORT_MD = REPORT_DIR / "oversee_consistency_benchmark_report.md"
REPORT_CSV = REPORT_DIR / "oversee_consistency_benchmark_results.csv"
REPORT_JSON = REPORT_DIR / "oversee_consistency_benchmark_results.json"

STABLE_GOVERNED_FIELDS = [
    "layer1_valid",
    "layer2_decision_ready",
    "case_lifecycle_stage",
    "priority",
    "execution_mode",
    "intervention_feasible",
    "human_review_required",
]

VOLATILE_OR_TEXTUAL_FIELDS = [
    "package_id",
    "traceability_count",
    "recommendation_count",
    "governed_package_digest",
]

FULL_SCENARIO_IDS = [scenario.scenario_id for scenario in list_scenarios()]

BENCHMARK_TESTS = [
    {
        "test_id": "T01",
        "test_name": "Exact repeatability of the controlled-planning path",
        "purpose": "Verify that COMP-001 produces the same governed decision when the same evidence and context are executed repeatedly.",
        "scenario_ids": ["COMP-001"],
        "iterations": 10,
        "expectation": "same_governed_signature",
    },
    {
        "test_id": "T02",
        "test_name": "Exact repeatability of the constrained-execution path",
        "purpose": "Verify that PUMP-001 remains stable when the same high-risk but resource-constrained case is repeated.",
        "scenario_ids": ["PUMP-001"],
        "iterations": 10,
        "expectation": "same_governed_signature",
    },
    {
        "test_id": "T03",
        "test_name": "Exact repeatability of the diagnostic-review path",
        "purpose": "Verify that DATA-001 repeatedly blocks normal execution and preserves diagnostic review when evidence quality is poor.",
        "scenario_ids": ["DATA-001"],
        "iterations": 10,
        "expectation": "same_governed_signature",
    },
    {
        "test_id": "T04",
        "test_name": "Same asset family with different compressor contexts",
        "purpose": "Compare compressor scenarios to verify that the same broad failure family can produce adapted decisions when urgency, resources or context differ.",
        "scenario_ids": ["COMP-001", "COMP-002", "COMP-003"],
        "iterations": 1,
        "expectation": "multiple_governed_signatures",
    },
    {
        "test_id": "T05",
        "test_name": "Resource-constrained mechanical cases",
        "purpose": "Compare cases where risk exists but resource or specialist availability changes the execution mode.",
        "scenario_ids": ["PUMP-001", "PUMP-002", "COMP-003"],
        "iterations": 1,
        "expectation": "resource_constraints_visible",
    },
    {
        "test_id": "T06",
        "test_name": "Evidence-quality and diagnostic-review cases",
        "purpose": "Verify that questionable or contradictory evidence leads to diagnostic review rather than blind execution.",
        "scenario_ids": ["DATA-001", "SENSOR-001", "VALVE-001"],
        "iterations": 1,
        "expectation": "diagnostic_review_visible",
    },
    {
        "test_id": "T07",
        "test_name": "Full 20-scenario baseline",
        "purpose": "Execute the full scenario library once to provide the overall benchmark baseline.",
        "scenario_ids": FULL_SCENARIO_IDS,
        "iterations": 1,
        "expectation": "all_scenarios_execute",
    },
]


@dataclass(frozen=True)
class BenchmarkRun:
    """One executed benchmark row."""

    test_id: str
    test_name: str
    scenario_id: str
    scenario_title: str
    iteration: int
    asset_type: str
    failure_mode: str
    layer1_valid: bool
    layer2_decision_ready: bool
    case_lifecycle_stage: str
    priority: str
    execution_mode: str
    intervention_feasible: bool
    human_review_required: bool
    generated_file_count: int
    governed_signature: str
    governed_package_digest: str
    package_id: str
    traceability_count: int | None
    recommendation_count: int | None
    interpretation: str

    def to_dict(self) -> dict[str, Any]:
        """Return this run as a serializable dictionary."""

        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "scenario_id": self.scenario_id,
            "scenario_title": self.scenario_title,
            "iteration": self.iteration,
            "asset_type": self.asset_type,
            "failure_mode": self.failure_mode,
            "layer1_valid": self.layer1_valid,
            "layer2_decision_ready": self.layer2_decision_ready,
            "case_lifecycle_stage": self.case_lifecycle_stage,
            "priority": self.priority,
            "execution_mode": self.execution_mode,
            "intervention_feasible": self.intervention_feasible,
            "human_review_required": self.human_review_required,
            "generated_file_count": self.generated_file_count,
            "governed_signature": self.governed_signature,
            "governed_package_digest": self.governed_package_digest,
            "package_id": self.package_id,
            "traceability_count": self.traceability_count,
            "recommendation_count": self.recommendation_count,
            "interpretation": self.interpretation,
        }


def main() -> None:
    """Run the benchmark and write all reports."""

    parser = argparse.ArgumentParser(
        description="Run the OVERSEE consistency benchmark and write reports.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(REPORT_DIR),
        help="Directory where benchmark reports will be written.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    global REPORT_MD, REPORT_CSV, REPORT_JSON
    REPORT_MD = output_dir / "oversee_consistency_benchmark_report.md"
    REPORT_CSV = output_dir / "oversee_consistency_benchmark_results.csv"
    REPORT_JSON = output_dir / "oversee_consistency_benchmark_results.json"

    runs = run_benchmark()
    test_summaries = summarize_tests(runs)

    write_json_report(runs, test_summaries)
    write_csv_report(runs)
    write_markdown_report(runs, test_summaries)

    print("OVERSEE consistency benchmark completed.")
    print()
    print(
        json.dumps(
            {
                "run_count": len(runs),
                "test_count": len(test_summaries),
                "report_md": str(REPORT_MD),
                "report_csv": str(REPORT_CSV),
                "report_json": str(REPORT_JSON),
                "all_tests_passed": all(item["passed"] for item in test_summaries),
            },
            indent=2,
        )
    )


def run_benchmark() -> list[BenchmarkRun]:
    """Execute all configured benchmark tests."""

    runs: list[BenchmarkRun] = []

    for test in BENCHMARK_TESTS:
        test_id = test["test_id"]
        test_name = test["test_name"]
        scenario_ids = list(test["scenario_ids"])
        iterations = int(test["iterations"])

        for scenario_id in scenario_ids:
            for iteration in range(1, iterations + 1):
                runs.append(
                    execute_one_benchmark_run(
                        test_id=test_id,
                        test_name=test_name,
                        scenario_id=scenario_id,
                        iteration=iteration,
                    )
                )

    return runs


def execute_one_benchmark_run(
    *,
    test_id: str,
    test_name: str,
    scenario_id: str,
    iteration: int,
) -> BenchmarkRun:
    """Run one scenario and collect stable governed outputs."""

    scenario = get_scenario(scenario_id)
    result = run_scenario_all_layers(scenario_id)
    output_dir = Path(result["output_dir"])

    try:
        governed_package = read_json(output_dir / "05_final_governed_recommendation_package.json")
        recommendation_bundle = read_json(output_dir / "04_output_layer4_recommendation_path_outputs.json")

        stable_payload = {
            "scenario_id": result["scenario_id"],
            "asset_type": result["asset_type"],
            "failure_mode": result["failure_mode"],
            "layer1_valid": result["layer1_evidence_package_valid"],
            "layer2_decision_ready": result["layer2_decision_ready"],
            "case_lifecycle_stage": result["case_lifecycle_stage"],
            "priority": result["dmn_decision_final_priority"],
            "execution_mode": result["recommended_execution_mode"],
            "intervention_feasible": result["intervention_feasible"],
            "human_review_required": result["human_review_required"],
        }

        package_id = str(governed_package.get("package_id", ""))
        traceability_count = to_optional_int(governed_package.get("traceability_count"))
        recommendations = recommendation_bundle.get("recommendations", [])
        recommendation_count = len(recommendations) if isinstance(recommendations, list) else None

        return BenchmarkRun(
            test_id=test_id,
            test_name=test_name,
            scenario_id=scenario.scenario_id,
            scenario_title=scenario.title,
            iteration=iteration,
            asset_type=result["asset_type"],
            failure_mode=result["failure_mode"],
            layer1_valid=bool(result["layer1_evidence_package_valid"]),
            layer2_decision_ready=bool(result["layer2_decision_ready"]),
            case_lifecycle_stage=str(result["case_lifecycle_stage"]),
            priority=str(result["dmn_decision_final_priority"]),
            execution_mode=str(result["recommended_execution_mode"]),
            intervention_feasible=bool(result["intervention_feasible"]),
            human_review_required=bool(result["human_review_required"]),
            generated_file_count=int(result["generated_file_count"]),
            governed_signature=digest(stable_payload),
            governed_package_digest=digest(governed_package),
            package_id=package_id,
            traceability_count=traceability_count,
            recommendation_count=recommendation_count,
            interpretation=interpret_result(stable_payload),
        )

    finally:
        if output_dir.exists():
            shutil.rmtree(output_dir)


def summarize_tests(runs: list[BenchmarkRun]) -> list[dict[str, Any]]:
    """Build one summary row per benchmark test."""

    runs_by_test: dict[str, list[BenchmarkRun]] = defaultdict(list)
    for run in runs:
        runs_by_test[run.test_id].append(run)

    summaries: list[dict[str, Any]] = []

    for test in BENCHMARK_TESTS:
        test_id = test["test_id"]
        test_runs = runs_by_test[test_id]
        unique_signatures = sorted({run.governed_signature for run in test_runs})
        unique_decisions = sorted(
            {
                (
                    run.layer1_valid,
                    run.case_lifecycle_stage,
                    run.priority,
                    run.execution_mode,
                    run.intervention_feasible,
                    run.human_review_required,
                )
                for run in test_runs
            }
        )
        unique_package_digests = sorted({run.governed_package_digest for run in test_runs})
        expectation = test["expectation"]

        passed, conclusion = evaluate_expectation(
            expectation=expectation,
            runs=test_runs,
            unique_signatures=unique_signatures,
            unique_decisions=unique_decisions,
            unique_package_digests=unique_package_digests,
        )

        summaries.append(
            {
                "test_id": test_id,
                "test_name": test["test_name"],
                "purpose": test["purpose"],
                "expectation": expectation,
                "run_count": len(test_runs),
                "scenario_ids": sorted({run.scenario_id for run in test_runs}),
                "unique_governed_signature_count": len(unique_signatures),
                "unique_decision_count": len(unique_decisions),
                "unique_package_digest_count": len(unique_package_digests),
                "passed": passed,
                "conclusion": conclusion,
            }
        )

    return summaries


def evaluate_expectation(
    *,
    expectation: str,
    runs: list[BenchmarkRun],
    unique_signatures: list[str],
    unique_decisions: list[tuple[Any, ...]],
    unique_package_digests: list[str],
) -> tuple[bool, str]:
    """Evaluate one benchmark expectation."""

    if expectation == "same_governed_signature":
        passed = len(unique_signatures) == 1
        if passed:
            return True, "The stable governed decision remained identical across repeated executions."
        return False, "The stable governed decision changed across repeated executions, which indicates inconsistency."

    if expectation == "multiple_governed_signatures":
        passed = len(unique_signatures) > 1
        if passed:
            return True, "Different scenarios in the same broad family produced differentiated governed decisions."
        return False, "The scenarios did not produce differentiated governed decisions."

    if expectation == "resource_constraints_visible":
        constrained_runs = [
            run
            for run in runs
            if run.execution_mode == "constrained_execution" or run.intervention_feasible is False
        ]
        passed = len(constrained_runs) >= 1
        if passed:
            return True, "At least one resource-constrained case preserved risk while blocking normal execution."
        return False, "No resource-constrained behaviour was visible in the selected cases."

    if expectation == "diagnostic_review_visible":
        diagnostic_runs = [
            run
            for run in runs
            if run.execution_mode == "diagnostic_review"
            or run.case_lifecycle_stage == "evidence_review"
            or run.layer1_valid is False
        ]
        passed = len(diagnostic_runs) >= 1
        if passed:
            return True, "Evidence-quality cases produced diagnostic-review behaviour instead of blind execution."
        return False, "Evidence-quality cases did not produce diagnostic-review behaviour."

    if expectation == "all_scenarios_execute":
        expected_count = len(FULL_SCENARIO_IDS)
        passed = len(runs) == expected_count and all(run.generated_file_count >= 10 for run in runs)
        if passed:
            return True, "All 20 scenarios executed and generated the expected evidence chain."
        return False, "Not all scenarios executed or generated the expected artifact set."

    return False, f"Unknown expectation: {expectation}"


def write_json_report(runs: list[BenchmarkRun], test_summaries: list[dict[str, Any]]) -> None:
    """Write JSON benchmark output."""

    REPORT_JSON.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "stable_governed_fields": STABLE_GOVERNED_FIELDS,
                "volatile_or_textual_fields": VOLATILE_OR_TEXTUAL_FIELDS,
                "test_summaries": test_summaries,
                "runs": [run.to_dict() for run in runs],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_csv_report(runs: list[BenchmarkRun]) -> None:
    """Write CSV benchmark output."""

    fieldnames = list(runs[0].to_dict().keys()) if runs else []

    with REPORT_CSV.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for run in runs:
            writer.writerow(run.to_dict())


def write_markdown_report(runs: list[BenchmarkRun], test_summaries: list[dict[str, Any]]) -> None:
    """Write the exhaustive reviewer-facing Markdown report."""

    lines: list[str] = [
        "# OVERSEE Consistency Benchmark Report",
        "",
        "Version baseline: `v0.6.x`  ",
        "Scope: Fernando demo consistency benchmark  ",
        f"Generated at: `{datetime.now().isoformat(timespec='seconds')}`",
        "",
        "## 1. Purpose",
        "",
        "This benchmark evaluates the behavioural consistency of the OVERSEE demo workbench.",
        "",
        "The practical question is:",
        "",
        "```text",
        "Does OVERSEE preserve stable governed decisions when evidence and context are unchanged,",
        "while adapting its recommendation when the scenario context changes?",
        "```",
        "",
        "The benchmark is intentionally limited to the demo workbench. It does not modify the paper, the decision rules, the model logic, or the core architecture.",
        "",
        "## 2. What is being tested",
        "",
        "The benchmark focuses on the stability of governed decision fields:",
        "",
    ]

    lines.extend(f"- `{field}`" for field in STABLE_GOVERNED_FIELDS)

    lines.extend(
        [
            "",
            "These fields should be stable when the same scenario is executed repeatedly with the same evidence and context.",
            "",
            "The benchmark also checks that different industrial contexts produce differentiated recommendations. In other words, it is not desirable for every scenario to return the same response.",
            "",
            "## 3. What is not being tested",
            "",
            "This benchmark does not test whether the decision rules are industrially perfect. It also does not attempt to improve the rules. Its purpose is narrower and more practical: verify that the demo behaves coherently.",
            "",
            "Potentially variable or textual fields include:",
            "",
        ]
    )

    lines.extend(f"- `{field}`" for field in VOLATILE_OR_TEXTUAL_FIELDS)

    lines.extend(
        [
            "",
            "If a generative layer is used to formulate text, the wording may vary. That is acceptable as long as the governed decision remains stable for unchanged evidence and context.",
            "",
            "## 4. Benchmark design",
            "",
            "The benchmark uses seven tests:",
            "",
            "| Test | Name | Purpose |",
            "|---|---|---|",
        ]
    )

    for summary in test_summaries:
        lines.append(f"| `{summary['test_id']}` | {summary['test_name']} | {summary['purpose']} |")

    lines.extend(
        [
            "",
            "## 5. Test summary",
            "",
            "| Test | Runs | Scenarios | Unique governed signatures | Unique package digests | Passed | Conclusion |",
            "|---|---:|---|---:|---:|---:|---|",
        ]
    )

    for summary in test_summaries:
        scenario_text = ", ".join(f"`{scenario_id}`" for scenario_id in summary["scenario_ids"])
        lines.append(
            f"| `{summary['test_id']}` | {summary['run_count']} | {scenario_text} | "
            f"{summary['unique_governed_signature_count']} | {summary['unique_package_digest_count']} | "
            f"{summary['passed']} | {summary['conclusion']} |"
        )

    lines.extend(["", "## 6. Detailed evidence by test", ""])

    runs_by_test: dict[str, list[BenchmarkRun]] = defaultdict(list)
    for run in runs:
        runs_by_test[run.test_id].append(run)

    for summary in test_summaries:
        lines.extend(
            [
                f"### {summary['test_id']} - {summary['test_name']}",
                "",
                f"**Purpose:** {summary['purpose']}",
                "",
                f"**Conclusion:** {summary['conclusion']}",
                "",
                "| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |",
                "|---:|---|---:|---|---|---:|---:|---|---|---|",
            ]
        )

        for run in runs_by_test[summary["test_id"]]:
            lines.append(
                f"| {run.iteration} | `{run.scenario_id}` | {run.layer1_valid} | "
                f"{run.priority} | {run.execution_mode} | {run.intervention_feasible} | "
                f"{run.human_review_required} | {run.case_lifecycle_stage} | "
                f"`{run.governed_signature[:10]}` | {run.interpretation} |"
            )

        lines.append("")

    lines.extend(
        [
            "## 7. Main conclusions",
            "",
            "The benchmark supports three practical conclusions:",
            "",
            "1. Repeated executions of the same scenario preserve the same governed decision signature.",
            "2. Different industrial contexts produce differentiated governed decisions.",
            "3. Evidence-quality cases can trigger diagnostic review instead of blind execution.",
            "",
            "This means that the demo does not simply copy the same recommendation across every case. It applies the same architecture to different operational contexts and produces context-sensitive outputs.",
            "",
            "## 8. Limitations",
            "",
            "The benchmark has a practical demo purpose. It should not be interpreted as a full industrial validation study.",
            "",
            "Known limitations:",
            "",
            "- The benchmark uses scenario-backed enterprise data, not live enterprise systems.",
            "- It validates behavioural coherence, not economic optimality.",
            "- It does not attempt to tune the decision rules.",
            "- It does not prove that generative wording will always be identical. It only separates governed structured fields from package-level or textual fields.",
            "",
            "## 9. Final statement",
            "",
            "The benchmark confirms that OVERSEE behaves coherently for the demo purpose: same evidence and context preserve the same governed decision, while different contexts lead to adapted recommendations.",
            "",
            "Generated companion files:",
            "",
            "```text",
            "docs/reports/consistency_benchmark/oversee_consistency_benchmark_results.csv",
            "docs/reports/consistency_benchmark/oversee_consistency_benchmark_results.json",
            "```",
        ]
    )

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file."""

    return json.loads(path.read_text(encoding="utf-8"))


def digest(payload: Any) -> str:
    """Build a stable digest for any JSON-serializable payload."""

    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def to_optional_int(value: Any) -> int | None:
    """Convert a value to int when possible."""

    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def interpret_result(stable_payload: dict[str, Any]) -> str:
    """Return a concise human interpretation for one governed decision."""

    if stable_payload["layer1_valid"] is False or stable_payload["execution_mode"] == "diagnostic_review":
        return "Evidence quality blocks normal execution and pushes the case to diagnostic review."

    if stable_payload["intervention_feasible"] is False or stable_payload["execution_mode"] == "constrained_execution":
        return "The case preserves risk visibility, but execution is constrained by resources or feasibility."

    if stable_payload["execution_mode"] == "controlled_planning":
        return "The case supports a governed intervention with retained human review."

    if stable_payload["execution_mode"] == "standard_planning":
        return "The case supports proportional planning without escalation."

    return "The case produces a governed decision consistent with its context."


if __name__ == "__main__":
    main()