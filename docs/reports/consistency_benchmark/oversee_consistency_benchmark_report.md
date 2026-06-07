# OVERSEE Consistency Benchmark Report

Version baseline: `v0.6.x`  
Scope: Fernando demo consistency benchmark  
Generated at: `2026-06-07T11:47:31`

## 1. Purpose

This benchmark evaluates the behavioural consistency of the OVERSEE demo workbench.

The practical question is:

```text
Does OVERSEE preserve stable governed decisions when evidence and context are unchanged,
while adapting its recommendation when the scenario context changes?
```

The benchmark is intentionally limited to the demo workbench. It does not modify the paper, the decision rules, the model logic, or the core architecture.

## 2. What is being tested

The benchmark focuses on the stability of governed decision fields:

- `layer1_valid`
- `layer2_decision_ready`
- `case_lifecycle_stage`
- `priority`
- `execution_mode`
- `intervention_feasible`
- `human_review_required`

These fields should be stable when the same scenario is executed repeatedly with the same evidence and context.

The benchmark also checks that different industrial contexts produce differentiated recommendations. In other words, it is not desirable for every scenario to return the same response.

## 3. What is not being tested

This benchmark does not test whether the decision rules are industrially perfect. It also does not attempt to improve the rules. Its purpose is narrower and more practical: verify that the demo behaves coherently.

Potentially variable or textual fields include:

- `package_id`
- `traceability_count`
- `recommendation_count`
- `governed_package_digest`

If a generative layer is used to formulate text, the wording may vary. That is acceptable as long as the governed decision remains stable for unchanged evidence and context.

## 4. Benchmark design

The benchmark uses seven tests:

| Test | Name | Purpose |
|---|---|---|
| `T01` | Exact repeatability of the controlled-planning path | Verify that COMP-001 produces the same governed decision when the same evidence and context are executed repeatedly. |
| `T02` | Exact repeatability of the constrained-execution path | Verify that PUMP-001 remains stable when the same high-risk but resource-constrained case is repeated. |
| `T03` | Exact repeatability of the diagnostic-review path | Verify that DATA-001 repeatedly blocks normal execution and preserves diagnostic review when evidence quality is poor. |
| `T04` | Same asset family with different compressor contexts | Compare compressor scenarios to verify that the same broad failure family can produce adapted decisions when urgency, resources or context differ. |
| `T05` | Resource-constrained mechanical cases | Compare cases where risk exists but resource or specialist availability changes the execution mode. |
| `T06` | Evidence-quality and diagnostic-review cases | Verify that questionable or contradictory evidence leads to diagnostic review rather than blind execution. |
| `T07` | Full 20-scenario baseline | Execute the full scenario library once to provide the overall benchmark baseline. |

## 5. Test summary

| Test | Runs | Scenarios | Unique governed signatures | Unique package digests | Passed | Conclusion |
|---|---:|---|---:|---:|---:|---|
| `T01` | 10 | `COMP-001` | 1 | 10 | True | The stable governed decision remained identical across repeated executions. |
| `T02` | 10 | `PUMP-001` | 1 | 10 | True | The stable governed decision remained identical across repeated executions. |
| `T03` | 10 | `DATA-001` | 1 | 10 | True | The stable governed decision remained identical across repeated executions. |
| `T04` | 3 | `COMP-001`, `COMP-002`, `COMP-003` | 3 | 3 | True | Different scenarios in the same broad family produced differentiated governed decisions. |
| `T05` | 3 | `COMP-003`, `PUMP-001`, `PUMP-002` | 3 | 3 | True | At least one resource-constrained case preserved risk while blocking normal execution. |
| `T06` | 3 | `DATA-001`, `SENSOR-001`, `VALVE-001` | 3 | 3 | True | Evidence-quality cases produced diagnostic-review behaviour instead of blind execution. |
| `T07` | 20 | `AGV-001`, `BOILER-001`, `CHILLER-001`, `CIP-001`, `COMP-001`, `COMP-002`, `COMP-003`, `CONV-001`, `DATA-001`, `FAN-001`, `GEAR-001`, `HVAC-001`, `MIXER-001`, `MOTOR-001`, `PACK-001`, `PUMP-001`, `PUMP-002`, `ROBOT-001`, `SENSOR-001`, `VALVE-001` | 20 | 20 | True | All 20 scenarios executed and generated the expected evidence chain. |

