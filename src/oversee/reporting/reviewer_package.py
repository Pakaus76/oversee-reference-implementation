"""
Reviewer-facing OVERSEE demo package.

This module builds a clean evidence package for reviewers. It runs the Digital
Factory scenarios through the deterministic anchor and the live generative path,
then adds a Markdown reviewer summary, a traceability index, and an execution
manifest.

The package does not claim that the live generative path is superior. It exposes
what happened, which files were produced, and which governance signals were
observed.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from oversee.comparison.deterministic_generative_comparison import (
    run_deterministic_generative_comparison,
)


EXPECTED_ARTIFACTS = [
    "01_digital_factory_scenarios.json",
    "02_oversee_input_candidates.json",
    "03_deterministic_anchor_results.json",
    "04_live_generative_path_results.json",
    "05_deterministic_generative_comparison.json",
    "05_deterministic_generative_comparison.csv",
    "06_comparison_summary.json",
    "07_reviewer_summary.md",
    "08_traceability_index.json",
    "09_execution_manifest.json",
]


def read_json(path: Path) -> Any:
    """Read one JSON file."""

    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    """Write JSON with stable formatting."""

    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    """Compute the SHA-256 checksum of one file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)

    return digest.hexdigest()


def build_reviewer_summary(summary: dict[str, Any], run_folder: Path) -> str:
    """Build a reviewer-facing Markdown summary."""

    return f"""# OVERSEE reviewer demo summary

## Purpose

This demo package shows an executable OVERSEE flow using the migrated Digital
Factory, deterministic anchor, and live generative path.

The purpose is not to prove that the live generative path is universally better
than the deterministic anchor. The purpose is to expose comparable outputs,
fallback behavior, governance signals, and traceability across the same Digital
Factory cases.

## Execution mode

This reviewer package is generated in offline-safe mode by default. The script
removes `OPENAI_API_KEY` from the local process before execution. Therefore, the
live generative path is expected to activate safe fallback behavior rather than
performing an external model call.

## Summary metrics

| Metric | Value |
|---|---:|
| Cases evaluated | {summary["case_count"]} |
| Action differences | {summary["action_differences"]} |
| Priority differences | {summary["priority_differences"]} |
| Rationale differences | {summary["rationale_differences"]} |
| Live generative fallback count | {summary["live_generative_fallback_count"]} |
| Live generative model response count | {summary["live_generative_model_response_count"]} |
| Live generative evidence reference count | {summary["live_generative_evidence_reference_count"]} |
| Live generative priority governance count | {summary["live_generative_priority_governance_count"]} |

## Interpretation

In the offline-safe run, the live generative path does not call an external
model. It falls back to the governed internal path while preserving comparable
recommendation outputs and traceability signals.

The expected offline pattern is:

- deterministic anchor and live generative path preserve the same action when
  fallback is active;
- deterministic anchor and live generative path preserve the same priority when
  fallback is active;
- rationales differ because the live generative path records the fallback chain
  and governance-relevant execution context;
- model response identifiers are absent because external model execution is
  disabled.

## Generated artifacts

| File | Meaning |
|---|---|
| `01_digital_factory_scenarios.json` | Synthetic Digital Factory cases used as input. |
| `02_oversee_input_candidates.json` | OVERSEE input candidates derived from Digital Factory scenarios. |
| `03_deterministic_anchor_results.json` | Recommendations from the deterministic anchor. |
| `04_live_generative_path_results.json` | Recommendations from the live generative path. |
| `05_deterministic_generative_comparison.json` | Case-by-case comparison rows in JSON format. |
| `05_deterministic_generative_comparison.csv` | Case-by-case comparison rows in CSV format. |
| `06_comparison_summary.json` | Compact summary metrics. |
| `07_reviewer_summary.md` | Human-readable reviewer summary. |
| `08_traceability_index.json` | File-level traceability index with checksums. |
| `09_execution_manifest.json` | Execution manifest for the reviewer demo. |

## Output folder

```text
{run_folder}
```
"""


