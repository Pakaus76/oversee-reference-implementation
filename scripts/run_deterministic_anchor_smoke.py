"""
Run a smoke test for the OVERSEE deterministic anchor.

This script builds a minimal structured decision case, executes the deterministic
anchor, and prints the resulting recommendation. It is intended as an early
migration validation script.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.deterministic_anchor import run_deterministic_anchor  # noqa: E402
from oversee.domain import Asset, DecisionCase, PredictiveAlert  # noqa: E402


def to_jsonable(value: object) -> object:
    """Convert dataclass-based outputs to JSON-serializable objects."""

    if is_dataclass(value):
        return asdict(value)

    if hasattr(value, "__dict__"):
        return value.__dict__

    return value


def build_smoke_decision_case() -> DecisionCase:
    """Build a minimal high-criticality compressor decision case."""

    asset = Asset(
        asset_id="COMP-001",
        asset_type="compressor",
        criticality=5,
        location="Packaging line utilities area",
    )

    alert = PredictiveAlert(
        alert_id="ALERT-COMP-001-SMOKE",
        asset_id="COMP-001",
        predicted_issue="bearing wear progression",
        time_to_failure_hours=24.0,
        confidence_score=0.86,
    )

    return DecisionCase(
        case_id="CASE-COMP-001-SMOKE",
        asset=asset,
        alert=alert,
        context_note=(
            "High production dependency. Spare part available. Technician available. "
            "Planned intervention window possible within the next shift."
        ),
    )


def main() -> None:
    """Execute the deterministic anchor smoke run."""

    decision_case = build_smoke_decision_case()
    recommendation = run_deterministic_anchor(decision_case)

    print("OVERSEE deterministic anchor smoke run completed.")
    print()
    print(json.dumps(to_jsonable(recommendation), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
