# Situational Awareness: Trading Thesis Extraction

**Source:** Leopold Aschenbrenner, "Situational Awareness: The Decade Ahead" (June 2024)
**Purpose:** Extract actionable trading signals from macro AI thesis for RavenX-Trade model training

---

## Core Thesis Summary

The paper argues AGI arrives by 2027 and superintelligence by end of decade. The key insight for trading: **this is the largest industrial mobilization since WWII, and almost nobody is pricing it in.**

---

## Trading Signal 1: Compute Infrastructure Buildout

### The Thesis
- $10B → $100B → $1T clusters being planned
- 0.5 OOMs/year compute scaling (consistent for 15+ years)
- US electricity production must grow 10s of percent
- "Every voltage transformer that can possibly be procured"

### Actionable Positions
```
LONG (Infrastructure):
  → NVDA: GPU monopoly, every cluster needs their chips
  → AVGO: Networking (InfiniBand alternatives), custom ASICs
  → VRT/POWL: Power transformers — 2-3 year backlog
  → CEG/VST: Nuclear power (24/7 baseload for datacenters)
  → EQIX/DLR: Datacenter REITs
  → ETN/GEV: Electrical infrastructure
  → SMR/NNE: Small modular nuclear reactors

LONG (Power):
  → Uranium miners (CCJ, UEC, UUUU)
  → Natural gas (EQT, AR) — bridge fuel for datacenter power
  → Grid infrastructure (AMSC, POWI)

SHORT CANDIDATES:
  → Legacy IT services being automated
  → Companies with high AI-automatable workforce
  → Overvalued "AI wrapper" companies with no moat
```

## Trading Signal 2: The OOM Trendlines

### The Thesis
- GPT-2 → GPT-4: ~100,000x effective compute in 4 years
- Another ~100,000x expected by 2027
- Algorithmic efficiency: ~0.5 OOMs/year (100x in 4 years)
- "Unhobbling" gains unlock latent capabilities

### Actionable Positions
```
LONG (Model Developers):
  → Companies building frontier models (watch for IPOs)
  → Anthropic (private, watch secondary market)
  → Cloud providers hosting AI (AMZN/AWS, MSFT/Azure, GOOG/GCP)

TIMING SIGNALS:
  → New model release → capability jump → adoption spike → revenue
  → Benchmark saturation → next benchmark cycle
  → Each 10x compute increase = qualitative capability jump
  → Watch for "unhobbling" moments (agents, tool use, coding)

VOLATILITY PLAYS:
  → Model releases create volatility events
  → Benchmark surprises move sentiment
  → Regulatory announcements create fear/opportunity
```

## Trading Signal 3: The Intelligence Explosion

### The Thesis
- AI automating AI research = "the last invention"
- Hundreds of millions of AGIs compressing a decade of progress into 1 year
- 5+ OOMs of algorithmic progress in ~1 year once AGI hits
- "The power and peril of superintelligence would be dramatic"

### Actionable Positions
```
SCENARIO PLANNING:
  Pre-AGI (now-2027):
    → Infrastructure buildout is the trade
    → Compute providers, power, datacenter construction
    → Software companies adopting AI (productivity gains)
  
  AGI Transition (2027-2028):
    → Massive volatility event
    → Government intervention likely
    → Defense/security companies benefit (PLTR, LMT, NOC)
    → Traditional knowledge workers at risk
  
  Post-AGI (2028+):
    → Complete economic restructuring
    → Companies that adapted early win
    → Robotics becomes critical (physical world automation)
    → Energy becomes the constraining resource
```

## Trading Signal 4: National Security & The CCP Race

### The Thesis
- "An all-out race with the CCP; if we're unlucky, an all-out war"
- Labs are "handing AGI secrets to the CCP on a silver platter"
- Government AGI project ("The Project") by 2027/28
- "No startup can handle superintelligence"

