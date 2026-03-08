"""
agents.py — Multi-Agent AI Orchestration Layer
==============================================
Three specialized agents working in concert:
  1. ChartAgent    — Technical analysis & trend extraction
  2. ContractAgent — Options chain scanning with Δ > |θ| filter
  3. StrategyAgent — Composite options strategy construction
"""

import anthropic
from dataclasses import dataclass
from typing import Optional
import pandas as pd


# ═══════════════════════════════════════════════
# AGENT DEFINITIONS
# ═══════════════════════════════════════════════

CHART_AGENT_SYSTEM = """You are an elite quantitative chart analyst with expertise across ALL technical analysis schools:
- Wyckoff Method (accumulation/distribution phases, composite operator)
- Elliott Wave Theory (wave counts, Fibonacci extensions/retracements)
- ICT — Inner Circle Trader (fair value gaps, order blocks, liquidity sweeps, NWOG)
- Supply & Demand (institutional zones, POI identification)  
- Volume Profile (VPOC, VAH, VAL, TPO, naked POCs)
- Market Structure (BOS, CHoCH, MSS, HH/HL/LH/LL)
- Classic Indicators (RSI, MACD, Bollinger Bands, ATR, VWAP)
- Options Flow & Greeks-based sentiment

Output your analysis in this EXACT format:

## TREND DIRECTION
[Bull/Bear/Neutral with confidence %]

## MARKET STRUCTURE  
[Current phase, key BOS/CHoCH levels]

## KEY LEVELS
[Support 1, Support 2, Resistance 1, Resistance 2 with exact prices]

## MOMENTUM
[RSI reading, divergences, momentum direction]

## VOLATILITY REGIME
[Low/Normal/Elevated/Extreme IV with IV rank context]

## OPTIONS BIAS
[Directional bias for options: calls/puts/neutral spreads]

## TRADE TIMEFRAME
[Recommended DTE and timing]

Be precise. Use exact price levels. No generic statements."""


CONTRACT_AGENT_SYSTEM = """You are a quantitative options contract specialist and mathematical filter engine.

Your core mandate: Apply the Delta > |Theta| (Δ > |θ|) filter to identify options contracts where 
directional exposure exceeds time-decay cost — creating a positive-expectancy edge.

MATHEMATICAL FOUNDATION:
- Delta (Δ): Rate of price change per $1 move in underlying
- Theta (θ): Daily time decay cost (always negative)
- Condition: |Δ| > |θ|  means the contract moves more per dollar of underlying movement 
  than it loses per day of time decay

For each selected contract, provide:
Strike | Type | DTE | Premium | Max Loss (per contract) | Net Profit Target | Δ | |θ| | Edge Ratio (|Δ|/|θ|) | IV%

Output format:

## FILTER STATISTICS
[Pass rate, total scanned, distribution analysis]

## TOP 3 CALLS SELECTED
[Table with all required fields]

## TOP 3 PUTS SELECTED  
[Table with all required fields]

## RISK/REWARD MATRIX
[For each selected contract: max loss, 50% profit target, breakeven]

## CONTRACT RECOMMENDATION
[Final ranked picks with rationale — quantitative justification only]

Be mathematically rigorous. Format all numbers consistently."""


STRATEGY_AGENT_SYSTEM = """You are a master options strategy architect with 20+ years of institutional trading experience.
You design multi-leg options strategies optimized for the current market regime.

Strategy toolkit:
- Vertical spreads (bull call, bear put, bull put, bear call)
- Horizontal spreads (calendars, diagonals)
- Neutral structures (iron condors, butterflies, strangles)
- Directional (synthetic long/short, ratio spreads, backspreads)
- Volatility plays (straddles, strangles, VIX-correlated)

For each strategy, output this EXACT structure:

## STRATEGY [N]: [NAME]

### STRUCTURE
| Leg | Action | Type | Strike | DTE | Qty |
|-----|--------|------|--------|-----|-----|

### COST & P&L TABLE
| Strike | Type | Position | Premium | Cost (Max Loss) | Net Profit Target |
|--------|------|----------|---------|-----------------|-------------------|
| TOTAL  |      |          |         | NET DEBIT/CREDIT| MAX GAIN          |

### METRICS
- Net Debit/Credit: $X
- Max Loss: $X (where and why)
- Max Gain: $X (where and why)
- Breakeven(s): $X [, $Y]
- Probability of Profit: X%
- Risk/Reward Ratio: 1:X

### GREEKS SUMMARY
- Net Delta: X | Net Gamma: X | Net Theta: X/day | Net Vega: X

### IDEAL CONDITIONS
[Specific market conditions, IV environment, catalyst timing]

### ENTRY RULES
[Specific triggers, price levels, timing]

### EXIT RULES
[Take profit %, stop loss %, time-based exits, adjustment triggers]

Design 2-3 strategies. Make them specific, actionable, and mathematically sound."""


