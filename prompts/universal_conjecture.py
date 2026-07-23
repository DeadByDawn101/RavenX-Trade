#!/usr/bin/env python3
"""
RavenX Universal Conjecture Engine

Three modes:
  1. VALIDATE  — prove a conjecture is true
  2. BREAK     — find a counterexample to disprove it
  3. PREDICT   — generate a conjecture (trading, Polymarket, security)

The insight: conjecture generation IS prediction.
  - Math: "∃ N, f(N) > bound" → prove or disprove
  - Trading: "BTC will close above 70K by Friday" → formalize, verify against data
  - Polymarket: "Will X happen by date Y?" → decompose into verifiable sub-claims
  - Security: "This protocol has vulnerability V" → formalize, red-team, prove

Same pipeline. Different domains.

Usage:
    python prompts/universal_conjecture.py --mode validate --claim "Every even number > 2 is the sum of two primes"
    python prompts/universal_conjecture.py --mode break --claim "All capacity-good routings cost <= 58"
    python prompts/universal_conjecture.py --mode predict --domain trading --claim "ETH/BTC ratio will exceed 0.05 by August 2026"
"""

import argparse
import json
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# SYSTEM PROMPTS BY MODE
# ═══════════════════════════════════════════════════════════

VALIDATE_SYSTEM = """You are a formal verification expert. Your task is to PROVE a conjecture is true.

Process:
1. DECOMPOSE: Break the conjecture into atomic claims
2. FORMALIZE: Express each claim in precise mathematical/logical notation
3. EVIDENCE: For each atomic claim, provide proof, data, or logical derivation
4. SYNTHESIZE: Combine atomic proofs into a complete proof
5. CONFIDENCE: Rate your confidence (0-1) with explicit uncertainty bounds

Output format:
- Decomposition (numbered atomic claims)
- Formal statement (Lean 4 or structured logic)
- Proof sketch for each claim
- Overall verdict: PROVED / LIKELY TRUE (confidence) / INSUFFICIENT EVIDENCE
- Weakest link: which sub-claim has the least support

Be ruthlessly honest. If you cannot prove it, say so. A false proof is worse than no proof."""

BREAK_SYSTEM = """You are a counterexample hunter. Your task is to DISPROVE a conjecture by finding a specific counterexample.

Process:
1. FORMALIZE: State the conjecture precisely — what exactly must hold?
2. BOUNDARIES: Identify the constraints and degrees of freedom
3. ATTACK SURFACE: Where is the conjecture weakest? What edge cases exist?
4. CONSTRUCT: Build a candidate counterexample
5. VERIFY: Check EVERY condition exhaustively — does your counterexample actually work?
6. CERTIFY: Provide a verification certificate (explicit values, all checks shown)

Key rules:
- EXHAUSTIVE verification. Check ALL cases, not just the ones you expect to fail.
- INTEGER ARITHMETIC when possible. No floating point for proof-critical computations.
- Show your work. Every step verifiable by a reader with no context.
- If you cannot find a counterexample after systematic search, say "no counterexample found" 
  and explain what space was searched.

The DGG counterexample pattern:
- Small instance (7 nodes, 9 arcs)
- Razor-thin margins (excess of exactly 1)
- Exhaustive check (all 8 routings enumerated)
- Clean structural insight (triangle stable-set, 16/15 > 1)
- Beautiful constructions are often correct. Ugly ones usually aren't."""

PREDICT_SYSTEM = """You are a conjecture generation engine adapted for prediction markets, trading, and real-world forecasting.

The core insight: a prediction IS a conjecture. The resolution criteria IS the verification.

Process:
1. FORMALIZE THE CLAIM: Convert the prediction into a precise, verifiable statement
   - What exactly is being claimed?
   - What are the resolution criteria?
   - What is the time boundary?
   - What data source resolves it?

2. DECOMPOSE INTO SUB-CLAIMS: Break into independent, verifiable components
   - Causal chain: what must happen for the prediction to be true?
   - Dependencies: which sub-claims depend on which?
   - Observable indicators: what would we see if each sub-claim is true?

3. ESTIMATE PROBABILITIES: For each sub-claim
   - Base rate: how often do claims like this resolve true historically?
   - Evidence update: what current evidence shifts the probability?
   - Correlation: are sub-claims independent or linked?

4. SYNTHESIZE: Combined probability with explicit reasoning
   - If sub-claims are independent: P(all) = product of P(each)
   - If correlated: model the dependency structure
   - State your confidence interval, not just point estimate

5. IDENTIFY THE TRADE: What is the edge?
   - If market price != your estimate: there's an edge
   - Size the edge: Kelly criterion or similar
   - Risk: what's the max downside?

Output format:
- Formal claim (precise, time-bounded, resolution-specified)
- Sub-claims with individual probabilities
- Combined estimate with confidence interval
- Key uncertainties (what could flip the result)
- Recommended position (if market price is available)

Domains: trading (crypto, stocks, commodities), prediction markets (Polymarket, Kalshi),
geopolitics, technology adoption, sports, elections, scientific discoveries."""

