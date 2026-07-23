# Conjecture-Trading Dataset

Training data for the RavenX prediction/trading model using the
Universal Conjecture Engine methodology.

## Format

Each example is a prediction formalized as a conjecture:

```json
{
  "messages": [
    {"role": "system", "content": "You are a prediction engine..."},
    {"role": "user", "content": "Claim: BTC > 100K by Sept 2026\nMarket Price: 0.35"},
    {"role": "assistant", "content": "FORMAL CLAIM: ...\nSUB-CLAIMS: ...\nPROBABILITY: ...\nEDGE: ..."}
  ],
  "metadata": {
    "domain": "trading",
    "asset": "BTC",
    "resolved": true,
    "outcome": true,
    "timestamp": "2026-07-22"
  }
}
```

## Data Sources (Tomorrow's Build)

1. **Polymarket historical resolutions** — resolved markets with outcomes
2. **Crypto price data** — OHLCV + on-chain (Dune, Flipside)
3. **Prediction market odds history** — Kalshi, Polymarket, Metaculus
4. **Macro data** — Fed rates, CPI, employment, earnings
5. **NuminaMath-LEAN** — mathematical reasoning foundation (already trained)

## Pipeline

Same as ConjectureBench but for markets:
1. Conjecture = Prediction
2. Formalization = Resolution criteria
3. Verification = Did it resolve true/false?
4. Training signal = was the probability estimate accurate?

See: [ravenx-conjecturebench](https://github.com/DeadByDawn101/ravenx-conjecturebench)
