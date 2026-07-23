#!/usr/bin/env python3
"""Download resolved Polymarket data for conjecture-trading training.

Polymarket CLOB API: https://docs.polymarket.com/
Gamma Markets API for historical resolution data.

Tomorrow's build: pull resolved markets, extract resolution criteria,
build training examples in conjecture format.
"""

import json
import requests
from pathlib import Path
from datetime import datetime


def fetch_resolved_markets(limit: int = 100) -> list:
    """Fetch recently resolved markets from Polymarket."""
    # Polymarket Gamma API endpoint for resolved markets
    url = "https://gamma-api.polymarket.com/markets"
    params = {
        "limit": limit,
        "active": False,  # resolved only
        "closed": True,
    }
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        markets = resp.json()
        print(f"Fetched {len(markets)} resolved markets")
        return markets
    except Exception as e:
        print(f"Error fetching Polymarket data: {e}")
        return []


def market_to_conjecture(market: dict) -> dict:
    """Convert a Polymarket market to conjecture training format."""
    question = market.get("question", "")
    description = market.get("description", "")
    outcome = market.get("outcome", "")
    end_date = market.get("endDate", "")

    resolved_true = outcome.lower() in ["yes", "true", "1"]

    return {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a prediction engine. A prediction IS a conjecture. "
                    "FORMALIZE the claim precisely. DECOMPOSE into sub-claims. "
                    "ESTIMATE probability with base rate + evidence. "
                    "IDENTIFY the edge vs market price."
                ),
            },
            {
                "role": "user",
                "content": f"**Claim:** {question}\n**Context:** {description[:500]}\n**Deadline:** {end_date}\n/no_think",
            },
            {
                "role": "assistant",
                "content": f"RESOLUTION: {'TRUE' if resolved_true else 'FALSE'}\nOUTCOME: {outcome}",
            },
        ],
        "metadata": {
            "source": "polymarket",
            "question": question,
            "resolved": True,
            "outcome": resolved_true,
            "end_date": end_date,
            "fetched_at": datetime.utcnow().isoformat(),
        },
    }


def main():
    out_dir = Path("data/conjecture_trading")
    out_dir.mkdir(parents=True, exist_ok=True)

    markets = fetch_resolved_markets(limit=500)

    examples = []
    for m in markets:
        try:
            ex = market_to_conjecture(m)
            examples.append(ex)
        except Exception:
            continue

    out_file = out_dir / "polymarket_resolved.jsonl"
    with open(out_file, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")

    print(f"Saved {len(examples)} examples to {out_file}")

    # Stats
    true_count = sum(1 for e in examples if e["metadata"]["outcome"])
    print(f"Resolved TRUE: {true_count}/{len(examples)}")
    print(f"Resolved FALSE: {len(examples) - true_count}/{len(examples)}")
    print(f"Base rate: {true_count / len(examples) * 100:.1f}%")


if __name__ == "__main__":
    main()
