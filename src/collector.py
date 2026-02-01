"""
IkizuLive Weekly Bot - ツイート収集モジュール

過去7日間のツイートを収集します。
"""

import asyncio
import random
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

from twikit import Client, TooManyRequests

from src.config import TARGET_MEMBERS, MIN_WAIT_TIME, MAX_WAIT_TIME

# 日本時間(JST)のタイムゾーン
JST = timezone(timedelta(hours=9))


async def collect_weekly_tweets(client: Client) -> List[Dict[str, Any]]:
    """
    過去7日間（168時間）のツイートを全メンバーから収集します。
    
    Args:
        client: 初期化済みのtwikitクライアント
    
    Returns:
        List[Dict[str, Any]]: ツイートデータのリスト
    """
    # 現在時刻(JST)
    now = datetime.now(JST)
    
    # 7日前（168時間前）を計算
    start_date = now - timedelta(days=7)
    end_date = now
    
    print(f"\n収集期間(JST): {start_date.strftime('%Y-%m-%d %H:%M')} ~ {end_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"対象メンバー: {len(TARGET_MEMBERS)}人\n")
    
    all_tweets = []
    
    for i, username in enumerate(TARGET_MEMBERS, 1):
        print(f"[{i}/{len(TARGET_MEMBERS)}] {username}")
        
        try:
            tweets = await _fetch_user_tweets(client, username, start_date, end_date)
            all_tweets.extend(tweets)
            print(f"  ✓ {len(tweets)}件取得")
            
            # レート制限対策: 次のユーザーまで待機
            if i < len(TARGET_MEMBERS):
                wait_time = random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME)
                print(f"  → {wait_time:.1f}秒待機中...")
                await asyncio.sleep(wait_time)
        
        except Exception as e:
            print(f"  ✗ エラー: {e}")
            continue
    
    print(f"\n✓ 合計 {len(all_tweets)}件のツイートを収集しました")
    return all_tweets


async def _fetch_user_tweets(
    client: Client,
    username: str,
    start_date: datetime,
    end_date: datetime,
    retry_count: int = 0
) -> List[Dict[str, Any]]:
    """
    指定ユーザーの指定期間のツイートを取得します。
    
    Args:
        client: twikitクライアント
        username: ユーザー名
        start_date: 開始日
        end_date: 終了日
        retry_count: リトライ回数
    
    Returns:
        List[Dict[str, Any]]: ツイートデータのリスト
    """
    # 終了日が未来の場合は現在時刻に制限
    now = datetime.now(JST)
    actual_end_date = min(end_date, now)
    
    # 検索クエリ作成
    query = (
        f"from:{username} "
        f"since:{start_date.strftime('%Y-%m-%d')} "
        f"until:{actual_end_date.strftime('%Y-%m-%d')} "
        f"include:replies"
    )
    
    try:
        # ツイート検索
        tweets = await client.search_tweet(query, product='Latest')
        
        # データ抽出
        tweet_list = []
        if tweets:
            for tweet in tweets:
                tweet_list.append({
                    'id': tweet.id,
                    'created_at': tweet.created_at,
                    'text': tweet.text,
                    'user': tweet.user.screen_name,
                })
        
        return tweet_list
    
    except TooManyRequests as e:
        # 429エラー: リトライ
        if retry_count < 3:
            backoff_time = (2 ** retry_count) * 60
            print(f"  ⚠ レート制限エラー (429)")
            print(f"  → {backoff_time:.0f}秒待機してリトライ ({retry_count + 1}/3)")
            await asyncio.sleep(backoff_time)
            return await _fetch_user_tweets(client, username, start_date, end_date, retry_count + 1)
        else:
            print(f"  ✗ 最大リトライ回数に達しました")
            raise
    
    except Exception as e:
        print(f"  ✗ 取得エラー: {e}")
        return []
