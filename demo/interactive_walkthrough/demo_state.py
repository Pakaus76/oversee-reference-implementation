"""Runtime state for the interactive OVERSEE walkthrough."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from demo.interactive_walkthrough.scenario_catalog import DemoScenario


@dataclass
class DemoRunState:
    """State shared across walkthrough steps."""

    scenario: DemoScenario
    output_dir: Path
    generated_artifacts: dict[str, Path] = field(default_factory=dict)
    layer_outputs: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def record_artifact(self, key: str, path: Path) -> None:
        """Register a generated artifact path."""
        self.generated_artifacts[key] = path

    def record_layer_output(self, layer_id: str, summary: str) -> None:
        """Register the paper-facing output summary for a layer."""
        self.layer_outputs[layer_id] = summary

    def to_manifest(self) -> dict[str, Any]:
        """Return a serializable manifest for the demo run."""
        return {
            "scenario_id": self.scenario.scenario_id,
            "scenario_title": self.scenario.title,
            "asset_id": self.scenario.asset_id,
            "asset_type": self.scenario.asset_type,
            "failure_mode": self.scenario.failure_mode,
            "paper_aligned": self.scenario.paper_aligned,
            "output_dir": str(self.output_dir),
            "generated_artifacts": {
                key: str(path) for key, path in self.generated_artifacts.items()
            },
            "layer_outputs": self.layer_outputs,
            "notes": self.notes,
        }
