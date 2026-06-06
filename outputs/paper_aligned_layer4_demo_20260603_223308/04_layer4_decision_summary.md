# Paper-aligned Layer 4 decision and recommendation summary

## Purpose

Layer 4 consolidates the contextualized case into decision and recommendation logic. This layer uses DMN-like decision rules, a deterministic anchor path and a live generative recommendation path.

## Difference from Layer 2

- Layer 2 DMN-like rules derive contextual decision factors from evidence.
- Layer 4 DMN-like rules consolidate priority, constraints and recommendation logic.

## Decision result

- Final priority: high
- Recommended execution mode: controlled_planning
- Recommendation paths: 2

## Generative path

- Model call attempted: True
- Model call successful: True
- Fallback used: False

## Deterministic vs generative comparison

- Priority alignment: True
- Action alignment: different
- Protected fact violations: 0

## Interpretation

The generative recommendation is not treated as an uncontrolled final answer. It is compared against a deterministic anchor and checked against protected facts and governance constraints.
