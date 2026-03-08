import requests
import json
import os

def fetch_options_data():
    # سحب التوكن من GitHub Secrets بشكل آمن
    ACCESS_TOKEN = os.environ.get("TRADIER_TOKEN") 
    
    # إعدادات جلب بيانات SPX
    symbol = "SPX"
    expiration = "2026-03-20"  # تاريخ انتهاء متاح في الـ Sandbox
    
    url = "https://sandbox.tradier.com/v1/markets/options/chains"
    params = {'symbol': symbol, 'expiration': expiration, 'greeks': 'true'}
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Accept': 'application/json'}

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            options_list = data.get('options', {}).get('option', [])
            
            # ترتيب البيانات (التكلفة، صافي الربح، السترايك) كما تفضل دائماً
            processed_data = []
            for opt in options_list:
                bid = opt.get('bid', 0)
                ask = opt.get('ask', 0)
                processed_data.append({
                    "strike": opt.get('strike'),
                    "type": opt.get('option_type'),
                    "cost": bid * 100,      # أقصى خسارة (التكلفة)
                    "profit": (ask - bid) * 100, # صافي الربح المتوقع
                    "delta": opt.get('greeks', {}).get('delta', 0),
                    "volume": opt.get('volume')
                })
            
            # حفظ النتائج في ملف JSON ليقرأه موقعك
            with open('options_data.json', 'w') as f:
                json.dump(processed_data, f, indent=4)
            print("تم تحديث ملف options_data.json بنجاح!")
        else:
            print(f"فشل الطلب: {response.status_code}")
    except Exception as e:
        print(f"خطأ تقني: {e}")

if __name__ == "__main__":
    fetch_options_data()
