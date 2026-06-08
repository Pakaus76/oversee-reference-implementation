"""
Module: live_generative_path.py

Purpose:
    Implement the first real second-pass deliberative condition of the rebuild.

Architectural role:
    This module provides the first executable deliberative implementation of
    live generative path. It preserves explicit continuity with the deterministic
    backbone by executing deterministic anchor, preserves explicit continuity with the
    real model-backed and grounded baselines by executing Conditions D and E,
    and then invokes one bounded second-pass OpenAI review/refinement step.

Thesis traceability:
    - Chapter 5: Progression from grounded recommendation toward bounded
      deliberative recommendation
    - Chapter 6: Controlled artefact progression through explicit reconduction
      of F into a real second-pass deliberative condition
    - Chapter 7: First honest implementation of bounded second-pass
      deliberation in the rebuild
    - Chapter 8: Future interpretability of differences between E and F under
      controlled comparison

Inputs:
    - DecisionCase

Outputs:
    - Recommendation

Key assumptions:
    - deterministic anchor remains the deterministic backbone beneath F.
    - model-backed anchor remains the earlier model-backed anchor beneath E.
    - grounded model path remains the immediate grounded anchor of F.
    - F must use one bounded second-pass OpenAI call only.
    - F must validate the structured deliberative payload before building the
      final Recommendation.
    - If retrieval reuse, model execution, or payload validation fails, F must
      fall back to a safe bounded output derived from grounded model path.

Dependencies:
    - src.oversee.domain
    - src.oversee.deterministic_anchor
    - src.oversee.model_backed_anchor
    - src.oversee.grounded_model_path
    - src.oversee.live_generative_path.live_generative_payload
    - src.oversee.conditions.contracts
    - src.oversee.retrieval.evidence_bundle
    - src.oversee.retrieval.maintenance_guidance_retriever
    - src.oversee.utils.openai_client
    - src.oversee.config.settings

Notes:
    - This module introduces the first explicit second-pass deliberative step of
      the rebuild.
    - This implementation does not add broad agentic orchestration, recursive
      reflection loops, or mature autonomy claims.
    - The fallback implemented here is a minimal execution safeguard required by
      the first real deliberative condition, not a broader governance layer.
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
from oversee.grounded_model_path import run_grounded_model_path
from oversee.live_generative_path.live_generative_payload import (
    LiveGenerativePayload,
    LiveGenerativePayloadError,
    parse_live_generative_payload,
)
from oversee.governance.contracts import build_recommendation_id

PROTECTED_NEAR_FAILURE_HOURS = 24.0
CRITICAL_ASSET_THRESHOLD = 5
DEFAULT_MAX_EVIDENCE_SNIPPETS = 3


def _build_priority_vocabulary_text() -> str:
    """
    Build the repository priority vocabulary for the F prompt.

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


def _build_evidence_reference_text(evidence_bundle: EvidenceBundle | None) -> str:
    """
    Build the list of evidence snippet identifiers available to F.

    Args:
        evidence_bundle: Optional retrieved evidence bundle.

    Returns:
        str: Readable snippet-id list, or a short placeholder when no bundle is
            available.
    """
    if evidence_bundle is None:
        return "no evidence snippets provided"

    return ", ".join(f"[{snippet.snippet_id}]" for snippet in evidence_bundle.snippets)


def _build_live_generative_path_instructions(evidence_bundle: EvidenceBundle | None) -> str:
    """
    Build the bounded instruction block for the deliberative F step.

    Args:
        evidence_bundle: Optional retrieved evidence bundle reused by F.

    Returns:
        str: Instruction text constraining the second-pass model role and output.
    """
    allowed_priorities = _build_priority_vocabulary_text()
    evidence_reference_text = _build_evidence_reference_text(evidence_bundle)

    return (
        "You are generating live generative path of a thesis prototype called the "
        "OVERSEE. "
        "live generative path is the first second-pass deliberative condition. "
        "It must remain explicitly anchored to the grounded recommendation of "
        "grounded model path, to the model-backed recommendation of model-backed anchor, and to "
        "the deterministic backbone of deterministic anchor. "
        "Your role is not to restart the whole problem from zero. "
        "Your role is to review the existing grounded recommendation and either "
        "confirm it or refine it in a bounded way. "
        "Return only one JSON object with exactly these string fields: "
        '"priority", "action", and "rationale". '
        f'The "priority" value must be one of: {allowed_priorities}. '
        "Stay within the same compact operational recommendation space already "
        "used by the repository. "
        "Do not use Markdown. "
        "Do not return explanations outside the JSON object. "
        "Treat grounded model path as the immediate anchor. "
        "If you refine E, do so in a bounded and clearly justified way. "
        "In the rationale, explicitly indicate that a second-pass review took "
        "place by using wording such as 'second-pass review', 'review', "
        "'refined', or 'after reviewing'. "
        "If documentary evidence is provided, you may reference it, including "
        f"the following snippet identifiers: {evidence_reference_text}. "
        "Do not invent new data, broader retrieval evidence, or external "
        "knowledge beyond the supplied context."
    )


