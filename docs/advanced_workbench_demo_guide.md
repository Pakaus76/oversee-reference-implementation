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

## Key reviewer-facing message

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
05_final_governed_recommendation_package.json
04_deterministic_vs_generative_comparison.json
04_live_generative_recommendation.json
00_generative_factory_result.json
02_canonical_case_context.json
03_output_layer3_case_management_state.json
04_output_layer4_dmn_decision_evaluation.json
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

<!-- BEGIN: V0.5.0_PAPER_ALIGNED_ALL_LAYERS_DEMO -->
## Relationship between v0.4.0 and v0.5.0

`v0.4.0` demonstrated the advanced generative workbench, including the Generative Digital Factory and live generative recommendation path.

`v0.5.0` adds a paper-aligned, five-layer compressor demo that makes the artifact more concrete and reviewer-friendly.

The main difference is focus:

```text
v0.4.0 - shows the advanced generative workbench capability.
v0.5.0 - shows how the OVERSEE layers operate on one concrete compressor case from alert intake to governed package.
```

Use `v0.5.0` for the reviewer-facing demo because it directly addresses the requested "how" questions:

```text
How does the alert enter OVERSEE?
What JSON is received?
Which enterprise APIs are consulted?
How are evidences aggregated and validated?
How does contextualization work?
How does the lifecycle become decision-ready?
How are deterministic and generative outputs compared?
How is the final recommendation governed and traced?
```
<!-- END: V0.5.0_PAPER_ALIGNED_ALL_LAYERS_DEMO -->

## v0.5.0 paper-aligned demo validation anchors

The advanced workbench documentation now distinguishes the v0.4.0 generative workbench from the v0.5.0 paper-aligned compressor demo.

```text
Version: v0.5.0
Demo case: COMP-001
Official command: python scripts\run_paper_aligned_all_layers_demo.py
Layer 2: DMN-like contextualization rules
Layer 3: CMMN-inspired case lifecycle
Layer 4: DMN-like decision rules and generative comparison
Layer 5: governed recommendation package
```
