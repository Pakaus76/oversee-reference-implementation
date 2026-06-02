"""
Module: deterministic_anchor.py

Purpose:
    Define the first compact deterministic C-condition implementation of the
    rebuild.

Architectural role:
    This module provides the first structured deterministic condition of the
    A-B-C progression. It keeps the compact signal family already used in A and
    B, but organizes those signals through explicit decision functions rather
    than through a purely sequential modulation flow.

Thesis traceability:
    - Chapter 5: Progression toward a more structured deterministic policy layer
    - Chapter 6: Controlled artefact progression across comparable conditions
    - Chapter 7: First structured condition-layer implementation beyond B
    - Chapter 8: Future cross-deterministic anchoromparison across A, B, and C

Inputs:
    DecisionCase objects containing one validated asset and one predictive alert.

Outputs:
    Recommendation objects representing the deterministic output of deterministic anchor.

Key assumptions:
    deterministic anchor must remain deterministic, explicit, inspectable, and
    non-generative at its first implementation stage.
    The same compact signal family used in A and B should be preserved:
    - time to failure
    - asset criticality
    - alert confidence score
    The policy should expose named decision functions and one explicit
    deterministic consolidation rule.

Dependencies:
    Internal domain contracts
    Shared deterministic anchorontracts

Notes:
    Policy summary of deterministic anchor at the current rebuild stage:
    - derive baseline urgency from time to failure
    - derive operational importance from asset criticality
    - derive evidence reliability from alert confidence
    - consolidate those assessments through one deterministic rule
    - keep the implementation compact and non-generative
"""

from ..domain import DecisionCase, PriorityLevel, Recommendation, validate_decision_case
from .contracts import build_recommendation_id

HIGH_CRITICALITY_THRESHOLD = 4
LOW_CONFIDENCE_THRESHOLD = 0.40
PROTECTED_NEAR_FAILURE_HOURS = 24.0


def _increase_priority(priority: str) -> str:
    """
    Increase one priority level while preserving the upper bound.

    Args:
        priority: Current priority label.

    Returns:
        str: Increased priority label, or the original one if already high.

    Side effects:
        None.

    Notes:
        This helper keeps the consolidation rule explicit and bounded so that
        deterministic anchor remains easy to audit and compare with A and B.
    """
    if priority == PriorityLevel.LOW.value:
        return PriorityLevel.MEDIUM.value

    if priority == PriorityLevel.MEDIUM.value:
        return PriorityLevel.HIGH.value

    return PriorityLevel.HIGH.value


def _decrease_priority(priority: str) -> str:
    """
    Decrease one priority level while preserving the lower bound.

    Args:
        priority: Current priority label.

    Returns:
        str: Decreased priority label, or the original one if already low.

    Side effects:
        None.

    Notes:
        This helper applies the cautious reduction rule defined for low
        evidence-reliability cases in the first implementation of C.
    """
    if priority == PriorityLevel.HIGH.value:
        return PriorityLevel.MEDIUM.value

    if priority == PriorityLevel.MEDIUM.value:
        return PriorityLevel.LOW.value

    return PriorityLevel.LOW.value


def _assess_baseline_urgency(decision_case: DecisionCase) -> str:
    """
    Derive the baseline urgency assessment from time to failure.

    Args:
        decision_case: Decision situation to assess.

    Returns:
        str: Baseline urgency label.

    Side effects:
        None.

    Notes:
        This assessment intentionally preserves the same baseline urgency anchor
        already established in A and reused conceptually in B.
    """
    time_to_failure_hours = decision_case.alert.time_to_failure_hours

    if time_to_failure_hours is None:
        return PriorityLevel.MEDIUM.value

    if time_to_failure_hours <= PROTECTED_NEAR_FAILURE_HOURS:
        return PriorityLevel.HIGH.value

    if time_to_failure_hours <= 72.0:
        return PriorityLevel.MEDIUM.value

    return PriorityLevel.LOW.value


def _assess_operational_importance(decision_case: DecisionCase) -> str:
    """
    Derive the operational importance assessment from asset criticality.

    Args:
        decision_case: Decision situation to assess.

    Returns:
        str: Operational importance label.

    Side effects:
        None.

    Notes:
        deterministic anchor makes operational importance explicit as its own assessment
        instead of leaving criticality only as an implicit modulation signal.
    """
    if decision_case.asset.criticality >= HIGH_CRITICALITY_THRESHOLD:
        return "high"

    return "standard"


