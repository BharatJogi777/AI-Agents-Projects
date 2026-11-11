import argparse
import json

from app.budget import BudgetConfig, BudgetPlanner, ContextItem
from app.token_counting import HeuristicTokenCounter


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan context items under an estimated token budget")
    parser.add_argument("--context-window", type=int, default=8192)
    parser.add_argument("--output-reserve", type=int, default=1024)
    parser.add_argument("--safety-margin", type=int, default=256)
    parser.add_argument("--chars-per-token", type=float, default=4.0)
    args = parser.parse_args()

    planner = BudgetPlanner(
        HeuristicTokenCounter(chars_per_token=args.chars_per_token),
        BudgetConfig(
            context_window_tokens=args.context_window,
            reserved_output_tokens=args.output_reserve,
            safety_margin_tokens=args.safety_margin,
            per_item_overhead_tokens=4,
        ),
    )
    items = [
        ContextItem("system", "system", "You are a careful backend engineering assistant.", 100, True),
        ContextItem("current-user", "user", "Explain why the checkout API latency increased.", 100, True),
        ContextItem("recent-history", "history", "We recently deployed version 2.4 and saw p95 latency rise.", 50),
        ContextItem("old-history", "history", "Earlier we discussed unrelated database indexing work.", 10),
        ContextItem("retrieved-runbook", "retrieval", "Check recent deploys, dependency latency, saturation, and error rates.", 30),
        ContextItem("tool-output", "tool", "Deployment completed at 10:42 UTC; three pods restarted.", 40),
    ]
    plan = planner.plan(items)

    print(json.dumps({
        "token_counting_mode": "heuristic_estimate",
        "warning": "Counts are approximate; use the target model tokenizer for production.",
        "available_input_tokens": plan.available_input_tokens,
        "estimated_input_tokens": plan.estimated_input_tokens,
        "remaining_input_tokens": plan.remaining_input_tokens,
        "included": [
            {"id": entry.item.item_id, "kind": entry.item.kind, "estimated_tokens": entry.estimated_tokens}
            for entry in plan.included
        ],
        "dropped": [
            {"id": entry.item.item_id, "kind": entry.item.kind, "estimated_tokens": entry.estimated_tokens}
            for entry in plan.dropped
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
