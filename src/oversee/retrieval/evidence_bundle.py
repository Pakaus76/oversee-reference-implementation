"""
Module: evidence_bundle.py

Purpose:
    Define the typed documentary-evidence contract used by the future real-E
    grounded condition of the rebuild.

Architectural role:
    This module provides the compact evidence structures that retrieval logic
    can return before grounded model path constructs its grounded prompt. Its role is
    intentionally narrow:
    - represent one retrieved evidence snippet
    - represent one bounded evidence bundle
    - validate the minimum integrity of that evidence bundle

Thesis traceability:
    - Chapter 5: Progression toward grounded decision support
    - Chapter 6: Bounded evidence-informed artefact evolution
    - Chapter 7: Minimal retrieval-side infrastructure for lightweight grounding
    - Chapter 8: Future D-versus-E comparison under controlled conditions

Inputs:
    Evidence metadata and snippet text produced by retrieval helpers.

Outputs:
    - EvidenceSnippet instances
    - EvidenceBundle instances

Key assumptions:
    - The first grounded model path condition should use a small, explicit, and inspectable
      evidence bundle.
    - Evidence must remain local, curated, and traceable.
    - This module validates evidence structure, not retrieval relevance.

Dependencies:
    - dataclasses

Notes:
    - This module does not perform retrieval by itself.
    - This module does not call the model.
    - This module should remain stable and compact so that grounded model path can rely
      on a clear evidence contract.
"""

from __future__ import annotations

from dataclasses import dataclass


class EvidenceBundleError(ValueError):
    """
    Represent an integrity error in the retrieval evidence contract.

    Why this exists:
        The future real-E condition will rely on documentary evidence as part of
        its bounded grounding path. The repository therefore needs a readable
        and specific error whenever evidence structure is empty, malformed, or
        internally inconsistent.
    """


@dataclass(frozen=True, slots=True)
class EvidenceSnippet:
    """
    Store one retrieved documentary evidence snippet.

    Args:
        snippet_id: Unique identifier of the retrieved snippet.
        source_path: Repository-relative or otherwise traceable source path.
        title: Short readable evidence title.
        content: Non-empty snippet text passed into the grounded prompt.

    Returns:
        EvidenceSnippet: Typed snippet ready for inclusion in an evidence
        bundle.

    Raises:
        EvidenceBundleError: If any required field is empty.
    """

    snippet_id: str
    source_path: str
    title: str
    content: str

    def __post_init__(self) -> None:
        """
        Validate the minimum structural integrity of the snippet.
        """
        if not self.snippet_id.strip():
            raise EvidenceBundleError("snippet_id must not be empty.")

        if not self.source_path.strip():
            raise EvidenceBundleError("source_path must not be empty.")

        if not self.title.strip():
            raise EvidenceBundleError("title must not be empty.")

        if not self.content.strip():
            raise EvidenceBundleError("content must not be empty.")


@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    """
    Store one bounded set of documentary evidence snippets for grounded model path.

    Args:
        source_name: Human-readable name of the bounded evidence source.
        snippets: Non-empty tuple of retrieved evidence snippets.

    Returns:
        EvidenceBundle: Typed bounded evidence package for grounded prompting.

    Raises:
        EvidenceBundleError: If the bundle is empty or structurally invalid.
    """

    source_name: str
    snippets: tuple[EvidenceSnippet, ...]

    def __post_init__(self) -> None:
        """
        Validate the minimum integrity of the evidence bundle.
        """
        if not self.source_name.strip():
            raise EvidenceBundleError("source_name must not be empty.")

        if not self.snippets:
            raise EvidenceBundleError("Evidence bundle must contain at least one snippet.")

        snippet_ids: set[str] = set()

        for snippet in self.snippets:
            if snippet.snippet_id in snippet_ids:
                raise EvidenceBundleError(
                    "Evidence bundle must not contain duplicate snippet_id values."
                )

            snippet_ids.add(snippet.snippet_id)


def render_evidence_bundle_for_prompt(evidence_bundle: EvidenceBundle) -> str:
    """
    Render one bounded evidence bundle into a compact prompt-ready text block.

    Args:
        evidence_bundle: Typed evidence bundle to serialize.

    Returns:
        str: Readable text block containing the evidence snippets.

    Side effects:
        None.

    Notes:
        This helper keeps the evidence representation explicit and inspectable.
        Prompt construction in grounded model path can therefore rely on one stable
        serialization format rather than rebuilding it ad hoc.
    """
    rendered_parts: list[str] = [
        f"Evidence source: {evidence_bundle.source_name}",
        "Retrieved evidence snippets:",
    ]

    for snippet in evidence_bundle.snippets:
        rendered_parts.append(
            (
                f"- [{snippet.snippet_id}] {snippet.title} "
                f"(source: {snippet.source_path})\n"
                f"  {snippet.content}"
            )
        )

    return "\n".join(rendered_parts).strip()