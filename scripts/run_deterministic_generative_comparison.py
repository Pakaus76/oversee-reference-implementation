"""
Run the OVERSEE deterministic-versus-generative comparison.

This script creates reviewer-facing JSON and CSV outputs comparing the
deterministic anchor and live generative path over the same Digital Factory
scenarios.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.comparison.deterministic_generative_comparison import (  # noqa: E402
    run_deterministic_generative_comparison,
)


def main() -> None:
    """Run the comparison and print a compact summary."""

    # This run is intentionally safe offline unless the caller provides a model key.
    os.environ.pop("OPENAI_API_KEY", None)

    result = run_deterministic_generative_comparison(
        outputs_root=PROJECT_ROOT / "outputs"
    )

    print("OVERSEE deterministic-versus-generative comparison completed.")
    print()
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
    print()
    print("Outputs saved to:")
    print(result["run_folder"])


if __name__ == "__main__":
    main()
