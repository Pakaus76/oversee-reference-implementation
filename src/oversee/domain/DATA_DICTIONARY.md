# Domain Data Dictionary

## Purpose
Provide a compact reference for the current domain entities, contracts, and semantic fields used in the rebuild.

## Scope
This dictionary documents only what is currently implemented in the domain layer.
It must be updated incrementally as the domain evolves.

## Current entities

### Asset
| Field | Type | Meaning |
|---|---|---|
| asset_id | str | Unique identifier of the asset |
| asset_type | str | Broad asset category |
| criticality | int | Integer criticality level |
| location | Optional[str] | Optional asset location label |

### PredictiveAlert
| Field | Type | Meaning |
|---|---|---|
| alert_id | str | Unique identifier of the predictive alert |
| asset_id | str | Identifier of the affected asset |
| predicted_issue | str | Short textual description of the predicted issue |
| time_to_failure_hours | Optional[float] | Estimated time to failure in hours |
| confidence_score | Optional[float] | Optional numeric confidence estimate |

### Recommendation
| Field | Type | Meaning |
|---|---|---|
| recommendation_id | str | Unique identifier of the recommendation |
| asset_id | str | Identifier of the affected asset |
| action | str | Recommended action in plain English |
| rationale | str | Short justification |
| priority | str | Priority label for comparison purposes |

### InterventionRequest
| Field | Type | Meaning |
|---|---|---|
| request_id | str | Unique identifier of the intervention request |
| asset_id | str | Identifier of the affected asset |
| requested_action | str | Operational action to be executed |
| priority | str | Priority label |
| justification | str | Short textual reason for the request |

### DecisionCase
| Field | Type | Meaning |
|---|---|---|
| case_id | str | Unique identifier of the decision case |
| asset | Asset | Typed asset involved in the case |
| alert | PredictiveAlert | Predictive alert associated with the case |
| context_note | Optional[str] | Optional additional case note |

## Current enumerations

### PriorityLevel
- low
- medium
- high

### RiskLevel
- low
- medium
- high
- critical

### ConfidenceLevel
- low
- medium
- high

## Notes
- This dictionary reflects the current implemented baseline only.
- Some fields still use plain strings and may later be tightened through direct enum usage.
- This file exists to reduce semantic drift across implementation, evaluation, and documentation layers.

## Thesis traceability

### Related thesis sections
- Chapter 5:
- Chapter 6:
- Chapter 7:
- Chapter 8:

### Why this artifact exists
This file makes the current semantic backbone explicit in a documentation-friendly form.

### What thesis promise it supports
It supports implementation clarity, traceability, and controlled evolution of the artefact data model.

### Demonstration scope status
- In scope for demonstration in the current rebuild
