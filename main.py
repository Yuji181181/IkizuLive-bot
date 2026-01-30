"""
IkizuLive Weekly Bot - メインスクリプト

週次活動ログの自動投稿を実行します。
"""

import asyncio
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

from src.auth import initialize_twikit_client
from src.collector import collect_weekly_tweets
from src.summarizer import summarize_tweets
from src.poster import post_thread


async def main():
    """メイン処理"""
    print("=" * 60)
    print("IkizuLive 週次活動ログ自動投稿ボット (twikit版)")
    print("=" * 60)
    
    # 環境変数読み込み(.envファイルがある場合)
    load_dotenv()
    
    # 1. twikit認証
    print("\n[ステップ 1/4] twikit認証")
    print("-" * 60)
    client = await initialize_twikit_client()
    if not client:
        print("✗ 認証に失敗しました")
        return False
    
    # 2. ツイート収集
    print("\n[ステップ 2/4] ツイート収集")
    print("-" * 60)
    tweets = await collect_weekly_tweets(client)
    if not tweets:
        print("⚠ 収集されたツイートがありません")
        return False
    
    # 3. 要約生成
    print("\n[ステップ 3/4] 要約生成")
    print("-" * 60)
    posts = summarize_tweets(tweets)
    if not posts:
        print("✗ 要約生成に失敗しました")
        return False
    
    # 4. 投稿 (twikit使用)
    print("\n[ステップ 4/4] X投稿")
    print("-" * 60)
    success = await post_thread(client, posts)
    
    print("\n" + "=" * 60)
    if success:
        print("✓ 全処理完了！")
    else:
        print("✗ 投稿に失敗しました")
    print("=" * 60)
    
    return success


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
