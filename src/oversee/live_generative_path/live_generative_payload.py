"""
Module: live_generative_payload.py

Purpose:
    Define the structured payload contract expected from the future real
    second-pass deliberative implementation of live generative path.

Architectural role:
    This module isolates the parsing and validation discipline of the model
    response used by live generative path. Its role is intentionally narrow:
    - define the typed payload expected from the second-pass deliberative model
    - parse one JSON-like text response
    - validate the minimum structural integrity of that response before
      live generative path builds the final repository Recommendation

Thesis traceability:
    - Chapter 6: Controlled progression from grounded recommendation toward
      deliberative recommendation through explicit structured validation
    - Chapter 7: First typed payload contract for the real deliberative F
      condition
    - Chapter 8: Better comparability and reproducibility of E-versus-F
      evaluation through disciplined output validation

Inputs:
    - Raw text returned by the OpenAI helper for live generative path

Outputs:
    - LiveGenerativePayload instances containing validated recommendation fields

Key assumptions:
    - The first live generative path condition should require a narrow structured response.
    - The model is expected to return only one compact JSON object.
    - Structural validation must happen before the repository builds the final
      Recommendation output.
    - This module validates structure and bounded field integrity, not broader
      deliberative plausibility. Deliberative plausibility should be checked in
      the F condition where the E anchor is available.

Dependencies:
    - dataclasses
    - json
    - typing
    - internal domain priority vocabulary

Notes:
    - This module intentionally accepts a narrow JSON payload only.
    - This module does not call the model by itself.
    - This module does not implement retrieval, fallback logic, or broader
      orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from oversee.domain import PriorityLevel


class LiveGenerativePayloadError(ValueError):
    """
    Represent a validation error in the structured payload returned for F.

    Why this exists:
        Real live generative path introduces deliberative model-generated content. The
        repository therefore needs a specific and readable validation error when
        the model output is missing, malformed, or outside the accepted bounded
        contract.
    """


@dataclass(frozen=True, slots=True)
class LiveGenerativePayload:
    """
    Store the validated structured response expected from the live generative path model call.

    Args:
        priority: Repository-compatible priority label.
        action: Non-empty recommended action text.
        rationale: Non-empty justification text.

    Returns:
        LiveGenerativePayload: Typed validated payload ready for live generative path.

    Raises:
        LiveGenerativePayloadError: If any field is empty or invalid.
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
            raise LiveGenerativePayloadError("priority must not be empty.")

        if normalized_priority not in allowed_priorities:
            raise LiveGenerativePayloadError(
                "priority must belong to the repository priority vocabulary."
            )

        if not normalized_action:
            raise LiveGenerativePayloadError("action must not be empty.")

        if not normalized_rationale:
            raise LiveGenerativePayloadError("rationale must not be empty.")


def _strip_optional_code_fences(raw_text: str) -> str:
    """
    Remove one optional surrounding Markdown code fence from model output.

    Args:
        raw_text: Raw text returned by the model helper.

    Returns:
        str: Text without one outer fenced block when present.
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
        LiveGenerativePayloadError: If the text is empty, invalid JSON, or not an
            object.
    """
    if not raw_text.strip():
        raise LiveGenerativePayloadError("Model output text must not be empty.")

    normalized_text = _strip_optional_code_fences(raw_text)

    try:
        parsed_payload = json.loads(normalized_text)
    except json.JSONDecodeError as exc:
        raise LiveGenerativePayloadError(
            "Model output is not valid JSON for live generative path."
        ) from exc

    if not isinstance(parsed_payload, dict):
        raise LiveGenerativePayloadError(
            "Model output for live generative path must be a JSON object."
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
        LiveGenerativePayloadError: If the field is missing, not a string, or empty.
    """
    if field_name not in payload:
        raise LiveGenerativePayloadError(
            f"Missing required field '{field_name}' in live generative path payload."
        )

    raw_value = payload[field_name]

    if not isinstance(raw_value, str):
        raise LiveGenerativePayloadError(
            f"Field '{field_name}' in live generative path payload must be a string."
        )

    normalized_value = raw_value.strip()

    if not normalized_value:
        raise LiveGenerativePayloadError(
            f"Field '{field_name}' in live generative path payload must not be empty."
        )

    return normalized_value


def parse_live_generative_payload(raw_text: str) -> LiveGenerativePayload:
    """
    Parse and validate the structured payload returned for live generative path.

    Args:
        raw_text: Raw text returned by the OpenAI helper.

    Returns:
        LiveGenerativePayload: Typed validated payload ready for live generative path.

    Raises:
        LiveGenerativePayloadError: If the raw text cannot be parsed into a valid
            live generative payload.

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

    return LiveGenerativePayload(
        priority=priority,
        action=action,
        rationale=rationale,
    )
