"""
Run the OVERSEE Digital Factory through the deterministic anchor.

This script validates the migrated path:

Digital Factory scenarios
→ bridge-ready payloads
→ OVERSEE input candidates
→ deterministic anchor recommendations
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.digital_factory import (  # noqa: E402
    build_bridge_ready_payloads,
    evaluate_deterministic_anchor_candidates,
    generate_compressor_scenarios,
    map_bridge_ready_payloads_to_oversee_inputs,
)


def to_dict(value: Any) -> Any:
    """Convert dataclass-based objects to dictionaries recursively."""

    if is_dataclass(value):
        return asdict(value)

    if isinstance(value, list):
        return [to_dict(item) for item in value]

    if isinstance(value, dict):
        return {key: to_dict(item) for key, item in value.items()}

    return value


def main() -> None:
    """Run the Digital Factory deterministic anchor smoke test."""

    scenarios = generate_compressor_scenarios()
    scenario_dicts = [scenario.to_dict() for scenario in scenarios]

    bridge_payloads = build_bridge_ready_payloads(scenario_dicts)
    bridge_payload_dicts = [payload.to_dict() for payload in bridge_payloads]

    oversee_inputs = map_bridge_ready_payloads_to_oversee_inputs(bridge_payload_dicts)
    oversee_input_dicts = [candidate.to_dict() for candidate in oversee_inputs]

    recommendations = evaluate_deterministic_anchor_candidates(oversee_input_dicts)
    recommendation_dicts = [to_dict(recommendation) for recommendation in recommendations]

    print("OVERSEE Digital Factory deterministic anchor smoke run completed.")
    print()
    print(json.dumps(
        {
            "scenario_count": len(scenarios),
            "bridge_payload_count": len(bridge_payloads),
            "oversee_input_count": len(oversee_inputs),
            "recommendation_count": len(recommendations),
            "recommendations": recommendation_dicts,
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
