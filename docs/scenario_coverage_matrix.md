# OVERSEE Scenario Coverage Matrix

Author: F. Requena-Alcaraz  
Repository: `oversee-reference-implementation`  
Scope: Executable multi-scenario OVERSEE workbench  
Current baseline: `v0.5.7`

---

## 1. Purpose

This document defines the scenario coverage matrix for the executable OVERSEE workbench.

The objective is not to create many scenarios for volume. The objective is to cover the main industrial decision patterns that an AI-supported maintenance decision system should handle.

Each scenario must be able to follow the OVERSEE architecture from evidence intake to governed recommendation:

1. Enterprise and operational sources provide evidence.
2. Layer 1 validates and aggregates evidence.
3. Layer 2 contextualizes the case.
4. Layer 3 manages the case lifecycle.
5. Layer 4 evaluates decision logic.
6. Layer 5 produces a governed recommendation package.

At this stage, the workbench already supports executable scenarios through:

- `executable_inputs` in each scenario JSON file.
- `ScenarioBackedEnterpriseApiClient`.
- `run_scenario_all_layers_demo.py`.
- Interactive walkthrough integration with the executable scenario runner.

---

## 2. Design principle

The scenario library must support two simultaneous needs.

First, it must be broad enough to test the decision behaviour of OVERSEE across a realistic industrial spectrum.

Second, it must remain understandable for humans. For that reason, the full library contains 20 executable scenarios, but only 5 master cases will be used in detailed manuals and guided explanations.

The intended structure is:

```text
20 executable scenarios
    -> broad industrial coverage

5 master cases
    -> deep explanation, manuals, and teaching material
```

---

## 3. Master cases

The 5 master cases are the scenarios that will be used later in manuals, demonstrations, and detailed walkthroughs.

| Master case | Scenario ID | Main role | What it demonstrates |
|---:|---|---|---|
| 1 | `COMP-001` | Main paper case | Critical risk, feasible intervention, controlled planning, mandatory human review |
| 2 | `COMP-002` | Early warning case | Not every predictive alert requires urgent action; standard planning can be enough |
| 3 | `PUMP-001` | Resource-constrained case | High risk can still require constrained execution when resources are not available |
| 4 | `CONV-001` | Production conflict case | Technical risk may conflict with production availability and require escalation |
| 5 | `DATA-001` | Evidence quality case | OVERSEE should not force a recommendation when evidence is incomplete or contradictory |

The five master cases explain the core decision behaviours:

```text
COMP-001 -> act with controlled planning
COMP-002 -> plan without overreacting
PUMP-001 -> escalate because resources block execution
CONV-001 -> resolve production-maintenance conflict
DATA-001 -> stop and request better evidence
```

---

## 4. Full 20-scenario matrix

| # | Scenario ID | Asset | Failure mode / issue | Decision pattern | Master case |
|---:|---|---|---|---|---|
| 1 | `COMP-001` | Industrial air compressor | Bearing degradation | Critical but feasible controlled planning | Yes |
| 2 | `COMP-002` | Industrial air compressor | Early vibration anomaly | Medium urgency planned inspection | Yes |
| 3 | `PUMP-001` | Industrial pump | Seal degradation | High risk with resource-constrained escalation | Yes |
| 4 | `CONV-001` | Conveyor system | Belt drive degradation | High risk with production-maintenance conflict | Yes |
| 5 | `DATA-001` | Electric motor | Contradictory thermal and vibration evidence | Evidence quality stop / request more data | Yes |
| 6 | `FAN-001` | Industrial fan | Mild vibration drift | Low criticality monitoring | No |
| 7 | `MOTOR-001` | Electric motor | Moderate overheating | Planned electrical inspection | No |
| 8 | `GEAR-001` | Gearbox | Repeated gear wear | High recurrence risk intervention | No |
| 9 | `ROBOT-001` | Industrial robot | Axis abnormality | Safety-sensitive review required | No |
| 10 | `CHILLER-001` | Industrial chiller | Energy efficiency degradation | Energy optimization action | No |
| 11 | `BOILER-001` | Boiler system | Pressure instability | Compliance and safety escalation | No |
| 12 | `VALVE-001` | Critical valve | Intermittent actuation fault | Diagnostic action before intervention | No |
| 13 | `AGV-001` | Automated guided vehicle | Battery degradation | Redundant asset planned replacement | No |
| 14 | `PACK-001` | Packaging line asset | Intermittent stoppages | Bottleneck-driven operational priority | No |
| 15 | `CIP-001` | CIP system | Cleaning cycle reliability issue | Quality and availability coordination | No |
| 16 | `HVAC-001` | Industrial HVAC | Air handling degradation | Environmental condition control | No |
| 17 | `PUMP-002` | Industrial pump | Bearing wear | Spare available but technician unavailable | No |
| 18 | `COMP-003` | Industrial air compressor | Rapid degradation | High urgency with missing specialist | No |
| 19 | `SENSOR-001` | Critical sensor | Sensor drift suspected | Validate sensor before asset intervention | No |
| 20 | `MIXER-001` | Industrial mixer | Mixing instability | Product-quality-driven intervention | No |

