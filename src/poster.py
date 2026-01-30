"""
IkizuLive Weekly Bot - 投稿モジュール

twikitを使用してスレッド形式で投稿します。
"""

import asyncio
import random
from typing import List

from twikit import Client

from src.config import MIN_WAIT_TIME, MAX_WAIT_TIME


async def post_thread(client: Client, posts: List[str]) -> bool:
    """
    スレッド形式でツイートを投稿します(twikit使用)。
    
    Args:
        client: 初期化済みのtwikitクライアント
        posts: 投稿テキストのリスト
    
    Returns:
        bool: 投稿成功時True
    """
    if not posts:
        print("⚠ 投稿するテキストがありません")
        return False
    
    print(f"\n投稿開始 ({len(posts)}ツイート)")
    
    try:
        # 最初のツイートを投稿
        first_tweet = await client.create_tweet(text=posts[0])
        print(f"  ✓ 1/{len(posts)} 投稿完了")
        
        # 残りをリプライとして投稿
        previous_tweet = first_tweet
        for i, text in enumerate(posts[1:], start=2):
            # 連続投稿対策: 少し待機
            wait_time = random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME)
            print(f"  → {wait_time:.1f}秒待機中...")
            await asyncio.sleep(wait_time)
            
            reply_tweet = await client.create_tweet(
                text=text,
                reply_to=previous_tweet.id
            )
            print(f"  ✓ {i}/{len(posts)} 投稿完了")
            previous_tweet = reply_tweet
        
        print("✓ 全ての投稿が完了しました")
        return True
    
    except Exception as e:
        print(f"✗ 投稿エラー: {e}")
        return False