def _assess_evidence_reliability(decision_case: DecisionCase) -> str:
    """
    Derive the evidence reliability assessment from alert confidence.

    Args:
        decision_case: Decision situation to assess.

    Returns:
        str: Evidence reliability label.

    Side effects:
        None.

    Notes:
        deterministic anchor exposes evidence reliability explicitly so that the final
        rationale can describe not only the final result but also the quality of
        the supporting predictive evidence.
    """
    confidence_score = decision_case.alert.confidence_score

    if confidence_score is not None and confidence_score < LOW_CONFIDENCE_THRESHOLD:
        return "low"

    return "acceptable"


def _consolidate_priority(
    baseline_urgency: str,
    operational_importance: str,
    evidence_reliability: str,
    *,
    protected_near_failure_case: bool,
) -> str:
    """
    Consolidate the C-condition assessments into one final priority.

    Args:
        baseline_urgency: Baseline urgency assessment derived from time to failure.
        operational_importance: Operational importance assessment derived from
            asset criticality.
        evidence_reliability: Evidence reliability assessment derived from alert
            confidence.
        protected_near_failure_case: Whether the case is protected from
            confidence-only reduction because it is near failure.

    Returns:
        str: Final consolidated priority.

    Side effects:
        None.

    Notes:
        This is the key structured step of deterministic anchor. It keeps the policy
        deterministic while making the named assessments explicit.
    """
    consolidated_priority = baseline_urgency

    if operational_importance == "high":
        consolidated_priority = _increase_priority(consolidated_priority)

    if evidence_reliability == "low" and not protected_near_failure_case:
        consolidated_priority = _decrease_priority(consolidated_priority)

    return consolidated_priority


def _select_action_from_priority(priority: str) -> str:
    """
    Select the operational action text associated with the final priority.

    Args:
        priority: Final priority label after C-deterministic anchoronsolidation.

    Returns:
        str: Recommendation action aligned with the final priority.

    Side effects:
        None.

    Notes:
        The first implementation of C keeps the action vocabulary compact and
        aligned with the early rebuild stage.
    """
    if priority == PriorityLevel.HIGH.value:
        return "Plan immediate inspection and maintenance preparation."

    if priority == PriorityLevel.MEDIUM.value:
        return "Schedule near-term inspection and maintenance review."

    return "Monitor the asset and review the next maintenance window."


def run_deterministic_anchor(decision_case: DecisionCase) -> Recommendation:
    """
    Produce the first structured deterministic recommendation of deterministic anchor.

    Args:
        decision_case: Typed decision situation to be processed by the C
            condition.

    Returns:
        Recommendation: Structured deterministic recommendation.

    Side effects:
        None.

    Raises:
        ValueError: Propagated if the decision case is semantically invalid or
            if the final Recommendation contract receives invalid data.

    Notes:
        deterministic anchor differs from B by exposing explicit decision functions:
        - baseline urgency
        - operational importance
        - evidence reliability

        It then consolidates those assessments through one deterministic rule
        instead of relying only on a compact sequential modulation narrative.
    """
    # Preserve semantic integrity explicitly before performing any condition
    # logic so that the structured assessments of C operate on coherent input.
    validate_decision_case(decision_case)

    baseline_urgency = _assess_baseline_urgency(decision_case)
    operational_importance = _assess_operational_importance(decision_case)
    evidence_reliability = _assess_evidence_reliability(decision_case)

    time_to_failure_hours = decision_case.alert.time_to_failure_hours
    confidence_score = decision_case.alert.confidence_score

    protected_near_failure_case = (
        time_to_failure_hours is not None
        and time_to_failure_hours <= PROTECTED_NEAR_FAILURE_HOURS
    )

    final_priority = _consolidate_priority(
        baseline_urgency,
        operational_importance,
        evidence_reliability,
        protected_near_failure_case=protected_near_failure_case,
    )

    action = _select_action_from_priority(final_priority)

    rationale_parts: list[str] = [
        f"deterministic anchor baseline urgency assessment: '{baseline_urgency}'.",
        f"deterministic anchor operational importance assessment: '{operational_importance}'.",
        f"deterministic anchor evidence reliability assessment: '{evidence_reliability}'.",
    ]

    if evidence_reliability == "low" and protected_near_failure_case:
        rationale_parts.append(
            "The case remained protected from confidence-based reduction because it is a near-failure case."
        )

    if confidence_score is not None and evidence_reliability == "low":
        rationale_parts.append(
            f"Confidence score {confidence_score:.2f} was treated as low evidence reliability."
        )

    rationale_parts.append(
        f"deterministic anchor final consolidated priority: '{final_priority}'."
    )

    return Recommendation(
        recommendation_id=build_recommendation_id("c", decision_case),
        asset_id=decision_case.alert.asset_id,
        action=action,
        rationale=" ".join(rationale_parts),
        priority=final_priority,
    )