### Actionable Positions
```
LONG (Defense/Security):
  → PLTR: AI defense platform, already embedded in DoD
  → LMT/NOC/RTX: Defense primes with AI divisions
  → CRWD/PANW: Cybersecurity (protecting AI infrastructure)
  → NET: Edge security + AI inference at edge
  → BKSY: Satellite imagery + AI analysis

LONG (US Onshoring):
  → TSMC Arizona fab (TSM)
  → Intel foundry services (INTC — high risk/reward)
  → US-based chip packaging (AMKR)

GEOPOLITICAL HEDGES:
  → If US-China tensions escalate → defense up, trade down
  → Taiwan risk premium on semiconductor supply chain
  → Watch for export control tightening (NVDA China revenue)
```

## Trading Signal 5: The Trillion-Dollar Cluster Economics

### The Thesis
- "The most extraordinary techno-capital acceleration"
- AI revenue growing rapidly enough to fund trillions in buildout
- Power contracts being secured for rest of decade
- "Hundreds of millions of GPUs will hum"

### Actionable Positions
```
INFRASTRUCTURE TIMELINE:
  2024-2025: GPU supply constrained → NVDA pricing power
  2025-2026: Datacenter construction boom → construction/HVAC
  2026-2027: Power grid upgrades → utility capex cycle
  2027-2028: Next-gen chips (2nm, 1.4nm) → ASML, KLAC, LRCX
  
CAPEX CHAIN:
  Chips: NVDA → AMD → custom ASICs (AVGO, MRVL)
  Memory: SK Hynix, Samsung, Micron (HBM)
  Networking: AVGO, ANET, CSCO
  Power: VRT, POWL, ETN, CEG, VST
  Cooling: VRT, JCI (liquid cooling for GPUs)
  Construction: PRIM, FLR, PWR (datacenter builders)
  Real Estate: EQIX, DLR, AMT
```

## Trading Signal 6: Benchmark as Leading Indicators

### The Thesis
- Benchmarks get saturated predictably as compute scales
- MMLU (2020) → solved by 2023
- MATH (2021) → solved by 2024
- GPQA (PhD-level) → being solved now
- Each benchmark saturation = capability milestone = market event

### Actionable Model
```
BENCHMARK TRADING SIGNALS:
  → Track frontier model benchmark scores
  → Rapid improvement = "unhobbling" happening = adoption accelerates
  → Saturated benchmark + no replacement = possible "wall" narrative
  → New harder benchmark = capability expanding, bull signal
  
LEADING INDICATORS:
  → ML researcher sentiment (Twitter/X, papers)
  → Compute purchase orders (NVDA earnings calls)
  → Power contract announcements
  → Lab hiring patterns (scaling team growth)
  → API pricing drops (algorithmic efficiency gains)
```

---

## Polymarket Opportunities

```
BINARY PREDICTION MARKETS:
  → "Will AI pass [specific benchmark] by [date]?" 
    → Use OOM counting to estimate probability
  → "Will [company] announce [cluster size] by [date]?"
    → Track power contracts, GPU orders
  → "Will US restrict AI chip exports further?"
    → Track geopolitical signals
  → "Will AGI be achieved by 2027?"
    → The core thesis bet
    
METHODOLOGY:
  → Use GRAM multi-trajectory for scenario analysis
  → Use OpenMAI hill-climbing for probability calibration
  → Use OpenSelfRevise to detect when our model is wrong
  → Identity Training: the model KNOWS it's a trading agent
```

---

## RavenX-Trade Model Training Data Categories

Based on the Situational Awareness thesis, our trading model needs:

```
1. COMPUTE SCALING DATA
   → NVDA quarterly revenue + guidance
   → Datacenter power consumption trends
   → GPU pricing and supply data
   → Cloud provider capex announcements

2. BENCHMARK PROGRESSION DATA
   → Model benchmark scores over time
   → Time to saturation per benchmark
   → New benchmark creation dates
   → Capability milestone timeline

3. GEOPOLITICAL SIGNALS
   → US-China trade actions
   → Export control announcements
   → Defense budget allocations
   → Lab security incidents

4. MARKET SENTIMENT
   → AI stock correlation patterns
   → Hype cycle position
   → Analyst coverage changes
   → Retail vs institutional positioning

5. ENERGY/INFRASTRUCTURE
   → Power contract announcements
   → Grid upgrade timelines
   → Nuclear restart decisions
   → Natural gas pricing
```
