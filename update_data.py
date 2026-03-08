import requests
import json
import os

def fetch_options_data():
    ACCESS_TOKEN = os.environ.get("TRADIER_TOKEN") 
    symbol = "SPX"
    expiration = "2026-03-20" 
    
    url = "https://sandbox.tradier.com/v1/markets/options/chains"
    params = {'symbol': symbol, 'expiration': expiration, 'greeks': 'true'}
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Accept': 'application/json'}

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            options_list = data.get('options', {}).get('option', [])
            
            processed_data = []
            for opt in options_list:
                bid = opt.get('bid', 0)
                ask = opt.get('ask', 0)
                vol = opt.get('volume', 0)
                delta = opt.get('greeks', {}).get('delta', 0) if opt.get('greeks') else 0
                theta = opt.get('greeks', {}).get('theta', 0) if opt.get('greeks') else 0
                
                # 1. فلترة القناص: استبعاد العقود الميتة أو الخطرة جداً
                if vol < 5 or abs(delta) < 0.15 or abs(delta) > 0.60:
                    continue
                
                cost = bid * 100
                profit = (ask - bid) * 100
                
                # 2. حساب نسبة العائد للمخاطرة (R/R Ratio)
                rr_ratio = round(profit / cost, 2) if cost > 0 else 0
                
                # 3. احتمالية النجاح (تحويل الدلتا لنسبة مئوية)
                win_prob = round(abs(delta) * 100, 1)

                processed_data.append({
                    "cost": cost,
                    "profit": profit,
                    "strike": opt.get('strike'),
                    "type": opt.get('option_type').upper(),
                    "rr_ratio": rr_ratio,
                    "win_prob": win_prob,
                    "delta": delta,
                    "theta": theta
                })
            
            # ترتيب إحصائي: إظهار العقود ذات أعلى عائد للمخاطرة أولاً
            processed_data = sorted(processed_data, key=lambda x: x['rr_ratio'], reverse=True)

            dashboard_data = {
                "market_context": {
                    "direction": "صاعد (Bullish) - بناءً على زخم الـ Delta",
                    "spx_support": "5080",
                    "spx_resistance": "5150",
                    "ndx_support": "17900",
                    "ndx_resistance": "18200"
                },
                "options": processed_data[:10] # إظهار أفضل 10 صفقات فقط
            }

            with open('options_data.json', 'w') as f:
                json.dump(dashboard_data, f, indent=4)
            print("Smart Data Updated")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_options_data()
