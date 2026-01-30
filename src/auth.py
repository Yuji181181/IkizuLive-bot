"""
IkizuLive Weekly Bot - 認証モジュール

Cookie復元とtwikit初期化を提供します。
"""

import json
import os
from twikit import Client
from src.config import COOKIES_FILE


def restore_cookies_from_env() -> bool:
    """
    環境変数TWITTER_COOKIES_JSONからcookies.jsonを復元します。
    
    Returns:
        bool: 復元成功時True
    """
    cookies_json = os.getenv("TWITTER_COOKIES_JSON")
    
    if not cookies_json:
        print("⚠ 環境変数TWITTER_COOKIES_JSONが設定されていません")
        return False
    
    try:
        # JSON文字列をパース
        cookies_data = json.loads(cookies_json)
        
        # ファイルに書き出し
        with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Cookieを復元しました: {COOKIES_FILE}")
        return True
    
    except json.JSONDecodeError as e:
        print(f"✗ Cookie JSONのパースに失敗: {e}")
        return False
    except Exception as e:
        print(f"✗ Cookie復元エラー: {e}")
        return False


async def initialize_twikit_client() -> Client:
    """
    twikitクライアントを初期化します。
    
    Returns:
        Client: 初期化されたクライアント、失敗時None
    """
    # Cookie復元
    if not COOKIES_FILE.exists():
        if not restore_cookies_from_env():
            print("✗ Cookieファイルが見つかりません")
            return None
    
    try:
        client = Client('ja-JP')
        client.load_cookies(str(COOKIES_FILE))
        print("✓ twikitクライアント初期化完了")
        return client
    
    except Exception as e:
        print(f"✗ twikitクライアント初期化エラー: {e}")
        return None