def build_traceability_index(run_folder: Path) -> dict[str, Any]:
    """Build a file-level traceability index for the reviewer package."""

    artifacts = []

    descriptions = {
        "01_digital_factory_scenarios.json": "Digital Factory scenarios used as executable input cases.",
        "02_oversee_input_candidates.json": "OVERSEE input candidates mapped from Digital Factory scenarios.",
        "03_deterministic_anchor_results.json": "Deterministic anchor recommendations.",
        "04_live_generative_path_results.json": "Live generative path recommendations.",
        "05_deterministic_generative_comparison.json": "Case-by-case deterministic-versus-generative comparison in JSON format.",
        "05_deterministic_generative_comparison.csv": "Case-by-case deterministic-versus-generative comparison in CSV format.",
        "06_comparison_summary.json": "Summary metrics for the comparison run.",
        "07_reviewer_summary.md": "Human-readable reviewer summary.",
        "08_traceability_index.json": "Traceability index for generated artifacts.",
        "09_execution_manifest.json": "Execution manifest for the reviewer demo.",
    }

    for artifact_name in EXPECTED_ARTIFACTS:
        path = run_folder / artifact_name

        artifact = {
            "artifact_name": artifact_name,
            "path": str(path),
            "exists": path.exists(),
            "size_bytes": path.stat().st_size if path.exists() else 0,
            "sha256": sha256_file(path) if path.exists() else None,
            "description": descriptions.get(artifact_name, ""),
        }

        artifacts.append(artifact)

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }


def build_execution_manifest(
    run_folder: Path,
    summary: dict[str, Any],
    force_offline: bool,
) -> dict[str, Any]:
    """Build an execution manifest for the reviewer package."""

    return {
        "artifact": "OVERSEE reviewer demo package",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "run_folder": str(run_folder),
        "force_offline": force_offline,
        "external_model_call_expected": not force_offline,
        "execution_note": (
            "Offline-safe mode removes OPENAI_API_KEY from the local process "
            "before execution, so live generative fallback behavior is expected."
            if force_offline
            else "External model execution may occur if runtime settings are configured."
        ),
        "summary": summary,
        "expected_artifacts": EXPECTED_ARTIFACTS,
    }


def run_oversee_reviewer_demo(
    outputs_root: str | Path = "outputs",
    force_offline: bool = True,
) -> dict[str, Any]:
    """
    Run the reviewer-facing OVERSEE demo package.

    Args:
        outputs_root: Folder where the timestamped output package is created.
        force_offline: If true, remove OPENAI_API_KEY from this process before
            executing the comparison.

    Returns:
        Dictionary with run folder, summary, manifest, traceability index, and
        output paths.
    """

    if force_offline:
        os.environ.pop("OPENAI_API_KEY", None)

    comparison_result = run_deterministic_generative_comparison(
        outputs_root=outputs_root
    )

    run_folder = Path(comparison_result["run_folder"])
    summary = comparison_result["summary"]

    reviewer_summary_path = run_folder / "07_reviewer_summary.md"
    traceability_index_path = run_folder / "08_traceability_index.json"
    execution_manifest_path = run_folder / "09_execution_manifest.json"

    reviewer_summary = build_reviewer_summary(
        summary=summary,
        run_folder=run_folder,
    )
    reviewer_summary_path.write_text(reviewer_summary, encoding="utf-8")

    execution_manifest = build_execution_manifest(
        run_folder=run_folder,
        summary=summary,
        force_offline=force_offline,
    )
    write_json(execution_manifest_path, execution_manifest)

    traceability_index = build_traceability_index(run_folder)
    write_json(traceability_index_path, traceability_index)

    # Rebuild traceability after writing itself so its own checksum is included
    # from the final persisted version.
    traceability_index = build_traceability_index(run_folder)
    write_json(traceability_index_path, traceability_index)

    return {
        "run_folder": run_folder,
        "summary": summary,
        "reviewer_summary_path": reviewer_summary_path,
        "traceability_index_path": traceability_index_path,
        "execution_manifest_path": execution_manifest_path,
        "traceability_index": traceability_index,
        "execution_manifest": execution_manifest,
        "paths": {
            "reviewer_summary": reviewer_summary_path,
            "traceability_index": traceability_index_path,
            "execution_manifest": execution_manifest_path,
        },
    }
