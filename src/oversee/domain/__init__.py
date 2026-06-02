"""
Module: __init__.py

Purpose:
    Expose the core domain entities, contracts, and reusable semantic elements
    of the rebuilt system.

Architectural role:
    This module defines the public import surface of the domain package so that
    later layers can depend on stable domain structures.

Thesis traceability:
    - Chapter 5: Artefact structure and conceptual core
    - Chapter 6: Software artefacts and evaluation structure
    - Chapter 7: Technical implementation baseline
    - Chapter 8: Controlled evaluation inputs and outputs

Inputs:
    This module does not consume runtime inputs directly.

Outputs:
    Re-exported domain classes, enums, and validators for convenient imports.

Key assumptions:
    The domain layer must remain simple, explicit, and free from higher-level
    execution logic.

Dependencies:
    Internal domain modules only.

Notes:
    This package is created before substantive DO logic so that later layers
    depend on stable contracts rather than informal dictionaries.
"""

from .asset import Asset
from .decision_case import DecisionCase
from .enums import ConfidenceLevel, PriorityLevel, RiskLevel
from .intervention import InterventionRequest
from .predictive_alert import PredictiveAlert
from .recommendation import Recommendation
from .validators import validate_asset_alert_alignment, validate_decision_case

__all__ = [
    "Asset",
    "PredictiveAlert",
    "Recommendation",
    "InterventionRequest",
    "DecisionCase",
    "PriorityLevel",
    "RiskLevel",
    "ConfidenceLevel",
    "validate_asset_alert_alignment",
    "validate_decision_case",
]

