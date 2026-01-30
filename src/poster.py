"""
IkizuLive Weekly Bot - 投稿モジュール

twikitを使用してスレッド形式で投稿します。
"""

import asyncio
import random
from typing import List

from twikit import Client
from twikit.errors import DuplicateTweet

from src.config import MIN_WAIT_TIME, MAX_WAIT_TIME


async def post_thread(client: Client, posts: List[str]) -> bool:
    """
    スレッド形式でツイートを投稿します(twikit使用、リトライ機能付き)。
    
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
        # 最初のツイートを投稿(リトライロジック付き)
        first_tweet = None
        max_retries = 3
        
        for retry in range(max_retries):
            try:
                first_tweet = await client.create_tweet(text=posts[0])
                print(f"  ✓ 1/{len(posts)} 投稿完了")
                break  # 成功したらループを抜ける
            except DuplicateTweet:
                print(f"  ⚠ 1/{len(posts)} 重複スキップ(既に投稿済み)")
                # 重複の場合、この週は既に投稿済みとみなす
                return True
            except Exception as retry_error:
                if retry < max_retries - 1:
                    wait_time = (retry + 1) * 60  # 60秒, 120秒, 180秒
                    print(f"  ⚠ 1/{len(posts)} エラー発生。{wait_time}秒後にリトライ... ({retry + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                else:
                    # 最後のリトライでも失敗した場合は例外を再発生
                    raise retry_error
        
        if first_tweet is None:
            # リトライ後も投稿できなかった場合
            return False
        
        # 残りをリプライとして投稿
        previous_tweet = first_tweet
        for i, text in enumerate(posts[1:], start=2):
            # 連続投稿対策: 待機
            wait_time = random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME)
            print(f"  → {wait_time:.1f}秒待機中...")
            await asyncio.sleep(wait_time)
            
            # リトライロジック
            max_retries = 3
            for retry in range(max_retries):
                try:
                    reply_tweet = await client.create_tweet(
                        text=text,
                        reply_to=previous_tweet.id
                    )
                    print(f"  ✓ {i}/{len(posts)} 投稿完了")
                    previous_tweet = reply_tweet
                    break  # 成功したらループを抜ける
                except DuplicateTweet:
                    print(f"  ⚠ {i}/{len(posts)} 重複スキップ(既に投稿済み)")
                    # 重複の場合もスキップして続行
                    break
                except Exception as retry_error:
                    if retry < max_retries - 1:
                        wait_time = (retry + 1) * 60  # 60秒, 120秒, 180秒
                        print(f"  ⚠ {i}/{len(posts)} エラー発生。{wait_time}秒後にリトライ... ({retry + 1}/{max_retries})")
                        await asyncio.sleep(wait_time)
                    else:
                        # 最後のリトライでも失敗した場合は例外を再発生
                        raise retry_error
        
        print("✓ 全ての投稿が完了しました")
        return True
    
    except Exception as e:
        # エラーの詳細を安全に表示
        import traceback
        
        print(f"✗ 投稿エラー: {type(e).__name__}: {str(e)}")
        
        # 例外の属性を確認
        if hasattr(e, '__dict__') and e.__dict__:
            print(f"   例外属性: {e.__dict__}")
        
        # レスポンス情報があれば表示
        if hasattr(e, 'response'):
            print(f"   レスポンス: {e.response}")
        
        # トレースバックの最後の数行を表示
        tb_lines = traceback.format_exc().split('\n')
        print(f"   トレースバック:")
        for line in tb_lines[-5:]:
            if line.strip():
                print(f"     {line}")
        
        return False
