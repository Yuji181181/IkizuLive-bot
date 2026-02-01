"""
IkizuLive Weekly Bot - 要約モジュール

Groq APIを使用して活動ログを生成します。
"""

import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

from groq import Groq

from src.config import GROQ_MODEL, SYSTEM_PROMPT, MAX_TWEET_LENGTH

# 日本時間(JST)のタイムゾーン
JST = timezone(timedelta(hours=9))


def summarize_tweets(tweets: List[Dict[str, Any]]) -> List[str]:
    """
    ツイートリストを要約して投稿用テキストのリストを返します。
    
    Args:
        tweets: ツイートデータのリスト
    
    Returns:
        List[str]: 投稿用テキストのリスト(160文字以内に分割済み)
    """
    if not tweets:
        print("⚠ 要約対象のツイートがありません")
        return []
    
    # Groq APIキー確認
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("✗ GROQ_API_KEY環境変数が設定されていません")
        return []
    
    # Groqクライアント初期化
    client = Groq(api_key=api_key)
    
    # プロンプト作成
    tweets_text = _create_prompt(tweets)
    
    print(f"\n要約生成中... ({len(tweets)}件のツイート)")
    
    try:
        # Groq API呼び出し
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": tweets_text}
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        
        summary_text = response.choices[0].message.content.strip()
        
        if not summary_text:
            print("⚠ 要約が生成されませんでした")
            return []
        
        print("✓ 要約生成完了")
        
        # 投稿用に分割
        posts = _split_into_posts(summary_text)
        print(f"✓ {len(posts)}個のツイートに分割しました")
        
        return posts
    
    except Exception as e:
        print(f"✗ 要約生成エラー: {e}")
        return []


def _create_prompt(tweets: List[Dict[str, Any]]) -> str:
    """
    ツイートリストからプロンプトを作成します。
    
    Args:
        tweets: ツイートデータのリスト
    
    Returns:
        str: プロンプト文字列
    """
    # 日付でソート
    sorted_tweets = sorted(tweets, key=lambda x: x['created_at'])
    
    # ツイートテキストを日付付きで整形
    tweet_lines = []
    for tweet in sorted_tweets:
        # created_atをパース
        try:
            if isinstance(tweet['created_at'], str):
                # 文字列の場合はパース
                date_str = datetime.strptime(
                    tweet['created_at'],
                    '%a %b %d %H:%M:%S %z %Y'
                ).strftime('%Y-%m-%d')
            else:
                # datetimeオブジェクトの場合
                date_str = tweet['created_at'].strftime('%Y-%m-%d')
        except:
            # パースできない場合は現在日時
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        user = tweet['user']
        text = tweet['text'].replace('\n', ' ')
        tweet_lines.append(f"[{date_str}] @{user}: {text}")
    
    return '\n'.join(tweet_lines)


def _split_into_posts(summary_text: str) -> List[str]:
    """
    要約テキストを投稿用に分割します。
    
    Args:
        summary_text: 要約テキスト
    
    Returns:
        List[str]: 分割されたテキストのリスト
    """
    # 期間ヘッダーを作成（過去7日間、JST）
    now = datetime.now(JST)
    start_date = now - timedelta(days=7)
    
    header = f"{start_date.strftime('%Y/%m/%d')} - {now.strftime('%Y/%m/%d')}\nイキヅライブ！活動ログ\n\n"
    
    posts = []
    current_chunk = header
    is_first_chunk = True
    
    lines = summary_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 次の行を追加したときの長さをチェック
        # 155文字制限(余裕を持たせる)
        if len(current_chunk) + len(line) + 1 > 155:
            posts.append(current_chunk.strip())
            # 新しいブロック作成
            current_chunk = line
            is_first_chunk = False
        else:
            if is_first_chunk and current_chunk == header:
                current_chunk += line
            elif not is_first_chunk and not current_chunk:
                current_chunk = line
            else:
                current_chunk += "\n" + line
    
    # 最後のブロックを追加
    if current_chunk and current_chunk != header:
        posts.append(current_chunk.strip())
    
    return posts
