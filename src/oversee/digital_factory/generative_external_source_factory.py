"""Generative Digital Factory source generation for OVERSEE.

This module uses generative AI before OVERSEE Layer 1. Its responsibility is not
to recommend a decision, but to generate or enrich synthetic external source
payloads for a compressor case. The generated source package is then processed
by the normal five-layer OVERSEE pipeline.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from oversee.external_sources import (
    ExternalSourcePackage,
    ExternalSourcePayload,
    build_compressor_external_source_package,
)


REQUIRED_SOURCE_NAMES = [
    "asset_registry",
    "sensor_historian",
    "predictive_maintenance",
    "maintenance_history",
    "production_planning",
    "inventory_and_resources",
    "policy_governance",
]


@dataclass(slots=True)
class GenerativeDigitalFactoryResult:
    """Result of the Generative Digital Factory source generation path."""

    result_id: str
    case_id: str
    asset_id: str
    model_call_attempted: bool
    model_call_successful: bool
    fallback_used: bool
    fallback_reason: str | None
    model_name: str
    response_id: str | None
    prompt_hash: str
    prompt: str
    raw_response: str | None
    source_package: ExternalSourcePackage
    validation_errors: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    path_version: str = "0.1.0"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        data = asdict(self)
        data["source_package"] = self.source_package.to_dict()
        return data


def run_generative_digital_factory_source_generation(
    *,
    allow_live_call: bool = False,
) -> GenerativeDigitalFactoryResult:
    """Generate a Layer 1 external source package using live generative AI."""

    model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    prompt = _build_prompt()
    prompt_hash = _hash_text(prompt)

    if not allow_live_call:
        return _fallback_result(
            model_name=model_name,
            prompt=prompt,
            prompt_hash=prompt_hash,
            reason="live_call_not_allowed",
            attempted=False,
            raw_response=None,
            response_id=None,
            validation_errors=[],
        )

    if not os.getenv("OPENAI_API_KEY"):
        return _fallback_result(
            model_name=model_name,
            prompt=prompt,
            prompt_hash=prompt_hash,
            reason="missing_openai_api_key",
            attempted=False,
            raw_response=None,
            response_id=None,
            validation_errors=[],
        )

    try:
        from openai import OpenAI

        client = OpenAI()
        response = client.responses.create(
            model=model_name,
            input=prompt,
        )
        raw_response = _extract_response_text(response)
        response_id = getattr(response, "id", None)

        parsed = _parse_json_response(raw_response)
        source_package, validation_errors = _build_source_package_from_model_output(parsed)

        if validation_errors:
            return _fallback_result(
                model_name=model_name,
                prompt=prompt,
                prompt_hash=prompt_hash,
                reason="invalid_generative_factory_response",
                attempted=True,
                raw_response=raw_response,
                response_id=response_id,
                validation_errors=validation_errors,
            )

        return GenerativeDigitalFactoryResult(
            result_id=f"generative_digital_factory_{source_package.case_id}",
            case_id=source_package.case_id,
            asset_id=source_package.asset_id,
            model_call_attempted=True,
            model_call_successful=True,
            fallback_used=False,
            fallback_reason=None,
            model_name=model_name,
            response_id=response_id,
            prompt_hash=prompt_hash,
            prompt=prompt,
            raw_response=raw_response,
            source_package=source_package,
            validation_errors=[],
        )
    except Exception as exc:
        return _fallback_result(
            model_name=model_name,
            prompt=prompt,
            prompt_hash=prompt_hash,
            reason=f"api_error:{type(exc).__name__}",
            attempted=True,
            raw_response=str(exc),
            response_id=None,
            validation_errors=[],
        )


def _build_prompt() -> str:
    """Build the prompt for Generative Digital Factory source generation."""

    required_schema = {
        "case_id": "GEN_DF_COMP_001_LIVE",
        "asset_id": "COMP-001",
        "line_id": "PKG-LINE-01",
        "payloads": [
            {
                "source_name": "asset_registry",
                "source_system": "enterprise_asset_registry",
                "source_type": "master_data",
                "endpoint": "GET /assets/COMP-001",
                "raw_payload": {},
                "normalized_fields": {},
                "data_quality_flags": [],
            }
        ],
    }

    return (
        "You are the Generative Digital Factory for the OVERSEE workbench.\n"
        "Generate a realistic synthetic external source package for an industrial "
        "air compressor maintenance decision. This is data generation, not decision "
        "recommendation. Return ONLY valid JSON. Do not use Markdown.\n\n"
        "Mandatory facts that must not change:\n"
        "- case_id: GEN_DF_COMP_001_LIVE\n"
        "- asset_id: COMP-001\n"
        "- asset_type: industrial_air_compressor\n"
        "- line_id: PKG-LINE-01\n"
        "- criticality_score: 5\n"
        "- estimated_time_to_failure_hours: 48\n"
        "- confidence_score: 0.88\n"
        "- production_pressure: high\n"
        "- spare_part_available: true\n"
        "- specialist_technician_available_next_shift: true\n"
        "- human_review_required: true\n\n"
        "You must provide exactly these source_name values:\n"
        + json.dumps(REQUIRED_SOURCE_NAMES, ensure_ascii=False)
        + "\n\n"
        "Each payload must contain source_name, source_system, source_type, endpoint, "
        "raw_payload, normalized_fields and data_quality_flags.\n\n"
        "Required top-level JSON shape example:\n"
        + json.dumps(required_schema, indent=2, ensure_ascii=False)
    )


def _build_source_package_from_model_output(
    parsed: dict[str, Any],
) -> tuple[ExternalSourcePackage, list[str]]:
    """Convert parsed model output into an ExternalSourcePackage."""

    errors: list[str] = []

    case_id = str(parsed.get("case_id", "GEN_DF_COMP_001_LIVE")).strip()
    asset_id = str(parsed.get("asset_id", "COMP-001")).strip()
    line_id = str(parsed.get("line_id", "PKG-LINE-01")).strip()
    raw_payloads = parsed.get("payloads")

    if case_id != "GEN_DF_COMP_001_LIVE":
        errors.append("case_id_mismatch")
    if asset_id != "COMP-001":
        errors.append("asset_id_mismatch")
    if line_id != "PKG-LINE-01":
        errors.append("line_id_mismatch")
    if not isinstance(raw_payloads, list):
        errors.append("payloads_must_be_list")
        raw_payloads = []

    payloads: list[ExternalSourcePayload] = []
    seen_names: set[str] = set()
    generated_at = datetime.now(timezone.utc).isoformat()

    for item in raw_payloads:
        if not isinstance(item, dict):
            errors.append("payload_item_must_be_object")
            continue

        source_name = str(item.get("source_name", "")).strip()
        seen_names.add(source_name)

        payloads.append(
            ExternalSourcePayload(
                source_name=source_name,
                source_system=str(item.get("source_system", "generative_source_system")),
                source_type=str(item.get("source_type", "synthetic_source")),
                endpoint=str(item.get("endpoint", f"GET /synthetic-sources/{source_name}")),
                generated_at=generated_at,
                case_id=case_id,
                asset_id=asset_id,
                line_id=line_id,
                raw_payload=_dict_or_empty(item.get("raw_payload")),
                normalized_fields=_dict_or_empty(item.get("normalized_fields")),
                data_quality_flags=_list_of_text(item.get("data_quality_flags")),
            )
        )

    missing = set(REQUIRED_SOURCE_NAMES) - seen_names
    extra = seen_names - set(REQUIRED_SOURCE_NAMES)

    for source_name in sorted(missing):
        errors.append(f"missing_source:{source_name}")
    for source_name in sorted(extra):
        errors.append(f"unexpected_source:{source_name}")

    if not errors:
        errors.extend(_validate_required_normalized_fields(payloads))

    package = ExternalSourcePackage(
        package_id=f"generative_external_sources_{case_id}",
        case_id=case_id,
        asset_id=asset_id,
        line_id=line_id,
        created_at=generated_at,
        payloads=payloads,
        package_version="0.1.0",
    )

    return package, errors



def _validate_required_normalized_fields(payloads: list[ExternalSourcePayload]) -> list[str]:
    """Validate and complete fields required by the Layer 2 canonical context builder."""

    errors: list[str] = []
    by_source = {payload.source_name: payload for payload in payloads}

    def as_number(value: Any, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    def as_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"true", "yes", "1", "y"}
        return bool(value)

    def numeric_trend(values: Any) -> str:
        if not isinstance(values, list) or len(values) < 2:
            return "unknown"
        try:
            first = float(values[0])
            last = float(values[-1])
        except (TypeError, ValueError):
            return "unknown"
        if last > first:
            return "increasing"
        if last < first:
            return "decreasing"
        return "stable"

    asset_registry = by_source.get("asset_registry")
    if asset_registry is not None:
        fields = asset_registry.normalized_fields
        raw = asset_registry.raw_payload
        criticality_score = as_number(fields.get("criticality_score", raw.get("criticalityScore", 5)), 5)
        fields.setdefault("asset_type", raw.get("type", "industrial_air_compressor"))
        fields.setdefault("criticality_score", int(criticality_score))
        fields.setdefault("asset_criticality", "high" if criticality_score >= 5 else "medium")

    sensor_historian = by_source.get("sensor_historian")
    if sensor_historian is not None:
        fields = sensor_historian.normalized_fields
        raw = sensor_historian.raw_payload
        vibration_values = fields.get("vibration_mms", raw.get("vibration_mms", []))
        temperature_values = fields.get("temperature_celsius", raw.get("temperature_celsius", []))
        status_alert_count = as_number(fields.get("status_alert_count", 0), 0)
        fields.setdefault("vibration_trend", numeric_trend(vibration_values))
        fields.setdefault("temperature_trend", numeric_trend(temperature_values))
        fields.setdefault("sensor_severity", "high" if status_alert_count >= 1 else "medium")

    predictive = by_source.get("predictive_maintenance")
    if predictive is not None:
        fields = predictive.normalized_fields
        raw = predictive.raw_payload
        estimated_hours = as_number(
            fields.get("estimated_time_to_failure_hours", raw.get("estimatedTimeToFailureHours", 48)),
            48,
        )
        confidence = as_number(fields.get("confidence_score", raw.get("confidenceScore", 0.88)), 0.88)
        fields.setdefault("alert_type", "predictive_degradation_alert")
        fields.setdefault("estimated_time_to_failure_hours", estimated_hours)
        fields.setdefault("confidence_score", confidence)
        fields.setdefault("alert_severity", "high" if estimated_hours <= 72 and confidence >= 0.75 else "medium")

    maintenance = by_source.get("maintenance_history")
    if maintenance is not None:
        fields = maintenance.normalized_fields
        total_events = as_number(fields.get("total_maintenance_events", 0), 0)
        last_type = str(fields.get("last_maintenance_type", "")).strip().lower()
        fields.setdefault("recent_repeated_failures", bool(total_events >= 2 or last_type == "corrective"))

    production = by_source.get("production_planning")
    if production is not None:
        fields = production.normalized_fields
        raw = production.raw_payload
        production_pressure = str(fields.get("production_pressure", raw.get("productionPressure", "high"))).strip().lower()
        scheduled_downtime = as_number(
            fields.get("scheduled_downtime_hours", raw.get("scheduledDowntimeHours", 36)),
            36,
        )
        fields.setdefault("production_pressure", production_pressure)
        fields.setdefault("production_load_pct", 92.0 if production_pressure == "high" else 75.0)
        fields.setdefault("next_planned_downtime_hours", scheduled_downtime)

    inventory = by_source.get("inventory_and_resources")
    if inventory is not None:
        fields = inventory.normalized_fields
        raw = inventory.raw_payload
        spare_part_available = as_bool(fields.get("spare_part_available", raw.get("sparePartAvailable", True)))
        technician_available = as_bool(
            fields.get(
                "specialist_technician_available_next_shift",
                raw.get("specialistTechnicianAvailableNextShift", True),
            )
        )
        fields.setdefault("spare_part_available", spare_part_available)
        fields.setdefault("specialist_technician_available_next_shift", technician_available)
        fields.setdefault("intervention_feasible", spare_part_available and technician_available)

    policy = by_source.get("policy_governance")
    if policy is not None:
        fields = policy.normalized_fields
        raw = policy.raw_payload
        human_review = as_bool(fields.get("human_review_required", raw.get("humanReviewRequired", raw.get("mandatoryReview", True))))
        fields.setdefault("mandatory_human_review_for_high_criticality", True)
        fields.setdefault("expected_human_review_required", human_review)

    required_fields = {
        "asset_registry": ["asset_type", "asset_criticality", "criticality_score"],
        "sensor_historian": ["vibration_trend", "temperature_trend", "sensor_severity"],
        "predictive_maintenance": [
            "alert_type",
            "estimated_time_to_failure_hours",
            "confidence_score",
            "alert_severity",
        ],
        "maintenance_history": ["recent_repeated_failures"],
        "production_planning": [
            "production_load_pct",
            "next_planned_downtime_hours",
            "production_pressure",
        ],
        "inventory_and_resources": [
            "spare_part_available",
            "specialist_technician_available_next_shift",
            "intervention_feasible",
        ],
        "policy_governance": [
            "mandatory_human_review_for_high_criticality",
            "expected_human_review_required",
        ],
    }

    for source_name, fields in required_fields.items():
        payload = by_source.get(source_name)
        if payload is None:
            continue
        for field_name in fields:
            if field_name not in payload.normalized_fields:
                errors.append(f"missing_normalized_field:{source_name}.{field_name}")

    return errors


def _fallback_result(
    *,
    model_name: str,
    prompt: str,
    prompt_hash: str,
    reason: str,
    attempted: bool,
    raw_response: str | None,
    response_id: str | None,
    validation_errors: list[str],
) -> GenerativeDigitalFactoryResult:
    """Build fallback output using deterministic Digital Factory source package."""

    source_package = build_compressor_external_source_package()

    return GenerativeDigitalFactoryResult(
        result_id=f"generative_digital_factory_{source_package.case_id}",
        case_id=source_package.case_id,
        asset_id=source_package.asset_id,
        model_call_attempted=attempted,
        model_call_successful=False,
        fallback_used=True,
        fallback_reason=reason,
        model_name=model_name,
        response_id=response_id,
        prompt_hash=prompt_hash,
        prompt=prompt,
        raw_response=raw_response,
        source_package=source_package,
        validation_errors=validation_errors,
    )


def _extract_response_text(response: Any) -> str:
    """Extract text from an OpenAI Responses API response object."""

    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    if hasattr(response, "model_dump_json"):
        return response.model_dump_json()

    return str(response)


def _parse_json_response(raw_response: str) -> dict[str, Any]:
    """Parse a JSON object from model text."""

    cleaned = raw_response.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        parsed = json.loads(cleaned[start : end + 1])

    if not isinstance(parsed, dict):
        raise ValueError("Generative Digital Factory response was not a JSON object.")

    return parsed


def _dict_or_empty(value: Any) -> dict[str, Any]:
    """Return a dictionary, preserving list payloads inside a records wrapper."""

    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return {"records": value}
    return {}


def _list_of_text(value: Any) -> list[str]:
    """Return a list of text values."""

    if not isinstance(value, list):
        return []

    return [str(item) for item in value]


def _hash_text(text: str) -> str:
    """Return a stable SHA-256 hash."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
