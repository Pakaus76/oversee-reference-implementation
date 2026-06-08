"""
Module: model_backed_payload.py

Purpose:
    Define the structured payload contract expected from the first real
    OpenAI-backed implementation of model-backed anchor.

Architectural role:
    This module isolates the parsing and validation discipline of the model
    response used by model-backed anchor. Its role is intentionally narrow:
    - define the typed payload expected from the model
    - parse one JSON-like text response
    - validate the minimum structural integrity of that response before
      model-backed anchor builds the final repository Recommendation

Thesis traceability:
    - Chapter 6: Controlled progression from deterministic to model-backed
      conditions through explicit structured validation
    - Chapter 7: First typed payload contract for the real model-backed anchor
      condition
    - Chapter 8: Better comparability and reproducibility of C-versus-D
      evaluation through disciplined output validation

Inputs:
    - Raw text returned by the OpenAI helper for model-backed anchor

Outputs:
    - ModelBackedPayload instances containing validated recommendation fields

Key assumptions:
    - The first model-backed anchor condition must require a narrow structured response.
    - The model is expected to return only one compact JSON object.
    - Structural validation must happen before the repository builds the final
      Recommendation output.
    - This module validates structure and bounded field integrity, not broader
      governance or fallback policy.

Dependencies:
    - dataclasses
    - json
    - typing
    - internal domain priority vocabulary

Notes:
    - This module intentionally accepts a narrow JSON payload only.
    - This module does not call the model by itself.
    - This module does not implement retrieval, governance, or second-pass
      deliberation.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from oversee.domain import PriorityLevel


class ModelBackedPayloadError(ValueError):
    """
    Represent a validation error in the structured payload returned for D.

    Why this exists:
        Real model-backed anchor introduces model-generated content. The repository
        therefore needs a specific and readable validation error when the model
        output is missing, malformed, or outside the accepted bounded contract.
    """


@dataclass(frozen=True, slots=True)
class ModelBackedPayload:
    """
    Store the validated structured response expected from the model-backed anchor model call.

    Args:
        priority: Repository-compatible priority label.
        action: Non-empty recommended action text.
        rationale: Non-empty justification text.

    Returns:
        ModelBackedPayload: Typed validated payload ready for model-backed anchor.

    Raises:
        ModelBackedPayloadError: If any field is empty or invalid.
    """

    priority: str
    action: str
    rationale: str

    def __post_init__(self) -> None:
        """
        Validate the minimum integrity of the typed payload.
        """
        allowed_priorities = {level.value for level in PriorityLevel}

        normalized_priority = self.priority.strip()
        normalized_action = self.action.strip()
        normalized_rationale = self.rationale.strip()

        if not normalized_priority:
            raise ModelBackedPayloadError("priority must not be empty.")

        if normalized_priority not in allowed_priorities:
            raise ModelBackedPayloadError(
                "priority must belong to the repository priority vocabulary."
            )

        if not normalized_action:
            raise ModelBackedPayloadError("action must not be empty.")

        if not normalized_rationale:
            raise ModelBackedPayloadError("rationale must not be empty.")


def _strip_optional_code_fences(raw_text: str) -> str:
    """
    Remove one optional surrounding Markdown code fence from model output.

    Args:
        raw_text: Raw text returned by the model helper.

    Returns:
        str: Text without one outer fenced block when present.

    Notes:
        The D contract asks the model to return only JSON. This helper still
        removes one outer code fence defensively so that minor presentation
        noise does not automatically break execution.
    """
    normalized_text = raw_text.strip()

    if not normalized_text.startswith("```"):
        return normalized_text

    lines = normalized_text.splitlines()

    if len(lines) < 3:
        return normalized_text

    if not lines[-1].strip().startswith("```"):
        return normalized_text

    inner_lines = lines[1:-1]
    return "\n".join(inner_lines).strip()


def _parse_json_object(raw_text: str) -> Mapping[str, Any]:
    """
    Parse the raw model text into one JSON object.

    Args:
        raw_text: Raw text returned by the model helper.

    Returns:
        Mapping[str, Any]: Parsed top-level JSON object.

    Raises:
        ModelBackedPayloadError: If the text is empty, invalid JSON, or not an
            object.
    """
    if not raw_text.strip():
        raise ModelBackedPayloadError("Model output text must not be empty.")

    normalized_text = _strip_optional_code_fences(raw_text)

    try:
        parsed_payload = json.loads(normalized_text)
    except json.JSONDecodeError as exc:
        raise ModelBackedPayloadError(
            "Model output is not valid JSON for model-backed anchor."
        ) from exc

    if not isinstance(parsed_payload, dict):
        raise ModelBackedPayloadError(
            "Model output for model-backed anchor must be a JSON object."
        )

    return parsed_payload


def _require_string_field(
    payload: Mapping[str, Any],
    field_name: str,
) -> str:
    """
    Read one required string field from the parsed payload.

    Args:
        payload: Parsed JSON object.
        field_name: Name of the required field.

    Returns:
        str: Normalized non-empty string value.

    Raises:
        ModelBackedPayloadError: If the field is missing, not a string, or empty.
    """
    if field_name not in payload:
        raise ModelBackedPayloadError(
            f"Missing required field '{field_name}' in model-backed anchor payload."
        )

    raw_value = payload[field_name]

    if not isinstance(raw_value, str):
        raise ModelBackedPayloadError(
            f"Field '{field_name}' in model-backed anchor payload must be a string."
        )

    normalized_value = raw_value.strip()

    if not normalized_value:
        raise ModelBackedPayloadError(
            f"Field '{field_name}' in model-backed anchor payload must not be empty."
        )

    return normalized_value


def parse_model_backed_payload(raw_text: str) -> ModelBackedPayload:
    """
    Parse and validate the structured payload returned for model-backed anchor.

    Args:
        raw_text: Raw text returned by the OpenAI helper.

    Returns:
        ModelBackedPayload: Typed validated payload ready for model-backed anchor.

    Raises:
        ModelBackedPayloadError: If the raw text cannot be parsed into a valid
            model-backed payload.

    Validation scope:
        - top-level JSON object required
        - required fields: priority, action, rationale
        - non-empty string fields
        - repository-compatible priority vocabulary
    """
    payload = _parse_json_object(raw_text)

    priority = _require_string_field(payload, "priority")
    action = _require_string_field(payload, "action")
    rationale = _require_string_field(payload, "rationale")

    return ModelBackedPayload(
        priority=priority,
        action=action,
        rationale=rationale,
    )
