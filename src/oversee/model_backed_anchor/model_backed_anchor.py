"""
Module: model_backed_anchor.py

Purpose:
    Implement the first real model-backed path of the rebuild.

Architectural role:
    This module provides the first executable model-backed implementation of
    model-backed anchor. It preserves explicit continuity with the deterministic
    backbone by executing deterministic anchor first and then invoking one bounded
    model-backed recommendation step anchored to the C output.

Thesis traceability:
    - Chapter 5: Transition from deterministic decision logic toward the first
      real model-backed recommendation layer
    - Chapter 6: Controlled artefact progression through explicit reconduction
      of D into a real model-backed path
    - Chapter 7: First honest implementation of generative AI integration in
      the rebuild
    - Chapter 8: Future interpretability of differences between C and D under
      controlled comparison

Inputs:
    - DecisionCase

Outputs:
    - Recommendation

Key assumptions:
    - deterministic anchor remains the deterministic anchor for model-backed anchor.
    - D must use one bounded OpenAI call only.
    - D must remain directly comparable with C.
    - D must validate the structured model payload before building the final
      Recommendation.
    - If model execution or payload validation fails, D must fall back to a
      safe bounded output derived from deterministic anchor.

Dependencies:
    - src.oversee.domain
    - src.oversee.deterministic_anchor
    - src.oversee.model_backed_anchor.model_backed_payload
    - src.oversee.conditions.contracts
    - src.oversee.utils.openai_client
    - src.oversee.config.settings

Notes:
    - This module introduces the first real external model dependency of the
      rebuild.
    - This implementation does not add retrieval, external grounding,
      multi-step deliberation, or mature later-layer governance.
    - The fallback implemented here is a minimal execution safeguard required
      by the first real model-backed condition, not a broader governance layer.
"""

from __future__ import annotations

from oversee.config.settings import ConfigurationError
from oversee.domain import (
    DecisionCase,
    PriorityLevel,
    Recommendation,
    validate_decision_case,
)
from oversee.utils.model_client import OpenAIExecutionError, generate_text_response
from oversee.deterministic_anchor import run_deterministic_anchor
from oversee.model_backed_anchor.model_backed_payload import (
    ModelBackedPayload,
    ModelBackedPayloadError,
    parse_model_backed_payload,
)
from oversee.governance.contracts import build_recommendation_id


PROTECTED_NEAR_FAILURE_HOURS = 24.0
CRITICAL_ASSET_THRESHOLD = 5


def _build_priority_vocabulary_text() -> str:
    """
    Build the repository priority vocabulary for the D prompt.

    Returns:
        str: Comma-separated quoted priority values.

    Side effects:
        None.
    """
    return ", ".join(f'"{level.value}"' for level in PriorityLevel)


def _format_optional_value(value: object | None) -> str:
    """
    Convert one optional value into a readable prompt-safe string.

    Args:
        value: Value to serialize.

    Returns:
        str: Readable string representation.
    """
    if value is None:
        return "None"

    return str(value)


def _build_model_backed_anchor_instructions() -> str:
    """
    Build the bounded instruction block for the model-backed anchor step.

    Returns:
        str: Instruction text constraining the model role and output.

    Side effects:
        None.
    """
    allowed_priorities = _build_priority_vocabulary_text()

    return (
        "You are generating model-backed anchor of a thesis prototype called the "
        "OVERSEE. "
        "model-backed anchor is the first real model-backed condition, but it must "
        "remain explicitly anchored to the deterministic recommendation of "
        "deterministic anchor. "
        "Return only one JSON object with exactly these string fields: "
        '"priority", "action", and "rationale". '
        f'The "priority" value must be one of: {allowed_priorities}. '
        "Stay within the same compact operational recommendation space already "
        "used by the repository. "
        "Do not use Markdown. "
        "Do not return explanations outside the JSON object. "
        "Use the deterministic anchor recommendation as the deterministic anchor. "
        "You may preserve the same recommendation as C or produce a bounded "
        "variation if the case context justifies it clearly. "
        "Do not invent new data, retrieval evidence, or broader orchestration."
    )


def _build_model_backed_anchor_input_text(
    case: DecisionCase,
    c_recommendation: Recommendation,
) -> str:
    """
    Build the compact model input for the model-backed anchor step.

    Args:
        case: Decision case being processed.
        c_recommendation: Deterministic anchor produced by deterministic anchor.

    Returns:
        str: Structured prompt input text for one bounded model call.

    Side effects:
        None.
    """
    return (
        "Decision case:\n"
        f"- case_id: {case.case_id}\n"
        f"- asset_id: {case.asset.asset_id}\n"
        f"- asset_type: {_format_optional_value(case.asset.asset_type)}\n"
        f"- location: {_format_optional_value(case.asset.location)}\n"
        f"- asset_criticality: {case.asset.criticality}\n"
        f"- alert_id: {case.alert.alert_id}\n"
        f"- predicted_issue: {_format_optional_value(case.alert.predicted_issue)}\n"
        f"- time_to_failure_hours: {_format_optional_value(case.alert.time_to_failure_hours)}\n"
        f"- confidence_score: {_format_optional_value(case.alert.confidence_score)}\n"
        f"- context_note: {_format_optional_value(case.context_note)}\n\n"
        "Deterministic anchor from deterministic anchor:\n"
        f"- priority: {c_recommendation.priority}\n"
        f"- action: {c_recommendation.action}\n"
        f"- rationale: {c_recommendation.rationale}\n\n"
        "Task:\n"
        "Produce the bounded Condition model-backed anchor recommendation as one JSON object."
    )


