"""
╔══════════════════════════════════════════════════════════════════╗
║         QUANTUM OPTIONS INTELLIGENCE — Multi-Agent Platform      ║
║                    v2.0 | Powered by AI Agents                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import json
import threading
from dataclasses import dataclass, field
from typing import Optional
import anthropic
import yfinance as yf
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════
# PAGE CONFIG & THEME
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="QUANTUM OPTIONS INTELLIGENCE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════
# CUSTOM CSS — DARK LUXURY TERMINAL AESTHETIC
# ═══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Bebas+Neue&family=Space+Grotesk:wght@300;400;600;700&display=swap');

:root {
    --bg-void: #020408;
    --bg-panel: #080d14;
    --bg-card: #0d1520;
    --bg-hover: #121e2d;
    --accent-cyan: #00d4ff;
    --accent-green: #00ff88;
    --accent-red: #ff3355;
    --accent-gold: #ffd700;
    --accent-purple: #9945ff;
    --text-primary: #e8f4fd;
    --text-secondary: #7a9bbf;
    --text-muted: #3d5a78;
    --border: #1a2d45;
    --border-glow: #00d4ff33;
    --glow-cyan: 0 0 20px #00d4ff44, 0 0 40px #00d4ff22;
    --glow-green: 0 0 20px #00ff8844, 0 0 40px #00ff8822;
    --glow-red: 0 0 20px #ff335544, 0 0 40px #ff335522;
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-void) !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: 
        radial-gradient(ellipse at 20% 20%, #00d4ff08 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, #9945ff06 0%, transparent 50%),
        repeating-linear-gradient(0deg, transparent, transparent 60px, #00d4ff03 60px, #00d4ff03 61px),
        repeating-linear-gradient(90deg, transparent, transparent 60px, #00d4ff03 60px, #00d4ff03 61px);
    pointer-events: none;
    z-index: 0;
}

.stApp { background: transparent !important; }
[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── MASTER HEADER ── */
.master-header {
    background: linear-gradient(180deg, #020408 0%, #080d14 100%);
    border-bottom: 1px solid var(--border);
    padding: 16px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo-section { display: flex; align-items: center; gap: 16px; }
.logo-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: var(--glow-cyan);
}

.logo-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 26px;
    letter-spacing: 3px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
}

.live-badge {
    display: flex; align-items: center; gap: 8px;
    background: #00ff8811;
    border: 1px solid #00ff8844;
    border-radius: 20px;
    padding: 6px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--accent-green);
    letter-spacing: 1px;
}

.live-dot {
    width: 8px; height: 8px;
    background: var(--accent-green);
    border-radius: 50%;
    box-shadow: var(--glow-green);
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── METRIC TICKER ── */
.ticker-bar {
    background: var(--bg-panel);
    border-bottom: 1px solid var(--border);
    padding: 10px 32px;
    display: flex; gap: 32px; align-items: center;
    overflow-x: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}

.ticker-item { display: flex; gap: 8px; align-items: center; white-space: nowrap; }
.ticker-label { color: var(--text-muted); letter-spacing: 1px; }
.ticker-value { color: var(--text-primary); font-weight: 500; }
.ticker-change.up { color: var(--accent-green); }
.ticker-change.down { color: var(--accent-red); }

/* ── PANELS ── */
.panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    height: 100%;
    transition: border-color 0.3s;
}

.panel:hover { border-color: var(--border-glow); }

.panel-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

.panel-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 18px;
    letter-spacing: 2px;
    color: var(--text-primary);
}

.panel-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 1px;
}

.badge-cyan { background: #00d4ff22; color: var(--accent-cyan); border: 1px solid #00d4ff44; }
.badge-green { background: #00ff8822; color: var(--accent-green); border: 1px solid #00ff8844; }
.badge-gold { background: #ffd70022; color: var(--accent-gold); border: 1px solid #ffd70044; }
.badge-purple { background: #9945ff22; color: var(--accent-purple); border: 1px solid #9945ff44; }

/* ── AGENT CARDS ── */
.agent-card {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.3s;
}

.agent-card.active {
    border-color: var(--accent-cyan);
    box-shadow: var(--glow-cyan);
}

.agent-card.completed {
    border-color: var(--accent-green);
    box-shadow: var(--glow-green);
}

.agent-card.error { border-color: var(--accent-red); }

.agent-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }

.agent-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}

.agent-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: 1px;
}

.agent-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
}

.agent-output {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--text-secondary);
    line-height: 1.6;
    white-space: pre-wrap;
    max-height: 200px;
    overflow-y: auto;
}

/* ── METRIC CARDS ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

.metric-card {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}

.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    letter-spacing: 1px;
}

.metric-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--text-secondary);
    margin-top: 2px;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: all 0.3s !important;
    box-shadow: var(--glow-cyan) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px #00d4ff66, 0 0 60px #00d4ff33 !important;
}

/* ── SELECTS & INPUTS ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}

/* ── DATAFRAMES ── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

[data-testid="stDataFrameResizable"] {
    background: var(--bg-panel) !important;
}

/* ── STRATEGY OUTPUT ── */
.strategy-box {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 1.8;
    color: var(--text-secondary);
    white-space: pre-wrap;
}

.strategy-box .highlight { color: var(--accent-cyan); font-weight: 600; }
.strategy-box .profit { color: var(--accent-green); font-weight: 600; }
.strategy-box .risk { color: var(--accent-red); font-weight: 600; }
.strategy-box .neutral { color: var(--accent-gold); font-weight: 600; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-panel) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    padding: 12px 20px !important;
    border-bottom: 2px solid transparent !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-cyan) !important;
    border-bottom-color: var(--accent-cyan) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--accent-cyan) !important; }

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── MAIN CONTENT PADDING ── */
.main-content { padding: 20px 28px; }

/* ── OPTION CHAIN TABLE ── */
.chain-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}

.chain-table th {
    background: var(--bg-void);
    color: var(--accent-cyan);
    padding: 10px 12px;
    text-align: right;
    letter-spacing: 1px;
    font-size: 10px;
    border-bottom: 1px solid var(--border);
}

.chain-table td {
    padding: 8px 12px;
    text-align: right;
    border-bottom: 1px solid #0d1520;
    color: var(--text-secondary);
    transition: background 0.2s;
}

.chain-table tr:hover td { background: var(--bg-hover); color: var(--text-primary); }
.chain-table .itm { background: #00d4ff08; }
.chain-table .atm td { color: var(--accent-gold) !important; font-weight: 600; }
.chain-table .delta-pass { color: var(--accent-green) !important; }
.chain-table .delta-fail { color: var(--text-muted) !important; }

/* ── GREEKS GRID ── */
.greeks-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
}

.greek-item {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}

.greek-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 16px;
    color: var(--text-muted);
    letter-spacing: 1px;
}

.greek-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 600;
}

/* Alerts */
div[data-testid="stAlert"] {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# BLACK-SCHOLES ENGINE
# ═══════════════════════════════════════════════
class BlackScholes:
    @staticmethod
    def d1(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0: return 0
        return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    @staticmethod
    def d2(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0: return 0
        return BlackScholes.d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

    @staticmethod
    def call_price(S, K, T, r, sigma):
        if T <= 0: return max(S - K, 0)
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    @staticmethod
    def put_price(S, K, T, r, sigma):
        if T <= 0: return max(K - S, 0)
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    @staticmethod
    def greeks(S, K, T, r, sigma, option_type='call'):
        if T <= 0 or sigma <= 0:
            return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        sqrt_T = np.sqrt(T)

        gamma = norm.pdf(d1) / (S * sigma * sqrt_T)
        vega = S * norm.pdf(d1) * sqrt_T / 100
        
        if option_type == 'call':
            delta = norm.cdf(d1)
            theta = (-S * norm.pdf(d1) * sigma / (2 * sqrt_T) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
        else:
            delta = norm.cdf(d1) - 1
            theta = (-S * norm.pdf(d1) * sigma / (2 * sqrt_T) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
        
        return {'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': vega, 'rho': rho}

    @staticmethod
    def implied_vol(market_price, S, K, T, r, option_type='call', tol=1e-6, max_iter=100):
        sigma = 0.2
        for _ in range(max_iter):
            if option_type == 'call':
                price = BlackScholes.call_price(S, K, T, r, sigma)
            else:
                price = BlackScholes.put_price(S, K, T, r, sigma)
            d1 = BlackScholes.d1(S, K, T, r, sigma)
            vega = S * norm.pdf(d1) * np.sqrt(T)
            if vega == 0: break
            diff = market_price - price
            if abs(diff) < tol: break
            sigma += diff / vega
            sigma = max(0.001, min(sigma, 5.0))
        return sigma


# ═══════════════════════════════════════════════
# MARKET DATA ENGINE
# ═══════════════════════════════════════════════
@st.cache_data(ttl=60)
def fetch_market_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="5m")
        info = ticker.fast_info
        return hist, info
    except:
        return None, None

def generate_option_chain(S, sigma=0.20, r=0.05, days_to_exp=30):
    """Generate synthetic option chain with full Greeks."""
    T = days_to_exp / 365
    bs = BlackScholes()
    
    # Strike range: ±8% from ATM in 1% increments
    strikes = np.arange(
        round(S * 0.92 / 5) * 5,
        round(S * 1.08 / 5) * 5 + 5,
        5
    )
    
    rows = []
    for K in strikes:
        moneyness = S / K
        # Volatility smile
        smile_adj = 0.02 * ((K - S) / S) ** 2 - 0.005 * ((K - S) / S)
        iv = max(0.05, sigma + smile_adj)
        
        for opt_type in ['call', 'put']:
            greeks = bs.greeks(S, K, T, r, iv, opt_type)
            if opt_type == 'call':
                price = bs.call_price(S, K, T, r, iv)
            else:
                price = bs.put_price(S, K, T, r, iv)
            
            delta = greeks['delta']
            theta = greeks['theta']
            
            # KEY FILTER: |Δ| > |θ|
            abs_delta = abs(delta)
            abs_theta = abs(theta)
            passes_filter = abs_delta > abs_theta
            
            rows.append({
                'type': opt_type.upper(),
                'strike': K,
                'price': round(price, 2),
                'cost_max_loss': round(price * 100, 2),      # per contract
                'net_profit': round((price * 100) * 0.5, 2),  # target 50% gain
                'delta': round(delta, 4),
                'gamma': round(greeks['gamma'], 6),
                'theta': round(theta, 4),
                'vega': round(greeks['vega'], 4),
                'rho': round(greeks['rho'], 4),
                'iv': round(iv * 100, 2),
                'abs_delta': round(abs_delta, 4),
                'abs_theta': round(abs_theta, 4),
                'delta_gt_theta': passes_filter,
                'moneyness': 'ITM' if (opt_type == 'call' and S > K) or (opt_type == 'put' and S < K) else ('ATM' if abs(S - K) < S * 0.01 else 'OTM'),
                'breakeven': round(K + price if opt_type == 'call' else K - price, 2),
                'T_days': days_to_exp,
            })
    
    return pd.DataFrame(rows)

def get_filtered_contracts(chain_df):
    """Apply Δ > |θ| filter and rank by attractiveness."""
    filtered = chain_df[chain_df['delta_gt_theta']].copy()
    filtered['edge_ratio'] = (filtered['abs_delta'] / (filtered['abs_theta'] + 0.0001)).round(3)
    filtered = filtered.sort_values('edge_ratio', ascending=False)
    return filtered


# ═══════════════════════════════════════════════
# MULTI-AGENT AI SYSTEM
# ═══════════════════════════════════════════════
def call_agent(client, system_prompt, user_message, stream_container=None):
    """Call Anthropic Claude as an agent."""
    try:
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        ) as stream:
            full_text = ""
            for text in stream.text_stream:
                full_text += text
                if stream_container:
                    stream_container.markdown(f"""<div class="agent-output">{full_text}▌</div>""", 
                                              unsafe_allow_html=True)
            if stream_container:
                stream_container.markdown(f"""<div class="agent-output">{full_text}</div>""", 
                                          unsafe_allow_html=True)
            return full_text
    except Exception as e:
        return f"Agent error: {str(e)}"

# ── AGENT 1: CHART ANALYST ──
CHART_AGENT_SYSTEM = """You are an elite quantitative chart analyst and technical analysis expert.
You analyze market data using multiple schools: Wyckoff, Elliott Wave, ICT (Inner Circle Trader), 
Supply/Demand, Volume Profile, Market Structure, and Greek-based sentiment analysis.

