"""
Deterministic compressor scenario generator for the Digital Factory.

This module creates a first small batch of synthetic industrial scenarios for
testing the OVERSEE. No generative AI call is made in this version.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from oversee.digital_factory.synthetic_case_schema import (
    AssetContext,
    ExpectedDecision,
    GenerationMetadata,
    MaintenanceContext,
    NarrativeContext,
    OperationalContext,
    PredictiveAlert,
    SensorEvidence,
    SyntheticDecisionCase,
    UncertaintyContext,
)


GENERATOR_NAME = "digital_factory_compressor_scenario_generator"
GENERATOR_VERSION = "0.1.0"
SCENARIO_FAMILY = "compressor_degradation_decision_posture"


def _base_asset_context() -> AssetContext:
    return AssetContext(
        asset_id="COMP-001",
        asset_type="compressor",
        criticality="high",
        location="Line A - utilities area",
        production_dependency="Feeds compressed air to a production-critical line.",
        maintenance_history_summary=(
            "Recurring vibration observations during the last month, "
            "with no completed corrective intervention yet."
        ),
    )


def build_controlled_monitoring_case() -> SyntheticDecisionCase:
    """Build a deterministic controlled-monitoring compressor case."""
    return SyntheticDecisionCase(
        case_id="DF_COMP_001_CONTROLLED_MONITORING",
        scenario_family=SCENARIO_FAMILY,
        asset_context=_base_asset_context(),
        sensor_evidence=SensorEvidence(
            vibration_mm_s=6.8,
            temperature_c=74.0,
            pressure_bar=7.1,
            current_draw_a=42.0,
            alarm_count_24h=2,
            signal_consistency="consistent",
        ),
        predictive_alert=PredictiveAlert(
            alert_type="early_degradation",
            predicted_failure_mode="bearing_wear",
            time_to_failure_hours=96,
            confidence_score=0.86,
            model_uncertainty="low",
            supporting_signals=["vibration_trend", "temperature_trend"],
        ),
        operational_context=OperationalContext(
            production_pressure="moderate",
            shift="day",
            demand_urgency="normal",
            downtime_window="available within 48 hours",
            line_dependency="high but manageable with planning",
            customer_impact="limited if intervention is planned",
        ),
        maintenance_context=MaintenanceContext(
            spare_part_status="available",
            spare_part_eta_hours=0,
            technician_available=True,
            maintenance_window_available=True,
            workaround_available=True,
            inspection_required=True,
        ),
        uncertainty_context=UncertaintyContext(
            data_quality="good",
            conflicting_evidence=False,
            diagnosis_clarity="clear",
            model_confidence_comment="Signals are consistent with early bearing degradation.",
        ),
        narrative_context=NarrativeContext(
            technician_note="The compressor is noisier than usual but remains stable.",
            supervisor_note="Production can tolerate a short planned inspection.",
            maintenance_log_excerpt="Previous observation recorded mild vibration increase.",
            shift_handover_note="Monitor vibration trend and prepare inspection work order.",
        ),
        expected_decision=ExpectedDecision(
            expected_decision_posture="controlled_monitoring",
            expected_review_focus="planned inspection and trend monitoring",
            expected_human_review_required=False,
            expectation_rationale=(
                "Risk is relevant but controlled: evidence is consistent, "
                "parts are available, and there is a feasible maintenance window."
            ),
        ),
        generation_metadata=GenerationMetadata(
            generator_name=GENERATOR_NAME,
            generator_version=GENERATOR_VERSION,
            generation_mode="deterministic",
            uses_generative_ai=False,
            scenario_family=SCENARIO_FAMILY,
            scenario_variant="controlled_monitoring",
        ),
    )


def build_constrained_execution_case() -> SyntheticDecisionCase:
    """Build a deterministic constrained-execution compressor case."""
    return SyntheticDecisionCase(
        case_id="DF_COMP_002_CONSTRAINED_EXECUTION",
        scenario_family=SCENARIO_FAMILY,
        asset_context=_base_asset_context(),
        sensor_evidence=SensorEvidence(
            vibration_mm_s=9.4,
            temperature_c=82.5,
            pressure_bar=6.6,
            current_draw_a=48.0,
            alarm_count_24h=7,
            signal_consistency="consistent",
        ),
        predictive_alert=PredictiveAlert(
            alert_type="accelerated_degradation",
            predicted_failure_mode="bearing_wear",
            time_to_failure_hours=24,
            confidence_score=0.88,
            model_uncertainty="low",
            supporting_signals=["vibration_spike", "temperature_increase", "alarm_frequency"],
        ),
        operational_context=OperationalContext(
            production_pressure="high",
            shift="night",
            demand_urgency="critical customer order",
            downtime_window="not available in the next 24 hours",
            line_dependency="critical",
            customer_impact="high if the line stops unexpectedly",
        ),
        maintenance_context=MaintenanceContext(
            spare_part_status="delayed",
            spare_part_eta_hours=48,
            technician_available=True,
            maintenance_window_available=False,
            workaround_available=False,
            inspection_required=True,
        ),
        uncertainty_context=UncertaintyContext(
            data_quality="good",
            conflicting_evidence=False,
            diagnosis_clarity="clear",
            model_confidence_comment="Signals support accelerated degradation, but execution is constrained.",
        ),
        narrative_context=NarrativeContext(
            technician_note="The compressor shows clear deterioration.",
            supervisor_note="Stopping the line now would affect a critical customer order.",
            maintenance_log_excerpt="Alarm frequency increased sharply during the last shift.",
            shift_handover_note="Escalate to operations and confirm spare part ETA.",
        ),
        expected_decision=ExpectedDecision(
            expected_decision_posture="constrained_execution",
            expected_review_focus="operational constraint and spare part risk",
            expected_human_review_required=True,
            expectation_rationale=(
                "Technical risk is high and evidence is clear, but execution is "
                "constrained by production pressure and delayed spare part availability."
            ),
        ),
        generation_metadata=GenerationMetadata(
            generator_name=GENERATOR_NAME,
            generator_version=GENERATOR_VERSION,
            generation_mode="deterministic",
            uses_generative_ai=False,
            scenario_family=SCENARIO_FAMILY,
            scenario_variant="constrained_execution",
        ),
    )


def build_diagnostic_review_case() -> SyntheticDecisionCase:
    """Build a deterministic diagnostic-review compressor case."""
    return SyntheticDecisionCase(
        case_id="DF_COMP_003_DIAGNOSTIC_REVIEW",
        scenario_family=SCENARIO_FAMILY,
        asset_context=_base_asset_context(),
        sensor_evidence=SensorEvidence(
            vibration_mm_s=8.1,
            temperature_c=70.0,
            pressure_bar=7.0,
            current_draw_a=40.5,
            alarm_count_24h=4,
            signal_consistency="conflicting",
        ),
        predictive_alert=PredictiveAlert(
            alert_type="possible_degradation",
            predicted_failure_mode="uncertain_rotating_component_issue",
            time_to_failure_hours=72,
            confidence_score=0.58,
            model_uncertainty="high",
            supporting_signals=["vibration_anomaly"],
        ),
        operational_context=OperationalContext(
            production_pressure="moderate",
            shift="day",
            demand_urgency="normal",
            downtime_window="available within 72 hours",
            line_dependency="high but not immediately critical",
            customer_impact="moderate if inspection is delayed",
        ),
        maintenance_context=MaintenanceContext(
            spare_part_status="unknown",
            spare_part_eta_hours=None,
            technician_available=True,
            maintenance_window_available=True,
            workaround_available=True,
            inspection_required=True,
        ),
        uncertainty_context=UncertaintyContext(
            data_quality="mixed",
            conflicting_evidence=True,
            diagnosis_clarity="uncertain",
            model_confidence_comment="Vibration is abnormal, but other signals do not confirm a clear pattern.",
        ),
        narrative_context=NarrativeContext(
            technician_note="The vibration reading looks abnormal, but supporting symptoms are weak.",
            supervisor_note="Do not rush into a full intervention without confirming the failure mode.",
            maintenance_log_excerpt="Previous similar event was caused by a sensor mounting issue.",
            shift_handover_note="Validate sensor condition and repeat measurement.",
        ),
        expected_decision=ExpectedDecision(
            expected_decision_posture="diagnostic_review",
            expected_review_focus="diagnostic uncertainty and evidence validation",
            expected_human_review_required=True,
            expectation_rationale=(
                "The alert is relevant, but evidence is conflicting and confidence is lower. "
                "A diagnostic review should precede execution."
            ),
        ),
        generation_metadata=GenerationMetadata(
            generator_name=GENERATOR_NAME,
            generator_version=GENERATOR_VERSION,
            generation_mode="deterministic",
            uses_generative_ai=False,
            scenario_family=SCENARIO_FAMILY,
            scenario_variant="diagnostic_review",
        ),
    )


def generate_compressor_scenarios() -> list[SyntheticDecisionCase]:
    """Generate the first deterministic compressor scenario batch."""
    return [
        build_controlled_monitoring_case(),
        build_constrained_execution_case(),
        build_diagnostic_review_case(),
    ]


def write_scenarios_to_json(path: Path, scenarios: Iterable[SyntheticDecisionCase]) -> None:
    """Write generated scenarios to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [scenario.to_dict() for scenario in scenarios]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