## 6. Detailed evidence by test

### T01 - Exact repeatability of the controlled-planning path

**Purpose:** Verify that COMP-001 produces the same governed decision when the same evidence and context are executed repeatedly.

**Conclusion:** The stable governed decision remained identical across repeated executions.

| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
|---:|---|---:|---|---|---:|---:|---|---|---|
| 1 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 2 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 3 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 4 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 5 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 6 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 7 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 8 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 9 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 10 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |

### T02 - Exact repeatability of the constrained-execution path

**Purpose:** Verify that PUMP-001 remains stable when the same high-risk but resource-constrained case is repeated.

**Conclusion:** The stable governed decision remained identical across repeated executions.

| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
|---:|---|---:|---|---|---:|---:|---|---|---|
| 1 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 2 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 3 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 4 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 5 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 6 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 7 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 8 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 9 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 10 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |

### T03 - Exact repeatability of the diagnostic-review path

**Purpose:** Verify that DATA-001 repeatedly blocks normal execution and preserves diagnostic review when evidence quality is poor.

**Conclusion:** The stable governed decision remained identical across repeated executions.

| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
|---:|---|---:|---|---|---:|---:|---|---|---|
| 1 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 2 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 3 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 4 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 5 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 6 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 7 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 8 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 9 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 10 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |

### T04 - Same asset family with different compressor contexts

**Purpose:** Compare compressor scenarios to verify that the same broad failure family can produce adapted decisions when urgency, resources or context differ.

**Conclusion:** Different scenarios in the same broad family produced differentiated governed decisions.

| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
|---:|---|---:|---|---|---:|---:|---|---|---|
| 1 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 1 | `COMP-002` | True | medium | standard_planning | True | True | evidence_review | `95513eda7c` | The case supports proportional planning without escalation. |
| 1 | `COMP-003` | True | critical | constrained_execution | False | True | evidence_review | `1212266b52` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |

### T05 - Resource-constrained mechanical cases

**Purpose:** Compare cases where risk exists but resource or specialist availability changes the execution mode.

**Conclusion:** At least one resource-constrained case preserved risk while blocking normal execution.

| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
|---:|---|---:|---|---|---:|---:|---|---|---|
| 1 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 1 | `PUMP-002` | True | medium | constrained_execution | False | True | evidence_review | `8eeff38387` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 1 | `COMP-003` | True | critical | constrained_execution | False | True | evidence_review | `1212266b52` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |

### T06 - Evidence-quality and diagnostic-review cases

**Purpose:** Verify that questionable or contradictory evidence leads to diagnostic review rather than blind execution.

**Conclusion:** Evidence-quality cases produced diagnostic-review behaviour instead of blind execution.

| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
|---:|---|---:|---|---|---:|---:|---|---|---|
| 1 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 1 | `SENSOR-001` | False | medium | diagnostic_review | True | True | evidence_review | `b971609413` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 1 | `VALVE-001` | False | medium | diagnostic_review | True | True | evidence_review | `ea81a6d3f4` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |

### T07 - Full 20-scenario baseline

**Purpose:** Execute the full scenario library once to provide the overall benchmark baseline.

**Conclusion:** All 20 scenarios executed and generated the expected evidence chain.