Output format — use these exact headers:
## TREND DIRECTION
## MARKET STRUCTURE
## KEY LEVELS
## MOMENTUM
## VOLATILITY REGIME
## OPTIONS BIAS
## TRADE TIMEFRAME

Be precise, quantitative, and actionable. Use exact price levels. No fluff."""

# ── AGENT 2: CONTRACT SCANNER ──
CONTRACT_AGENT_SYSTEM = """You are a quantitative options contract specialist and mathematical filter expert.
Your specialty is the Delta > |Theta| condition: contracts where time-decay (theta) 
is exceeded by directional exposure (delta). This ensures positive theta-adjusted edge.

Analyze the filtered contracts data and output:
## TOP 3 CALLS SELECTED
## TOP 3 PUTS SELECTED  
## FILTER STATISTICS
## RISK/REWARD MATRIX
## CONTRACT RECOMMENDATION

For each contract show: Strike, Expiry, Cost (max loss), Net Profit Target, Delta, |Theta|, Edge Ratio.
Format numbers cleanly. Be mathematically rigorous."""

# ── AGENT 3: STRATEGY ARCHITECT ──
STRATEGY_AGENT_SYSTEM = """You are a master options strategy architect with 20+ years on Wall Street.
You design multi-leg options strategies: spreads, condors, butterflies, ratio spreads, calendars.

