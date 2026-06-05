"""Output folder management for the interactive OVERSEE walkthrough."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def create_demo_output_dir(base_dir: str = "outputs") -> Path:
    """Create a timestamped output directory for one interactive demo run."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(base_dir) / f"interactive_demo_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=False)
    return output_dir


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write JSON data using UTF-8 without relying on external libraries."""
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_text(path: Path, text: str) -> None:
    """Write text data using UTF-8."""
    path.write_text(text, encoding="utf-8")
