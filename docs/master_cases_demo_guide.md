# OVERSEE Master Cases Demo Guide

Version baseline: `v0.6.0`  
Scope: 5 master cases selected from the 20 executable OVERSEE scenario library  
Author: F. Requena-Alcaraz

---

## 1. Purpose

This guide explains how to use the 5 OVERSEE master cases in a clear reviewer-facing demonstration.

The full workbench contains 20 executable scenarios. That full library is useful for technical validation and coverage, but it is too broad for a short explanation.

The 5 master cases are the recommended set for live demos, manuals and reviewer conversations:

```text
COMP-001
COMP-002
PUMP-001
CONV-001
DATA-001
```

Together, they show the most important behaviours of OVERSEE:

```text
act
plan
escalate
negotiate
stop and review evidence
```

---

## 2. Core message

The main message of the demo is:

```text
OVERSEE does not jump from prediction to action.
It builds a governed decision through evidence, context, case lifecycle, explicit rules and traceability.
```

A predictive alert is only the starting point.

OVERSEE asks:

```text
Is the evidence valid?
What is the operational context?
Is the organization ready to act?
Are resources available?
Is production aligned?
Is human review required?
Can the decision be traced?
```

---

## 3. Recommended demo sequence

Use this sequence for a complete explanation:

| Step | Scenario | Main question | Expected behaviour |
|---:|---|---|---|
| 1 | `COMP-001` | What happens when risk is high and action is feasible? | Controlled planning |
| 2 | `COMP-002` | What happens when the alert is early and less urgent? | Standard planning |
| 3 | `PUMP-001` | What happens when risk is high but resources block execution? | Constrained execution |
| 4 | `CONV-001` | What happens when maintenance needs conflict with production availability? | Escalation planning |
| 5 | `DATA-001` | What happens when the evidence is contradictory? | Diagnostic review |

For a shorter meeting, use:

```text
COMP-001
PUMP-001
DATA-001
```

This shorter set already demonstrates:

```text
normal governed action
resource-constrained execution
evidence-quality stop
```

---

## 4. Master case 1 - `COMP-001`

### Role

`COMP-001` is the main paper-aligned compressor case.

It represents an industrial air compressor with a bearing degradation risk.

### Why it matters

This case shows the normal high-value path:

```text
high risk
valid evidence
available resources
near feasible stop
human review retained
controlled planning
```

### Simple explanation

Use this explanation:

```text
The system receives a predictive alert, but it does not act immediately.
It enriches the alert with asset criticality, condition trends, maintenance history, production context, resource availability and policy rules.
Only then does it recommend controlled planning.
```

### Expected result

```text
priority: high
execution_mode: controlled_planning
intervention_feasible: true
human_review_required: true
```

### Recommended command

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001
```

---

## 5. Master case 2 - `COMP-002`

### Role

`COMP-002` is the lower-urgency compressor case.

It represents an early vibration anomaly with a longer predictive horizon and lower operational pressure.

### Why it matters

This case shows that OVERSEE does not overreact to every alert.

### Simple explanation

Use this explanation:

```text
The alert is real, but the context does not justify urgent escalation.
OVERSEE keeps the case under control and recommends standard planning instead of treating the alert as an emergency.
```

### Expected result

```text
priority: medium
execution_mode: standard_planning
intervention_feasible: true
human_review_required: true
```

### Recommended command

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-002 --no-pause
```

---

## 6. Master case 3 - `PUMP-001`

### Role

`PUMP-001` is the resource-constrained pump case.

It represents a pump with seal degradation risk where the intervention is blocked by spare-part or specialist constraints.

### Why it matters

This case shows that risk and feasibility are different things.

A high-risk alert does not automatically mean direct execution.

### Simple explanation

Use this explanation:

```text
The system recognizes high risk, but it also detects that the organization is not ready to execute normally.
The recommendation is therefore constrained execution with escalation and human review.
```

### Expected result

```text
priority: high
execution_mode: constrained_execution
intervention_feasible: false
human_review_required: true
```