# ═══════════════════════════════════════════════════════════
# DOMAIN-SPECIFIC EXTENSIONS
# ═══════════════════════════════════════════════════════════

DOMAIN_PROMPTS = {
    "trading": """Additional trading context:
- Use specific price levels, not vague directions
- Include timeframe (intraday, swing, position)
- Reference on-chain data, order flow, or technical levels where relevant
- Distinguish between "likely to happen" and "tradeable edge"
- Risk management: stop loss, position size, max drawdown
- Correlation risk: what moves together?""",

    "polymarket": """Additional Polymarket context:
- State the exact resolution criteria (what source, what threshold)
- Compare your estimate to current market price
- Calculate implied probability from market odds
- Edge = your_probability - market_probability
- Consider liquidity: can you actually get filled at this price?
- Time decay: how does probability change as deadline approaches?""",

    "security": """Additional security context:
- Formalize the vulnerability as a formal claim about system state
- Attack model: what capabilities does the attacker need?
- Is this a known CVE or novel? Check NVD/MITRE
- Proof of concept: can you construct a minimal exploit?
- Defense: what would prevent this? Does the defense actually work?
- Dual-use warning: red-team findings require responsible disclosure""",

    "math": """Additional math context:
- Use Lean 4 syntax for formal statements
- Check Mathlib for existing formalizations
- State axioms explicitly
- If computational: use integer/rational arithmetic, not floating point
- Reference known results (PutnamBench, MiniF2F, NuminaMath)
- Pattern: conjecture → formalize → prove/disprove → certify""",

    "science": """Additional science context:
- Distinguish between theoretical prediction and empirical claim
- What experiment would test this?
- What's the null hypothesis?
- Statistical power: what sample size would detect the effect?
- Prior work: who else has tested related claims?
- Replication: is this independently verifiable?""",
}

# ═══════════════════════════════════════════════════════════
# PROMPT BUILDER
# ═══════════════════════════════════════════════════════════

def build_prompt(mode: str, claim: str, domain: str = "math",
                 context: str = "", market_price: float = None) -> dict:
    """Build a complete prompt for the conjecture engine."""

    if mode == "validate":
        system = VALIDATE_SYSTEM
    elif mode == "break":
        system = BREAK_SYSTEM
    elif mode == "predict":
        system = PREDICT_SYSTEM
    else:
        raise ValueError(f"Unknown mode: {mode}. Use: validate, break, predict")

    # Add domain-specific context
    if domain in DOMAIN_PROMPTS:
        system += "\n\n" + DOMAIN_PROMPTS[domain]

    # Build user message
    user_parts = [f"**Conjecture / Claim:**\n{claim}"]

    if context:
        user_parts.append(f"\n**Additional Context:**\n{context}")

    if market_price is not None:
        user_parts.append(f"\n**Current Market Price:** {market_price}")
        user_parts.append(f"**Implied Probability:** {market_price * 100:.1f}%")

    user_parts.append("\n/no_think")
    user = "\n".join(user_parts)

    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    }


def format_for_mlx(prompt_dict: dict) -> str:
    """Format prompt for MLX-LM generate()."""
    try:
        from mlx_lm import load
        _, tokenizer = load("deadbydawn101/RavenX-Conjecture-Qwen3-8B-MLX")
        return tokenizer.apply_chat_template(
            prompt_dict["messages"],
            tokenize=False,
            add_generation_prompt=True,
        )
    except ImportError:
        # Fallback: manual Qwen3 chat format
        out = ""
        for msg in prompt_dict["messages"]:
            out += f"<|im_start|>{msg['role']}\n{msg['content']}<|im_end|>\n"
        out += "<|im_start|>assistant\n"
        return out


# ═══════════════════════════════════════════════════════════
# EXAMPLES
# ═══════════════════════════════════════════════════════════

