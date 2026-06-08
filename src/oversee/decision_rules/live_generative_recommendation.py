"""Live generative recommendation path for OVERSEE Layer 4.

This module performs the first real generative AI integration inside OVERSEE.
The model receives the already-governed case context from Layers 1 to 4 and
returns a structured recommendation. The output is validated before it can be
included in the governed Layer 5 package.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from oversee.case_context import CanonicalCaseContext
from oversee.case_management import CaseManagementState
from oversee.decision_rules import DecisionRuleEvaluation


@dataclass(slots=True)
class LiveGenerativeRecommendationResult:
    """Result of the live generative recommendation path."""

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
    protected_facts: dict[str, Any]
    prompt: str
    raw_response: str | None
    parsed_recommendation: dict[str, Any]
    validation_errors: list[str] = field(default_factory=list)
    protected_fact_violations: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    path_version: str = "0.1.0"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


def run_live_generative_recommendation(
    *,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
    allow_live_call: bool = False,
) -> LiveGenerativeRecommendationResult:
    """Run the live generative recommendation path with fallback protection."""

    model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    protected_facts = _build_protected_facts(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
    )
    prompt = _build_prompt(
        canonical_context=canonical_context,
        case_state=case_state,
        rule_evaluation=rule_evaluation,
        protected_facts=protected_facts,
    )
    prompt_hash = _hash_text(prompt)

    if not allow_live_call:
        return _fallback_result(
            canonical_context=canonical_context,
            model_name=model_name,
            prompt_hash=prompt_hash,
            protected_facts=protected_facts,
            prompt=prompt,
            reason="live_call_not_allowed",
            attempted=False,
            raw_response=None,
            response_id=None,
        )

    if not os.getenv("OPENAI_API_KEY"):
        return _fallback_result(
            canonical_context=canonical_context,
            model_name=model_name,
            prompt_hash=prompt_hash,
            protected_facts=protected_facts,
            prompt=prompt,
            reason="missing_openai_api_key",
            attempted=False,
            raw_response=None,
            response_id=None,
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
        validation_errors, protected_fact_violations = _validate_recommendation(
            parsed=parsed,
            protected_facts=protected_facts,
        )

        if validation_errors or protected_fact_violations:
            fallback = _fallback_result(
                canonical_context=canonical_context,
                model_name=model_name,
                prompt_hash=prompt_hash,
                protected_facts=protected_facts,
                prompt=prompt,
                reason="invalid_model_response",
                attempted=True,
                raw_response=raw_response,
                response_id=response_id,
            )
            fallback.validation_errors.extend(validation_errors)
            fallback.protected_fact_violations.extend(protected_fact_violations)
            return fallback

        return LiveGenerativeRecommendationResult(
            result_id=f"live_generative_{canonical_context.case_id}",
            case_id=canonical_context.case_id,
            asset_id=canonical_context.asset.asset_id,
            model_call_attempted=True,
            model_call_successful=True,
            fallback_used=False,
            fallback_reason=None,
            model_name=model_name,
            response_id=response_id,
            prompt_hash=prompt_hash,
            protected_facts=protected_facts,
            prompt=prompt,
            raw_response=raw_response,
            parsed_recommendation=parsed,
            validation_errors=[],
            protected_fact_violations=[],
        )
    except Exception as exc:
        return _fallback_result(
            canonical_context=canonical_context,
            model_name=model_name,
            prompt_hash=prompt_hash,
            protected_facts=protected_facts,
            prompt=prompt,
            reason=f"api_error:{type(exc).__name__}",
            attempted=True,
            raw_response=str(exc),
            response_id=None,
        )


def _build_prompt(
    *,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
    protected_facts: dict[str, Any],
) -> str:
    """Build the prompt for the live generative recommendation path."""

    case_payload = {
        "protected_facts": protected_facts,
        "canonical_context": canonical_context.to_dict(),
        "case_management_state": case_state.to_dict(),
        "dmn_like_rule_evaluation": rule_evaluation.to_dict(),
    }

    return (
        "You are the live generative recommendation path inside OVERSEE.\n"
        "You must produce one governed industrial maintenance recommendation.\n"
        "Use only the supplied data. Do not invent or alter protected facts.\n"
        "Return ONLY valid JSON. Do not use Markdown.\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "recommended_action": "string",\n'
        '  "priority": "low|medium|high|critical",\n'
        '  "recommended_execution_mode": "string",\n'
        '  "human_review_required": true,\n'
        '  "rationale": "string",\n'
        '  "risks": ["string"],\n'
        '  "constraints": ["string"],\n'
        '  "evidence_used": ["string"]\n'
        "}\n\n"
        "Case payload:\n"
        + json.dumps(case_payload, indent=2, ensure_ascii=False)
    )


def _build_protected_facts(
    *,
    canonical_context: CanonicalCaseContext,
    case_state: CaseManagementState,
    rule_evaluation: DecisionRuleEvaluation,
) -> dict[str, Any]:
    """Build facts that the model must not change."""

    return {
        "case_id": canonical_context.case_id,
        "asset_id": canonical_context.asset.asset_id,
        "asset_type": canonical_context.asset.asset_type,
        "criticality_score": canonical_context.asset.criticality_score,
        "estimated_time_to_failure_hours": (
            canonical_context.predictive_evidence.estimated_time_to_failure_hours
        ),
        "confidence_score": canonical_context.predictive_evidence.confidence_score,
        "production_pressure": canonical_context.operational_context.production_pressure,
        "intervention_feasible": rule_evaluation.intervention_feasible,
        "human_review_required": rule_evaluation.human_review_required,
        "decision_ready": case_state.decision_ready,
        "dmn_like_final_priority": rule_evaluation.final_priority,
        "recommended_execution_mode": rule_evaluation.recommended_execution_mode,
    }


def _validate_recommendation(
    *,
    parsed: dict[str, Any],
    protected_facts: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Validate parsed model output against required fields and protected facts."""

    validation_errors: list[str] = []
    protected_fact_violations: list[str] = []

    required_fields = [
        "recommended_action",
        "priority",
        "recommended_execution_mode",
        "human_review_required",
        "rationale",
        "risks",
        "constraints",
        "evidence_used",
    ]

    for field_name in required_fields:
        if field_name not in parsed:
            validation_errors.append(f"missing_required_field:{field_name}")

    priority = str(parsed.get("priority", "")).lower()
    if priority not in {"low", "medium", "high", "critical"}:
        validation_errors.append("invalid_priority")

    if "human_review_required" in parsed:
        parsed_review = bool(parsed["human_review_required"])
        expected_review = bool(protected_facts["human_review_required"])
        if parsed_review != expected_review:
            protected_fact_violations.append(
                "human_review_required_mismatch"
            )

    if "priority" in parsed:
        expected_priority = str(protected_facts["dmn_like_final_priority"]).lower()
        if priority not in {expected_priority, "critical"}:
            validation_errors.append(
                f"priority_not_aligned_with_governance:{priority}!={expected_priority}"
            )

    for list_field in ["risks", "constraints", "evidence_used"]:
        if list_field in parsed and not isinstance(parsed[list_field], list):
            validation_errors.append(f"field_must_be_list:{list_field}")

    return validation_errors, protected_fact_violations


