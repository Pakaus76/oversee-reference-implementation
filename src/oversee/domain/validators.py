"""
Module: validators.py

Purpose:
    Provide lightweight reusable validation helpers for the domain layer.

Architectural role:
    This module centralizes simple semantic validation checks so that later
    layers can reuse consistent domain-level validation rules without embedding
    them ad hoc across the repository.

Thesis traceability:
    - Chapter 5: Explicit and governable handling of decision-related inputs
    - Chapter 6: Cleaner artefact discipline and validation consistency
    - Chapter 7: Early implementation support layer
    - Chapter 8: More stable comparative input integrity

Inputs:
    Typed domain entities created by the domain layer.

Outputs:
    Boolean or exception-based validation outcomes.

Key assumptions:
    This first version must remain lightweight and generic.
    It should validate semantic integrity, not implement decision logic.

Dependencies:
    internal domain modules

Notes:
    These helpers complement dataclass-level validation and may later support
    ingestion, benchmark construction, and controlled case preparation.
"""

from .asset import Asset
from .decision_case import DecisionCase
from .predictive_alert import PredictiveAlert


def validate_asset_alert_alignment(asset: Asset, alert: PredictiveAlert) -> None:
    """
    Validate that an alert refers to the provided asset.

    Args:
        asset: Asset entity expected to match the alert target.
        alert: Predictive alert associated with the asset.

    Returns:
        None

    Side effects:
        None.

    Raises:
        ValueError: If the alert does not refer to the provided asset.
    """
    if asset.asset_id != alert.asset_id:
        raise ValueError(
            "Asset and alert are not aligned: asset.asset_id must match alert.asset_id."
        )


def validate_decision_case(case: DecisionCase) -> None:
    """
    Validate the semantic integrity of a decision case.

    Args:
        case: DecisionCase instance to validate.

    Returns:
        None

    Side effects:
        None.

    Raises:
        ValueError: If the internal asset-alert relationship is inconsistent.
    """
    validate_asset_alert_alignment(case.asset, case.alert)