---

## 5. Coverage by decision dimension

| Decision dimension | Covered by scenarios |
|---|---|
| High technical urgency | `COMP-001`, `PUMP-001`, `CONV-001`, `BOILER-001`, `COMP-003` |
| Medium or low urgency | `COMP-002`, `FAN-001`, `CHILLER-001`, `AGV-001` |
| Feasible intervention | `COMP-001`, `COMP-002`, `GEAR-001`, `MIXER-001` |
| Resource-constrained intervention | `PUMP-001`, `PUMP-002`, `COMP-003` |
| Production-maintenance conflict | `CONV-001`, `PACK-001`, `CIP-001` |
| Evidence quality issue | `DATA-001`, `VALVE-001`, `SENSOR-001` |
| Safety or compliance sensitivity | `ROBOT-001`, `BOILER-001` |
| Monitoring or non-urgent follow-up | `FAN-001`, `CHILLER-001`, `AGV-001` |
| Escalation required | `PUMP-001`, `CONV-001`, `BOILER-001`, `COMP-003` |
| Product quality impact | `CIP-001`, `MIXER-001` |
| Asset redundancy | `AGV-001`, `FAN-001` |
| Critical utility impact | `COMP-001`, `BOILER-001`, `CHILLER-001`, `HVAC-001` |

---

## 6. Expected scenario behaviours

| Scenario ID | Expected priority | Expected execution mode | Expected intervention feasibility | Expected human review | Expected interpretation |
|---|---|---|---|---|---|
| `COMP-001` | High | Controlled planning | Feasible | Required | Act during the near feasible downtime window |
| `COMP-002` | Medium | Standard planning | Feasible | Required or recommended depending on policy | Plan inspection without overreacting |
| `PUMP-001` | High | Constrained execution | Not feasible | Required | Escalate because resources block direct execution |
| `CONV-001` | High | Escalation planning | Technically feasible but operationally constrained | Required | Resolve production-maintenance conflict |
| `DATA-001` | Low or blocked | Evidence review | Not confirmed | Required for exception handling | Do not recommend action until evidence is improved |
| `FAN-001` | Low | Monitoring | Feasible if needed | Not required | Continue monitoring |
| `MOTOR-001` | Medium | Standard planning | Feasible | Recommended | Plan electrical inspection |
| `GEAR-001` | High | Controlled planning | Feasible | Required | Act due to recurrence risk |
| `ROBOT-001` | High | Safety review | Conditional | Required | Review before intervention because of safety sensitivity |
| `CHILLER-001` | Medium | Optimization planning | Feasible | Recommended | Treat as energy/performance optimization |
| `BOILER-001` | High | Compliance escalation | Conditional | Required | Escalate because of compliance and safety implications |
| `VALVE-001` | Medium | Diagnostic review | Not confirmed | Recommended | Diagnose intermittent evidence before intervention |
| `AGV-001` | Low or medium | Planned replacement | Feasible | Not required | Use fleet redundancy to plan replacement |
| `PACK-001` | High | Operational priority planning | Feasible | Recommended | Prioritize due to flow bottleneck impact |
| `CIP-001` | Medium or high | Coordinated planning | Feasible | Required if quality risk is high | Coordinate production, maintenance, and quality |
| `HVAC-001` | Medium | Standard planning | Feasible | Recommended | Protect environmental conditions |
| `PUMP-002` | Medium | Deferred planning | Partially constrained | Recommended | Wait for technician availability |
| `COMP-003` | High | Resource escalation | Not feasible | Required | Escalate specialist availability |
| `SENSOR-001` | Blocked or diagnostic | Sensor validation | Not confirmed | Recommended | Validate measurement system first |
| `MIXER-001` | High | Controlled planning | Feasible | Required | Act because product quality is at risk |

