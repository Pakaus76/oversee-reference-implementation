"""
Module: intervention.py

Purpose:
    Define the intervention request contract used by complementary operational
    layers such as simulation_v1 and later governed execution-oriented flows.

Architectural role:
    This module provides a typed operational request structure that remains
    separate from the high-level recommendation contract.

Thesis traceability:
    - Chapter 5: Decision to action transition
    - Chapter 6: Artefact outputs and controlled experimentation
    - Chapter 7: Operational implementation baseline
    - Chapter 8: Execution-oriented evaluation support

Inputs:
    Intervention attributes created by later translation or operational layers.

Outputs:
    InterventionRequest instances that can support simulation or governed
    execution-oriented workflows.

Key assumptions:
    This initial contract is intentionally lightweight and should only grow when
    later workbench needs are explicit and documented.

Dependencies:
    dataclasses

Notes:
    The intervention contract is complementary and does not replace the DO as
    the principal artefact of the thesis.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class InterventionRequest:
    """
    Represent an operational intervention request.

    Args:
        request_id: Unique identifier of the intervention request.
        asset_id: Identifier of the affected asset.
        requested_action: Operational action to be executed.
        priority: Priority label used by later operational layers.
        justification: Short textual reason for the request.

    Returns:
        InterventionRequest: Typed intervention request instance.

    Side effects:
        None.

    Raises:
        ValueError: If identifiers or required textual fields are empty.
    """

    request_id: str
    asset_id: str
    requested_action: str
    priority: str
    justification: str

    def __post_init__(self) -> None:
        """Validate the minimum integrity of the intervention request."""
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty.")
        if not self.asset_id.strip():
            raise ValueError("asset_id must not be empty.")
        if not self.requested_action.strip():
            raise ValueError("requested_action must not be empty.")
        if not self.priority.strip():
            raise ValueError("priority must not be empty.")
        if not self.justification.strip():
            raise ValueError("justification must not be empty.")