def _validate_bounded_alignment(
    case: DecisionCase,
    payload: ModelBackedPayload,
    c_recommendation: Recommendation,
) -> None:
    """
    Validate minimal bounded alignment of the model-backed payload against repository rules.

    Args:
        case: Decision case being processed.
        payload: Parsed structured payload returned by the model.
        c_recommendation: Deterministic anchor from deterministic anchor.

    Raises:
        ModelBackedPayloadError: If the payload violates the bounded role of D.

    Notes:
        This validation is intentionally narrow. It is not a mature governance
        layer. It only blocks clearly unacceptable de-escalations that would
        break the bounded role of the first model-backed anchor condition.
    """
    time_to_failure_hours = case.alert.time_to_failure_hours
    model_priority = payload.priority

    if (
        time_to_failure_hours is not None
        and time_to_failure_hours <= PROTECTED_NEAR_FAILURE_HOURS
        and model_priority == PriorityLevel.LOW.value
    ):
        raise ModelBackedPayloadError(
            "model-backed anchor must not return low priority for a protected near-failure case."
        )

    if (
        case.asset.criticality >= CRITICAL_ASSET_THRESHOLD
        and model_priority == PriorityLevel.LOW.value
    ):
        raise ModelBackedPayloadError(
            "model-backed anchor must not return low priority for a critical asset case."
        )

    if (
        c_recommendation.priority == PriorityLevel.HIGH.value
        and model_priority == PriorityLevel.LOW.value
    ):
        raise ModelBackedPayloadError(
            "model-backed anchor must not de-escalate directly from high to low priority relative to deterministic anchor."
        )


def _build_response_trace_clause(response_id: str | None) -> str:
    """
    Build one optional trace clause for the validated D rationale.

    Args:
        response_id: Optional provider response identifier.

    Returns:
        str: Short trace clause that can be prefixed to the rationale.
    """
    if response_id is None:
        return ""

    return f" model response id: {response_id}."


def _build_validated_model_backed_recommendation(
    case: DecisionCase,
    payload: ModelBackedPayload,
    *,
    response_id: str | None,
) -> Recommendation:
    """
    Build the final validated Recommendation for a successful D execution.

    Args:
        case: Decision case being processed.
        payload: Validated structured payload returned by the model.
        response_id: Optional provider response identifier.

    Returns:
        Recommendation: Final repository recommendation for model-backed anchor.
    """
    rationale = (
        "model-backed anchor produced a validated model-backed recommendation anchored "
        "to deterministic anchor."
        f"{_build_response_trace_clause(response_id)} "
        f"{payload.rationale.strip()}"
    )

    return Recommendation(
        recommendation_id=build_recommendation_id("D", case),
        asset_id=case.alert.asset_id,
        action=payload.action.strip(),
        rationale=rationale.strip(),
        priority=payload.priority.strip(),
    )


def _build_fallback_recommendation(
    case: DecisionCase,
    c_recommendation: Recommendation,
    *,
    failure_reason: str,
) -> Recommendation:
    """
    Build the safe fallback Recommendation derived from deterministic anchor.

    Args:
        case: Decision case being processed.
        c_recommendation: Deterministic anchor recommendation from deterministic anchor.
        failure_reason: Readable reason for fallback activation.

    Returns:
        Recommendation: Bounded fallback recommendation labeled as model-backed anchor.
    """
    rationale = (
        "model-backed anchor fell back to the deterministic anchor "
        "because the external model step could not be executed or validated "
        f"safely. Reason: {failure_reason} "
        f"Original deterministic anchor rationale: {c_recommendation.rationale}"
    )

    return Recommendation(
        recommendation_id=build_recommendation_id("D", case),
        asset_id=case.alert.asset_id,
        action=c_recommendation.action,
        rationale=rationale,
        priority=c_recommendation.priority,
    )


def run_model_backed_anchor(case: DecisionCase) -> Recommendation:
    """
    Execute the first real model-backed path of the rebuild.

    Execution shape:
        1. validate the incoming decision case
        2. execute deterministic anchor as deterministic anchor
        3. build one bounded OpenAI prompt
        4. perform one model call
        5. parse and validate the structured payload
        6. return a comparable Recommendation
        7. if execution or validation fails, return a safe fallback derived
           from deterministic anchor

    Important boundary:
        This function introduces the first real model-backed recommendation
        step, but it does not implement retrieval, second-pass deliberation,
        or mature later-layer governance.
    """
    validate_decision_case(case)
    c_recommendation = run_deterministic_anchor(case)

    try:
        model_result = generate_text_response(
            instructions=_build_model_backed_anchor_instructions(),
            input_text=_build_model_backed_anchor_input_text(case, c_recommendation),
        )
        payload = parse_model_backed_payload(model_result.output_text)
        _validate_bounded_alignment(case, payload, c_recommendation)

        return _build_validated_model_backed_recommendation(
            case,
            payload,
            response_id=model_result.response_id,
        )

    except (
        ConfigurationError,
        OpenAIExecutionError,
        ModelBackedPayloadError,
        ValueError,
    ) as exc:
        return _build_fallback_recommendation(
            case,
            c_recommendation,
            failure_reason=str(exc),
        )

