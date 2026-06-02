"""
Module: enums.py

Purpose:
    Define reusable domain enumerations for the rebuilt system.

Architectural role:
    This module provides controlled label sets so that later layers do not rely
    on free-text values for key semantic fields such as priority, risk, and
    confidence.

Thesis traceability:
    - Chapter 5: Decision structure and explicit recommendation semantics
    - Chapter 6: Controlled artefact comparison and evaluation discipline
    - Chapter 7: Technical implementation baseline
    - Chapter 8: Consistent comparative outputs across conditions

Inputs:
    This module does not consume runtime inputs directly.

Outputs:
    Reusable string-based enumerations for downstream domain and evaluation
    layers.

Key assumptions:
    The initial enumeration set must remain compact and generic.
    New enumerations should only be introduced when they support an explicit
    implementation need.

Dependencies:
    enum

Notes:
    These enumerations exist to reduce semantic drift across the rebuild.
"""

from enum import StrEnum


class PriorityLevel(StrEnum):
    """
    Represent the urgency level of a recommendation or intervention.

    The enum is intentionally compact in the early rebuild stage.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(StrEnum):
    """
    Represent the assessed risk level associated with an asset situation.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConfidenceLevel(StrEnum):
    """
    Represent the confidence level attached to an assessment or recommendation.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

