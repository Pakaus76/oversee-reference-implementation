"""
Module: decision_case.py

Purpose:
    Define an aggregated decision-case contract for the rebuilt system.

Architectural role:
    This module groups the minimum contextual elements of a maintenance-related
    decision situation so that later layers can operate on one explicit case
    object instead of passing disconnected pieces of data.

Thesis traceability:
    - Chapter 5: Decision context and artefact input framing
    - Chapter 6: Controlled case-based evaluation structure
    - Chapter 7: Technical implementation baseline
    - Chapter 8: Comparable experimental case handling

Inputs:
    Typed domain entities representing the asset and predictive evidence.

Outputs:
    DecisionCase instances ready for later benchmark, condition, governance,
    and evaluation layers.

Key assumptions:
    This initial version is intentionally compact.
    Additional contextual fields should only be added when required by later
    documented implementation needs.

Dependencies:
    dataclasses
    typing
    internal domain modules

Notes:
    This contract represents a decision situation, not a final recommendation.
"""

from dataclasses import dataclass
from typing import Optional

from .asset import Asset
from .predictive_alert import PredictiveAlert


@dataclass(slots=True)
class DecisionCase:
    """
    Represent the minimum context of a decision situation.

    Args:
        case_id: Unique identifier of the decision case.
        asset: Typed asset involved in the case.
        alert: Predictive alert associated with the case.
        context_note: Optional short note with additional case context.

    Returns:
        DecisionCase: Typed aggregated decision-case instance.

    Side effects:
        None.

    Raises:
        ValueError: If case_id is empty.
    """

    case_id: str
    asset: Asset
    alert: PredictiveAlert
    context_note: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the minimum integrity of the decision case."""
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty.")

