"""
Module: openai_client.py

Purpose:
    Provide the minimal reusable OpenAI client helper required by the first
    real model-backed condition of the rebuild.

Architectural role:
    This module encapsulates the narrow external model call introduced by
    model-backed anchor. Its responsibility is intentionally limited:
    - resolve repository OpenAI settings
    - create the OpenAI client
    - execute one Responses API call
    - return normalized text output for downstream validation

Thesis traceability:
    - Chapter 6: Controlled progression from deterministic conditions toward
      the first real model-backed condition
    - Chapter 7: Minimal implementation infrastructure for the first
      model-backed generative layer
    - Chapter 8: Reproducible execution basis for controlled C-versus-D
      comparison

Inputs:
    - OpenAI runtime settings
    - Instructions text
    - Input text

Outputs:
    - OpenAITextResult containing the normalized model output text and the
      optional provider response identifier

Key assumptions:
    - The first real model-backed anchor implementation should use one narrow model call only.
    - Output validation belongs to the condition layer that consumes the model
      result, not to this helper.
    - This helper should remain small, explicit, and easy to audit.

Dependencies:
    - dataclasses
    - typing
    - src.oversee.config.settings
    - openai (runtime dependency imported lazily)

Notes:
    - This helper uses the OpenAI Python client through the Responses API.
    - This module does not implement retrieval, fallback policy, governance,
      or recommendation validation.
    - This module should be treated as infrastructural support for model-backed anchor,
      not as a broader orchestration layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from oversee.config.settings import OpenAISettings, get_openai_settings


class OpenAIExecutionError(RuntimeError):
    """
    Represent an execution failure while calling the external OpenAI service.

    Why this exists:
        The first model-backed anchor condition introduces an external dependency. Failures
        should therefore surface through a specific, readable exception rather
        than through ambiguous generic runtime errors.
    """


@dataclass(frozen=True, slots=True)
class OpenAITextResult:
    """
    Store the normalized result returned by one OpenAI text-generation call.

    Args:
        response_id: Optional provider response identifier when available.
        output_text: Normalized non-empty text returned by the model.

    Returns:
        OpenAITextResult: Compact normalized model result for downstream use.

    Raises:
        ValueError: If the normalized output text is empty.
    """

    response_id: str | None
    output_text: str

    def __post_init__(self) -> None:
        """
        Validate the minimum integrity of the normalized model output.
        """
        if not self.output_text.strip():
            raise ValueError("output_text must not be empty.")


def _import_openai_client_class() -> type[Any]:
    """
    Import the OpenAI client class lazily.

    Returns:
        type[Any]: OpenAI client class from the installed SDK.

    Raises:
        OpenAIExecutionError: If the dependency is not installed.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise OpenAIExecutionError(
            "The 'openai' package is not installed. Install project "
            "dependencies before executing the model-backed anchor condition."
        ) from exc

    return OpenAI


def build_openai_client(settings: OpenAISettings | None = None) -> Any:
    """
    Build the minimal OpenAI client used by model-backed conditions.

    Args:
        settings: Optional pre-resolved runtime settings. If omitted, the
            repository environment settings are loaded explicitly.

    Returns:
        Any: Configured OpenAI client instance.
    """
    resolved_settings = settings or get_openai_settings()
    openai_client_class = _import_openai_client_class()

    return openai_client_class(api_key=resolved_settings.api_key)


def _extract_output_text_from_content_block(content_block: Any) -> str | None:
    """
    Try to extract text from one content block returned by the provider.

    Args:
        content_block: Provider content block.

    Returns:
        str | None: Extracted text if available, otherwise None.
    """
    block_type = getattr(content_block, "type", None)

    if block_type == "output_text":
        text_value = getattr(content_block, "text", None)
        if isinstance(text_value, str) and text_value.strip():
            return text_value.strip()

    text_attribute = getattr(content_block, "text", None)
    if isinstance(text_attribute, str) and text_attribute.strip():
        return text_attribute.strip()

    return None


def _extract_output_text_from_response_output(response: Any) -> str | None:
    """
    Try to reconstruct output text from the response.output structure.

    Args:
        response: Raw provider response object.

    Returns:
        str | None: Joined non-empty text if recoverable, otherwise None.
    """
    output_items = getattr(response, "output", None)

    if not output_items:
        return None

    collected_parts: list[str] = []

    for output_item in output_items:
        content_items = getattr(output_item, "content", None)

        if not content_items:
            continue

        for content_block in content_items:
            extracted_text = _extract_output_text_from_content_block(content_block)
            if extracted_text:
                collected_parts.append(extracted_text)

    if not collected_parts:
        return None

    return "\n".join(collected_parts).strip()


def _extract_output_text(response: Any) -> str:
    """
    Extract normalized text from the provider response.

    Extraction strategy:
        1. Prefer response.output_text when available.
        2. Fall back to parsing response.output content blocks.
        3. Fail explicitly if no usable text is available.

    Args:
        response: Raw provider response object.

    Returns:
        str: Normalized non-empty text.

    Raises:
        OpenAIExecutionError: If no usable text can be extracted.
    """
    direct_output_text = getattr(response, "output_text", None)

    if isinstance(direct_output_text, str) and direct_output_text.strip():
        return direct_output_text.strip()

    reconstructed_output_text = _extract_output_text_from_response_output(response)

    if reconstructed_output_text:
        return reconstructed_output_text

    raise OpenAIExecutionError(
        "model provider returned no usable textual output for model-backed anchor execution."
    )


def generate_text_response(
    *,
    instructions: str,
    input_text: str,
    settings: OpenAISettings | None = None,
) -> OpenAITextResult:
    """
    Execute one narrow OpenAI Responses API text call.

    Args:
        instructions: System/developer-style instruction text that constrains
            the role and output of the model.
        input_text: User/input payload text passed to the model.
        settings: Optional pre-resolved runtime settings.

    Returns:
        OpenAITextResult: Normalized provider result with non-empty output text.

    Raises:
        ValueError: If instructions or input_text are empty.
        ConfigurationError: Propagated if OpenAI settings are unavailable.
        OpenAIExecutionError: If the model call fails or returns no usable text.
    """
    if not instructions.strip():
        raise ValueError("instructions must not be empty.")

    if not input_text.strip():
        raise ValueError("input_text must not be empty.")

    resolved_settings = settings or get_openai_settings()
    client = build_openai_client(resolved_settings)

    try:
        response = client.responses.create(
            model=resolved_settings.model,
            instructions=instructions,
            input=input_text,
        )
    except Exception as exc:
        raise OpenAIExecutionError(
            "external model call failed during model-backed anchor execution."
        ) from exc

    output_text = _extract_output_text(response)
    response_id = getattr(response, "id", None)

    return OpenAITextResult(
        response_id=response_id,
        output_text=output_text,
    )
