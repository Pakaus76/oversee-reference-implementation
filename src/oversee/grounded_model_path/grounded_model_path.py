"""
Module: grounded_model_path.py

Purpose:
    Implement the first real lightweight grounded condition of the rebuild.

Architectural role:
    This module provides the first executable grounded implementation of
    grounded model path. It preserves explicit continuity with the deterministic
    backbone by executing deterministic anchor, preserves explicit continuity with the
    active model-backed baseline by executing model-backed anchor, and then invokes one
    bounded grounded OpenAI recommendation step informed by a small retrieved
    evidence bundle.

Thesis traceability:
    - Chapter 5: Progression from model-backed recommendation toward bounded
      grounded recommendation
    - Chapter 6: Controlled artefact progression through explicit reconduction
      of E into a real lightweight grounded condition
    - Chapter 7: First honest implementation of lightweight grounding in the
      rebuild
    - Chapter 8: Future interpretability of differences between D and E under
      controlled comparison

Inputs:
    - DecisionCase

Outputs:
    - Recommendation

Key assumptions:
    - deterministic anchor remains the deterministic backbone beneath E.
    - model-backed anchor remains the immediate model-backed anchor of E.
    - E must use one bounded documentary evidence bundle only.
    - E must use one bounded OpenAI call only.
    - E must validate the structured grounded payload before building the final
      Recommendation.
    - If retrieval, model execution, or payload validation fails, E must fall
      back to a safe bounded output derived from model-backed anchor.

Dependencies:
    - src.oversee.domain
    - src.oversee.deterministic_anchor
    - src.oversee.model_backed_anchor
    - src.oversee.grounded_model_path.grounded_model_payload
    - src.oversee.conditions.contracts
    - src.oversee.retrieval.evidence_bundle
    - src.oversee.retrieval.maintenance_guidance_retriever
    - src.oversee.utils.openai_client
    - src.oversee.config.settings

Notes:
    - This module introduces the first real documentary grounding step of the
      rebuild.
    - This implementation does not add second-pass deliberation, broad agentic
      orchestration, or mature later-layer governance.
    - The fallback implemented here is a minimal execution safeguard required by
      the first real grounded condition, not a broader retrieval governance
      layer.
"""

from __future__ import annotations

from oversee.config.settings import ConfigurationError
from oversee.domain import (
    DecisionCase,
    PriorityLevel,
    Recommendation,
    validate_decision_case,
)
from oversee.retrieval.evidence_bundle import (
    EvidenceBundle,
    EvidenceBundleError,
    render_evidence_bundle_for_prompt,
)
from oversee.retrieval.maintenance_guidance_retriever import (
    RetrievalError,
    retrieve_maintenance_guidance_bundle,
)
from oversee.utils.model_client import OpenAIExecutionError, generate_text_response
from oversee.deterministic_anchor import run_deterministic_anchor
from oversee.model_backed_anchor import run_model_backed_anchor
from oversee.grounded_model_path.grounded_model_payload import (
    GroundedModelPayload,
    GroundedModelPayloadError,
    parse_grounded_model_payload,
)
from oversee.governance.contracts import build_recommendation_id

PROTECTED_NEAR_FAILURE_HOURS = 24.0
CRITICAL_ASSET_THRESHOLD = 5
DEFAULT_MAX_EVIDENCE_SNIPPETS = 3


