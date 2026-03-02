import yfinance as yf
import pandas as pd
import json
import requests
import os
import re
from datetime import datetime
from alpaca.data.historical import OptionHistoricalDataClient
from alpaca.data.requests import OptionChainRequest

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'ضع_توكن_التليجرام_هنا')
CHAT_ID = os.getenv('CHAT_ID', 'ضع_ايدي_المحادثة_هنا')
ALPACA_KEY = os.getenv('ALPACA_KEY', 'AKO2RAWKPKN27WA2Y6ZNOK4XIT')
ALPACA_SECRET = os.getenv('ALPACA_SECRET', 'okjvrkLGfPihbGsQ6jM8jXAte1ZzdeDa4MXNc3wgf3n')

SYMBOLS = ['^SPX', 'TSLA', 'NVDA', 'AAPL']
opt_client = OptionHistoricalDataClient(ALPACA_KEY, ALPACA_SECRET)

def analyze_symbol(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="60d", interval="1d")
    df_hour = ticker.history(period="20d", interval="1h")
    
    if df.empty or df_hour.empty: return None

    current_price = df_hour['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
    daily_change = ((current_price - prev_close) / prev_close) * 100

    prev_high, prev_low = df['High'].iloc[-2], df['Low'].iloc[-2]
    pivot = (prev_high + prev_low + prev_close) / 3
    r1, s1 = (2 * pivot) - prev_low, (2 * pivot) - prev_high

    sma_50 = df['Close'].rolling(window=50).mean().iloc[-1]
    dist_sma50 = ((current_price - sma_50) / sma_50) * 100

    df['tr1'] = df['High'] - df['Low']
    df['tr2'] = abs(df['High'] - df['Close'].shift())
    df['tr3'] = abs(df['Low'] - df['Close'].shift())
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    atr = df['tr'].rolling(window=14).mean().iloc[-1]

    q, r, s = 14, 3, 3
    hh, ll = df_hour['High'].rolling(window=q).max(), df_hour['Low'].rolling(window=q).min()
    center = (hh + ll) / 2
    m = df_hour['Close'] - center
    diff = hh - ll
    smi = 100 * (m.ewm(span=r).mean().ewm(span=s).mean() / (0.5 * diff.ewm(span=r).mean().ewm(span=s).mean()))
    smi_val = smi.iloc[-1]

    df_hour['vol'] = df_hour['Volume']
    if df_hour['vol'].sum() > 0:
        vwap = (df_hour['Close'] * df_hour['vol']).cumsum() / df_hour['vol'].cumsum()
    else:
        vwap = df_hour['Close'].rolling(window=14).mean()
    vwap_val = vwap.iloc[-1]

    delta = df_hour['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_val = (100 - (100 / (1 + rs))).iloc[-1]

    is_breakout = current_price > sma_50 and prev_close <= sma_50
    clean_symbol = symbol.replace('^', '')

    return {
        "symbol": clean_symbol,
        "price": round(current_price, 2),
        "change": round(daily_change, 2),
        "r1": round(r1, 2),
        "s1": round(s1, 2),
        "atr": round(atr, 2),
        "dist_sma50": round(dist_sma50, 2),
        "smi": round(smi_val, 2),
        "rsi": round(rsi_val, 2),
        "vwap": round(vwap_val, 2),
        "highlight": is_breakout
    }

def get_nearest_expiry(chain):
    dates = {re.search(r'\d{6}', sym).group(0) for sym in chain.keys() if re.search(r'\d{6}', sym)}
    return sorted(list(dates))[0] if dates else None

def scan_options_for_spx(spx_data):
    req = OptionChainRequest(underlying_symbol="SPX")
    try:
        chain = opt_client.get_option_chain(req)
    except:
        return 

    target_exp = get_nearest_expiry(chain)
    if not target_exp: return

    call_vol, put_vol = 0, 0
    for sym, data in chain.items():
        if target_exp in sym and data.latest_quote:
            q = data.latest_quote
            if q.bid_size and q.ask_size:
                if 'C' in sym.split("SPX")[-1]: call_vol += q.bid_size + q.ask_size
                elif 'P' in sym.split("SPX")[-1]: put_vol += q.bid_size + q.ask_size
    gamma_score = (call_vol / (call_vol + put_vol)) * 100 if (call_vol + put_vol) > 0 else 50

    bull_score, bear_score = 0, 0
    price, vwap, smi, rsi = spx_data['price'], spx_data['vwap'], spx_data['smi'], spx_data['rsi']
    
    if gamma_score > 55: bull_score += 30
    elif gamma_score < 45: bear_score += 30
    if smi > 20: bull_score += 20
    elif smi < -20: bear_score += 20
    if price > vwap: bull_score += 20
    else: bear_score += 20
    if rsi > 50: bull_score += 10
    else: bear_score += 10

    if bull_score >= 80:
        find_best_option("BULL", "Bull Call Spread 🚀", spx_data, chain, target_exp)
    elif bear_score >= 80:
        find_best_option("BEAR", "Bear Put Spread 🩸", spx_data, chain, target_exp)

def find_best_option(direction, strat_name, spx_data, chain, target_exp):
    price = spx_data['price']
    contracts = []
    
    for sym, d in chain.items():
        if target_exp in sym and d.latest_quote:
            q = d.latest_quote
            if (q.ask_price - q.bid_price) < 0.5 and q.bid_size > 0: 
                strike = float(re.findall(r'\d{8}', sym)[0]) / 1000
                if price * 0.98 <= strike <= price * 1.02:
                    c_type = 'C' if 'C' in sym else 'P'
                    delta = abs(d.greeks.delta) if d.greeks and d.greeks.delta else 0.50
                    theta = d.greeks.theta if d.greeks and d.greeks.theta else -0.50
                    contracts.append({'sym': sym, 'strike': strike, 'type': c_type, 'bid': q.bid_price, 'ask': q.ask_price, 'delta': delta, 'theta': theta})
    
    tp = price + (spx_data['atr'] * 1.5) if direction == "BULL" else price - (spx_data['atr'] * 1.5)
    sl = price - (spx_data['atr'] * 1.0) if direction == "BULL" else price + (spx_data['atr'] * 1.0)

    contracts.sort(key=lambda x: x['strike'], reverse=(direction == "BEAR"))
    valid_contracts = [c for c in contracts if c['type'] == direction[0] and (c['strike'] >= price if direction == "BULL" else c['strike'] <= price)]

    for i in range(len(valid_contracts)-1):
        c1 = valid_contracts[i]
        for j in range(i+1, min(i+6, len(valid_contracts))):
            c2 = valid_contracts[j]
            spread_width = abs(c1['strike'] - c2['strike'])
            
            if 5 <= spread_width <= 10:
                cost = round(c1['ask'] - c2['bid'], 2)
                net_theta = c1['theta'] - c2['theta']
                if cost > 0 and net_theta > -1.5:
                    profit = round(spread_width - cost, 2)
                    send_alert(strat_name, c1['strike'], c2['strike'], cost, profit, spx_data, tp, sl, c1['delta'])
                    return

def send_alert(strat, s1, s2, cost, profit, data, tp, sl, delta):
    msg = (f"☢️ *تقرير القناص الأسطوري (SPX Greeks + ATR)* ☢️\n\n"
           f"🧱 *مستويات السعر اللحظية:*\n🔴 المقاومة: `{data['r1']}`\n🟢 الدعم: `{data['s1']}`\n\n"
           f"🎯 *الاستراتيجية:* {strat}\n\n"
           f"📊 *جدول عقود الأوبشن:*\n"
           f"| التكلفة (أقصى خسارة) | صافي الربح
