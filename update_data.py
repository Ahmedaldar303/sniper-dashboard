import requests
import json
import os

def fetch_options_data():
    # سحب التوكن من GitHub Secrets التي أضفتها
    ACCESS_TOKEN = os.environ.get("TRADIER_TOKEN") 
    
    symbol = "SPX"
    # تاريخ انتهاء قريب متاح في الـ Sandbox (تم تحديثه ليكون متوافقاً)
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
                processed_data.append({
                    "strike": opt.get('strike'),
                    "type": opt.get('option_type').upper(),
                    "cost": bid * 100,  # أقصى خسارة (التكلفة) كما طلبت
                    "profit": (ask - bid) * 100,  # صافي الربح
                    "delta": opt.get('greeks', {}).get('delta', 0) if opt.get('greeks') else 0,
                    "volume": opt.get('volume', 0)
                })
            
            # حفظ البيانات في ملف JSON ليقرأه المتصفح
            with open('options_data.json', 'w') as f:
                json.dump(processed_data, f, indent=4)
            print("Done: options_data.json updated.")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    fetch_options_data()
