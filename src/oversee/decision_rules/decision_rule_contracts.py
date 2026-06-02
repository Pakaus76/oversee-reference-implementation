"""Contracts for OVERSEE Layer 4 decision rules and recommendation paths."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class RuleEvaluation:
    """One explicit DMN-like rule evaluation."""

    rule_id: str
    rule_name: str
    decision_table: str
    status: str
    input_fields: dict[str, Any]
    output_fields: dict[str, Any]
    triggered: bool
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class DecisionRuleEvaluation:
    """Layer 4 decision-rule evaluation bundle."""

    evaluation_id: str
    case_id: str
    asset_id: str
    source_context_id: str
    source_case_state: str
    rules: list[RuleEvaluation]
    final_priority: str
    recommended_execution_mode: str
    human_review_required: bool
    intervention_feasible: bool
    decision_rule_version: str = "0.1.0"

    @property
    def triggered_rule_count(self) -> int:
        """Return the number of triggered rules."""

        return sum(1 for rule in self.rules if rule.triggered)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        data = asdict(self)
        data["triggered_rule_count"] = self.triggered_rule_count
        return data


@dataclass(slots=True)
class RecommendationPathOutput:
    """One recommendation path output."""

    path_name: str
    path_type: str
    status: str
    recommendation: dict[str, Any]
    input_refs: list[str] = field(default_factory=list)
    governance_refs: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class RecommendationPathBundle:
    """Layer 4 recommendation path bundle."""

    bundle_id: str
    case_id: str
    asset_id: str
    decision_rule_evaluation_id: str
    path_outputs: list[RecommendationPathOutput]
    bundle_version: str = "0.1.0"

    @property
    def path_count(self) -> int:
        """Return the number of recommendation path outputs."""

        return len(self.path_outputs)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        data = asdict(self)
        data["path_count"] = self.path_count
        return data
