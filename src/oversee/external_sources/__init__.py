"""External source simulation layer for OVERSEE.

This package exposes Digital Factory information as external source payloads.
It intentionally avoids old bridge terminology. The purpose is to make Layer 1
explicit: information enters OVERSEE as if it came from industrial systems.
"""

from oversee.external_sources.compressor_external_source_factory import (
    build_compressor_external_source_package,
)
from oversee.external_sources.external_source_contracts import (
    ExternalSourcePackage,
    ExternalSourcePayload,
)

__all__ = [
    "ExternalSourcePackage",
    "ExternalSourcePayload",
    "build_compressor_external_source_package",
]
