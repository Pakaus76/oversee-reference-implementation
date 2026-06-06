# OVERSEE Interactive Walkthrough Demo Manual

Version baseline: `v0.6.0`  
Scope: 20 executable scenarios, with 5 master cases for guided explanation

---

## 1. Purpose

This manual explains how to run and explain the interactive OVERSEE walkthrough demo.

The walkthrough helps a non-programmer reviewer understand how OVERSEE transforms industrial maintenance evidence into a governed recommendation package.

The key idea is simple:

```text
A predictive alert is not enough to make a decision.
OVERSEE builds the decision step by step.
```

The demo follows the OVERSEE architecture:

```text
Enterprise sources
-> API access layer
-> Layer 1
-> Layer 2
-> Layer 3
-> Layer 4
-> Layer 5
-> final governed recommendation package
```

---

## 2. Repository location

Use the repository root:

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
```

Set the repository root as part of the Python import path:

```powershell
$env:PYTHONPATH = "."
```

---

## 3. Main launcher

```powershell
python scripts\run_interactive_oversee_demo.py
```

The launcher supports:

```text
--scenario <SCENARIO_ID>
--list-scenarios
--no-pause
--show-artifacts
```

---

## 4. What the demo does

When a scenario is executed, the interactive walkthrough does two things.

First, it executes the selected scenario through the real all-layers runner:

```text
scenario JSON
-> executable_inputs
-> scenario-backed enterprise APIs
-> Layer 1
-> Layer 2
-> Layer 3
-> Layer 4
-> Layer 5
```

Second, it presents the generated artifacts layer by layer.

This is like building a car first and then walking through the factory to explain what each station did.

---

## 5. Available scenarios

At v0.6.0, the demo contains 20 executable scenarios.

### 5.1 Master cases

Use these 5 cases for manuals, reviewer sessions and deep explanations.

| Scenario | Description | Demonstrates |
|---|---|---|
| `COMP-001` | Paper-aligned compressor case | Critical risk, feasible intervention, controlled planning |
| `COMP-002` | Lower-urgency compressor case | Early warning without overreaction |
| `PUMP-001` | Resource-constrained pump case | High risk with blocked execution |
| `CONV-001` | Production-constrained conveyor case | Production-maintenance conflict |
| `DATA-001` | Evidence-quality stop case | Diagnostic review due to contradictory evidence |

### 5.2 Coverage cases

Use these cases for broader testing and industrial coverage.

| Scenario | Description |
|---|---|
| `FAN-001` | Low-criticality fan monitoring |
| `MOTOR-001` | Moderate motor overheating |
| `GEAR-001` | Repeated gearbox wear |
| `ROBOT-001` | Safety-sensitive robot axis abnormality |
| `CHILLER-001` | Chiller energy efficiency degradation |
| `BOILER-001` | Boiler pressure instability |
| `VALVE-001` | Intermittent critical valve fault |
| `AGV-001` | Redundant AGV battery degradation |
| `PACK-001` | Packaging bottleneck stoppages |
| `CIP-001` | CIP cleaning reliability issue |
| `HVAC-001` | Industrial HVAC degradation |
| `PUMP-002` | Pump spare available but technician unavailable |
| `COMP-003` | Rapid compressor degradation with missing specialist |
| `SENSOR-001` | Critical sensor drift suspected |
| `MIXER-001` | Mixer product quality instability |

---

# 6. Demo options

## Option 1 - List available scenarios

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --list-scenarios
```

### What this shows

This lists the 20 executable scenarios available in the walkthrough.

### When to use it

Use it at the beginning if the reviewer asks what cases are available.

---

## Option 2 - Run the guided `COMP-001` walkthrough

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001
```

### What this shows

This is the main paper-aligned case.

It shows a compressor with bearing degradation risk. The system receives a predictive alert, enriches it with enterprise context, checks operational feasibility and produces a governed recommendation.

### Recommended explanation

Use this case to explain:

```text
This is not just predictive maintenance.
This is prediction-to-decision governance.
```

The key output is:

```text
high priority
controlled planning
human review retained
```

---

## Option 3 - Run `COMP-001` without pauses

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001 --no-pause
```

### When to use it

Use it to test quickly before a meeting.

---

## Option 4 - Run with artifact details

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001 --no-pause --show-artifacts
```

### What this shows

This reveals the copied real artifacts generated by the executable runner and captured by the interactive demo.

Use this when the reviewer asks:

```text
Where is the evidence stored?
Where is the decision trace?
Where is the final package?
```

---

## Option 5 - Run `PUMP-001`

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario PUMP-001 --no-pause
```

### What this shows

This case shows that a high-risk condition does not automatically mean direct execution.

The pump has a serious seal degradation risk, but the spare part or specialist resource situation blocks normal execution.

Expected result:

```text
high priority
constrained execution
human review retained
```

### Recommended explanation

Use this phrase:

```text
OVERSEE does not only ask whether there is a risk.
It also asks whether the organization is ready to act safely and realistically.
```

---

## Option 6 - Run `DATA-001`

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario DATA-001 --no-pause
```

### What this shows

This is the strongest governance case.

The system receives contradictory evidence. Temperature rises, but vibration and current remain stable. The evidence package contains data quality flags.

Expected result:

```text
layer1_evidence_package_valid = false
evidence_review
diagnostic_review
human review required
```

### Recommended explanation

Use this phrase:

```text
OVERSEE does not automate blindly.
When evidence quality is questionable, it stops the operational recommendation and asks for diagnostic review.
```

---

## Option 7 - Run `SENSOR-001`

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario SENSOR-001 --no-pause
```

### What this shows

This scenario is useful to explain that not every alert means the asset is failing.

Sometimes the real issue is the measurement system.

Expected result:

```text
diagnostic_review
sensor validation before asset intervention
```

---

## Option 8 - Run `MIXER-001`

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario MIXER-001 --no-pause
```

### What this shows

This case links maintenance decisions with product quality.

Expected result:

```text
high priority
controlled planning
human review retained
```

Use it to show that OVERSEE is not limited to equipment availability. It can also represent quality-driven maintenance decisions.

---

## Option 9 - Run the scenario runner directly

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python scripts\run_scenario_all_layers_demo.py --scenario COMP-001
```

### What this does

This runs the selected scenario through the real Layer 1 to Layer 5 path without the guided presentation.

Use this when you want the raw execution result quickly.

---

## Option 10 - Run the formal scenario library test

### Command

```powershell
cd C:\Users\franc\OneDrive\Documentos\oversee-reference-implementation
$env:PYTHONPATH = "."
python -m pytest tests\oversee\integration\test_full_executable_scenario_library.py -q
```

Expected result:

```text
21 passed
```

This validates:

```text
1 catalog test
20 scenario execution tests
```

---

## 7. How to explain the five layers

### Layer 1 - Evidence intake, aggregation and validation

Layer 1 receives the predictive alert and collects supporting information.

It brings together:

```text
predictive alert
sensor context
asset metadata
maintenance history
production context
inventory and resources
policy governance
```

Output:

```text
validated evidence package
```

Simple explanation:

```text
Layer 1 builds the evidence folder.
```

---

### Layer 2 - Contextualization

Layer 2 interprets the evidence in its operational context.

It asks:

```text
How urgent is the risk?
How critical is the asset?
Is there a production window?
Are resources available?
Is human review required?
```

Output:

```text
contextualized decision profile
```

Simple explanation:

```text
Layer 2 turns raw evidence into operational meaning.
```

---

### Layer 3 - Case lifecycle

Layer 3 manages the case state.

It identifies:

```text
open tasks
milestones
blockers
case lifecycle stage
whether the case is ready for decision or needs review
```

Output:

```text
case management state
```

Simple explanation:

```text
Layer 3 decides whether the organization is ready to move.
```

---

### Layer 4 - Decision logic

Layer 4 applies explicit DMN-like rules.

It decides:

```text
final priority
execution mode
intervention feasibility
human review requirement
```

Possible execution modes include:

```text
standard_planning
controlled_planning
constrained_execution
diagnostic_review
```

Output:

```text
decision evaluation and recommendation record
```

Simple explanation:

```text
Layer 4 converts context into a governed decision.
```

---

### Layer 5 - Governed packaging and traceability

Layer 5 packages the final result.

It creates:

```text
governed recommendation package
traceability index
execution manifest
human-readable summary
workflow handoff proposal
```

Output:

```text
governed recommendation package
```

Simple explanation:

```text
Layer 5 makes the decision auditable, reviewable and ready for handoff.
```

---

## 8. Output folders

Interactive demo outputs are written to:

```text
outputs/interactive_demo_YYYYMMDD_HHMMSS/
```

Direct scenario runner outputs are written to:

```text
outputs/scenario_all_layers_<scenario_id>_YYYYMMDD_HHMMSS/
```

During automated tests, temporary outputs are removed to keep the repository clean.

---

## 9. Recommended reviewer demo path

For a short meeting, use:

```text
1. COMP-001
2. PUMP-001
3. DATA-001
```

For a complete master-case explanation, use:

```text
1. COMP-001
2. COMP-002
3. PUMP-001
4. CONV-001
5. DATA-001
```

For technical validation, show:

```text
python -m pytest tests\oversee -q
```

Expected at v0.6.0:

```text
88 passed
```

---

## 10. Key message

The key message of the demo is:

```text
OVERSEE does not jump from prediction to action.
It builds a governed decision through evidence, context, lifecycle state, explicit rules and traceability.
```
