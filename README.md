# ⚡ QUANTUM OPTIONS INTELLIGENCE
## Multi-Agent AI Options Trading Platform — v2.0

```
╔══════════════════════════════════════════════════════════════════╗
║         QUANTUM OPTIONS INTELLIGENCE — Multi-Agent Platform      ║
║                    v2.0 | Powered by AI Agents                   ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🤖 AGENT ARCHITECTURE

### Agent 1 — Chart Analyst (`ChartAgent`)
Analyzes price action using multiple technical schools simultaneously:
- **Wyckoff**: Accumulation/distribution phases, composite operator tracking
- **Elliott Wave**: Wave count with Fibonacci targets
- **ICT**: Fair value gaps, order blocks, liquidity sweeps
- **Volume Profile**: VPOC, value area, naked POCs
- **Market Structure**: BOS/CHoCH identification

**Output**: Trend direction, key levels, volatility regime, options bias

---

### Agent 2 — Contract Scanner (`ContractAgent`)
Mathematical filter engine using the **Δ > |θ|** condition:

```
FILTER CONDITION:  |Delta| > |Theta|

This ensures: directional exposure (Δ) exceeds time decay cost (θ)
creating a positive-expectancy edge before any price movement.

Edge Ratio = |Δ| / |θ|  (higher = better)
```

**Output**: Ranked contracts table with Strike | Cost | Max Loss | Net Profit | Delta | Theta | Edge Ratio

---

### Agent 3 — Strategy Architect (`StrategyAgent`)
Designs multi-leg composite strategies:
- Vertical spreads (bull call, bear put, bull put, bear call)
- Iron condors, butterflies
- Calendars & diagonals
- Straddles & strangles

**Output**: Complete strategy with legs table, P&L table, Greeks summary, entry/exit rules

---

## 📊 DASHBOARD FEATURES

| Feature | Description |
|---------|-------------|
| **Candlestick Chart** | Live price with EMA9/21/50, VWAP, Bollinger Bands |
| **RSI(3) Subpanel** | Scalping-optimized momentum oscillator |
| **Volume Subpanel** | Color-coded volume with trend confirmation |
| **Full Option Chain** | Complete chain with all Greeks, filterable |
| **Δ>θ Filter** | Filtered contracts sorted by Edge Ratio |
| **P&L Diagram** | Interactive strategy payoff diagrams |
| **ATM Greeks** | Live Greek calculations with filter status |
| **Agent Outputs** | Real-time streaming AI analysis |

---

## 🚀 INSTALLATION

```bash
# 1. Clone/download the platform
cd options_platform/

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the platform
bash run.sh

# OR directly:
streamlit run app.py
```

**Requirements**: Python 3.9+, Anthropic API key (claude.ai)

---

## ⚙️ CONFIGURATION

In the top control bar:
1. **API Key**: Your Anthropic API key (`sk-ant-...`)
2. **Ticker**: SPY, QQQ, AAPL, TSLA, NVDA, AMZN, META
3. **Spot Price**: Current underlying price
4. **DTE**: Days to expiration (7, 14, 21, 30, 45, 60, 90)
5. **IV%**: Implied volatility percentage

Click **⚡ ACTIVATE AGENTS** to run all three AI agents in sequence.

---

## 📐 MATHEMATICAL ENGINE

### Black-Scholes Greeks Implementation

```python
# Delta
call_delta = N(d1)
put_delta  = N(d1) - 1

# Gamma (same for calls/puts)
gamma = N'(d1) / (S * σ * √T)

# Theta (per day)
theta_call = (-S*N'(d1)*σ/(2√T) - r*K*e^(-rT)*N(d2)) / 365

# Vega (per 1% IV change)
vega = S * N'(d1) * √T / 100

# The Filter:
# |Δ| > |θ|  →  directional edge exceeds daily time decay
```

### Volatility Smile
Contracts include a quadratic volatility smile:
```
IV(K) = base_IV + 0.02*(K-S/S)² - 0.005*(K-S/S)
```

---

## 📋 CONTRACT TABLE COLUMNS

| Column | Description |
|--------|-------------|
| **STRIKE** | Option strike price |
| **PREMIUM** | Option market price |
| **MAX LOSS ($)** | Premium × 100 (cost per contract) |
| **NET PROFIT ($)** | 50% of max loss (target take-profit) |
| **DELTA** | Δ directional sensitivity |
| **THETA** | θ daily time decay |
| **\|Δ\|** | Absolute delta |
| **\|θ\|** | Absolute theta |
| **EDGE RATIO** | \|Δ\|/\|θ\| — higher is better |
| **IV%** | Implied volatility |
| **BREAKEVEN** | Price needed at expiry to profit |
| **DTE** | Days to expiration |

---

## ⚠️ DISCLAIMER

This platform is for **educational and research purposes only**.
Options trading involves substantial risk of loss.
This is NOT financial advice.
Always consult a licensed financial advisor before trading.

---

## 🔧 EXTENDING THE PLATFORM

### Adding a new agent:
```python
# In agents.py, add:

NEW_AGENT_SYSTEM = """Your new agent system prompt..."""

def run_new_agent(client, ...):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=NEW_AGENT_SYSTEM,
        messages=[{"role": "user", "content": user_message}]
    )
    return AgentResult("NewAgent", response.content[0].text, True)
```

### Adding real options data:
Replace `generate_option_chain()` in `app.py` with:
```python
import yfinance as yf
ticker = yf.Ticker("SPY")
chain = ticker.option_chain("2024-12-20")
# chain.calls | chain.puts
```

---

*Built with Streamlit + Anthropic Claude + Black-Scholes Engine*
