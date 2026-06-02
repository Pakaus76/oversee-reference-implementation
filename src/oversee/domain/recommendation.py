"""
Module: recommendation.py

Purpose:
    Define the recommendation contract that later DO conditions will produce.

Architectural role:
    This module provides a simple, typed decision-output contract that can be
    compared across conditions during controlled evaluation.

Thesis traceability:
    - Chapter 5: Decision recommendation and explanation logic
    - Chapter 6: Comparative artefact evaluation
    - Chapter 7: Implementation baseline for decision outputs
    - Chapter 8: Cross-deterministic anchoromparison

Inputs:
    Recommendation attributes created by later decision logic.

Outputs:
    Recommendation instances ready for governance, evaluation, or reporting.

Key assumptions:
    The initial contract is deliberately compact so that it remains stable while
    the workbench is still being constructed.

Dependencies:
    dataclasses

Notes:
    This initial version should be treated as a baseline contract, not as the
    final governed generative output schema.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Recommendation:
    """
    Represent a high-level recommendation produced by a DO condition.

    Args:
        recommendation_id: Unique identifier of the recommendation.
        asset_id: Identifier of the affected asset.
        action: Recommended action in plain English.
        rationale: Short justification for the recommendation.
        priority: Priority label used for controlled comparison.

    Returns:
        Recommendation: Typed recommendation instance.

    Side effects:
        None.

    Raises:
        ValueError: If identifiers or required textual fields are empty.
    """

    recommendation_id: str
    asset_id: str
    action: str
    rationale: str
    priority: str

    def __post_init__(self) -> None:
        """Validate the minimum integrity of the recommendation contract."""
        if not self.recommendation_id.strip():
            raise ValueError("recommendation_id must not be empty.")
        if not self.asset_id.strip():
            raise ValueError("asset_id must not be empty.")
        if not self.action.strip():
            raise ValueError("action must not be empty.")
        if not self.rationale.strip():
            raise ValueError("rationale must not be empty.")
        if not self.priority.strip():
            raise ValueError("priority must not be empty.")

