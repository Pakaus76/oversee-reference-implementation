# domain

## Purpose
Store the core typed entities and contracts of the rebuilt system.

## Why it exists
This folder defines the semantic backbone of the repository so that ingestion, benchmark generation, DO conditions, governance, evaluation, and reporting can all depend on stable domain structures instead of ad hoc dictionaries.

## Contents
This folder will progressively contain:
- core entities
- typed recommendation contracts
- intervention-related contracts
- validation-oriented domain structures
- domain enumerations where needed

## What must not be stored here
- CSV loading logic
- benchmark generation logic
- experiment-specific code
- reporting code
- thin script wrappers

## Inputs
- conceptual requirements of the Decision Orchestrator
- benchmark and evaluation needs
- thesis-driven artefact definitions

## Outputs
- stable typed structures for the rest of the repository
- reusable contracts for later implementation layers

## Thesis traceability
Supports Chapters 5 to 8 by defining the core entities on which the rebuilt artefact and its evaluation will depend.

## Notes
This folder should be implemented before substantive DO logic so that later layers depend on stable contracts rather than on informal structures.