### Recommended command

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario PUMP-001 --no-pause
```

---

## 7. Master case 4 - `CONV-001`

### Role

`CONV-001` is the production-maintenance conflict case.

It represents a conveyor belt-drive degradation risk where the technical intervention is possible, but production availability is constrained.

### Why it matters

This case shows that maintenance decisions are not only technical.

The asset may be repairable, but the organization still needs to negotiate the production window.

### Simple explanation

Use this explanation:

```text
The technical evidence supports action, and resources are available.
However, production pressure and lack of a near downtime window create an operational conflict.
OVERSEE makes that conflict visible and prepares an escalation path.
```

### Expected result

```text
priority: high
execution_mode: controlled_planning or escalation planning depending on rule interpretation
intervention_feasible: true
human_review_required: true
```

### Recommended command

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario CONV-001 --no-pause
```

---

## 8. Master case 5 - `DATA-001`

### Role

`DATA-001` is the evidence-quality stop case.

It represents a motor case where temperature rises, but vibration and current remain stable. The evidence is technically valid, but contradictory.

### Why it matters

This is the strongest governance case.

It shows that OVERSEE can stop an operational recommendation when evidence quality is questionable.

### Simple explanation

Use this explanation:

```text
OVERSEE does not automate blindly.
When the evidence is contradictory, it does not release a standard maintenance recommendation.
It sends the case to diagnostic review and preserves the reason in the traceability record.
```

### Expected result

```text
layer1_evidence_package_valid: false
case_lifecycle_stage: evidence_review
execution_mode: diagnostic_review
human_review_required: true
```

### Recommended command

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario DATA-001 --no-pause
```

---

## 9. How to explain the architecture during the demo

### Layer 1 - Evidence folder

Layer 1 builds the evidence package.

It collects:

```text
predictive alert
sensor context
asset metadata
maintenance history
production context
resources
policy information
```

Simple phrase:

```text
Layer 1 builds the evidence folder.
```

---

### Layer 2 - Operational meaning

Layer 2 gives operational meaning to the evidence.

It asks:

```text
How urgent is this?
How critical is the asset?
Is there a production window?
Are parts and people available?
Is review required?
```

Simple phrase:

```text
Layer 2 turns raw evidence into operational context.
```

---

### Layer 3 - Organizational readiness

Layer 3 manages the case lifecycle.

It identifies:

```text
tasks
milestones
blockers
case status
decision readiness
```

Simple phrase:

```text
Layer 3 checks whether the organization is ready to move.
```

---

### Layer 4 - Governed decision logic

Layer 4 applies explicit rules.

It decides:

```text
priority
execution mode
intervention feasibility
human review requirement
```

Simple phrase:

```text
Layer 4 converts context into a governed recommendation.
```

---

### Layer 5 - Traceable handoff

Layer 5 packages the final result.

It creates:

```text
recommendation package
traceability index
execution manifest
reviewer summary
workflow proposal
```

Simple phrase:

```text
Layer 5 makes the recommendation auditable and ready for handoff.
```

---

## 10. Suggested live script

A concise live explanation can follow this structure:

```text
First, we show COMP-001 to explain the normal controlled-planning path.
Then, we show PUMP-001 to demonstrate that high risk does not always mean immediate execution.
Finally, we show DATA-001 to prove that OVERSEE can stop and request diagnostic review when evidence quality is not good enough.
```

Use these commands:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001
python scripts\run_interactive_oversee_demo.py --scenario PUMP-001 --no-pause
python scripts\run_interactive_oversee_demo.py --scenario DATA-001 --no-pause
```

---

## 11. Validation commands

List the scenario library:

```powershell
$env:PYTHONPATH = "."
python scripts\run_scenario_all_layers_demo.py --list-scenarios
```

Run the full test suite:

```powershell
$env:PYTHONPATH = "."
python -m pytest tests\oversee -q
```

Expected at `v0.6.0`:

```text
88 passed
```

Run the formal 20-scenario regression test:

```powershell
$env:PYTHONPATH = "."
python -m pytest tests\oversee\integration\test_full_executable_scenario_library.py -q
```

Expected result:

```text
21 passed
```

---

## 12. Closing message

The closing message for a reviewer is:

```text
OVERSEE is not a predictive maintenance model.
It is a governed prediction-to-decision orchestration artifact.

It shows how evidence, enterprise context, case lifecycle, explicit rules, human review and traceability can be combined before maintenance action is recommended.
```