def _build_live_generative_path_input_text(
    case: DecisionCase,
    c_recommendation: Recommendation,
    d_recommendation: Recommendation,
    e_recommendation: Recommendation,
    evidence_bundle: EvidenceBundle | None,
) -> str:
    """
    Build the compact deliberative input for the second-pass F step.

    Args:
        case: Decision case being processed.
        c_recommendation: Deterministic backbone recommendation from C.
        d_recommendation: Earlier model-backed anchor from D.
        e_recommendation: Immediate grounded anchor from E.
        evidence_bundle: Optional bounded documentary evidence reused by F.

    Returns:
        str: Structured deliberative prompt input text for one bounded model call.
    """
    evidence_text = (
        render_evidence_bundle_for_prompt(evidence_bundle)
        if evidence_bundle is not None
        else "No documentary evidence bundle was passed to the second-pass review."
    )

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
        "Earlier model-backed anchor from model-backed anchor:\n"
        f"- priority: {d_recommendation.priority}\n"
        f"- action: {d_recommendation.action}\n"
        f"- rationale: {d_recommendation.rationale}\n\n"
        "Immediate grounded anchor from grounded model path:\n"
        f"- priority: {e_recommendation.priority}\n"
        f"- action: {e_recommendation.action}\n"
        f"- rationale: {e_recommendation.rationale}\n\n"
        "Optional documentary evidence context:\n"
        f"{evidence_text}\n\n"
        "Task:\n"
        "Review the Condition grounded model path recommendation and produce the bounded "
        "second-pass Condition live generative path recommendation as one JSON object."
    )


def _validate_bounded_alignment(
    case: DecisionCase,
    payload: LiveGenerativePayload,
    e_recommendation: Recommendation,
) -> None:
    """
    Validate minimal bounded alignment of the live generative payload against repository rules.

    Args:
        case: Decision case being processed.
        payload: Parsed structured payload returned by the model.
        e_recommendation: Immediate anchor recommendation from E.

    Raises:
        LiveGenerativePayloadError: If the payload violates the bounded role of F.

    Notes:
        This validation is intentionally narrow. It is not a mature governance
        layer. It only blocks clearly unacceptable deliberative outputs that
        would break the bounded role of the first live generative path condition.
    """
    time_to_failure_hours = case.alert.time_to_failure_hours
    model_priority = payload.priority

    if (
        time_to_failure_hours is not None
        and time_to_failure_hours <= PROTECTED_NEAR_FAILURE_HOURS
        and model_priority == PriorityLevel.LOW.value
    ):
        raise LiveGenerativePayloadError(
            "live generative path must not return low priority for a protected near-failure case."
        )

    if (
        case.asset.criticality >= CRITICAL_ASSET_THRESHOLD
        and model_priority == PriorityLevel.LOW.value
    ):
        raise LiveGenerativePayloadError(
            "live generative path must not return low priority for a critical asset case."
        )

    if (
        e_recommendation.priority == PriorityLevel.HIGH.value
        and model_priority == PriorityLevel.LOW.value
    ):
        raise LiveGenerativePayloadError(
            "live generative path must not de-escalate directly from high to low priority relative to grounded model path."
        )


