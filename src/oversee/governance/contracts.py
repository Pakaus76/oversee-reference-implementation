"""Shared execution contracts for OVERSEgrounded model path recommendation paths."""

from __future__ import annotations

import re
from typing import Protocol

from oversee.domain import DecisionCase, Recommendation


class RecommendationPathExecutor(Protocol):
    """Callable contract for OVERSEgrounded model path recommendation paths."""

    def __call__(self, decision_case: DecisionCase) -> Recommendation:
        """Execute one OVERSEgrounded model path recommendation path."""


def _normalize_path_label(path_label: str) -> str:
    """Normalize legacy and current labels to public OVERSEE output labels."""

    normalized = str(path_label).strip().lower()

    label_map = {
        "c": "det_anchor",
        
        "deterministic_anchor": "det_anchor",
        "det_anchor": "det_anchor",
        "d": "model_anchor",
        
        "model_backed_anchor": "model_anchor",
        "model_anchor": "model_anchor",
        "e": "grounded_model",
        
        "grounded_model_path": "grounded_model",
        "grounded_model": "grounded_model",
        "f": "live_gen",
        
        "live_generative_path": "live_gen",
        "live_gen": "live_gen",
    }

    if normalized in label_map:
        return label_map[normalized]

    cleaned = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")
    return cleaned or "oversee_path"


def build_recommendation_id(path_label: str, decision_case: object) -> str:
    """
    Build a public-facing recommendation identifier for an OVERSEE path.

    The second argument may be either a case identifier string or an object with
    a ``case_id`` attribute.
    """

    public_label = _normalize_path_label(path_label)

    if hasattr(decision_case, "case_id"):
        public_case_id = str(decision_case.case_id)
    else:
        public_case_id = str(decision_case)

    return f"{public_label}_{public_case_id}"

