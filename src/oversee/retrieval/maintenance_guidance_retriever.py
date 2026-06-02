"""
Module: maintenance_guidance_retriever.py

Purpose:
    Provide the first bounded retrieval helper for the future real-E grounded
    condition of the rebuild.

Architectural role:
    This module reads one controlled local knowledge artifact and converts it
    into a bounded evidence bundle that can later be consumed by grounded model path.
    Its role is intentionally narrow:
    - access one explicit local evidence source
    - extract a small number of guidance snippets
    - return a typed EvidenceBundle
    - remain readable, deterministic, and easy to audit

Thesis traceability:
    - Chapter 5: Progression toward grounded decision support
    - Chapter 6: Bounded evidence-informed artefact evolution
    - Chapter 7: Minimal retrieval implementation for lightweight grounding
    - Chapter 8: Future D-versus-E comparison under controlled conditions

Inputs:
    - Local repository knowledge file
    - Optional bounded max-snippet request

Outputs:
    - EvidenceBundle containing retrieved guidance snippets

Key assumptions:
    - The first grounded model path condition should use a small local evidence source only.
    - Retrieval should remain deterministic and inspectable at this stage.
    - The repository currently uses one seed file rather than a broader
      knowledge infrastructure.

Dependencies:
    - pathlib
    - src.oversee.retrieval.evidence_bundle

Notes:
    - This module does not perform semantic search.
    - This module does not call the model.
    - This module is intentionally simple so that the first grounded E layer
      can be implemented honestly without overclaiming full RAG behavior.
"""

from __future__ import annotations

from pathlib import Path

from oversee.retrieval.evidence_bundle import EvidenceBundle, EvidenceBundleError, EvidenceSnippet

DEFAULT_MAX_SNIPPETS = 3

_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_SOURCE_PATH = Path("knowledge_base/maintenance_guidance_seed.md")
DEFAULT_KNOWLEDGE_FILE = _REPO_ROOT / _DEFAULT_SOURCE_PATH


class RetrievalError(RuntimeError):
    """
    Represent a retrieval-side execution error.

    Why this exists:
        The future real-E condition will depend on one bounded documentary
        retrieval step. Retrieval failures should therefore surface through a
        readable and specific exception.
    """


def _normalize_max_snippets(max_snippets: int) -> int:
    """
    Validate and normalize the maximum number of snippets to return.

    Args:
        max_snippets: Requested maximum number of retrieved snippets.

    Returns:
        int: Validated maximum number of snippets.

    Raises:
        ValueError: If max_snippets is smaller than 1.
    """
    if max_snippets < 1:
        raise ValueError("max_snippets must be greater than or equal to 1.")

    return max_snippets


def _read_seed_file(seed_file: Path) -> str:
    """
    Read the local maintenance-guidance seed file.

    Args:
        seed_file: Absolute path to the controlled local evidence source.

    Returns:
        str: Full text of the seed file.

    Raises:
        RetrievalError: If the file does not exist or is empty.
    """
    if not seed_file.exists():
        raise RetrievalError(
            f"Knowledge file not found for retrieval: {seed_file}"
        )

    file_text = seed_file.read_text(encoding="utf-8").strip()

    if not file_text:
        raise RetrievalError(
            f"Knowledge file is empty and cannot support retrieval: {seed_file}"
        )

    return file_text


def _extract_guidance_sections(file_text: str) -> list[tuple[str, str]]:
    """
    Extract guidance sections from the seed file.

    Extraction rule:
        The current seed file contains sections under '## Guidance snippets'
        using '### <snippet id> - <title>' headings. This helper extracts each
        such section as one bounded snippet candidate.

    Args:
        file_text: Full text of the seed file.

    Returns:
        list[tuple[str, str]]: List of (heading, content) pairs.

    Raises:
        RetrievalError: If no guidance sections can be extracted.
    """
    lines = file_text.splitlines()
    collected_sections: list[tuple[str, str]] = []

    current_heading: str | None = None
    current_body_lines: list[str] = []

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("### "):
            if current_heading is not None:
                section_text = "\n".join(current_body_lines).strip()
                if section_text:
                    collected_sections.append((current_heading, section_text))

            current_heading = line[4:].strip()
            current_body_lines = []
            continue

        if current_heading is not None:
            current_body_lines.append(line)

    if current_heading is not None:
        section_text = "\n".join(current_body_lines).strip()
        if section_text:
            collected_sections.append((current_heading, section_text))

    if not collected_sections:
        raise RetrievalError(
            "No retrievable guidance sections were found in the maintenance seed file."
        )

    return collected_sections


def _split_heading(heading: str) -> tuple[str, str]:
    """
    Split one heading into snippet identifier and human-readable title.

    Expected heading format:
        'G1 - Near-failure escalation'

    Args:
        heading: Raw heading text extracted from the seed file.

    Returns:
        tuple[str, str]: (snippet_id, title)
    """
    if " - " not in heading:
        normalized_heading = heading.strip()
        return normalized_heading.lower().replace(" ", "_"), normalized_heading

    left_part, right_part = heading.split(" - ", 1)
    snippet_id = left_part.strip().lower()
    title = right_part.strip()

    return snippet_id, title


def retrieve_maintenance_guidance_bundle(
    *,
    max_snippets: int = DEFAULT_MAX_SNIPPETS,
    seed_file: Path | None = None,
) -> EvidenceBundle:
    """
    Retrieve a bounded maintenance-guidance evidence bundle from the local seed.

    Args:
        max_snippets: Maximum number of snippets to include in the evidence
            bundle.
        seed_file: Optional custom seed-file path for controlled testing.

    Returns:
        EvidenceBundle: Typed bounded documentary evidence package.

    Raises:
        ValueError: If max_snippets is invalid.
        RetrievalError: If the local evidence source cannot be read or parsed.
        EvidenceBundleError: If the resulting evidence bundle is invalid.

    Notes:
        The first implementation remains deterministic:
        it returns the first bounded set of guidance snippets in document order.
        This is intentional for the first real-E grounding step.
    """
    normalized_max_snippets = _normalize_max_snippets(max_snippets)
    resolved_seed_file = seed_file or DEFAULT_KNOWLEDGE_FILE

    file_text = _read_seed_file(resolved_seed_file)
    sections = _extract_guidance_sections(file_text)

    selected_sections = sections[:normalized_max_snippets]
    snippets: list[EvidenceSnippet] = []

    for heading, content in selected_sections:
        snippet_id, title = _split_heading(heading)

        snippets.append(
            EvidenceSnippet(
                snippet_id=snippet_id,
                source_path=str(_DEFAULT_SOURCE_PATH).replace("\\", "/"),
                title=title,
                content=content,
            )
        )

    return EvidenceBundle(
        source_name="maintenance_guidance_seed",
        snippets=tuple(snippets),
    )