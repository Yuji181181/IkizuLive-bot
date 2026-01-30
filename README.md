# IkizuLive Weekly Bot

イキヅライブ！の週次活動ログを自動投稿するボットです。

## 概要

- **収集**: 10個のターゲットアカウントから過去7日間のツイートを収集
- **要約**: Groq LLMを使用して活動ログを生成
- **投稿**: Xにスレッド形式で自動投稿
- **スケジュール**: 毎週日曜日22時(JST)に自動実行

## セットアップ

### 1. 依存関係のインストール

```bash
# uvをインストール(未インストールの場合)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係をインストール
uv sync
```

### 2. Cookie取得

ローカルでTwitterにログインしてCookieを取得します:

```bash
uv run python auth_helper.py
```

表示されたJSON文字列をコピーしてください。

### 3. Twitter API認証情報の取得

[Twitter Developer Portal](https://developer.twitter.com/)でアプリを作成し、以下を取得:

- API Key
- API Secret
- Access Token
- Access Token Secret

### 4. Groq APIキーの取得

[Groq Console](https://console.groq.com/)でAPIキーを取得してください。

### 5. GitHub Secretsの設定

GitHubリポジトリの `Settings > Secrets and variables > Actions` で以下のSecretsを追加:

| Secret名 | 説明 |
|---------|------|
| `GROQ_API_KEY` | Groq APIキー |
| `TWITTER_COOKIES_JSON` | auth_helper.pyで取得したCookie JSON |
| `TWITTER_API_KEY` | Twitter API Key |
| `TWITTER_API_SECRET` | Twitter API Secret |
| `TWITTER_ACCESS_TOKEN` | Twitter Access Token |
| `TWITTER_ACCESS_SECRET` | Twitter Access Token Secret |

### 6. ワークフローの有効化

`.github/workflows/weekly_post.yml`がリポジトリにプッシュされると、自動的にワークフローが有効になります。

## ローカルテスト

`.env`ファイルを作成して環境変数を設定:

```env
GROQ_API_KEY=your_groq_api_key
TWITTER_COOKIES_JSON={"cookie_data": "..."}
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

実行:

```bash
uv run python main.py
```

## 手動実行

GitHub Actionsから手動でワークフローを実行できます:

1. リポジトリの `Actions` タブを開く
2. `Weekly Activity Log Post` ワークフローを選択
3. `Run workflow` をクリック

## トラブルシューティング

### Cookieの有効期限切れ

Cookieは定期的に期限切れになります。エラーが発生した場合:

1. `auth_helper.py`を再実行してCookieを再取得
2. GitHub Secretsの`TWITTER_COOKIES_JSON`を更新

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
│   ├── config.py                # 設定
│   ├── auth.py                  # 認証
│   ├── collector.py             # ツイート収集
│   ├── summarizer.py            # 要約生成
│   └── poster.py                # 投稿
├── auth_helper.py               # Cookie取得ツール
├── main.py                      # メインスクリプト
├── pyproject.toml               # プロジェクト設定
├── .gitignore
└── README.md
```

## ライセンス

MIT License