| Iteration | Scenario | Layer 1 valid | Priority | Execution mode | Feasible | Human review | Lifecycle | Signature | Interpretation |
|---:|---|---:|---|---|---:|---:|---|---|---|
| 1 | `AGV-001` | True | medium | standard_planning | True | True | evidence_review | `7b5b51783a` | The case supports proportional planning without escalation. |
| 1 | `BOILER-001` | True | critical | controlled_planning | True | True | decision_ready | `be22bdf004` | The case supports a governed intervention with retained human review. |
| 1 | `CHILLER-001` | True | medium | standard_planning | True | True | evidence_review | `a7353201ea` | The case supports proportional planning without escalation. |
| 1 | `CIP-001` | True | high | standard_planning | True | True | decision_ready | `f5fb51b8db` | The case supports proportional planning without escalation. |
| 1 | `COMP-001` | True | high | controlled_planning | True | True | decision_ready | `d19edffe30` | The case supports a governed intervention with retained human review. |
| 1 | `COMP-002` | True | medium | standard_planning | True | True | evidence_review | `95513eda7c` | The case supports proportional planning without escalation. |
| 1 | `COMP-003` | True | critical | constrained_execution | False | True | evidence_review | `1212266b52` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 1 | `CONV-001` | True | high | controlled_planning | True | True | decision_ready | `704903bb25` | The case supports a governed intervention with retained human review. |
| 1 | `DATA-001` | False | medium | diagnostic_review | True | True | evidence_review | `6db1af1680` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 1 | `FAN-001` | True | low | standard_planning | True | True | evidence_review | `1996128e3d` | The case supports proportional planning without escalation. |
| 1 | `GEAR-001` | True | high | controlled_planning | True | True | decision_ready | `7c9f91b149` | The case supports a governed intervention with retained human review. |
| 1 | `HVAC-001` | True | medium | standard_planning | True | True | evidence_review | `cfd815c116` | The case supports proportional planning without escalation. |
| 1 | `MIXER-001` | True | high | controlled_planning | True | True | decision_ready | `ef6472da3d` | The case supports a governed intervention with retained human review. |
| 1 | `MOTOR-001` | True | medium | standard_planning | True | True | evidence_review | `6583d6029d` | The case supports proportional planning without escalation. |
| 1 | `PACK-001` | True | medium | controlled_planning | True | True | decision_ready | `7038531c19` | The case supports a governed intervention with retained human review. |
| 1 | `PUMP-001` | True | high | constrained_execution | False | True | evidence_review | `7a4bc2c9c6` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 1 | `PUMP-002` | True | medium | constrained_execution | False | True | evidence_review | `8eeff38387` | The case preserves risk visibility, but execution is constrained by resources or feasibility. |
| 1 | `ROBOT-001` | True | high | controlled_planning | True | True | decision_ready | `64357a7a31` | The case supports a governed intervention with retained human review. |
| 1 | `SENSOR-001` | False | medium | diagnostic_review | True | True | evidence_review | `b971609413` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |
| 1 | `VALVE-001` | False | medium | diagnostic_review | True | True | evidence_review | `ea81a6d3f4` | Evidence quality blocks normal execution and pushes the case to diagnostic review. |

## 7. Main conclusions

The benchmark supports three practical conclusions:

1. Repeated executions of the same scenario preserve the same governed decision signature.
2. Different industrial contexts produce differentiated governed decisions.
3. Evidence-quality cases can trigger diagnostic review instead of blind execution.

This means that the demo does not simply copy the same recommendation across every case. It applies the same architecture to different operational contexts and produces context-sensitive outputs.

## 8. Limitations

The benchmark has a practical demo purpose. It should not be interpreted as a full industrial validation study.

Known limitations:

- The benchmark uses scenario-backed enterprise data, not live enterprise systems.
- It validates behavioural coherence, not economic optimality.
- It does not attempt to tune the decision rules.
- It does not prove that generative wording will always be identical. It only separates governed structured fields from package-level or textual fields.

## 9. Final statement

The benchmark confirms that OVERSEE behaves coherently for the demo purpose: same evidence and context preserve the same governed decision, while different contexts lead to adapted recommendations.

Generated companion files:

```text
docs/reports/consistency_benchmark/oversee_consistency_benchmark_results.csv
docs/reports/consistency_benchmark/oversee_consistency_benchmark_results.json
```
