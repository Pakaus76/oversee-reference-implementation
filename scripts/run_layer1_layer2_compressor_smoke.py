"""Run Layer 1 and Layer 2 smoke test for the compressor case.

The script persists:
- 01_external_source_payloads.json
- 02_canonical_case_context.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.case_context import build_canonical_case_context  # noqa: E402
from oversee.external_sources import build_compressor_external_source_package  # noqa: E402


def main() -> None:
    """Run the Layer 1 and Layer 2 compressor smoke test."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"five_layer_layer1_layer2_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    source_package = build_compressor_external_source_package()
    canonical_context = build_canonical_case_context(source_package)

    external_sources_path = output_dir / "01_external_source_payloads.json"
    canonical_context_path = output_dir / "02_canonical_case_context.json"

    external_sources_path.write_text(
        json.dumps(source_package.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    canonical_context_path.write_text(
        json.dumps(canonical_context.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OVERSEE Layer 1 and Layer 2 compressor smoke completed.")
    print()
    print(json.dumps(
        {
            "case_id": canonical_context.case_id,
            "asset_id": canonical_context.asset.asset_id,
            "source_payload_count": canonical_context.source_payload_count,
            "source_names": canonical_context.source_names,
            "criticality_score": canonical_context.asset.criticality_score,
            "estimated_time_to_failure_hours": canonical_context.predictive_evidence.estimated_time_to_failure_hours,
            "confidence_score": canonical_context.predictive_evidence.confidence_score,
            "computed_human_review_required": canonical_context.governance_policy.computed_human_review_required,
            "key_risk_drivers": canonical_context.key_risk_drivers,
            "output_dir": str(output_dir),
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
