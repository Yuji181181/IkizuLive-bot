"""
IkizuLive Weekly Bot - Cookie取得ヘルパー (手動入力版)

ブラウザから取得したCookie情報（auth_token, ct0）を使用して
cookies.jsonを生成および検証します。
"""

import asyncio
import json
from pathlib import Path

from twikit import Client

async def main():
    print("=" * 60)
    print("IkizuLive Bot - Cookie手動設定ツール")
    print("=" * 60)
    print("\n自動ログインがブロックされたため、ブラウザのCookieを使用します。")
    print("\n【手順】")
    print("1. Chrome/EdgeでX(Twitter)にログインしてください")
    print("2. F12キーを押して「開発者ツール」を開きます")
    print("3. 「アプリケーション」タブ(Application) -> 左側「Cookie」 -> https://twitter.com または x.com を選択")
    print("4. 以下の2つの値をコピーして入力してください\n")

    auth_token = input("auth_token の値: ").strip()
    ct0 = input("ct0 (または csrf_token) の値: ").strip()

    if not auth_token or not ct0:
        print("✗ 値が入力されていません")
        return

    print("\n認証テスト中...")

    try:
        # クライアント初期化
        client = Client('ja-JP')
        
        # Cookieを手動設定
        # twikitは内部でhttpxを使用しており、cookiesをdictで渡せます
        cookies = {
            "auth_token": auth_token,
            "ct0": ct0
        }
        client.set_cookies(cookies)

        # ログイン確認（自分のユーザー情報を取得）
        user = await client.user()
        print(f"✓ 認証成功: @{user.screen_name} ({user.name})")

        # Cookieを保存
        cookies_file = Path("cookies.json")
        client.save_cookies(str(cookies_file))
        print(f"✓ Cookieを保存しました: {cookies_file}")

        # JSON表示
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies_data = json.load(f)
        
        cookies_json = json.dumps(cookies_data, ensure_ascii=False)

        print("\n" + "=" * 60)
        print("GitHub Secretsに登録するJSON文字列:")
        print("=" * 60)
        print(cookies_json)
        print("=" * 60)
        print("\n上記の文字列を GitHub Secrets (TWITTER_COOKIES_JSON) に登録してください。")

    except Exception as e:
        print(f"\n✗ 認証エラー: {e}")
        print("Cookieの値が正しいか、有効期限が切れていないか確認してください。")

if __name__ == "__main__":
    asyncio.run(main())
