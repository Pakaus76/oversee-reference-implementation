"""Contracts for OVERSEE external source payloads.

Layer 1 represents information as coming from external industrial systems. The
objects in this module are intentionally small and serializable so each payload
can be inspected as evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ExternalSourcePayload:
    """One payload produced by one simulated external industrial source."""

    source_name: str
    source_system: str
    source_type: str
    endpoint: str
    generated_at: str
    case_id: str
    asset_id: str
    line_id: str | None
    raw_payload: dict[str, Any] = field(default_factory=dict)
    normalized_fields: dict[str, Any] = field(default_factory=dict)
    data_quality_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class ExternalSourcePackage:
    """Collection of external source payloads for one industrial case."""

    package_id: str
    case_id: str
    asset_id: str
    line_id: str | None
    created_at: str
    payloads: list[ExternalSourcePayload]
    package_version: str = "0.1.0"

    @property
    def source_count(self) -> int:
        """Return the number of source payloads included in the package."""

        return len(self.payloads)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        data = asdict(self)
        data["source_count"] = self.source_count
        return data
