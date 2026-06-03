# Fernando all-layers OVERSEE demo guide

## One-sentence explanation

OVERSEE v0.5.0 demonstrates how a predictive maintenance alert for an industrial compressor is transformed into a governed, traceable recommendation package through five explicit layers.

## Demo case

```text
Asset ID: COMP-001
Asset type: industrial_air_compressor
Case ID: FERNANDO_ALERT-COMP-001-20260603
Suspected failure mode: bearing_degradation
Predictive horizon: 48 hours
Model confidence: 0.88
Production line: PKG-LINE-01
```

## Official demo command

Run from the repository root:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_fernando_all_layers_demo.py
```

Expected console summary:

```json
{
  "fernando_all_layers_demo_completed": true,
  "compressor_case_id": "FERNANDO_ALERT-COMP-001-20260603",
  "asset_id": "COMP-001",
  "layer1_evidence_package_valid": true,
  "layer2_decision_ready": true,
  "case_lifecycle_stage": "decision_ready",
  "dmn_decision_final_priority": "high",
  "recommended_execution_mode": "controlled_planning",
  "oversee_model_call_successful": true,
  "oversee_fallback_used": false,
  "priority_alignment": true,
  "action_alignment": "different",
  "governed_package_created": true,
  "traceability_count": 6,
  "generated_file_count": 22
}
```

## Output folder

The demo creates:

```text
outputs/fernando_all_layers_demo_YYYYMMDD_HHMMSS/
```

## Recommended file opening order

Open the outputs in this order during the review.

### 1. Trigger and Layer 1 inputs

```text
00_predictive_alert_request.json
01_received_predictive_alert.json
01_enterprise_api_calls.json
01_aggregated_evidence_package.json
01_validation_report.json
```

What this shows:

```text
A predictive maintenance agent submits a concrete alert JSON to OVERSEE.
The alert includes raw sensor context.
OVERSEE retrieves additional context through simulated enterprise APIs.
The layer aggregates and validates an evidence package.
```

### 2. Layer 2 contextualization

```text
02_contextualization_rule_trace.json
02_canonical_case_context.json
02_context_enrichment_summary.md
02_layer2_contextualization_result.json
```

What this shows:

```text
Layer 2 converts aggregated evidence into contextual decision factors.
It uses explicit DMN-like contextualization rules.
These rules do not make the final recommendation.
They derive factors such as technical urgency, operational constraint,
intervention feasibility and human review requirement.
```

Key distinction:

```text
Layer 2 DMN-like rules = contextualization.
Layer 4 DMN-like rules = decision and recommendation consolidation.
```

### 3. Layer 3 case lifecycle

```text
03_case_lifecycle_trace.json
03_case_management_state.json
03_layer3_case_lifecycle_summary.md
```

What this shows:

```text
The compressor alert becomes a managed decision case.
The lifecycle is CMMN-inspired.
The prototype does not claim to implement a formal CMMN engine.
It uses case-management concepts to represent events, tasks, milestones,
blockers and decision readiness.
```

### 4. Layer 4 decision and generative comparison

```text
04_dmn_decision_evaluation.json
04_recommendation_path_outputs.json
04_live_generative_recommendation.json
04_deterministic_vs_generative_comparison.json
04_layer4_decision_summary.md
```

What this shows:

```text
Layer 4 applies DMN-like decision rules.
It produces deterministic recommendation outputs.
It runs a live generative recommendation path when OpenAI credentials are available.
It compares deterministic and generative outputs.
The generative response is not accepted blindly.
```

### 5. Layer 5 governed package

```text
05_governed_recommendation_package.json
05_traceability_index.json
05_execution_manifest.json
05_reviewer_summary.md
05_full_layer_trace_summary.md
```

What this shows:

```text
The final output is a governed recommendation package.
It includes evidence, rule outputs, lifecycle status, deterministic/generative comparison,
traceability and reviewer-facing summary.
```

## How to explain the architectural choices

### Why simulated APIs in Layer 1?

The purpose is to make the integration mechanism executable and inspectable without requiring a real CMMS, MES, ERP or asset registry during the review.

Use this wording:

```text
The APIs are simulated, but they are not abstract placeholders.
They make explicit which enterprise systems would be called,
with what parameters and what type of JSON response would be aggregated.
```

### Why DMN-like rules in Layer 2?

Layer 2 interprets evidence.

Use this wording:

```text
Layer 2 uses DMN-like contextualization rules to derive decision factors from evidence.
It does not decide the final action.
```

### Why CMMN-inspired lifecycle in Layer 3?

Layer 3 manages a case.

Use this wording:

```text
Layer 3 uses CMMN-inspired concepts to represent a decision case lifecycle.
It does not claim full CMMN engine compliance.
```

### Why DMN-like rules again in Layer 4?

Layer 4 consolidates decision logic.

Use this wording:

```text
Layer 4 uses DMN-like decision rules to consolidate priority,
execution mode and recommendation constraints.
This is different from Layer 2, where the rules derive contextual factors.
```

### Why Layer 5?

Layer 5 prevents the final output from being just a model response.

Use this wording:

```text
Layer 5 packages the final recommendation with evidence, comparison metadata,
traceability and reviewer-facing explanation.
```

## What the demo does not claim

```text
It does not implement production HTTP APIs.
It does not integrate with a real CMMS, MES, ERP or asset registry.
It does not claim formal DMN engine compliance.
It does not claim formal CMMN engine compliance.
It does not prove generative AI is better than deterministic logic.
```

## What the demo does claim

```text
It demonstrates an executable reference implementation of OVERSEE.
It shows a concrete compressor case from alert intake to governed recommendation.
It makes each layer inspectable through persisted JSON and Markdown outputs.
It compares deterministic and generative recommendation behavior.
It preserves governance, traceability and human review signals.
```

## Suggested closing statement

```text
The goal of this version is not to show a complete industrial platform.
The goal is to make the OVERSEE artifact executable, inspectable and reviewable:
one compressor case, five layers, explicit mechanisms, persisted outputs and
a governed recommendation package at the end.
```