---

## 7. Scenario JSON requirements

Every executable scenario JSON must include the following top-level fields:

```json
{
  "scenario_id": "",
  "title": "",
  "description": "",
  "asset_id": "",
  "asset_type": "",
  "failure_mode": "",
  "paper_aligned": false,
  "master_case": false,
  "master_case_role": "",
  "decision_pattern": "",
  "layer_inputs": {},
  "expected_layer_outputs": {},
  "executable_inputs": {}
}
```

The `executable_inputs` section must include:

```json
{
  "alert": {},
  "raw_sensor_context": {},
  "requested_context": {},
  "enterprise_sources": {
    "asset_metadata": {},
    "maintenance_history": {},
    "operational_context": {},
    "inventory_and_resources": {},
    "policy_governance": {}
  }
}
```

This structure is required because the executable scenario runner builds the real Layer 1 request and the scenario-backed enterprise API client from these fields.

---

## 8. Implementation sequence

The implementation should proceed in this order:

1. Preserve the current 3 executable scenarios:
   - `COMP-001`
   - `COMP-002`
   - `PUMP-001`

2. Add the two missing master cases:
   - `CONV-001`
   - `DATA-001`

3. Validate the 5 master cases:
   - scenario catalog listing
   - `run_scenario_all_layers_demo.py`
   - `run_interactive_oversee_demo.py`
   - full test suite

4. Add the remaining 15 coverage scenarios.

5. Validate all 20 scenarios.

6. Update demo manuals using only the 5 master cases.

---

## 9. Validation commands

After adding scenarios, the minimum validation commands are:

```powershell
python scripts\run_scenario_all_layers_demo.py --list-scenarios
python scripts\run_scenario_all_layers_demo.py --scenario COMP-001
python scripts\run_scenario_all_layers_demo.py --scenario COMP-002
python scripts\run_scenario_all_layers_demo.py --scenario PUMP-001
python scripts\run_scenario_all_layers_demo.py --scenario CONV-001
python scripts\run_scenario_all_layers_demo.py --scenario DATA-001

python scripts\run_interactive_oversee_demo.py --scenario COMP-001 --no-pause
python scripts\run_interactive_oversee_demo.py --scenario COMP-002 --no-pause
python scripts\run_interactive_oversee_demo.py --scenario PUMP-001 --no-pause
python scripts\run_interactive_oversee_demo.py --scenario CONV-001 --no-pause
python scripts\run_interactive_oversee_demo.py --scenario DATA-001 --no-pause

python -m pytest tests\oversee -q
```

The expected state after each validation is:

```text
All selected scenarios execute through the real multi-scenario all-layers runner.
The interactive walkthrough reuses real scenario execution artifacts.
The test suite passes.
No temporary validation outputs remain untracked.
```

---

## 10. Current milestone status

At the time this document is updated:

- `v0.5.4` cleaned public naming.
- `v0.5.5` introduced the executable multi-scenario all-layers runner.
- `v0.5.6` cleaned scenario runner test outputs.
- `v0.5.7` connected the interactive walkthrough to the executable scenario runner.
- `v0.5.8` added the five executable master scenarios.
- `v0.5.9` made `DATA-001` a true diagnostic/evidence-quality review case.
- The executable scenario library now contains 20 scenarios:
  - 5 master scenarios for manuals and guided walkthroughs.
  - 15 additional coverage scenarios for broader industrial validation.

The next milestone is to formalize the complete 20-scenario validation baseline and prepare the documentation/manual layer.
