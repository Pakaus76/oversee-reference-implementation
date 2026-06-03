# Advanced OVERSEE workbench demo guide

## One-sentence explanation

OVERSEE v0.4.0 demonstrates how generative AI can create synthetic industrial source data and also participate in recommendation formulation, while the complete decision flow remains governed, traceable and comparable against deterministic anchors.

## Demo storyline

The demo should be explained as a sequence of controlled transformations:

```text
1. A Generative Digital Factory creates synthetic source-level industrial data.
2. OVERSEE receives those data as external source payloads.
3. OVERSEE normalizes them into a canonical compressor case.
4. OVERSEE manages the case through a lifecycle inspired by CMMN.
5. OVERSEE evaluates explicit DMN-like rules.
6. OVERSEE runs a deterministic recommendation path.
7. OVERSEE runs a live generative recommendation path.
8. OVERSEE compares deterministic and generative outputs.
9. OVERSEE packages the governed recommendation with traceability.
```

## Key message for Fernando

The workbench is not just a prompt demo.

It shows a governed architecture where generative AI is constrained by:

- source-level input structure;
- canonical case context;
- lifecycle state;
- DMN-like rule outputs;
- protected facts;
- fallback behavior;
- deterministic-vs-generative comparison;
- final traceability package.

## Suggested live demo command

```powershell
$env:PYTHONPATH = "src"
python scripts\run_generative_digital_factory_workbench_smoke.py
```

## Main output to open first

```text
05_reviewer_summary.md
```

Then open:

```text
05_governed_recommendation_package.json
04_deterministic_vs_generative_comparison.json
04_live_generative_recommendation.json
00_generative_factory_result.json
02_canonical_case_context.json
03_case_management_state.json
04_dmn_decision_evaluation.json
```

## How to explain the deterministic-vs-generative difference

The deterministic path is stable, compact and rule-driven.

The generative path uses the same governed inputs but can produce richer operational wording.

The comparison does not try to prove that generative AI is better. It shows whether the generative recommendation:

- keeps the same priority;
- respects human review requirements;
- avoids protected-fact violations;
- uses the same evidence base;
- adds useful rationale or operational framing;
- remains auditable inside Layer 5.

## Recommended demo close

The strongest closing statement is:

```text
This workbench shows that generative AI can be used in industrial decision support without turning the decision process into a black box. The generated data, the model recommendation, the deterministic anchor, the rules, the lifecycle and the final package are all visible and traceable.
```
