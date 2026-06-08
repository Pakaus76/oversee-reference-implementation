"""Decision rules layer for OVERSEE.

Layer 4 evaluates explicit DMN-like rules and connects them to recommendation
paths. This is not a full DMN engine. It is an inspectable decision-table-style
implementation that makes rule inputs, rule outputs and triggered logic visible.
"""

from oversee.decision_rules.decision_rule_contracts import (
    DecisionRuleEvaluation,
    RecommendationPathBundle,
    RecommendationPathOutput,
    RuleEvaluation,
)
from oversee.decision_rules.dmn_like_rules import evaluate_dmn_like_rules
from oversee.decision_rules.live_generative_recommendation import (
    LiveGenerativeRecommendationResult,
    run_live_generative_recommendation,
)
from oversee.decision_rules.recommendation_path_runner import run_recommendation_paths

__all__ = [
    "DecisionRuleEvaluation",
    "LiveGenerativeRecommendationResult",
    "RecommendationPathBundle",
    "RecommendationPathOutput",
    "RuleEvaluation",
    "evaluate_dmn_like_rules",
    "run_live_generative_recommendation",
    "run_recommendation_paths",
]
