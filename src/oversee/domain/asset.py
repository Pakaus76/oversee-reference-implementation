"""
Module: asset.py

Purpose:
    Define the core asset entity used across the rebuilt system.

Architectural role:
    This module provides a stable typed representation of an asset so that
    ingestion, benchmark generation, DO conditions, and evaluation layers can
    all refer to the same semantic structure.

Thesis traceability:
    - Chapter 5: Decision context centred on asset condition and operational relevance
    - Chapter 6: Core artefact inputs and evaluation context
    - Chapter 7: Data model and implementation baseline
    - Chapter 8: Controlled evaluation substrate

Inputs:
    Typed asset attributes provided by validated upstream layers.

Outputs:
    Asset instances that can be consumed by downstream layers.

Key assumptions:
    This initial version keeps the asset representation intentionally compact.
    Additional attributes may be introduced later only when they are needed and
    documented.

Dependencies:
    dataclasses
    typing

Notes:
    The asset entity is part of the semantic backbone of the rebuild and should
    remain free from execution logic.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Asset:
    """
    Represent a physical asset in the rebuilt system.

    Args:
        asset_id: Unique identifier of the asset.
        asset_type: Broad asset category used for contextual interpretation.
        criticality: Integer criticality level used by later decision layers.
        location: Optional location or plant area label.

    Returns:
        Asset: Typed asset instance.

    Side effects:
        None.

    Raises:
        ValueError: If asset_id is empty or criticality is negative.
    """

    asset_id: str
    asset_type: str
    criticality: int
    location: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the minimum integrity of the asset entity."""
        if not self.asset_id.strip():
            raise ValueError("asset_id must not be empty.")
        if self.criticality < 0:
            raise ValueError("criticality must be zero or positive.")

