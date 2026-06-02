"""
Module: predictive_alert.py

Purpose:
    Define the typed structure of a predictive alert produced or consumed by the
    rebuilt workbench.

Architectural role:
    This module captures the minimum predictive evidence that later conditions
    and governance layers will interpret.

Thesis traceability:
    - Chapter 5: Artefact decision context
    - Chapter 6: Evaluation cases and analytical evidence
    - Chapter 7: Data and implementation baseline
    - Chapter 8: Controlled comparative inputs

Inputs:
    Alert attributes originating from benchmark or validated ingestion layers.

Outputs:
    PredictiveAlert instances usable by decision-related layers.

Key assumptions:
    The initial alert model is intentionally minimal and can be extended later
    when the benchmark and evaluation design require more detail.

Dependencies:
    dataclasses
    typing

Notes:
    This module represents predictive evidence, not a decision.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class PredictiveAlert:
    """
    Represent a predictive maintenance alert.

    Args:
        alert_id: Unique identifier of the alert.
        asset_id: Identifier of the affected asset.
        predicted_issue: Short textual description of the predicted issue.
        time_to_failure_hours: Estimated time to failure in hours, when available.
        confidence_score: Optional numeric confidence estimate.

    Returns:
        PredictiveAlert: Typed predictive alert instance.

    Side effects:
        None.

    Raises:
        ValueError: If required identifiers are empty or if time_to_failure_hours
            is negative.
    """

    alert_id: str
    asset_id: str
    predicted_issue: str
    time_to_failure_hours: Optional[float] = None
    confidence_score: Optional[float] = None

    def __post_init__(self) -> None:
        """Validate the minimum integrity of the predictive alert."""
        if not self.alert_id.strip():
            raise ValueError("alert_id must not be empty.")
        if not self.asset_id.strip():
            raise ValueError("asset_id must not be empty.")
        if self.time_to_failure_hours is not None and self.time_to_failure_hours < 0:
            raise ValueError("time_to_failure_hours must be zero or positive.")