Given market data and filtered contracts, design 2-3 complete strategies.

For EACH strategy output:
## STRATEGY NAME
## STRUCTURE (legs with exact strikes/types/quantities)
## COST TABLE (strike | type | qty | cost | max_loss | net_profit_target)
## NET DEBIT/CREDIT
## MAX LOSS | MAX GAIN | BREAKEVEN(S)
## PROBABILITY OF PROFIT
## IDEAL CONDITIONS
## EXIT RULES

Use Greek analysis. Provide specific entry levels and targets."""


# ═══════════════════════════════════════════════
# CHART RENDERING
# ═══════════════════════════════════════════════
def render_price_chart(hist_data, symbol, S):
    """Render professional candlestick chart with indicators."""
    if hist_data is None or len(hist_data) < 20:
        # Synthetic demo data
        dates = pd.date_range(end=datetime.now(), periods=100, freq='5min')
        np.random.seed(42)
        close = S + np.cumsum(np.random.randn(100) * 5)
        high = close + np.abs(np.random.randn(100) * 3)
        low = close - np.abs(np.random.randn(100) * 3)
        open_ = np.roll(close, 1)
        hist_data = pd.DataFrame({'Open': open_, 'High': high, 'Low': low, 'Close': close, 
                                  'Volume': np.random.randint(1000, 50000, 100)}, index=dates)

    df = hist_data.tail(80).copy()
    
    # EMA calculations
    df['EMA9'] = df['Close'].ewm(span=9).mean()
    df['EMA21'] = df['Close'].ewm(span=21).mean()
    df['EMA50'] = df['Close'].ewm(span=50).mean()
    
    # VWAP
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['VWAP'] = (df['TP'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    # RSI(3) for scalping
    delta_close = df['Close'].diff()
    gain = delta_close.clip(lower=0)
    loss = -delta_close.clip(upper=0)
    avg_gain = gain.ewm(com=2, adjust=False).mean()
    avg_loss = loss.ewm(com=2, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df['RSI3'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_mid'] = df['Close'].rolling(20).mean()
    df['BB_std'] = df['Close'].rolling(20).std()
    df['BB_upper'] = df['BB_mid'] + 2 * df['BB_std']
    df['BB_lower'] = df['BB_mid'] - 2 * df['BB_std']
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.65, 0.2, 0.15],
        subplot_titles=('', '', '')
    )
    
    # Candlesticks
    colors_up = '#00ff88'
    colors_down = '#ff3355'
    
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name='Price',
        increasing=dict(line=dict(color=colors_up, width=1), fillcolor=colors_up + '88'),
        decreasing=dict(line=dict(color=colors_down, width=1), fillcolor=colors_down + '88'),
    ), row=1, col=1)
    
    # Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], name='BB Upper',
        line=dict(color='#00d4ff33', width=1), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], name='BB Lower',
        line=dict(color='#00d4ff33', width=1), fill='tonexty',
        fillcolor='#00d4ff08', showlegend=False), row=1, col=1)
    
    # EMAs
    for ema, color, name in [('EMA9', '#ffd700', 'EMA9'), ('EMA21', '#9945ff', 'EMA21'), ('EMA50', '#ff6644', 'EMA50')]:
        fig.add_trace(go.Scatter(x=df.index, y=df[ema], name=name,
            line=dict(color=color, width=1.5)), row=1, col=1)
    
    # VWAP
    fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], name='VWAP',
        line=dict(color='#00d4ff', width=2, dash='dot')), row=1, col=1)
    
    # Volume
    vol_colors = [colors_up if c >= o else colors_down 
                  for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
        marker_color=vol_colors, opacity=0.7, showlegend=False), row=2, col=1)
    
    # RSI(3)
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI3'], name='RSI(3)',
        line=dict(color='#ffd700', width=1.5), showlegend=False), row=3, col=1)
    fig.add_hline(y=80, line_dash="dot", line_color="#ff335544", row=3, col=1)
    fig.add_hline(y=20, line_dash="dot", line_color="#00ff8844", row=3, col=1)
    fig.add_hline(y=50, line_dash="dot", line_color="#ffffff22", row=3, col=1)
    
    # ATM strike line
    fig.add_hline(y=S, line_dash="dash", line_color="#00d4ff88", 
                  annotation_text=f" ATM {S:.0f}", row=1, col=1)
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#080d14',
        plot_bgcolor='#080d14',
        height=520,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation='h', yanchor='top', y=1.02, xanchor='left', x=0,
                    font=dict(family='JetBrains Mono', size=10, color='#7a9bbf'),
                    bgcolor='rgba(0,0,0,0)', borderwidth=0),
        font=dict(family='JetBrains Mono', color='#7a9bbf'),
    )
    
    for axis in ['xaxis', 'yaxis', 'xaxis2', 'yaxis2', 'xaxis3', 'yaxis3']:
        fig.update_layout(**{axis: dict(
            gridcolor='#1a2d45', gridwidth=1,
            zerolinecolor='#1a2d45',
            tickfont=dict(family='JetBrains Mono', size=9, color='#7a9bbf'),
        )})
    
    return fig

def render_pnl_chart(strategies):
    """Render P&L diagram for strategies."""
    if not strategies:
        return None
    
    S = strategies[0]['S']
    prices = np.linspace(S * 0.85, S * 1.15, 200)
    
    fig = go.Figure()
    colors = ['#00d4ff', '#00ff88', '#ffd700']
    
    for i, strat in enumerate(strategies):
        pnl = []
        for p in prices:
            profit = 0
            for leg in strat['legs']:
                if leg['type'] == 'call':
                    intrinsic = max(p - leg['strike'], 0)
                else:
                    intrinsic = max(leg['strike'] - p, 0)
                if leg['position'] == 'long':
                    profit += (intrinsic - leg['premium']) * leg['qty'] * 100
                else:
                    profit += (leg['premium'] - intrinsic) * leg['qty'] * 100
            pnl.append(profit)
        
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=prices, y=pnl, name=strat['name'],
            line=dict(color=color, width=2.5),
            fill='tozeroy',
            fillcolor=color.replace('#', '#') + '15' if color.startswith('#') else color,
        ))
    
    fig.add_hline(y=0, line_color='#ffffff33', line_dash='solid')
    fig.add_vline(x=S, line_color='#00d4ff44', line_dash='dash',
                  annotation_text=f'ATM {S:.0f}')
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#080d14',
        plot_bgcolor='#080d14',
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family='JetBrains Mono', color='#7a9bbf'),
        legend=dict(font=dict(family='JetBrains Mono', size=10)),
        yaxis=dict(title='P&L ($)', gridcolor='#1a2d45'),
        xaxis=dict(title='Underlying Price', gridcolor='#1a2d45'),
    )
    return fig


# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
def main():
    # ── HEADER ──
    st.markdown("""
    <div class="master-header">
        <div class="logo-section">
            <div class="logo-icon">⚡</div>
            <div>
                <div class="logo-text">QUANTUM OPTIONS INTELLIGENCE</div>
                <div class="logo-sub">Multi-Agent AI Trading Platform • v2.0</div>
            </div>
        </div>
        <div style="display:flex; gap:12px; align-items:center;">
            <div class="live-badge">
                <div class="live-dot"></div>
                AGENTS ONLINE
            </div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#3d5a78;">
    """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC") + """
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SESSION STATE ──
    if 'agent_results' not in st.session_state:
        st.session_state.agent_results = {'chart': '', 'contract': '', 'strategy': ''}
    if 'chain_df' not in st.session_state:
        st.session_state.chain_df = None
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = None
    if 'api_key' not in st.session_state:
        # Load from Streamlit Secrets if available (for GitHub/Cloud deployment)
        try:
            st.session_state.api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            st.session_state.api_key = ""

    # ── CONTROL PANEL ──
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1, 1, 1, 1])
        
        with col1:
            _secret_loaded = bool(st.session_state.api_key)
            _label_color = "#00ff88" if _secret_loaded else "#3d5a78"
            _label_text = "API KEY ✓ LOADED FROM SECRETS" if _secret_loaded else "ANTHROPIC API KEY"
            st.markdown(f'<p style="font-family:\'JetBrains Mono\',monospace; font-size:10px; color:{_label_color}; letter-spacing:2px; margin-bottom:4px;">{_label_text}</p>', unsafe_allow_html=True)
            api_key = st.text_input("", value=st.session_state.api_key,
                                     type="password",
                                     placeholder="sk-ant-...  (or set via Streamlit Secrets)",
                                     label_visibility="collapsed", key="api_input")
            st.session_state.api_key = api_key
        
        with col2:
            st.markdown('<p style="font-family:\'JetBrains Mono\',monospace; font-size:10px; color:#3d5a78; letter-spacing:2px; margin-bottom:4px;">TICKER</p>', unsafe_allow_html=True)
            symbol = st.selectbox("", ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "AMZN", "META"],
                                   label_visibility="collapsed")
        
        with col3:
            st.markdown('<p style="font-family:\'JetBrains Mono\',monospace; font-size:10px; color:#3d5a78; letter-spacing:2px; margin-bottom:4px;">SPOT PRICE</p>', unsafe_allow_html=True)
            spot_price = st.number_input("", value=580.0, step=1.0, 
                                          label_visibility="collapsed", key="spot")
        
        with col4:
            st.markdown('<p style="font-family:\'JetBrains Mono\',monospace; font-size:10px; color:#3d5a78; letter-spacing:2px; margin-bottom:4px;">DTE</p>', unsafe_allow_html=True)
            dte = st.selectbox("", [7, 14, 21, 30, 45, 60, 90],
                                label_visibility="collapsed", index=3)
        
        with col5:
            st.markdown('<p style="font-family:\'JetBrains Mono\',monospace; font-size:10px; color:#3d5a78; letter-spacing:2px; margin-bottom:4px;">IV%</p>', unsafe_allow_html=True)
            iv_pct = st.number_input("", value=20.0, step=0.5, 
                                      label_visibility="collapsed", key="iv")
        
        with col6:
            st.markdown('<div style="margin-top:22px;">', unsafe_allow_html=True)
            run_agents = st.button("⚡ ACTIVATE AGENTS", key="run")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    S = spot_price
    sigma = iv_pct / 100
    
    # Generate chain on load or parameter change
    chain_key = f"{symbol}_{S}_{dte}_{iv_pct}"
    if 'last_chain_key' not in st.session_state or st.session_state.last_chain_key != chain_key:
        st.session_state.chain_df = generate_option_chain(S, sigma, days_to_exp=dte)
        st.session_state.filtered_df = get_filtered_contracts(st.session_state.chain_df)
        st.session_state.last_chain_key = chain_key

    chain_df = st.session_state.chain_df
    filtered_df = st.session_state.filtered_df

    # ── METRICS BAR ──
    calls_pass = len(filtered_df[filtered_df['type'] == 'CALL'])
    puts_pass = len(filtered_df[filtered_df['type'] == 'PUT'])
    total_pass = len(filtered_df)
    total_contracts = len(chain_df)
    pass_rate = round(total_pass / total_contracts * 100, 1) if total_contracts > 0 else 0
    
    atm_call = chain_df[(chain_df['type'] == 'CALL') & (chain_df['strike'] >= S)].iloc[0] if len(chain_df) > 0 else None
    
    st.markdown(f"""
    <div class="ticker-bar">
        <div class="ticker-item">
            <span class="ticker-label">SYMBOL</span>
            <span class="ticker-value" style="color:#00d4ff;">{symbol}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">SPOT</span>
            <span class="ticker-value">${S:,.2f}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">ATM IV</span>
            <span class="ticker-value" style="color:#ffd700;">{iv_pct:.1f}%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">DTE</span>
            <span class="ticker-value">{dte}d</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">CONTRACTS SCANNED</span>
            <span class="ticker-value">{total_contracts}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">Δ>|θ| PASS</span>
            <span class="ticker-value" style="color:#00ff88;">{total_pass} ({pass_rate}%)</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">CALLS PASS</span>
            <span class="ticker-value" style="color:#00ff88;">{calls_pass}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">PUTS PASS</span>
            <span class="ticker-value" style="color:#ff3355;">{puts_pass}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">ATM DELTA</span>
            <span class="ticker-value">{atm_call['delta']:.4f if atm_call is not None else 'N/A'}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">ATM IV</span>
            <span class="ticker-value">{atm_call['iv']:.1f if atm_call is not None else 'N/A'}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MAIN GRID ──
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # ── AGENT RUN LOGIC ──
    if run_agents:
        if not api_key:
            st.error("⚠️ Enter your Anthropic API key above to activate the AI agents.")
        else:
            client = anthropic.Anthropic(api_key=api_key)
            
            # Prepare data summaries for agents
            top_filtered = filtered_df.head(10)
            top_calls = filtered_df[filtered_df['type'] == 'CALL'].head(5)
            top_puts = filtered_df[filtered_df['type'] == 'PUT'].head(5)
            
            # Build market context
            market_context = f"""
ASSET: {symbol} | SPOT: ${S:.2f} | DTE: {dte} | IV: {iv_pct}%

TOP 5 CALLS (Δ > |θ| filter passed):
{top_calls[['strike','price','cost_max_loss','net_profit','delta','theta','abs_delta','abs_theta','edge_ratio','iv','breakeven']].to_string()}

TOP 5 PUTS (Δ > |θ| filter passed):
{top_puts[['strike','price','cost_max_loss','net_profit','delta','theta','abs_delta','abs_theta','edge_ratio','iv','breakeven']].to_string()}

FILTER STATS:
- Total contracts scanned: {total_contracts}
- Contracts passing Δ>|θ|: {total_pass} ({pass_rate}%)
- Calls passing: {calls_pass} | Puts passing: {puts_pass}
"""
            
            col_a1, col_a2, col_a3 = st.columns(3)
            
            # ── AGENT 1: CHART ANALYST ──
            with col_a1:
                st.markdown(f"""
                <div class="agent-card active">
                    <div class="agent-header">
                        <div class="agent-icon" style="background:linear-gradient(135deg,#00d4ff,#0066ff);">📊</div>
                        <div>
                            <div class="agent-name">AGENT 1 — CHART ANALYST</div>
                            <div class="agent-status">● ANALYZING MARKET STRUCTURE...</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                output1_container = st.empty()
                
                chart_msg = f"""Analyze {symbol} at ${S:.2f} with {dte} DTE and IV of {iv_pct}%.
The option chain shows {calls_pass} calls and {puts_pass} puts passing the Delta > |Theta| filter.
Provide complete technical analysis and directional bias for options trading."""
                
                result1 = call_agent(client, CHART_AGENT_SYSTEM, chart_msg, output1_container)
                st.session_state.agent_results['chart'] = result1
            
            # ── AGENT 2: CONTRACT SCANNER ──
            with col_a2:
                st.markdown(f"""
                <div class="agent-card active">
                    <div class="agent-header">
                        <div class="agent-icon" style="background:linear-gradient(135deg,#00ff88,#00aa55);">🔍</div>
                        <div>
                            <div class="agent-name">AGENT 2 — CONTRACT SCANNER</div>
                            <div class="agent-status">● SCANNING Δ > |θ| FILTER...</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                output2_container = st.empty()
                
                contract_msg = f"""Review this options data and select the best contracts based on Δ > |θ| condition:

{market_context}

Chart analysis from Agent 1:
{result1[:500]}

Select and rank the top contracts with full financial analysis."""
                
                result2 = call_agent(client, CONTRACT_AGENT_SYSTEM, contract_msg, output2_container)
                st.session_state.agent_results['contract'] = result2
            
            # ── AGENT 3: STRATEGY ARCHITECT ──
            with col_a3:
                st.markdown(f"""
                <div class="agent-card active">
                    <div class="agent-header">
                        <div class="agent-icon" style="background:linear-gradient(135deg,#ffd700,#ff8800);">🏗️</div>
                        <div>
                            <div class="agent-name">AGENT 3 — STRATEGY ARCHITECT</div>
                            <div class="agent-status">● BUILDING COMPOSITE STRATEGIES...</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                output3_container = st.empty()
                
                strategy_msg = f"""Build complete multi-leg options strategies for {symbol} at ${S:.2f}:

Market context: {market_context}

Agent 1 (Chart) finding: {result1[:400]}
Agent 2 (Contracts) selection: {result2[:400]}

Design 2-3 specific strategies with exact strikes from the filtered contracts above.
Include complete P&L table for each strategy."""
                
                result3 = call_agent(client, STRATEGY_AGENT_SYSTEM, strategy_msg, output3_container)
                st.session_state.agent_results['strategy'] = result3
            
            st.success("✅ All 3 agents completed analysis successfully!")

    # ── MAIN TABS ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊  CHART & MARKET", 
        "🔗  OPTION CHAIN", 
        "⚡  FILTERED Δ>|θ|",
        "🤖  AGENT OUTPUTS",
        "📐  P&L DIAGRAM"
    ])
    
    with tab1:
        col_chart, col_greeks = st.columns([3, 1])
        
        with col_chart:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(f'<div class="panel-header"><span class="panel-title">{symbol} — PRICE ACTION</span><span class="panel-badge badge-cyan">LIVE CHART</span></div>', unsafe_allow_html=True)
            
            hist_data, info = fetch_market_data(symbol)
            fig_chart = render_price_chart(hist_data, symbol, S)
            st.plotly_chart(fig_chart, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_greeks:
            st.markdown('<div class="panel" style="height:580px;">', unsafe_allow_html=True)
            st.markdown('<div class="panel-header"><span class="panel-title">ATM GREEKS</span><span class="panel-badge badge-gold">LIVE</span></div>', unsafe_allow_html=True)
            
            if atm_call is not None:
                bs = BlackScholes()
                T = dte / 365
                g = bs.greeks(S, atm_call['strike'], T, 0.05, sigma, 'call')
                
                greeks_data = [
                    ('Δ DELTA', f"{g['delta']:.4f}", '#00d4ff'),
                    ('Γ GAMMA', f"{g['gamma']:.6f}", '#9945ff'),
                    ('θ THETA', f"{g['theta']:.4f}", '#ff3355'),
                    ('ν VEGA', f"{g['vega']:.4f}", '#ffd700'),
                    ('ρ RHO', f"{g['rho']:.4f}", '#00ff88'),
                ]
                
                for greek_name, greek_val, color in greeks_data:
                    st.markdown(f"""
                    <div class="greek-item" style="margin-bottom:10px;">
                        <div class="greek-name">{greek_name}</div>
                        <div class="greek-value" style="color:{color};">{greek_val}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<hr>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#7a9bbf; margin-top:12px;">
                <div style="margin-bottom:6px;">ATM STRIKE: <span style="color:#ffd700;">${atm_call['strike']:.0f}</span></div>
                <div style="margin-bottom:6px;">CALL PRICE: <span style="color:#00ff88;">${atm_call['price']:.2f}</span></div>
                <div style="margin-bottom:6px;">MAX LOSS: <span style="color:#ff3355;">${atm_call['cost_max_loss']:.0f}</span></div>
                <div style="margin-bottom:6px;">BREAKEVEN: <span style="color:#00d4ff;">${atm_call['breakeven']:.2f}</span></div>
                <div style="margin-bottom:6px;">EDGE RATIO: <span style="color:#9945ff;">{abs(g['delta'])/max(abs(g['theta']),0.0001):.2f}x</span></div>
                <div style="margin-top:10px; padding:8px; background:#00d4ff11; border:1px solid #00d4ff33; border-radius:6px;">
                    <div style="color:#00d4ff; margin-bottom:4px;">Δ > |θ| CHECK</div>
                    <div style="color:{'#00ff88' if abs(g['delta']) > abs(g['theta']) else '#ff3355'}; font-size:14px; font-weight:bold;">
                        {'✓ PASS' if abs(g['delta']) > abs(g['theta']) else '✗ FAIL'}
                    </div>
                    <div style="color:#7a9bbf; font-size:10px; margin-top:4px;">
                    |Δ| {abs(g['delta']):.4f} {'>' if abs(g['delta']) > abs(g['theta']) else '<'} |θ| {abs(g['theta']):.4f}
                    </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><span class="panel-title">FULL OPTION CHAIN</span><span class="panel-badge badge-cyan">ALL CONTRACTS</span></div>', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            opt_filter = st.selectbox("Type Filter", ["ALL", "CALL", "PUT"], key="chain_filter")
        with col_f2:
            money_filter = st.selectbox("Moneyness", ["ALL", "ITM", "ATM", "OTM"], key="money_filter")
        
        display_df = chain_df.copy()
        if opt_filter != "ALL":
            display_df = display_df[display_df['type'] == opt_filter]
        if money_filter != "ALL":
            display_df = display_df[display_df['moneyness'] == money_filter]
        
        display_cols = ['type', 'strike', 'moneyness', 'price', 'cost_max_loss', 'net_profit',
                        'delta', 'gamma', 'theta', 'vega', 'iv', 'breakeven', 'delta_gt_theta']
        
        styled = display_df[display_cols].rename(columns={
            'type': 'TYPE', 'strike': 'STRIKE', 'moneyness': 'MONEY',
            'price': 'PRICE', 'cost_max_loss': 'MAX LOSS ($)',
            'net_profit': 'NET PROFIT ($)', 'delta': 'DELTA', 'gamma': 'GAMMA',
            'theta': 'THETA', 'vega': 'VEGA', 'iv': 'IV%',
            'breakeven': 'BREAKEVEN', 'delta_gt_theta': 'Δ>|θ| PASS'
        })
        
        st.dataframe(
            styled,
            use_container_width=True,
            height=500,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("""
        <div class="panel-header">
            <span class="panel-title">FILTERED CONTRACTS — Δ > |θ|</span>
            <span class="panel-badge badge-green">MATHEMATICAL FILTER</span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#7a9bbf; margin-bottom:16px; 
                    padding:12px; background:#00ff8811; border:1px solid #00ff8844; border-radius:8px;">
            <span style="color:#00ff88; font-weight:600;">FILTER CONDITION:</span> |Δ| > |θ|  — 
            Only contracts where absolute Delta exceeds absolute Theta are selected.
            This ensures directional exposure outweighs time decay cost.
            Sorted by Edge Ratio (|Δ| / |θ|) — highest edge first.
        </div>
        """, unsafe_allow_html=True)
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown('<div style="color:#00d4ff; font-family:\'JetBrains Mono\',monospace; font-size:12px; letter-spacing:2px; margin-bottom:8px;">▶ TOP CALLS</div>', unsafe_allow_html=True)
            top_calls_disp = filtered_df[filtered_df['type'] == 'CALL'].head(10)
            if len(top_calls_disp) > 0:
                call_display = top_calls_disp[['strike', 'price', 'cost_max_loss', 'net_profit',
                                                'delta', 'theta', 'abs_delta', 'abs_theta', 
                                                'edge_ratio', 'iv', 'breakeven', 'T_days']].rename(columns={
                    'strike': 'STRIKE', 'price': 'PREMIUM', 'cost_max_loss': 'MAX LOSS ($)',
                    'net_profit': 'NET PROFIT ($)', 'delta': 'DELTA', 'theta': 'THETA',
                    'abs_delta': '|Δ|', 'abs_theta': '|θ|', 'edge_ratio': 'EDGE RATIO',
                    'iv': 'IV%', 'breakeven': 'BREAKEVEN', 'T_days': 'DTE'
                })
                st.dataframe(call_display, use_container_width=True, height=380, hide_index=True)
            else:
                st.info("No calls pass the filter with current parameters.")
        
        with col_t2:
            st.markdown('<div style="color:#ff3355; font-family:\'JetBrains Mono\',monospace; font-size:12px; letter-spacing:2px; margin-bottom:8px;">▶ TOP PUTS</div>', unsafe_allow_html=True)
            top_puts_disp = filtered_df[filtered_df['type'] == 'PUT'].head(10)
            if len(top_puts_disp) > 0:
                put_display = top_puts_disp[['strike', 'price', 'cost_max_loss', 'net_profit',
                                              'delta', 'theta', 'abs_delta', 'abs_theta', 
                                              'edge_ratio', 'iv', 'breakeven', 'T_days']].rename(columns={
                    'strike': 'STRIKE', 'price': 'PREMIUM', 'cost_max_loss': 'MAX LOSS ($)',
                    'net_profit': 'NET PROFIT ($)', 'delta': 'DELTA', 'theta': 'THETA',
                    'abs_delta': '|Δ|', 'abs_theta': '|θ|', 'edge_ratio': 'EDGE RATIO',
                    'iv': 'IV%', 'breakeven': 'BREAKEVEN', 'T_days': 'DTE'
                })
                st.dataframe(put_display, use_container_width=True, height=380, hide_index=True)
            else:
                st.info("No puts pass the filter with current parameters.")
        
        # Summary stats
        st.markdown('<hr>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Passing", f"{total_pass}", f"{pass_rate}% pass rate")
        with c2:
            avg_edge = filtered_df['edge_ratio'].mean() if len(filtered_df) > 0 else 0
            st.metric("Avg Edge Ratio", f"{avg_edge:.2f}x")
        with c3:
            avg_iv = filtered_df['iv'].mean() if len(filtered_df) > 0 else 0
            st.metric("Avg IV (Filtered)", f"{avg_iv:.1f}%")
        with c4:
            best_edge = filtered_df['edge_ratio'].max() if len(filtered_df) > 0 else 0
            st.metric("Best Edge Ratio", f"{best_edge:.2f}x")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><span class="panel-title">MULTI-AGENT AI OUTPUTS</span><span class="panel-badge badge-purple">AI ANALYSIS</span></div>', unsafe_allow_html=True)
        
        if not any(st.session_state.agent_results.values()):
            st.markdown("""
            <div style="text-align:center; padding:60px 20px; color:#3d5a78;">
                <div style="font-size:48px; margin-bottom:16px;">🤖</div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:28px; letter-spacing:3px; color:#1a2d45; margin-bottom:8px;">
                    AGENTS STANDING BY
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:2px;">
                    Enter your Anthropic API key and click ⚡ ACTIVATE AGENTS
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            col_r1, col_r2, col_r3 = st.columns(3)
            
            for col, agent_name, icon, color, result_key, badge in [
                (col_r1, "CHART ANALYST", "📊", "#00d4ff", "chart", "badge-cyan"),
                (col_r2, "CONTRACT SCANNER", "🔍", "#00ff88", "contract", "badge-green"),
                (col_r3, "STRATEGY ARCHITECT", "🏗️", "#ffd700", "strategy", "badge-gold"),
            ]:
                with col:
                    result = st.session_state.agent_results.get(result_key, '')
                    status = "completed" if result else "pending"
                    st.markdown(f"""
                    <div class="agent-card {status}">
                        <div class="agent-header">
                            <div class="agent-icon" style="background:linear-gradient(135deg,{color}88,{color}44);">{icon}</div>
                            <div>
                                <div class="agent-name">{agent_name}</div>
                                <div class="agent-status" style="color:{'#00ff88' if result else '#3d5a78'};">
                                    {'● ANALYSIS COMPLETE' if result else '○ AWAITING ACTIVATION'}
                                </div>
                            </div>
                        </div>
                        <div class="agent-output">{result if result else "Agent has not been activated yet."}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><span class="panel-title">P&L DIAGRAM BUILDER</span><span class="panel-badge badge-gold">STRATEGY VISUALIZER</span></div>', unsafe_allow_html=True)
        
        st.markdown('<p style="font-family:\'JetBrains Mono\',monospace; font-size:11px; color:#7a9bbf;">Build and visualize multi-leg strategies from the filtered contracts:</p>', unsafe_allow_html=True)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            preset = st.selectbox("Strategy Preset", [
                "Bull Call Spread", "Bear Put Spread", "Long Straddle", 
                "Iron Condor", "Bull Put Spread", "Custom"
            ])
        with col_s2:
            width = st.number_input("Spread Width ($)", value=10.0, step=5.0)
        
        ATM = round(S / 5) * 5
        
        strategy_presets = {
            "Bull Call Spread": [
                {'name': 'Bull Call Spread', 'S': S, 'legs': [
                    {'type': 'call', 'strike': ATM, 'premium': 5.0, 'position': 'long', 'qty': 1},
                    {'type': 'call', 'strike': ATM + width, 'premium': 2.5, 'position': 'short', 'qty': 1},
                ]}
            ],
            "Bear Put Spread": [
                {'name': 'Bear Put Spread', 'S': S, 'legs': [
                    {'type': 'put', 'strike': ATM, 'premium': 5.0, 'position': 'long', 'qty': 1},
                    {'type': 'put', 'strike': ATM - width, 'premium': 2.5, 'position': 'short', 'qty': 1},
                ]}
            ],
            "Long Straddle": [
                {'name': 'Long Straddle', 'S': S, 'legs': [
                    {'type': 'call', 'strike': ATM, 'premium': 5.0, 'position': 'long', 'qty': 1},
                    {'type': 'put', 'strike': ATM, 'premium': 4.5, 'position': 'long', 'qty': 1},
                ]}
            ],
            "Iron Condor": [
                {'name': 'Iron Condor', 'S': S, 'legs': [
                    {'type': 'put', 'strike': ATM - width*2, 'premium': 1.0, 'position': 'long', 'qty': 1},
                    {'type': 'put', 'strike': ATM - width, 'premium': 2.5, 'position': 'short', 'qty': 1},
                    {'type': 'call', 'strike': ATM + width, 'premium': 2.5, 'position': 'short', 'qty': 1},
                    {'type': 'call', 'strike': ATM + width*2, 'premium': 1.0, 'position': 'long', 'qty': 1},
                ]}
            ],
            "Bull Put Spread": [
                {'name': 'Bull Put Spread', 'S': S, 'legs': [
                    {'type': 'put', 'strike': ATM - width, 'premium': 2.5, 'position': 'short', 'qty': 1},
                    {'type': 'put', 'strike': ATM - width*2, 'premium': 1.0, 'position': 'long', 'qty': 1},
                ]}
            ],
        }
        
        if preset != "Custom":
            strategies = strategy_presets.get(preset, [])
            fig_pnl = render_pnl_chart(strategies)
            if fig_pnl:
                st.plotly_chart(fig_pnl, use_container_width=True, config={'displayModeBar': False})
            
            # Strategy table
            if strategies:
                strat = strategies[0]
                st.markdown(f"""
                <div style="font-family:'JetBrains Mono',monospace; margin-top:16px;">
                <div style="color:#00d4ff; font-size:14px; letter-spacing:2px; margin-bottom:12px;">
                    📋 {strat['name'].upper()} — LEGS TABLE
                </div>
                <table class="chain-table" style="width:100%;">
                <tr>
                    <th style="text-align:left;">LEG</th>
                    <th>TYPE</th>
                    <th>STRIKE</th>
                    <th>POSITION</th>
                    <th>PREMIUM</th>
                    <th>MAX LOSS ($)</th>
                    <th>PROFIT TARGET ($)</th>
                </tr>
                """, unsafe_allow_html=True)
                
                total_cost = 0
                for i, leg in enumerate(strat['legs']):
                    cost = leg['premium'] * 100 * leg['qty']
                    if leg['position'] == 'long':
                        total_cost += cost
                        max_loss = cost
                        profit_target = cost * 0.5
                    else:
                        total_cost -= cost
                        max_loss = 0
                        profit_target = cost
                    
                    color = '#00ff88' if leg['position'] == 'long' else '#ff3355'
                    st.markdown(f"""
                    <tr>
                        <td style="text-align:left; color:#7a9bbf;">LEG {i+1}</td>
                        <td style="color:#ffd700;">{leg['type'].upper()}</td>
                        <td style="color:#e8f4fd;">${leg['strike']:.0f}</td>
                        <td style="color:{color};">{leg['position'].upper()}</td>
                        <td>${leg['premium']:.2f}</td>
                        <td style="color:#ff3355;">${max_loss:.0f}</td>
                        <td style="color:#00ff88;">${profit_target:.0f}</td>
                    </tr>
                    """, unsafe_allow_html=True)
                
                net_debit = total_cost
                st.markdown(f"""
                <tr style="border-top:2px solid #1a2d45;">
                    <td colspan="4" style="text-align:left; color:#7a9bbf; font-weight:bold;">NET {'DEBIT' if net_debit > 0 else 'CREDIT'}</td>
                    <td></td>
                    <td style="color:{'#ff3355' if net_debit > 0 else '#00ff88'}; font-weight:bold;">
                        {'$' + str(abs(round(net_debit))) if net_debit != 0 else '$0'}
                    </td>
                    <td></td>
                </tr>
                </table>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ── FOOTER ──
    st.markdown("""
    <div style="background:#080d14; border-top:1px solid #1a2d45; padding:16px 32px; 
                display:flex; justify-content:space-between; align-items:center;
                font-family:'JetBrains Mono',monospace; font-size:10px; color:#3d5a78;
                letter-spacing:1px; margin-top:20px;">
        <div>QUANTUM OPTIONS INTELLIGENCE v2.0 — MULTI-AGENT AI PLATFORM</div>
        <div style="display:flex; gap:24px;">
            <span>⚠️ FOR EDUCATIONAL USE ONLY</span>
            <span>OPTIONS TRADING INVOLVES SUBSTANTIAL RISK</span>
            <span>NOT FINANCIAL ADVICE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
