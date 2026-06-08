"""Case management layer for OVERSEE.

Layer 3 provides a CMMN-inspired lifecycle for the compressor case. It is not a
full CMMN engine. It is an explicit, inspectable case-management representation
showing how the case progresses from evidence intake to decision readiness.
"""

from oversee.case_management.case_lifecycle import (
    CaseLifecycleEvent,
    CaseManagementState,
    CaseMilestone,
    CaseTask,
)
from oversee.case_management.case_lifecycle_builder import build_case_management_state

__all__ = [
    "CaseLifecycleEvent",
    "CaseManagementState",
    "CaseMilestone",
    "CaseTask",
    "build_case_management_state",
]