# ═══════════════════════════════════════════════
# AGENT RUNNER
# ═══════════════════════════════════════════════

@dataclass
class AgentResult:
    agent_name: str
    output: str
    success: bool
    error: Optional[str] = None


def run_chart_agent(client: anthropic.Anthropic, symbol: str, spot: float, 
                    dte: int, iv: float) -> AgentResult:
    """Agent 1: Analyze chart and extract trend."""
    user_message = f"""
Perform complete technical analysis for options trading:

Asset: {symbol}
Current Price: ${spot:.2f}
Target DTE: {dte} days
Current IV: {iv:.1f}%

Analyze current market structure, identify key levels, determine trend direction,
and provide options directional bias. Be specific with price levels.
"""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=CHART_AGENT_SYSTEM,
            messages=[{"role": "user", "content": user_message}]
        )
        return AgentResult("ChartAgent", response.content[0].text, True)
    except Exception as e:
        return AgentResult("ChartAgent", "", False, str(e))


def run_contract_agent(client: anthropic.Anthropic, symbol: str, spot: float,
                       filtered_df: pd.DataFrame, chain_df: pd.DataFrame,
                       chart_analysis: str) -> AgentResult:
    """Agent 2: Scan and filter contracts using Δ > |θ|."""
    
    top_calls = filtered_df[filtered_df['type'] == 'CALL'].head(5)
    top_puts = filtered_df[filtered_df['type'] == 'PUT'].head(5)
    
    total = len(chain_df)
    passing = len(filtered_df)
    
    user_message = f"""
Analyze these filtered options contracts for {symbol} at ${spot:.2f}:

FILTER RESULTS: {passing}/{total} contracts pass |Δ| > |θ|

TOP CALLS (pre-filtered, sorted by Edge Ratio):
{top_calls[['strike','price','cost_max_loss','net_profit','delta','theta','abs_delta','abs_theta','edge_ratio','iv','breakeven']].to_string(index=False)}

TOP PUTS (pre-filtered, sorted by Edge Ratio):
{top_puts[['strike','price','cost_max_loss','net_profit','delta','theta','abs_delta','abs_theta','edge_ratio','iv','breakeven']].to_string(index=False)}

Chart analysis context:
{chart_analysis[:600]}

Select and rank the best contracts. Provide complete financial metrics for each.
"""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=CONTRACT_AGENT_SYSTEM,
            messages=[{"role": "user", "content": user_message}]
        )
        return AgentResult("ContractAgent", response.content[0].text, True)
    except Exception as e:
        return AgentResult("ContractAgent", "", False, str(e))


def run_strategy_agent(client: anthropic.Anthropic, symbol: str, spot: float,
                       dte: int, iv: float, chart_analysis: str, 
                       contract_analysis: str) -> AgentResult:
    """Agent 3: Design composite options strategies."""
    
    user_message = f"""
Design 2-3 optimal multi-leg options strategies for:

Asset: {symbol} | Spot: ${spot:.2f} | DTE: {dte} | IV: {iv:.1f}%

=== AGENT 1 — CHART ANALYSIS ===
{chart_analysis[:600]}

=== AGENT 2 — CONTRACT SELECTION ===
{contract_analysis[:600]}

Use the selected contracts to construct concrete strategies.
Provide exact strikes, quantities, costs, and complete P&L tables.
All numbers must be specific and mathematically consistent.
"""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=STRATEGY_AGENT_SYSTEM,
            messages=[{"role": "user", "content": user_message}]
        )
        return AgentResult("StrategyAgent", response.content[0].text, True)
    except Exception as e:
        return AgentResult("StrategyAgent", "", False, str(e))


def run_all_agents(api_key: str, symbol: str, spot: float, dte: int, iv: float,
                   chain_df: pd.DataFrame, filtered_df: pd.DataFrame) -> dict:
    """
    Orchestrate all three agents in sequence.
    Returns dict with results from each agent.
    """
    client = anthropic.Anthropic(api_key=api_key)
    results = {}
    
    # Agent 1
    r1 = run_chart_agent(client, symbol, spot, dte, iv)
    results['chart'] = r1
    
    # Agent 2 (uses Agent 1 output)
    r2 = run_contract_agent(client, symbol, spot, filtered_df, chain_df, 
                             r1.output if r1.success else "")
    results['contract'] = r2
    
    # Agent 3 (uses both Agent 1 & 2 outputs)
    r3 = run_strategy_agent(client, symbol, spot, dte, iv,
                             r1.output if r1.success else "",
                             r2.output if r2.success else "")
    results['strategy'] = r3
    
    return results
