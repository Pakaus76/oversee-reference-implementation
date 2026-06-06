# OVERSEE v0.6.2 - 20-Scenario Results Summary

Version baseline: `v0.6.2`  
Scope: executable results generated from the 20-scenario OVERSEE workbench

## Purpose

This report summarizes the executable outcome of the 20 OVERSEE scenarios.

It is intended for demo preparation, reviewer explanation and quick comparison. It is not a new paper artifact and does not change the OVERSEE logic.

## Summary table

| Scenario | Master | Asset type | Failure mode | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Interpretation |
|---|---:|---|---|---:|---|---|---:|---:|---|---|
| COMP-001 | True | industrial_air_compressor | bearing_degradation | True | high | controlled_planning | True | True | decision_ready | Risk and operational context justify a governed intervention with retained human review. |
| COMP-002 | True | industrial_air_compressor | early_vibration_anomaly | True | medium | standard_planning | True | True | evidence_review | The situation is controlled enough for standard planning or monitoring without escalation. |
| PUMP-001 | True | industrial_pump | seal_degradation | True | high | constrained_execution | False | True | evidence_review | Risk exists, but normal execution is constrained by resources or specialist availability. |
| CONV-001 | True | conveyor_system | belt_drive_degradation | True | high | controlled_planning | True | True | decision_ready | Risk and operational context justify a governed intervention with retained human review. |
| DATA-001 | True | electric_motor | contradictory_thermal_vibration_evidence | False | medium | diagnostic_review | True | True | evidence_review | Contradictory evidence is detected. OVERSEE blocks normal execution and recommends diagnostic review. |
| FAN-001 | False | industrial_fan | mild_vibration_drift | True | low | standard_planning | True | True | evidence_review | The situation is controlled enough for standard planning or monitoring without escalation. |
| MOTOR-001 | False | electric_motor | moderate_overheating | True | medium | standard_planning | True | True | evidence_review | The situation is controlled enough for standard planning or monitoring without escalation. |
| GEAR-001 | False | gearbox | repeated_gear_wear | True | high | controlled_planning | True | True | decision_ready | Risk and operational context justify a governed intervention with retained human review. |
| ROBOT-001 | False | industrial_robot | axis_abnormality | True | high | controlled_planning | True | True | decision_ready | Risk and operational context justify a governed intervention with retained human review. |
| CHILLER-001 | False | industrial_chiller | energy_efficiency_degradation | True | medium | standard_planning | True | True | evidence_review | The situation is controlled enough for standard planning or monitoring without escalation. |
| BOILER-001 | False | boiler_system | pressure_instability | True | critical | controlled_planning | True | True | decision_ready | Risk and operational context justify a governed intervention with retained human review. |
| VALVE-001 | False | critical_valve | intermittent_actuation_fault | False | medium | diagnostic_review | True | True | evidence_review | Evidence quality or intermittent measurement behaviour requires diagnostic review before intervention. |
| AGV-001 | False | automated_guided_vehicle | battery_degradation | True | medium | standard_planning | True | True | evidence_review | The situation is controlled enough for standard planning or monitoring without escalation. |
| PACK-001 | False | packaging_line_asset | intermittent_stoppages | True | medium | controlled_planning | True | True | decision_ready | Risk and operational context justify a governed intervention with retained human review. |
| CIP-001 | False | cip_system | cleaning_cycle_reliability_issue | True | high | standard_planning | True | True | decision_ready | The situation is controlled enough for standard planning or monitoring without escalation. |
| HVAC-001 | False | industrial_hvac | air_handling_degradation | True | medium | standard_planning | True | True | evidence_review | The situation is controlled enough for standard planning or monitoring without escalation. |
| PUMP-002 | False | industrial_pump | bearing_wear | True | medium | constrained_execution | False | True | evidence_review | Risk exists, but normal execution is constrained by resources or specialist availability. |
| COMP-003 | False | industrial_air_compressor | rapid_degradation_missing_specialist | True | critical | constrained_execution | False | True | evidence_review | Risk exists, but normal execution is constrained by resources or specialist availability. |
| SENSOR-001 | False | critical_sensor | sensor_drift_suspected | False | medium | diagnostic_review | True | True | evidence_review | Evidence quality or intermittent measurement behaviour requires diagnostic review before intervention. |
| MIXER-001 | False | industrial_mixer | mixing_instability | True | high | controlled_planning | True | True | decision_ready | Risk and operational context justify a governed intervention with retained human review. |

## Key observation

The 20 scenarios do not produce a single repeated response. They exercise different governed behaviours:

- `controlled_planning` for high-risk but feasible intervention cases.
- `standard_planning` for proportional, non-emergency planning cases.
- `constrained_execution` when resources or specialists block normal execution.
- `diagnostic_review` when evidence quality or measurement reliability is questionable.

This is the main practical value of the demo: the same architecture adapts its output to the industrial context of each case.

## Generated companion files

```text
docs/reports/v0_6_2_scenario_results_summary.csv
docs/reports/v0_6_2_scenario_results_summary.json
```
