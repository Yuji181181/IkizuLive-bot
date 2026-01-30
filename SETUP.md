# IkizuLive Weekly Bot - セットアップガイド

## 概要

このボットは**完全無料**で運用できるように設計されています。
Twitter公式API(有料)の代わりに、`twikit`ライブラリを使用してCookie認証で動作します。

- **収集**: twikitを使用
- **要約**: Groq API (無料)を使用
- **投稿**: twikitを使用 (Cookie認証)
- **CI/CD**: GitHub Actions (無料枠)

## セットアップ手順

### 1. 依存関係のインストール

```bash
cd IkizuLive-bot
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

**入力項目:**
- ユーザー名
- メールアドレス
- パスワード

**出力:**
- `cookies.json`ファイルが作成されます
- GitHub Secretsに登録するJSON文字列が表示されます

**重要:** 表示されたJSON文字列をコピーしてください。

### 3. Groq APIキーの取得

[Groq Console](https://console.groq.com/)でAPIキーを取得します。

### 4. GitHub Secretsの設定

GitHubリポジトリの `Settings > Secrets and variables > Actions` で以下の**2つのSecrets**を追加します:

| Secret名 | 説明 |
|---------|------|
| `GROQ_API_KEY` | Groq APIキー |
| `TWITTER_COOKIES_JSON` | auth_helper.pyで取得したCookie JSON |

※ `TWITTER_API_KEY` などのAPIキーは**不要**です。

### 5. リポジトリにプッシュ

```bash
git add .
git commit -m "Refactor: Switch to twikit for free posting"
git push origin main
```

## ローカルテスト

`.env`ファイルを作成して環境変数を設定:

```env
GROQ_API_KEY=your_groq_api_key
TWITTER_COOKIES_JSON={"cookie_data": "..."}
```

実行:

```bash
uv run python main.py
```

## 注意事項

⚠️ **アカウント凍結リスク**
公式APIを使用しないため、過度な投稿を行うとアカウントがロックされる可能性があります。
本ボットは週1回の投稿頻度であり、適切なWait処理を入れていますが、リスクを理解した上で運用してください。

⚠️ **Cookieの有効期限**
Cookieは定期的に期限切れになります。エラーが発生した場合は、`auth_helper.py`を再実行してSecretsを更新してください。

## 構成
```
IkizuLive-bot/
├── .github/workflows/weekly_post.yml
├── src/
│   ├── auth.py         # Cookie認証
│   ├── collector.py    # ツイート収集
│   ├── summarizer.py   # Groq要約
│   ├── poster.py       # twikit投稿
├── main.py             # メインスクリプト
```
