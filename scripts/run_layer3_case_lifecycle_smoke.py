"""Run Layer 1, Layer 2 and Layer 3 smoke test for the compressor case.

The script persists:
- 01_external_source_payloads.json
- 02_canonical_case_context.json
- 03_case_lifecycle_trace.json
- 03_output_layer3_case_management_state.json
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.case_context import build_canonical_case_context  # noqa: E402
from oversee.case_management import build_case_management_state  # noqa: E402
from oversee.external_sources import build_compressor_external_source_package  # noqa: E402


def main() -> None:
    """Run the Layer 3 compressor case lifecycle smoke test."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"five_layer_layer3_case_lifecycle_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)
    case_state = build_case_management_state(canonical_context)

    paths = {
        "external_sources": output_dir / "01_external_source_payloads.json",
        "canonical_context": output_dir / "02_canonical_case_context.json",
        "case_lifecycle_trace": output_dir / "03_case_lifecycle_trace.json",
        "case_management_state": output_dir / "03_output_layer3_case_management_state.json",
    }

    paths["external_sources"].write_text(
        json.dumps(source_package.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["canonical_context"].write_text(
        json.dumps(canonical_context.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["case_lifecycle_trace"].write_text(
        json.dumps(case_state.lifecycle_trace(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["case_management_state"].write_text(
        json.dumps(case_state.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OVERSEE Layer 3 compressor case lifecycle smoke completed.")
    print()
    print(json.dumps(
        {
            "case_id": case_state.case_id,
            "asset_id": case_state.asset_id,
            "case_status": case_state.case_status,
            "lifecycle_stage": case_state.lifecycle_stage,
            "human_review_required": case_state.human_review_required,
            "maintenance_planning_required": case_state.maintenance_planning_required,
            "decision_ready": case_state.decision_ready,
            "event_count": case_state.event_count,
            "task_count": case_state.task_count,
            "milestone_count": case_state.milestone_count,
            "blockers": case_state.blockers,
            "output_dir": str(output_dir),
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
