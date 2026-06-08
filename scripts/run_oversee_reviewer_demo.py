"""
Run the OVERSEE reviewer-facing demo package.

This command generates a complete reviewer-facing output folder with comparison
outputs, Markdown summary, traceability index, and execution manifest.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.reporting.reviewer_package import run_oversee_reviewer_demo  # noqa: E402


def main() -> None:
    """Run the reviewer-facing OVERSEE demo."""

    result = run_oversee_reviewer_demo(
        outputs_root=PROJECT_ROOT / "outputs",
        force_offline=True,
    )

    print("OVERSEE reviewer-facing demo package completed.")
    print()
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
    print()
    print("Reviewer summary:")
    print(result["reviewer_summary_path"])
    print()
    print("Traceability index:")
    print(result["traceability_index_path"])
    print()
    print("Execution manifest:")
    print(result["execution_manifest_path"])
    print()
    print("Outputs saved to:")
    print(result["run_folder"])


if __name__ == "__main__":
    main()