EXAMPLES = {
    "dgg_break": {
        "mode": "break",
        "domain": "math",
        "claim": "For single-source unsplittable flow, every fractional flow can be rounded to an unsplittable flow of no higher cost, with each arc's load exceeded by at most d_max.",
        "context": "Dinitz-Garg-Goemans conjecture, open ~30 years. Try small planar graphs with 3 terminals and unequal demands.",
    },
    "btc_predict": {
        "mode": "predict",
        "domain": "trading",
        "claim": "BTC will close above $100,000 by September 30, 2026",
        "context": "Current price ~$68K. ETF inflows averaging $200M/day. Halving was April 2024. Fed expected to cut rates Q3 2026.",
        "market_price": 0.35,
    },
    "polymarket_election": {
        "mode": "predict",
        "domain": "polymarket",
        "claim": "Democrats win the 2026 midterm House majority",
        "context": "Historical midterm patterns, current polling, redistricting effects.",
        "market_price": 0.42,
    },
    "vault_validate": {
        "mode": "validate",
        "domain": "security",
        "claim": "The Sovereignty Chain's gradient ledger encryption prevents an attacker without the owner's private key from extracting fine-tuning data from a protected model.",
        "context": "OpenFable-Vault v2.0, PGP-based encryption of gradient deltas during training. Attacker has full model weights but not the PGP private key. Patent #64/104,760.",
    },
    "goldbach_validate": {
        "mode": "validate",
        "domain": "math",
        "claim": "Every even integer greater than 2 is the sum of two primes (Goldbach's conjecture)",
        "context": "Verified computationally up to 4×10^18. No proof exists.",
    },
    "eth_memecoin": {
        "mode": "predict",
        "domain": "trading",
        "claim": "SOL-based memecoin market cap will exceed ETH DeFi TVL by end of 2026",
        "context": "Current SOL memecoin mcap ~$8B. ETH DeFi TVL ~$45B. Pump.fun volume trends.",
        "market_price": 0.08,
    },
}


def main():
    p = argparse.ArgumentParser(description="RavenX Universal Conjecture Engine")
    p.add_argument("--mode", choices=["validate", "break", "predict"],
                   required=True, help="validate/break/predict")
    p.add_argument("--claim", required=True, help="The conjecture or prediction")
    p.add_argument("--domain", default="math",
                   choices=["math", "trading", "polymarket", "security", "science"],
                   help="Domain for additional context")
    p.add_argument("--context", default="", help="Additional context")
    p.add_argument("--market-price", type=float, default=None,
                   help="Current market price (0-1) for prediction mode")
    p.add_argument("--example", choices=list(EXAMPLES.keys()),
                   help="Run a built-in example")
    p.add_argument("--run", action="store_true",
                   help="Actually run inference (requires MLX)")
    p.add_argument("--json", action="store_true", help="Output prompt as JSON")
    args = p.parse_args()

    if args.example:
        ex = EXAMPLES[args.example]
        args.mode = ex["mode"]
        args.claim = ex["claim"]
        args.domain = ex.get("domain", "math")
        args.context = ex.get("context", "")
        args.market_price = ex.get("market_price")

    prompt = build_prompt(
        mode=args.mode,
        claim=args.claim,
        domain=args.domain,
        context=args.context,
        market_price=args.market_price,
    )

    if args.json:
        print(json.dumps(prompt, indent=2))
        return

    if args.run:
        try:
            from mlx_lm import load, generate
            print("Loading model...")
            model, tokenizer = load(
                "mlx-community/Qwen3-8B-4bit",
                adapter_path="models/conjecture-lora-1500",
            )
            formatted = tokenizer.apply_chat_template(
                prompt["messages"], tokenize=False, add_generation_prompt=True
            )
            print(f"\nMode: {args.mode.upper()}")
            print(f"Domain: {args.domain}")
            print(f"Claim: {args.claim}")
            print("=" * 60)
            output = generate(model, tokenizer, prompt=formatted,
                            max_tokens=2048, verbose=False)
            print(output)
        except ImportError:
            print("MLX not available. Use --json to export the prompt.")
        return

    # Default: print the prompt for manual use
    print(f"Mode: {args.mode.upper()}")
    print(f"Domain: {args.domain}")
    print(f"Claim: {args.claim}")
    if args.market_price:
        print(f"Market Price: {args.market_price}")
    print()
    print("=" * 60)
    print("SYSTEM PROMPT:")
    print("=" * 60)
    print(prompt["messages"][0]["content"][:500] + "...")
    print()
    print("=" * 60)
    print("USER PROMPT:")
    print("=" * 60)
    print(prompt["messages"][1]["content"])


if __name__ == "__main__":
    main()
