"""Digital Factory package for OVERSEE.

The Digital Factory provides synthetic industrial cases and, in the advanced
workbench, can also use live generative AI to produce source-level payloads that
enter OVERSEE through Layer 1.

The generative source factory is imported lazily to avoid circular imports with
the Layer 1 external source package.
"""

from oversee.digital_factory.compressor_scenario_generator import generate_compressor_scenarios
from oversee.digital_factory.deterministic_anchor_adapter import evaluate_deterministic_anchor_candidates
from oversee.digital_factory.live_generative_path_adapter import evaluate_live_generative_path_candidates
from oversee.digital_factory.oversee_input_mapper import map_bridge_ready_payloads_to_oversee_inputs
from oversee.digital_factory.scenario_bridge_adapter import build_bridge_ready_payloads

__all__ = [
    "GenerativeDigitalFactoryResult",
    "build_bridge_ready_payloads",
    "evaluate_deterministic_anchor_candidates",
    "evaluate_live_generative_path_candidates",
    "generate_compressor_scenarios",
    "map_bridge_ready_payloads_to_oversee_inputs",
    "run_generative_digital_factory_source_generation",
]


def __getattr__(name: str):
    """Lazily expose Generative Digital Factory symbols."""

    if name in {
        "GenerativeDigitalFactoryResult",
        "run_generative_digital_factory_source_generation",
    }:
        from oversee.digital_factory.generative_external_source_factory import (
            GenerativeDigitalFactoryResult,
            run_generative_digital_factory_source_generation,
        )

        mapping = {
            "GenerativeDigitalFactoryResult": GenerativeDigitalFactoryResult,
            "run_generative_digital_factory_source_generation": (
                run_generative_digital_factory_source_generation
            ),
        }
        return mapping[name]

    raise AttributeError(f"module 'oversee.digital_factory' has no attribute {name!r}")
