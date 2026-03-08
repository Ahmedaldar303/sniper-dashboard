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
                delta = abs(opt.get('greeks', {}).get('delta', 0) if opt.get('greeks') else 0)
                
                # استبعاد العقود البعيدة جداً أو العميقة جداً
                if bid == 0 or ask == 0 or delta < 0.15 or delta > 0.60:
                    continue
                
                cost = bid * 100
                profit = (ask - bid) * 100
                
                # الذكاء الإحصائي: حساب القيمة المتوقعة (Expected Value)
                win_prob = delta
                loss_prob = 1 - win_prob
                ev = (win_prob * profit) - (loss_prob * cost)
                
                # خوارزمية قرار القناص
                if ev > 0 and (profit / cost) >= 1.5:
                    signal = "🔥 صيد ثمين"
                elif ev > -20 and (profit / cost) >= 1:
                    signal = "⚠️ للمراقبة"
                else:
                    signal = "❌ تجاهل"

                processed_data.append({
                    "cost": cost,
                    "profit": profit,
                    "strike": opt.get('strike'),
                    "type": opt.get('option_type').upper(),
                    "ev": ev,
                    "signal": signal
                })
            
            # الترتيب: الصفقات ذات القيمة الإحصائية الأعلى تظهر أولاً
            processed_data = sorted(processed_data, key=lambda x: x['ev'], reverse=True)

            with open('options_data.json', 'w') as f:
                json.dump(processed_data[:10], f, indent=4)
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_options_data()