def _fallback_result(
    *,
    canonical_context: CanonicalCaseContext,
    model_name: str,
    prompt_hash: str,
    protected_facts: dict[str, Any],
    prompt: str,
    reason: str,
    attempted: bool,
    raw_response: str | None,
    response_id: str | None,
) -> LiveGenerativeRecommendationResult:
    """Build a governed fallback result."""

    fallback_recommendation = {
        "recommended_action": "Use deterministic governed recommendation path.",
        "priority": protected_facts["dmn_like_final_priority"],
        "recommended_execution_mode": protected_facts["recommended_execution_mode"],
        "human_review_required": protected_facts["human_review_required"],
        "rationale": (
            "Live generative path could not produce a validated recommendation. "
            "The governed deterministic path remains the safe fallback."
        ),
        "risks": ["live_generative_path_unavailable_or_invalid"],
        "constraints": ["fallback_to_deterministic_path"],
        "evidence_used": ["canonical_context", "case_lifecycle", "dmn_like_rules"],
    }

    return LiveGenerativeRecommendationResult(
        result_id=f"live_generative_{canonical_context.case_id}",
        case_id=canonical_context.case_id,
        asset_id=canonical_context.asset.asset_id,
        model_call_attempted=attempted,
        model_call_successful=False,
        fallback_used=True,
        fallback_reason=reason,
        model_name=model_name,
        response_id=response_id,
        prompt_hash=prompt_hash,
        protected_facts=protected_facts,
        prompt=prompt,
        raw_response=raw_response,
        parsed_recommendation=fallback_recommendation,
        validation_errors=[],
        protected_fact_violations=[],
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
    """Parse a JSON object from a model response."""

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
        raise ValueError("Model response did not parse to a JSON object.")

    return parsed


def _hash_text(text: str) -> str:
    """Return a stable SHA-256 hash for traceability."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
