# Changelog

## 2026-06-02 â€” Reviewer-facing OVERSEE package

- Archived the provisional scaffold under `paper_artifacts/provisional_scaffold_archive/`.
- Created the final `src/oversee/` package structure using current OVERSEE terminology.
- Migrated real domain contracts into `src/oversee/domain/`.
- Migrated the deterministic recommendation path as `deterministic_anchor`.
- Migrated the original Digital Factory scenario pipeline into `src/oversee/digital_factory/`.
- Connected Digital Factory scenarios to the deterministic anchor.
- Migrated the model-backed anchor, grounded model path, live generative path, payload parsers, retrieval layer, settings and model client.
- Added `knowledge_base/maintenance_guidance_seed.md` with retriever-compatible evidence snippets.
- Connected Digital Factory scenarios to the live generative path in offline-safe mode.
- Added deterministic-versus-generative comparison outputs in JSON and CSV.
- Added reviewer-facing package generation with:
  - reviewer summary;
  - execution manifest;
  - traceability index;
  - file-level checksums.
- Validated offline-safe behavior:
  - 3 Digital Factory cases;
  - 3 deterministic anchor recommendations;
  - 3 live generative path recommendations;
  - 3 fallback activations in offline mode;
  - no action differences;
  - no priority differences;
  - 3 rationale differences.
- Removed legacy terminology from active `src/oversee/` Python files.
## 2026-06-02

- Created clean OVERSEE reference implementation repository.
- Added COMP-001 industrial air compressor seed case.
- Added CMMN-inspired case states and milestones.
- Implemented strict Pydantic data models.
- Implemented JSON, Markdown, CSV, and output-folder utilities.
- Implemented traceability registry.
- Implemented simulated enterprise services:
  - predictive alert service
  - sensor data service
  - maintenance history service
  - operational context service
  - asset registry service
  - inventory and resource service
  - policy service
- Implemented CMMN-inspired case-state tracker and lifecycle trace builder.
- Implemented generic DMN-like decision table engine.
- Added contextualization, action eligibility, action ranking, and governance validation decision tables.
- Added bounded action catalogue.
- Implemented Layer 1: evidence ingestion and normalization.
- Implemented Layer 2: contextualization.
- Implemented Layer 3: deliberation and alternative evaluation.
- Implemented Layer 4: governance and review.
- Implemented Layer 5: decision-oriented output and persistence.
- Implemented full pipeline orchestration.
- Implemented command-line demo runner.
- Verified that the full demo generates all expected artifacts.

