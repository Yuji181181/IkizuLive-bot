"""
IkizuLive Weekly Bot - 設定ファイル

対象メンバーのXアカウントとGroq設定を定義します。
"""

from pathlib import Path

# プロジェクトルートディレクトリ
ROOT_DIR = Path(__file__).parent.parent

# Cookieファイル(環境変数から復元)
COOKIES_FILE = ROOT_DIR / "cookies.json"

# ターゲットメンバーのXアカウント (10アカウント)
TARGET_MEMBERS = [
    "polka_lion",      # ポルカ
    "My_Mai_Eld",      # 麻衣
    "ShaunTheBunny",   # 翔音
    "MiracleGoldSP",   # 奇跡
    "Noricco_U",       # のりこ
    "LittlegreenCom",  # 真緑
    "Rollie_twinkle",  # 輝夜
    "Yukuri_talk",     # ゆくり
    "G_Akky304250",    # 玲
    "hanabistarmine",  # 花火
]

# メンバー名マッピング(ID -> キャラクター名)
MEMBER_NAMES = {
    "polka_lion": "ポルカ",
    "My_Mai_Eld": "麻衣",
    "ShaunTheBunny": "翔音",
    "MiracleGoldSP": "奇跡",
    "Noricco_U": "のりこ",
    "LittlegreenCom": "真緑",
    "Rollie_twinkle": "輝夜",
    "Yukuri_talk": "ゆくり",
    "G_Akky304250": "玲",
    "hanabistarmine": "花火",
}

# Groq設定
GROQ_MODEL = "llama-3.3-70b-versatile"

# システムプロンプト(移行ツールと同じ)
SYSTEM_PROMPT = """あなたは「イキヅライブ！」（正式名称:イキヅライブ！ LOVELIVE! BLUEBIRD）活動記録データベースの作成者です。
提供されたSNSログから、具体的な行動・出来事・移動・重要な会話のみを抽出し、週ごとの活動ログを作成してください。

## プロジェクト概要: 「イキヅライブ！」（いきづらい部！）
- **概要**: 「ラブライブ！シリーズ」の新規プロジェクト。インターネット高校「Love学院高等学校（通称:L高）」に通う10人の生徒たちが結成したスクールアイドル同好会「いきづらい部！」の活動を描く。
- **ストーリー形式**: 物語は主に**X（旧Twitter）上でのリアルタイム投稿**によって進行する。メンバー自身が発信する言葉や写真、動画がそのままストーリーの一部となっている。

## メンバー対応表（ID -> キャラクター名）
- **polka_lion**: ポルカ
- **My_Mai_Eld**: 麻衣
- **ShaunTheBunny**: 翔音
- **MiracleGoldSP**: 奇跡
- **Noricco_U**: のりこ
- **LittlegreenCom**: 真緑
- **Rollie_twinkle**: 輝夜
- **Yukuri_talk**: ゆくり
- **G_Akky304250**: 玲
- **hanabistarmine**: 花火

## ルール
1. **フォーマット**:
   - 各行は `MM/DD (メンバー名): 行動内容` の形式のみ。
   - 箇条書き記号（- や ・）は**つけない**。
   - 行動内容は簡潔に（体言止め推奨）。
2. **ノイズ除去**:
   - 挨拶のみ、感情のみの投稿は除外。
3. **出力**:
   - ログの行のみを出力すること。ヘッダーや挨拶は不要。

出力例:
09/08 (のりこ): 昭和歌謡の特集を見てイメージについて話した
09/08 (のりこ): おばあちゃんの十八番について話した"""

# レート制限設定(秒)
MIN_WAIT_TIME = 180   # 最小待機時間
MAX_WAIT_TIME = 180  # 最大待機時間

# 投稿設定
MAX_TWEET_LENGTH = 160  # 日本語全角文字数制限
