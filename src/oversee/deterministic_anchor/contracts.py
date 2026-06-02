"""
Module: contracts.py

Purpose:
    Define the minimal shared execution discipline of the condition layer.

Architectural role:
    This module provides a lightweight common contract for recommendation path execution
    so that later conditions reuse the same input-output shape and
    recommendation-identifier discipline instead of drifting into ad hoc forms.

Thesis traceability:
    - Chapter 5: More explicit condition-layer discipline
    - Chapter 6: Better controlled artefact progression
    - Chapter 7: Stronger shared implementation baseline for conditions
    - Chapter 8: Better future cross-deterministic anchoromparability

Inputs:
    DecisionCase objects and condition labels.

Outputs:
    A shared condition-executor protocol and normalized recommendation IDs.

Key assumptions:
    This module must remain intentionally lightweight.
    It must not introduce governance logic, evaluation runners, or generative
    behavior.

Dependencies:
    re
    typing
    internal domain contracts only

Notes:
    This is a shared condition-layer discipline artifact, not a condition
    implementation by itself.
"""

import re
from typing import Protocol

from ..domain import DecisionCase, Recommendation


class ConditionExecutor(Protocol):
    """
    Represent the minimal callable shape expected from a condition module.
    """

    def __call__(self, decision_case: DecisionCase) -> Recommendation:
        """
        Execute one condition on one decision case.

        Args:
            decision_case: Typed decision situation to process.

        Returns:
            Recommendation: Typed recommendation output.
        """


def _normalize_condition_label(condition_label: str) -> str:
    """
    Normalize one condition label for identifier construction.

    Args:
        condition_label: Raw condition label.

    Returns:
        str: Normalized condition label.

    Side effects:
        None.

    Raises:
        ValueError: If the normalized label becomes empty.
    """
    normalized = condition_label.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = normalized.strip("_")

    if not normalized:
        raise ValueError("condition_label must not be empty after normalization.")

    return normalized


def build_recommendation_id(anchor_label: str, case_id: object) -> str:
    """
    Build a public-facing recommendation identifier for the deterministic anchor.

    Path labels are normalized to public OVERSEE recommendation identifiers
    so reviewer-facing outputs do not expose old internal experiment names.

    The second argument may be either a case identifier string or an object with
    a ``case_id`` attribute. This keeps the migrated logic compatible with the
    original call pattern while exposing clean OVERSEE output identifiers.
    """

    normalized_label = str(anchor_label).strip().lower()

    if normalized_label in {"c", "deterministic_anchor", "det_anchor"}:
        public_label = "det_anchor"
    else:
        public_label = normalized_label.replace(" ", "_").replace("-", "_")

    if hasattr(case_id, "case_id"):
        public_case_id = str(case_id.case_id)
    else:
        public_case_id = str(case_id)

    return f"{public_label}_{public_case_id}"