def _validate_deliberative_use(payload: LiveGenerativePayload) -> None:
    """
    Validate minimum deliberative plausibility of the F rationale.

    Args:
        payload: Parsed structured payload returned by the model.

    Raises:
        LiveGenerativePayloadError: If the rationale does not make the second-pass
            review legible in a minimally explicit way.
    """
    normalized_rationale = payload.rationale.lower()

    deliberative_markers = (
        "second-pass",
        "review",
        "refined",
        "after reviewing",
        "after review",
    )

    if any(marker in normalized_rationale for marker in deliberative_markers):
        return

    raise LiveGenerativePayloadError(
        "live generative path rationale must make the second-pass review legible."
    )


def _priority_rank(priority: str) -> int:
    """
    Return a stable numeric rank for one repository priority label.
    """
    normalized_priority = priority.strip().lower()

    priority_ranks = {
        PriorityLevel.LOW.value: 0,
        PriorityLevel.MEDIUM.value: 1,
        PriorityLevel.HIGH.value: 2,
    }

    if normalized_priority not in priority_ranks:
        raise LiveGenerativePayloadError(
            f"Unsupported priority value in live generative path governance: {priority!r}"
        )

    return priority_ranks[normalized_priority]


def _detect_explicit_priority_escalation_signal(context_note: str | None) -> bool:
    """
    Detect whether the effective context note contains an explicit enriched-context
    escalation signal strong enough to justify a one-level priority increase in F.

    Governance intent:
        This v1 governor is intentionally conservative. It does not allow the
        second-pass deliberative layer to escalate priority from narrative style
        alone. It requires both:
        1. evidence that enriched auxiliary layers reached the case context
        2. at least one escalation-relevant operational marker
    """
    if context_note is None:
        return False

    normalized_context = context_note.lower()

    enriched_layer_markers = (
        "hard-case layer:",
        "behavior layer:",
        "document layer:",
    )

    escalation_markers = (
        "delayed spare parts",
        "spare parts delay",
        "supplier delay",
        "intermittent behavior",
        "availability tracking",
        "contingency planning",
    )

    has_enriched_layer_signal = any(
        marker in normalized_context for marker in enriched_layer_markers
    )
    has_operational_escalation_signal = any(
        marker in normalized_context for marker in escalation_markers
    )

    return has_enriched_layer_signal and has_operational_escalation_signal


def _govern_priority_with_context(
    case: DecisionCase,
    payload: LiveGenerativePayload,
    e_recommendation: Recommendation,
) -> tuple[str, str]:
    """
    Apply a minimal governed priority policy for live generative path.

    Design intent:
        - grounded model path remains the immediate priority anchor.
        - F may preserve the anchor priority freely.
        - F may escalate by one level only when an explicit enriched-context
          escalation signal is present.
        - F may not de-escalate priority in this v1 governor.
        - Multi-level jumps are never allowed.
    """
    anchor_priority = e_recommendation.priority.strip()
    proposed_priority = payload.priority.strip()

    anchor_rank = _priority_rank(anchor_priority)
    proposed_rank = _priority_rank(proposed_priority)

    if proposed_rank == anchor_rank:
        return (
            proposed_priority,
            "Priority governance: preserved the grounded model path anchor priority.",
        )

    if proposed_rank < anchor_rank:
        return (
            anchor_priority,
            "Priority governance: preserved the grounded model path anchor priority "
            "because downward priority changes are not enabled in v1.",
        )

    if proposed_rank - anchor_rank > 1:
        return (
            anchor_priority,
            "Priority governance: preserved the grounded model path anchor priority "
            "because multi-level escalation is not allowed.",
        )

    if _detect_explicit_priority_escalation_signal(case.context_note):
        return (
            proposed_priority,
            "Priority governance: accepted a one-level escalation relative to "
            "grounded model path because an explicit enriched-context escalation signal "
            "was detected in the effective context note.",
        )

    return (
        anchor_priority,
        "Priority governance: preserved the grounded model path anchor priority because "
        "no explicit enriched-context escalation signal was detected.",
    )


def _build_response_trace_clause(response_id: str | None) -> str:
    """
    Build one optional trace clause for the validated F rationale.

    Args:
        response_id: Optional provider response identifier.

    Returns:
        str: Short trace clause that can be prefixed to the rationale.
    """
    if response_id is None:
        return ""

    return f" model response id: {response_id}."


