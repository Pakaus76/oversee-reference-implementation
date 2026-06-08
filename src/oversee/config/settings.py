"""
Module: settings.py

Purpose:
    Provide the minimal runtime configuration required by the first real
    model-backed path of the rebuild.

Architectural role:
    This module centralizes the explicit environment-based settings needed by
    the repository when external model execution is introduced in model-backed anchor.
    Its role is intentionally narrow: expose a small, typed configuration path
    that remains easy to inspect, document, and test.

Thesis traceability:
    - Chapter 6: Controlled progression from deterministic to model-backed
      conditions through explicit implementation discipline
    - Chapter 7: Minimal configuration infrastructure for the first real
      model-backed generative path
    - Chapter 8: Reproducible execution basis for controlled cross-condition
      comparison

Inputs:
    Environment variables:
        - OPENAI_API_KEY
        - OPENAI_MODEL

Outputs:
    - OpenAISettings instances containing validated runtime configuration

Key assumptions:
    - model-backed anchor is the first condition that requires external model
      configuration.
    - Configuration must remain explicit, small, typed, and easy to audit.
    - The API key is mandatory for real model execution.
    - The model name may fall back to a repository-default value if the
      environment variable is not set explicitly.

Dependencies:
    - dataclasses
    - os

Notes:
    - This module intentionally does not load .env files by itself.
      Environment preparation remains an external execution concern.
    - This module does not perform any OpenAI call.
    - This module should be treated as configuration infrastructure, not as
      a broader orchestration layer.
"""

from __future__ import annotations

from dataclasses import dataclass
import os

DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"


class ConfigurationError(ValueError):
    """
    Represent a repository configuration error.

    Why this exists:
        Real model-backed anchor introduces the first external model dependency of the
        rebuild. Missing or malformed configuration should therefore fail with a
        specific and readable error instead of producing ambiguous runtime
        behavior.
    """


@dataclass(frozen=True, slots=True)
class OpenAISettings:
    """
    Store the minimal configuration required for external model execution.

    Args:
        api_key: Non-empty API key used to authenticate model calls.
        model: Non-empty model name used for the repository execution path.

    Returns:
        OpenAISettings: Typed runtime configuration for external model execution.

    Raises:
        ConfigurationError: If any required value is empty after normalization.
    """

    api_key: str
    model: str

    def __post_init__(self) -> None:
        """
        Validate the integrity of the normalized runtime configuration.
        """
        if not self.api_key.strip():
            raise ConfigurationError("OPENAI_API_KEY must not be empty.")

        if not self.model.strip():
            raise ConfigurationError("OPENAI_MODEL must not be empty.")


def _read_env(name: str) -> str | None:
    """
    Read one environment variable and normalize surrounding whitespace.

    Args:
        name: Environment variable name.

    Returns:
        str | None: Stripped value if present and non-empty, otherwise None.

    Side effects:
        None.
    """
    raw_value = os.getenv(name)

    if raw_value is None:
        return None

    normalized_value = raw_value.strip()

    if not normalized_value:
        return None

    return normalized_value


def get_openai_settings() -> OpenAISettings:
    """
    Build the minimal OpenAI runtime settings from environment variables.

    Returns:
        OpenAISettings: Validated OpenAI configuration for the repository.

    Raises:
        ConfigurationError: If the API key is missing or empty.

    Notes:
        - OPENAI_API_KEY is mandatory.
        - OPENAI_MODEL falls back to a repository-default value when omitted.
        - The function is intentionally narrow so that the configuration path
          remains stable, explicit, and easy to document.
    """
    api_key = _read_env("OPENAI_API_KEY")
    model = _read_env("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL

    if api_key is None:
        raise ConfigurationError(
            "Missing OPENAI_API_KEY. Real model-backed anchor requires an API key for "
            "external model execution."
        )

    return OpenAISettings(
        api_key=api_key,
        model=model,
    )