def _build_priority_vocabulary_text() -> str:
    """
    Build the repository priority vocabulary for the E prompt.

    Returns:
        str: Comma-separated quoted priority values.
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


def _build_evidence_reference_text(evidence_bundle: EvidenceBundle) -> str:
    """
    Build the list of evidence snippet identifiers expected in the rationale.

    Args:
        evidence_bundle: Retrieved evidence bundle.

    Returns:
        str: Readable snippet-id list such as [g1], [g2], [g3].
    """
    return ", ".join(f"[{snippet.snippet_id}]" for snippet in evidence_bundle.snippets)


def _build_grounded_model_path_instructions(evidence_bundle: EvidenceBundle) -> str:
    """
    Build the bounded instruction block for the grounded E step.

    Args:
        evidence_bundle: Retrieved evidence bundle made available to E.

    Returns:
        str: Instruction text constraining the grounded model role and output.
    """
    allowed_priorities = _build_priority_vocabulary_text()
    evidence_reference_text = _build_evidence_reference_text(evidence_bundle)

    return (
        "You are generating grounded model path of a thesis prototype called the "
        "OVERSEE. "
        "grounded model path is the first lightweight grounded condition. "
        "It must remain explicitly anchored to the deterministic recommendation "
        "of deterministic anchor and to the active model-backed recommendation of "
        "model-backed anchor. "
        "You will also receive a bounded documentary evidence bundle. "
        "Return only one JSON object with exactly these string fields: "
        '"priority", "action", and "rationale". '
        f'The "priority" value must be one of: {allowed_priorities}. '
        "Stay within the same compact operational recommendation space already "
        "used by the repository. "
        "Do not use Markdown. "
        "Do not return explanations outside the JSON object. "
        "Use model-backed anchor as the immediate recommendation anchor and deterministic anchor "
        "as the deterministic backbone. "
        "Use the retrieved evidence to refine or support the recommendation in "
        "a bounded way. "
        "In the rationale, explicitly reference at least one retrieved evidence "
        f"snippet identifier exactly as provided here: {evidence_reference_text}. "
        "Do not invent new data, broader retrieval evidence, or external "
        "knowledge beyond the supplied evidence bundle."
    )


def _build_grounded_model_path_input_text(
    case: DecisionCase,
    c_recommendation: Recommendation,
    d_recommendation: Recommendation,
    evidence_bundle: EvidenceBundle,
) -> str:
    """
    Build the compact grounded model input for the grounded model path step.

    Args:
        case: Decision case being processed.
        c_recommendation: Deterministic backbone recommendation from C.
        d_recommendation: Immediate model-backed anchor from D.
        evidence_bundle: Retrieved documentary evidence bundle.

    Returns:
        str: Structured grounded prompt input text for one bounded model call.
    """
    evidence_text = render_evidence_bundle_for_prompt(evidence_bundle)

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
        "Deterministic backbone from deterministic anchor:\n"
        f"- priority: {c_recommendation.priority}\n"
        f"- action: {c_recommendation.action}\n"
        f"- rationale: {c_recommendation.rationale}\n\n"
        "Immediate model-backed anchor from model-backed anchor:\n"
        f"- priority: {d_recommendation.priority}\n"
        f"- action: {d_recommendation.action}\n"
        f"- rationale: {d_recommendation.rationale}\n\n"
        "Retrieved documentary evidence:\n"
        f"{evidence_text}\n\n"
        "Task:\n"
        "Produce the bounded grounded Condition grounded model path recommendation as one JSON object."
    )


def _validate_bounded_alignment(
    case: DecisionCase,
    payload: GroundedModelPayload,
    d_recommendation: Recommendation,
) -> None:
    """
    Validate minimal bounded alignment of the grounded model payload against repository rules.

    Args:
        case: Decision case being processed.
        payload: Parsed structured payload returned by the model.
        d_recommendation: Immediate anchor recommendation from model-backed anchor.

    Raises:
        GroundedModelPayloadError: If the payload violates the bounded role of E.

    Notes:
        This validation is intentionally narrow. It is not a mature governance
        layer. It only blocks clearly unacceptable grounded outputs that would
        break the bounded role of the first grounded model path condition.
    """
    time_to_failure_hours = case.alert.time_to_failure_hours
    model_priority = payload.priority

    if (
        time_to_failure_hours is not None
        and time_to_failure_hours <= PROTECTED_NEAR_FAILURE_HOURS
        and model_priority == PriorityLevel.LOW.value
    ):
        raise GroundedModelPayloadError(
            "grounded model path must not return low priority for a protected near-failure case."
        )

    if (
        case.asset.criticality >= CRITICAL_ASSET_THRESHOLD
        and model_priority == PriorityLevel.LOW.value
    ):
        raise GroundedModelPayloadError(
            "grounded model path must not return low priority for a critical asset case."
        )

    if (
        d_recommendation.priority == PriorityLevel.HIGH.value
        and model_priority == PriorityLevel.LOW.value
    ):
        raise GroundedModelPayloadError(
            "grounded model path must not de-escalate directly from high to low priority relative to model-backed anchor."
        )


def _validate_grounded_use(
    payload: GroundedModelPayload,
    evidence_bundle: EvidenceBundle,
) -> None:
    """
    Validate minimum grounded-use plausibility of the E rationale.

    Args:
        payload: Parsed structured payload returned by the model.
        evidence_bundle: Retrieved documentary evidence made available to E.

    Raises:
        GroundedModelPayloadError: If the rationale does not reference the provided
            evidence in a minimally legible way.
    """
    normalized_rationale = payload.rationale.lower()

    for snippet in evidence_bundle.snippets:
        if f"[{snippet.snippet_id}]" in normalized_rationale:
            return

    raise GroundedModelPayloadError(
        "grounded model path rationale must reference at least one retrieved evidence snippet identifier."
    )


def _build_response_trace_clause(response_id: str | None) -> str:
    """
    Build one optional trace clause for the validated E rationale.

    Args:
        response_id: Optional provider response identifier.

    Returns:
        str: Short trace clause that can be prefixed to the rationale.
    """
    if response_id is None:
        return ""

    return f" model response id: {response_id}."


def _build_validated_grounded_model_recommendation(
    case: DecisionCase,
    payload: GroundedModelPayload,
    evidence_bundle: EvidenceBundle,
    *,
    response_id: str | None,
) -> Recommendation:
    """
    Build the final validated Recommendation for a successful E execution.

    Args:
        case: Decision case being processed.
        payload: Validated structured payload returned by the model.
        evidence_bundle: Retrieved documentary evidence used by E.
        response_id: Optional provider response identifier.

    Returns:
        Recommendation: Final repository recommendation for grounded model path.
    """
    rationale = (
        "grounded model path produced a validated grounded recommendation anchored to "
        "model-backed anchor and supported by bounded documentary evidence."
        f"{_build_response_trace_clause(response_id)} "
        f"Evidence source: {evidence_bundle.source_name}. "
        f"{payload.rationale.strip()}"
    )

    return Recommendation(
        recommendation_id=build_recommendation_id("E", case),
        asset_id=case.alert.asset_id,
        action=payload.action.strip(),
        rationale=rationale.strip(),
        priority=payload.priority.strip(),
    )


def _build_fallback_recommendation(
    case: DecisionCase,
    d_recommendation: Recommendation,
    *,
    failure_reason: str,
) -> Recommendation:
    """
    Build the safe fallback Recommendation derived from model-backed anchor.

    Args:
        case: Decision case being processed.
        d_recommendation: Immediate anchor recommendation from model-backed anchor.
        failure_reason: Readable reason for fallback activation.

    Returns:
        Recommendation: Bounded fallback recommendation labeled as grounded model path.
    """
    rationale = (
        "grounded model path fell back to the model-backed anchor "
        "because the grounded step could not be executed or validated safely. "
        f"Reason: {failure_reason} "
        f"Original model-backed anchor rationale: {d_recommendation.rationale}"
    )

    return Recommendation(
        recommendation_id=build_recommendation_id("E", case),
        asset_id=case.alert.asset_id,
        action=d_recommendation.action,
        rationale=rationale,
        priority=d_recommendation.priority,
    )


def run_grounded_model_path(case: DecisionCase) -> Recommendation:
    """
    Execute the first real lightweight grounded condition of the rebuild.

    Execution shape:
        1. validate the incoming decision case
        2. execute deterministic anchor as deterministic backbone
        3. execute model-backed anchor as immediate model-backed anchor
        4. retrieve one bounded documentary evidence bundle
        5. build one grounded OpenAI prompt
        6. perform one model call
        7. parse and validate the structured payload
        8. return a comparable Recommendation
        9. if retrieval, execution, or validation fails, return a safe fallback
           derived from model-backed anchor

    Important boundary:
        This function introduces the first real documentary grounding step, but
        it does not implement second-pass deliberation, full RAG, or mature
        later-layer governance.
    """
    validate_decision_case(case)
    c_recommendation = run_deterministic_anchor(case)
    d_recommendation = run_model_backed_anchor(case)

    try:
        evidence_bundle = retrieve_maintenance_guidance_bundle(
            max_snippets=DEFAULT_MAX_EVIDENCE_SNIPPETS
        )

        model_result = generate_text_response(
            instructions=_build_grounded_model_path_instructions(evidence_bundle),
            input_text=_build_grounded_model_path_input_text(
                case,
                c_recommendation,
                d_recommendation,
                evidence_bundle,
            ),
        )

        payload = parse_grounded_model_payload(model_result.output_text)
        _validate_bounded_alignment(case, payload, d_recommendation)
        _validate_grounded_use(payload, evidence_bundle)

        return _build_validated_grounded_model_recommendation(
            case,
            payload,
            evidence_bundle,
            response_id=model_result.response_id,
        )

    except (
        ConfigurationError,
        RetrievalError,
        EvidenceBundleError,
        OpenAIExecutionError,
        GroundedModelPayloadError,
        ValueError,
    ) as exc:
        return _build_fallback_recommendation(
            case,
            d_recommendation,
            failure_reason=str(exc),
        )