def _build_validated_live_generative_recommendation(
    case: DecisionCase,
    payload: LiveGenerativePayload,
    e_recommendation: Recommendation,
    *,
    response_id: str | None,
) -> Recommendation:
    """
    Build the final validated Recommendation for a successful F execution.

    Args:
        case: Decision case being processed.
        payload: Validated structured payload returned by the model.
        e_recommendation: Immediate grounded anchor recommendation from E.
        response_id: Optional provider response identifier.

    Returns:
        Recommendation: Final repository recommendation for live generative path.
    """
    governed_priority, priority_governance_clause = _govern_priority_with_context(
        case,
        payload,
        e_recommendation,
    )

    rationale = (
        "live generative path produced a validated second-pass deliberative recommendation "
        "anchored to grounded model path."
        f"{_build_response_trace_clause(response_id)} "
        f"{priority_governance_clause} "
        f"{payload.rationale.strip()}"
    )

    return Recommendation(
        recommendation_id=build_recommendation_id("F", case),
        asset_id=case.alert.asset_id,
        action=payload.action.strip(),
        rationale=rationale.strip(),
        priority=governed_priority,
    )


def _build_fallback_recommendation(
    case: DecisionCase,
    e_recommendation: Recommendation,
    *,
    failure_reason: str,
) -> Recommendation:
    """
    Build the safe fallback Recommendation derived from grounded model path.

    Args:
        case: Decision case being processed.
        e_recommendation: Immediate anchor recommendation from grounded model path.
        failure_reason: Readable reason for fallback activation.

    Returns:
        Recommendation: Bounded fallback recommendation labeled as live generative path.
    """
    rationale = (
        "live generative path fell back to the grounded model path because the "
        "second-pass deliberative step could not be executed or validated safely. "
        f"Reason: {failure_reason} "
        f"Original grounded model path rationale: {e_recommendation.rationale}"
    )

    return Recommendation(
        recommendation_id=build_recommendation_id("F", case),
        asset_id=case.alert.asset_id,
        action=e_recommendation.action,
        rationale=rationale,
        priority=e_recommendation.priority,
    )


def run_live_generative_path(case: DecisionCase) -> Recommendation:
    """
    Execute the first real second-pass deliberative condition of the rebuild.

    Execution shape:
        1. validate the incoming decision case
        2. execute deterministic anchor as deterministic backbone
        3. execute model-backed anchor as earlier model-backed anchor
        4. execute grounded model path as immediate grounded anchor
        5. optionally retrieve the same bounded documentary evidence context
        6. build one second-pass deliberative prompt
        7. perform one model call
        8. parse and validate the structured payload
        9. return a comparable Recommendation
        10. if the second-pass execution or validation fails, return a safe
            fallback derived from E

    Important boundary:
        This function introduces the first real second-pass deliberative step,
        but it does not implement broad agentic orchestration, recursive
        reflection loops, or mature autonomy claims.
    """
    validate_decision_case(case)
    c_recommendation = run_deterministic_anchor(case)
    d_recommendation = run_model_backed_anchor(case)
    e_recommendation = run_grounded_model_path(case)

    try:
        try:
            evidence_bundle: EvidenceBundle | None = retrieve_maintenance_guidance_bundle(
                max_snippets=DEFAULT_MAX_EVIDENCE_SNIPPETS
            )
        except (RetrievalError, EvidenceBundleError, ValueError):
            evidence_bundle = None

        model_result = generate_text_response(
            instructions=_build_live_generative_path_instructions(evidence_bundle),
            input_text=_build_live_generative_path_input_text(
                case,
                c_recommendation,
                d_recommendation,
                e_recommendation,
                evidence_bundle,
            ),
        )

        payload = parse_live_generative_payload(model_result.output_text)
        _validate_bounded_alignment(case, payload, e_recommendation)
        _validate_deliberative_use(payload)

        return _build_validated_live_generative_recommendation(
            case,
            payload,
            e_recommendation,
            response_id=model_result.response_id,
        )

    except (
        ConfigurationError,
        OpenAIExecutionError,
        LiveGenerativePayloadError,
        ValueError,
    ) as exc:
        return _build_fallback_recommendation(
            case,
            e_recommendation,
            failure_reason=str(exc),
        )

