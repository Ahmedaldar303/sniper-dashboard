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
                processed_data.append({
                    "cost": bid * 100,
                    "profit": (ask - bid) * 100,
                    "strike": opt.get('strike'),
                    "type": opt.get('option_type').upper(),
                    "delta": opt.get('greeks', {}).get('delta', 0) if opt.get('greeks') else 0,
                    "theta": opt.get('greeks', {}).get('theta', 0) if opt.get('greeks') else 0,
                    "volume": opt.get('volume', 0)
                })
            
            dashboard_data = {
                "market_context": {
                    "direction": "صاعد (Bullish)",
                    "spx_support": "5080",
                    "spx_resistance": "5150",
                    "ndx_support": "17900",
                    "ndx_resistance": "18200"
                },
                "options": processed_data
            }

            with open('options_data.json', 'w') as f:
                json.dump(dashboard_data, f, indent=4)
            print("Done")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_options_data()
