"""
Run an offline smoke test for the OVERSEE live generative path.

This script intentionally removes OPENAI_API_KEY from the local process
environment. The goal is to validate that the live generative path preserves
safe fallback behavior when external model execution is unavailable.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.domain import Asset, DecisionCase, PredictiveAlert, Recommendation  # noqa: E402
from oversee.live_generative_path import run_live_generative_path  # noqa: E402


def to_jsonable(value: Any) -> Any:
    """Convert dataclass-based outputs to JSON-serializable objects."""

    if is_dataclass(value):
        return asdict(value)

    if hasattr(value, "__dict__"):
        return value.__dict__

    return value


def build_smoke_decision_case() -> DecisionCase:
    """Build a minimal compressor decision case for offline fallback validation."""

    asset = Asset(
        asset_id="COMP-001",
        asset_type="compressor",
        criticality=5,
        location="Packaging line utilities area",
    )

    alert = PredictiveAlert(
        alert_id="ALERT-COMP-001-LIVE-GEN-OFFLINE",
        asset_id="COMP-001",
        predicted_issue="bearing wear progression",
        time_to_failure_hours=24.0,
        confidence_score=0.86,
    )

    return DecisionCase(
        case_id="CASE-COMP-001-LIVE-GEN-OFFLINE",
        asset=asset,
        alert=alert,
        context_note=(
            "High production dependency. Spare part available. Technician available. "
            "Planned intervention window possible within the next shift."
        ),
    )


def main() -> None:
    """Execute the offline live generative path smoke run."""

    os.environ.pop("OPENAI_API_KEY", None)

    decision_case = build_smoke_decision_case()
    recommendation = run_live_generative_path(decision_case)

    if not isinstance(recommendation, Recommendation):
        raise TypeError("run_live_generative_path did not return a Recommendation.")

    print("OVERSEE live generative path offline smoke run completed.")
    print()
    print(json.dumps(to_jsonable(recommendation), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
