# IkizuLive Weekly Bot

イキヅライブ！の週次活動ログを自動投稿するボットです。

## 概要

- **収集**: 10個のターゲットアカウントから、過去7日間（168時間）のツイートを収集
- **要約**: Groq LLMを使用して活動ログを生成
- **投稿**: Xにスレッド形式で自動投稿
- **スケジュール**: 毎週日曜日22時(JST)に自動実行
- **通知**: Discord Webhookで実行結果を詳細に通知

## 特徴

✅ **完全無料**: 有料プランは不要  
✅ **自動リトライ**: エラー時は最大3回自動リトライ（60秒、120秒、180秒間隔）  
✅ **レート制限対策**: メンバー間・ツイート間に60秒の待機時間  
✅ **詳細な通知**: Discord Webhookで成功/失敗を詳細に通知（エラー内容を自動抽出）  
✅ **Cookie期限管理**: 約30〜90日ごとにCookie再取得が必要  
✅ **重複検出**: 既に投稿済みのツイートは自動スキップ

## セットアップ

### 1. 依存関係のインストール

```bash
uv sync
```

### 2. Cookie取得

ブラウザでX（Twitter）にログインし、開発者ツールからCookieを取得します:

```bash
uv run python auth_helper.py
```

**手順**:
1. Chrome/EdgeでX(Twitter)にログイン
2. F12キーを押して「開発者ツール」を開く
3. 「アプリケーション」タブ > 「Cookie」 > `x.com` を選択
4. `auth_token` と `ct0` の値をコピー
5. `auth_helper.py` に入力
6. 表示されたJSON文字列をコピー

### 3. Groq APIキーの取得

[Groq Console](https://console.groq.com/)でAPIキーを取得してください。

### 4. Discord Webhook URLの取得

実行結果をDiscordに通知したい場合:

1. Discordで通知を受け取りたいチャンネルを開く
2. チャンネル設定 > 連携サービス > ウェブフック
3. 「新しいウェブフック」を作成
4. Webhook URLをコピー

### 5. GitHub Secretsの設定

GitHubリポジトリの `Settings > Secrets and variables > Actions` で以下のSecretsを追加:

| Secret名 | 説明 | 必須 |
|---------|------|------|
| `GROQ_API_KEY` | Groq APIキー | ✅ |
| `TWITTER_COOKIES_JSON` | auth_helper.pyで取得したCookie JSON | ✅ |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | ⭕ (オプション) |


## ローカルテスト

`.env`ファイルを作成して環境変数を設定:

```env
GROQ_API_KEY=your_groq_api_key
TWITTER_COOKIES_JSON={"auth_token": "...", "ct0": "...", ...}
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

実行:

```bash
uv run python main.py
```


## 動作仕様

### 収集期間

- **期間**: 実行時刻から過去7日間（168時間）

### 実行スケジュール

- **自動実行**: 毎週日曜日 22:00 (JST)
- **cron**: UTC 13:00 = JST 22:00

### レート制限対策

- **メンバー間の待機時間**: 60秒
- **ツイート投稿間の待機時間**: 60秒
- **エラー時のリトライ間隔**: 60秒、120秒、180秒（指数バックオフ）
- **最大リトライ回数**: 3回

### Discord通知

**成功時**:
- ✅ タイトル: 成功
- 📅 実行時刻（JST）
- 🔗 ワークフロー実行ログへのリンク
- 📊 ステータス: 全処理完了

**失敗時**:
- ❌ タイトル: 失敗
- 📅 実行時刻（JST）
- 🔗 ワークフロー実行ログへのリンク
- ❗ **エラー内容**（ボット出力から自動抽出）
- 🔧 考えられる原因
  - Cookie期限切れ
  - ツイートが0件（収集失敗）
  - API制限
  - ネットワークエラー
- 💡 対処方法

## トラブルシューティング

### Cookieの有効期限切れ

エラーが発生した場合:

1. `auth_helper.py`を再実行してCookieを再取得
2. GitHub Secretsの`TWITTER_COOKIES_JSON`を更新
3. ワークフローを手動で再実行


### レート制限エラー

X APIのレート制限に引っかかった場合、自動的にリトライされます。それでも失敗する場合は、次回の実行を待ってください。



## プロジェクト構成

```
IkizuLive-bot/
├── .github/
│   └── workflows/
│       └── weekly_post.yml      # GitHub Actionsワークフロー
├── src/
│   ├── __init__.py
│   ├── config.py                # 設定（メンバーリスト、待機時間など）
│   ├── auth.py                  # twikit認証、Cookie復元
│   ├── collector.py             # ツイート収集
│   ├── summarizer.py            # 要約生成（Groq使用）、ツイート分割
│   └── poster.py                # 投稿
├── auth_helper.py               # Cookie取得ツール
├── main.py                      # メインスクリプト
├── pyproject.toml               # プロジェクト設定
├── .gitignore
└── README.md
```

## 技術スタック

- **Python**: 3.12
- **パッケージマネージャー**: uv
- **ツイート収集**: twikit
- **ツイート投稿**: twikit
- **LLM**: Groq
- **CI/CD**: GitHub Actions
- **通知**: Discord Webhook

## 主要機能の詳細

### ツイート収集

- **対象**: `src/config.py`の`TARGET_MEMBERS`に定義された10アカウント
- **期間**: 実行時刻から過去7日間（168時間）
- **検索クエリ**: `from:{username} since:{date}`
- **レート制限対策**: メンバー間に60秒の待機時間

### 要約生成

- **LLM**: Groq（llama-3.3-70b-versatile）
- **プロンプト**: `src/config.py`の`SYSTEM_PROMPT`で定義
- **分割**: 160文字以内に自動分割してスレッド形式で投稿

### 投稿

- **形式**: スレッド形式（最初のツイート + リプライ）
- **リトライ**: 各ツイートで最大3回リトライ
- **重複検出**: `DuplicateTweet`エラーを検出して自動スキップ
- **待機時間**: ツイート間に60秒の待機