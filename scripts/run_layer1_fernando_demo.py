"""Run Fernando-aligned OVERSEE Layer 1 demo."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from oversee.integration import (  # noqa: E402
    build_sample_predictive_alert_request,
    run_layer1_evidence_pipeline,
)


def main() -> None:
    """Run Layer 1 demo and persist inspectable outputs."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "outputs" / f"fernando_layer1_demo_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    alert_request = build_sample_predictive_alert_request()
    layer1_result = run_layer1_evidence_pipeline(alert_request)

    paths = {
        "predictive_alert_request": output_dir / "00_predictive_alert_request.json",
        "received_predictive_alert": output_dir / "01_received_predictive_alert.json",
        "enterprise_api_calls": output_dir / "01_enterprise_api_calls.json",
        "aggregated_evidence_package": output_dir / "01_aggregated_evidence_package.json",
        "validation_report": output_dir / "01_validation_report.json",
    }

    paths["predictive_alert_request"].write_text(
        json.dumps(alert_request, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["received_predictive_alert"].write_text(
        json.dumps(layer1_result.received_alert.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["enterprise_api_calls"].write_text(
        json.dumps(layer1_result.enterprise_api_calls, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["aggregated_evidence_package"].write_text(
        json.dumps(layer1_result.evidence_package.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["validation_report"].write_text(
        json.dumps(layer1_result.validation_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Fernando Layer 1 demo completed.")
    print()
    print(
        json.dumps(
            {
                "predictive_alert_received": layer1_result.received_alert.accepted,
                "api_endpoint": layer1_result.received_alert.endpoint,
                "raw_sensor_context_received": "raw_sensor_context" in alert_request,
                "enterprise_api_call_count": len(layer1_result.enterprise_api_calls),
                "maintenance_history_api_called": _api_called(
                    layer1_result.enterprise_api_calls,
                    "cmms_maintenance_history_api",
                ),
                "operational_context_api_called": _api_called(
                    layer1_result.enterprise_api_calls,
                    "mes_operational_context_api",
                ),
                "asset_metadata_api_called": _api_called(
                    layer1_result.enterprise_api_calls,
                    "asset_registry_api",
                ),
                "inventory_and_resources_api_called": _api_called(
                    layer1_result.enterprise_api_calls,
                    "inventory_and_resources_api",
                ),
                "policy_governance_api_called": _api_called(
                    layer1_result.enterprise_api_calls,
                    "policy_governance_api",
                ),
                "evidence_package_valid": layer1_result.validation_report["valid"],
                "evidence_payload_count": layer1_result.validation_report["payload_count"],
                "output_dir": str(output_dir),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def _api_called(api_calls: list[dict[str, object]], api_name: str) -> bool:
    """Return whether a simulated API was called."""

    return any(call.get("api_name") == api_name for call in api_calls)


if __name__ == "__main__":
    main()
