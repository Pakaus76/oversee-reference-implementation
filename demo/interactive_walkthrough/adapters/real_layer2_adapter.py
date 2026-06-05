"""Real Layer 2 adapter for the interactive walkthrough.

The adapter calls the existing Fernando-aligned Layer 2 script as a subprocess.
It does not reimplement Layer 2 and does not modify the OVERSEE core.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from demo.interactive_walkthrough.demo_state import DemoRunState
from demo.interactive_walkthrough.output_manager import write_json, write_text


def run_real_layer2(state: DemoRunState) -> dict[str, Any]:
    """Run the existing Layer 2 script and capture its generated artifacts."""
    repo_root = Path.cwd()
    script_path = repo_root / "scripts" / "run_layer2_fernando_demo.py"
    outputs_dir = repo_root / "outputs"

    if not script_path.exists():
        raise FileNotFoundError(f"Layer 2 script not found: {script_path}")

    before_dirs = _find_layer2_output_dirs(outputs_dir)

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    pythonpath_parts = ["src"]
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    completed = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    stdout_path = state.output_dir / "02_layer2_script_stdout.txt"
    stderr_path = state.output_dir / "02_layer2_script_stderr.txt"
    write_text(stdout_path, completed.stdout)
    write_text(stderr_path, completed.stderr)

    state.record_artifact("layer2_script_stdout", stdout_path)
    state.record_artifact("layer2_script_stderr", stderr_path)

    if completed.returncode != 0:
        failure_manifest = {
            "scenario_id": state.scenario.scenario_id,
            "layer_id": "layer2",
            "mode": "real_oversee_layer2_script",
            "script": str(script_path),
            "returncode": completed.returncode,
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
        }
        failure_path = state.output_dir / "02_layer2_real_execution_failure.json"
        write_json(failure_path, failure_manifest)
        state.record_artifact("layer2_real_execution_failure", failure_path)
        raise RuntimeError(
            "Layer 2 real script failed. Inspect stdout and stderr artifacts."
        )

    after_dirs = _find_layer2_output_dirs(outputs_dir)
    new_dirs = [path for path in after_dirs if path not in before_dirs]

    if new_dirs:
        source_output_dir = max(new_dirs, key=lambda item: item.stat().st_mtime)
    elif after_dirs:
        source_output_dir = max(after_dirs, key=lambda item: item.stat().st_mtime)
    else:
        raise RuntimeError("Layer 2 script completed but no output directory was found.")

    copied_files = _copy_layer2_artifacts(source_output_dir, state.output_dir)

    output_summary = state.scenario.expected_layer_outputs["layer2"]
    state.record_layer_output("layer2", output_summary)

    manifest = {
        "scenario_id": state.scenario.scenario_id,
        "layer_id": "layer2",
        "mode": "real_oversee_layer2_script",
        "script": str(script_path),
        "source_output_dir": str(source_output_dir),
        "copied_files": [str(path) for path in copied_files],
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "expected_output_summary": output_summary,
        "returncode": completed.returncode,
    }

    manifest_path = state.output_dir / "02_layer2_real_execution_manifest.json"
    write_json(manifest_path, manifest)
    state.record_artifact("layer2_real_execution_manifest", manifest_path)

    for copied_file in copied_files:
        state.record_artifact(copied_file.stem, copied_file)

    return manifest


def _find_layer2_output_dirs(outputs_dir: Path) -> set[Path]:
    """Return known Layer 2 Fernando output directories."""
    if not outputs_dir.exists():
        return set()

    return {
        path.resolve()
        for path in outputs_dir.glob("fernando_layer2_demo_*")
        if path.is_dir()
    }


def _copy_layer2_artifacts(source_output_dir: Path, target_output_dir: Path) -> list[Path]:
    """Copy useful Layer 2 artifacts into the interactive demo output folder.

    The Layer 2 script may also generate Layer 1 artifacts because the full path
    up to Layer 2 is executed. For the interactive walkthrough, this adapter only
    copies the artifacts that make Layer 2 visible.
    """
    copied_files: list[Path] = []

    prefixes_to_copy = (
        "02_",
    )

    for source_file in sorted(source_output_dir.iterdir()):
        if not source_file.is_file():
            continue

        if source_file.suffix.lower() not in {".json", ".md", ".txt"}:
            continue

        if not source_file.name.startswith(prefixes_to_copy):
            continue

        target_file = target_output_dir / f"02_layer2_real_{source_file.name}"
        shutil.copy2(source_file, target_file)
        copied_files.append(target_file)

    return copied_files

