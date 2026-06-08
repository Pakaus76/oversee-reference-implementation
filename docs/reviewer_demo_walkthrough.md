# OVERSEE v0.4.0 reviewer demo walkthrough

## Purpose

This document explains how to run and interpret the advanced OVERSEE workbench demo.

The v0.4.0 demo is designed to show the complete governed flow requested for the paper and for technical review:

```text
Generative Digital Factory
-> external source payloads
-> canonical compressor context
-> CMMN-inspired lifecycle
-> DMN-like rules
-> deterministic anchor
-> live generative recommendation
-> deterministic-vs-generative comparison
-> governed recommendation package
```

## Main command

From the repository root:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_generative_digital_factory_workbench_smoke.py
```

## Environment

The command expects the OpenAI environment variables to be available locally.

The local `.env` file is ignored by Git and must never be committed.

The workbench is designed with fallback protection. If a live model call fails, the execution records fallback metadata and keeps the governed deterministic path available.

## What a successful live run looks like

A successful v0.4.0 run should show:

```json
{
  "factory_model_call_attempted": true,
  "factory_model_call_successful": true,
  "factory_fallback_used": false,
  "oversee_model_call_attempted": true,
  "oversee_model_call_successful": true,
  "oversee_fallback_used": false,
  "final_priority": "high",
  "generative_priority": "high",
  "priority_alignment": true
}
```

## How to explain the demo

### Step 0 - Generative Digital Factory

The Generative Digital Factory uses a live model call to create or enrich synthetic source-level information for a compressor case.

It produces sources such as:

- asset registry;
- sensor historian;
- predictive maintenance;
- maintenance history;
- production planning;
- inventory and resources;
- policy governance.

The important point is that the model does not recommend an action here. It creates source-level data that must still pass through the governed OVERSEE layers.

### Layer 1 - External source payloads

Layer 1 packages the generated industrial information as external source payloads.

Reviewer file:

```text
01_external_source_payloads.json
```

### Layer 2 - Canonical case context

Layer 2 normalizes the external source payloads into a canonical compressor case context.

Reviewer file:

```text
02_canonical_case_context.json
```

Key fields include:

- asset ID;
- asset criticality;
- predicted failure horizon;
- confidence score;
- production pressure;
- intervention feasibility;
- governance policy.

### Layer 3 - CMMN-inspired case lifecycle

Layer 3 represents the case as a lifecycle with events, tasks and milestones.

Reviewer files:

```text
03_case_lifecycle_trace.json
03_output_layer3_case_management_state.json
```

This layer shows that the case is not just a static prediction. It is a managed decision case.

### Layer 4 - DMN-like rules and recommendation paths

Layer 4 evaluates explicit decision rules and then runs recommendation paths.

Reviewer files:

```text
04_output_layer4_dmn_decision_evaluation.json
04_output_layer4_recommendation_path_outputs.json
04_live_generative_recommendation.json
04_deterministic_vs_generative_comparison.json
```

This is where the deterministic and generative recommendation paths are compared.

### Layer 5 - Governed recommendation package

Layer 5 packages the evidence, recommendation, comparison and traceability.

Reviewer files:

```text
05_final_governed_recommendation_package.json
05_traceability_index.json
05_reviewer_summary.md
05_execution_manifest.json
```

Layer 5 is the main evidence package for review.

## Recommended review order

1. Open `05_reviewer_summary.md`.
2. Open `05_execution_manifest.json`.
3. Open `00_generative_factory_result.json`.
4. Open `02_canonical_case_context.json`.
5. Open `03_output_layer3_case_management_state.json`.
6. Open `04_output_layer4_dmn_decision_evaluation.json`.
7. Open `04_live_generative_recommendation.json`.
8. Open `04_deterministic_vs_generative_comparison.json`.
9. Open `05_final_governed_recommendation_package.json`.

## What the demo proves

The demo proves that the current workbench can execute:

- live generative source generation before OVERSEE;
- governed normalization of generated source data;
- explicit case lifecycle management;
- explicit DMN-like rule evaluation;
- deterministic recommendation;
- live generative recommendation;
- deterministic-vs-generative comparison;
- governed packaging with traceability.

## What the demo does not claim

The demo does not claim that the generative recommendation is universally better than the deterministic path.

The intended claim is narrower and stronger:

```text
The workbench shows how generative AI can be inserted into industrial decision support under governance, traceability, fallback protection and comparison against deterministic anchors.
```

## Main interpretation of the v0.4.0 run

In the validated v0.4.0 run:

- both live model calls succeeded;
- no fallback was used;
- the final priority remained high;
- deterministic and generative priorities aligned;
- the generative recommendation added richer operational wording;
- Layer 5 preserved the comparison and metadata.

<!-- BEGIN: V0.5.0_PAPER_ALIGNED_ALL_LAYERS_DEMO -->
## v0.5.0 reviewer walkthrough - paper-aligned all-layers demo

For reviewer-facing assessment, the recommended demo is now the all-layers compressor walkthrough:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_paper_aligned_all_layers_demo.py
```

The demo is based on a single compressor case, `COMP-001`, and shows how a predictive maintenance alert becomes a governed recommendation package.

Recommended file opening order:

```text
00_predictive_alert_request.json
01_enterprise_api_calls.json
01_output_layer1_aggregated_evidence_package.json
01_validation_report.json
02_contextualization_rule_trace.json
02_canonical_case_context.json
03_output_layer3_case_management_state.json
04_output_layer4_dmn_decision_evaluation.json
04_live_generative_recommendation.json
04_deterministic_vs_generative_comparison.json
05_final_governed_recommendation_package.json
05_reviewer_summary.md
05_full_layer_trace_summary.md
```

Reviewer message:

```text
The demo takes the compressor example from a predictive alert to a governed recommendation.
It does not claim to implement production APIs, a formal DMN engine or a formal CMMN engine.
It demonstrates an executable reference implementation where each layer has a concrete input,
mechanism, output and traceable artifact.
```
<!-- END: V0.5.0_PAPER_ALIGNED_ALL_LAYERS_DEMO -->
