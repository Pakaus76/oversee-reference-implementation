"""Layer 2 contextualization rules for the OVERSEE workbench.

Purpose:
    Transform validated evidence and canonical case context into a contextual
    decision profile.

Architectural role:
    Layer 2 applies DMN-like contextualization rules. It does not call external
    enterprise APIs directly in the current reference implementation; it
    consumes the evidence and canonical context prepared after Layer 1.

Main output:
    02_output_layer2_contextualization_result.json
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from oversee.case_context import CanonicalCaseContext


@dataclass(slots=True)
class ContextualizationRuleResult:
    """One DMN-like contextualization rule evaluation.
    
    Each instance records the rule name, the evaluated condition, whether it was
    triggered and the output facts produced for the contextual decision profile.
    """

    rule_id: str
    rule_name: str
    condition: str
    triggered: bool
    output_field: str
    output_value: Any
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class Layer2ContextualizationResult:
    """Complete Layer 2 contextualization result.
    
    The result contains the contextualization rule trace, the derived context and
    decision-readiness indicators consumed by the next layers.
    """

    case_id: str
    asset_id: str
    canonical_context: dict[str, Any]
    rule_trace: list[ContextualizationRuleResult]
    derived_context: dict[str, Any]
    layer2_ready: bool

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "case_id": self.case_id,
            "asset_id": self.asset_id,
            "canonical_context": self.canonical_context,
            "rule_trace": [rule.to_dict() for rule in self.rule_trace],
            "derived_context": self.derived_context,
            "layer2_ready": self.layer2_ready,
        }

#6.0 >-------------------------------------------------------------------------------------------------------------------------------

def run_layer2_contextualization(
    canonical_context: CanonicalCaseContext,
) -> Layer2ContextualizationResult:
    """Apply DMN-like contextualization rules to a canonical context.
    
    The function is the public Layer 2 entry point. It evaluates the contextual
    rules and returns the contextualized decision profile used by Layer 3 and Layer
    4.
    """

    rule_trace = apply_contextualization_rules(canonical_context)
    derived_context = _build_derived_context(rule_trace)

    return Layer2ContextualizationResult(
        case_id=canonical_context.case_id,
        asset_id=canonical_context.asset.asset_id,
        canonical_context=canonical_context.to_dict(),
        rule_trace=rule_trace,
        derived_context=derived_context,
        layer2_ready=bool(derived_context.get("layer2_decision_ready", False)),
    )

#6.1 >-------------------------------------------------------------------------------------------------------------------------------

def apply_contextualization_rules(
    canonical_context: CanonicalCaseContext,
) -> list[ContextualizationRuleResult]:
    """Apply explicit if-then contextualization rules.
    
    The rule set converts operational facts such as urgency, feasibility,
    production pressure, resource availability and evidence quality into a compact
    derived context.
    """

    asset = canonical_context.asset
    predictive = canonical_context.predictive_evidence
    operational = canonical_context.operational_context
    maintenance = canonical_context.maintenance_resources
    governance = canonical_context.governance_policy

    return [
        _rule(
            rule_id="L2_R001",
            rule_name="Technical urgency from failure horizon",
            condition=(
                "IF estimated_time_to_failure_hours <= 72 "
                "THEN technical_urgency = high"
            ),
            triggered=predictive.estimated_time_to_failure_hours <= 72,
            output_field="technical_urgency",
            output_value=(
                "high"
                if predictive.estimated_time_to_failure_hours <= 72
                else "medium"
            ),
            rationale="Short failure horizon increases technical urgency.",
        ),
        _rule(
            rule_id="L2_R002",
            rule_name="Asset escalation from criticality",
            condition="IF criticality_score >= 5 THEN asset_escalation = required",
            triggered=asset.criticality_score >= 5,
            output_field="asset_escalation",
            output_value="required" if asset.criticality_score >= 5 else "not_required",
            rationale="High-criticality assets require explicit escalation.",
        ),
        _rule(
            rule_id="L2_R003",
            rule_name="Operational constraint from production pressure",
            condition="IF production_pressure = high THEN operational_constraint = high",
            triggered=operational.production_pressure == "high",
            output_field="operational_constraint",
            output_value=(
                "high"
                if operational.production_pressure == "high"
                else "medium"
            ),
            rationale="High production pressure constrains maintenance timing.",
        ),
        _rule(
            rule_id="L2_R004",
            rule_name="Downtime window proximity",
            condition=(
                "IF next_planned_downtime_hours <= 48 "
                "THEN downtime_window = near"
            ),
            triggered=operational.next_planned_downtime_hours <= 48,
            output_field="downtime_window",
            output_value=(
                "near"
                if operational.next_planned_downtime_hours <= 48
                else "distant"
            ),
            rationale="A near downtime window creates a feasible planning opportunity.",
        ),
        _rule(
            rule_id="L2_R005",
            rule_name="Intervention feasibility from resources",
            condition=(
                "IF spare_part_available = true AND "
                "specialist_technician_available_next_shift = true "
                "THEN intervention_feasible = true"
            ),
            triggered=maintenance.intervention_feasible,
            output_field="intervention_feasible",
            output_value=maintenance.intervention_feasible,
            rationale="Available spare parts and specialist capacity make intervention feasible.",
        ),
        _rule(
            rule_id="L2_R006",
            rule_name="Recurrence risk from repeated failures",
            condition="IF recent_repeated_failures = true THEN recurrence_risk = high",
            triggered="recent_repeated_failures" in canonical_context.key_risk_drivers,
            output_field="recurrence_risk",
            output_value=(
                "high"
                if "recent_repeated_failures" in canonical_context.key_risk_drivers
                else "normal"
            ),
            rationale="Recent repeated failures increase recurrence risk.",
        ),
        _rule(
            rule_id="L2_R007",
            rule_name="Human review requirement from governance policy",
            condition=(
                "IF high criticality policy applies "
                "THEN human_review_required = true"
            ),
            triggered=governance.computed_human_review_required,
            output_field="human_review_required",
            output_value=governance.computed_human_review_required,
            rationale="Governance policy requires accountable human review.",
        ),
        _rule(
            rule_id="L2_R008",
            rule_name="Layer 2 decision readiness",
            condition=(
                "IF technical urgency, feasibility and governance context exist "
                "THEN layer2_decision_ready = true"
            ),
            triggered=True,
            output_field="layer2_decision_ready",
            output_value=True,
            rationale=(
                "Layer 2 has enough contextualized evidence for downstream "
                "case lifecycle and decision logic."
            ),
        ),
    ]


def contextualization_rules_to_dicts(
    results: list[ContextualizationRuleResult],
) -> list[dict[str, Any]]:
    """Convert rule results to dictionaries."""

    return [result.to_dict() for result in results]


def _build_derived_context(
    rule_trace: list[ContextualizationRuleResult],
) -> dict[str, Any]:
    """Build a compact derived context from rule outputs."""

    return {rule.output_field: rule.output_value for rule in rule_trace}


def _rule(
    *,
    rule_id: str,
    rule_name: str,
    condition: str,
    triggered: bool,
    output_field: str,
    output_value: Any,
    rationale: str,
) -> ContextualizationRuleResult:
    """Create one contextualization rule result."""

    return ContextualizationRuleResult(
        rule_id=rule_id,
        rule_name=rule_name,
        condition=condition,
        triggered=triggered,
        output_field=output_field,
        output_value=output_value,
        rationale=rationale,
    )
