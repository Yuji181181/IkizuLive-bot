# IkizuLive Weekly Bot

イキヅライブ！の週次活動ログを自動投稿するボットです。

## 概要

- **収集**: 10個のターゲットアカウントから、その週の月曜0時〜現在までのツイートを収集
- **要約**: Groq LLM（無料）を使用して活動ログを生成
- **投稿**: twikit（無料）を使用してXにスレッド形式で自動投稿
- **スケジュール**: 毎週日曜日22時(JST)に自動実行
- **通知**: Discord Webhookで実行結果を通知

## 特徴

✅ **完全無料**: Twitter API v2の有料プランは不要  
✅ **自動リトライ**: エラー時は最大3回自動リトライ  
✅ **レート制限対策**: メンバー間・ツイート間に60秒の待機時間  
✅ **詳細な通知**: Discord Webhookで成功/失敗を詳細に通知  
✅ **Cookie期限管理**: 約30〜90日ごとにCookie再取得が必要

## セットアップ

### 1. 依存関係のインストール

```bash
# uvをインストール(未インストールの場合)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係をインストール
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

[Groq Console](https://console.groq.com/)でAPIキーを取得してください（無料）。

### 4. Discord Webhook URLの取得（オプション）

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

**重要**: Secretsは**Repository secrets**として設定してください（Environment secretsではありません）。

### 6. ワークフローの有効化

`.github/workflows/weekly_post.yml`がリポジトリにプッシュされると、自動的にワークフローが有効になります。

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

**注意**: ローカル実行でも実際にツイートが投稿されます。

## 手動実行

GitHub Actionsから手動でワークフローを実行できます:

1. リポジトリの `Actions` タブを開く
2. `Weekly Activity Log Post` ワークフローを選択
3. `Run workflow` をクリック

## 動作仕様

### 収集期間

- **開始**: その週の月曜日 00:00 (JST)
- **終了**: 実行時刻（現在時刻）
- 例: 日曜22時に実行 → 月曜0時〜日曜22時のツイートを収集

### 実行スケジュール

- **自動実行**: 毎週日曜日 22:00 (JST)
- **cron**: `0 13 * * 0` (UTC 13:00 = JST 22:00)

### レート制限対策

- メンバー間の待機時間: 60秒
- ツイート投稿間の待機時間: 60秒
- エラー時のリトライ間隔: 60秒、120秒、180秒

### Discord通知

**成功時**:
- ✅ タイトル: 成功
- 📅 実行時刻（JST）
- 🔗 ワークフロー実行ログへのリンク
- 📊 ステータス

**失敗時**:
- ❌ タイトル: 失敗
- 📅 実行時刻（JST）
- 🔗 ワークフロー実行ログへのリンク
- ❗ エラー内容（自動抽出）
- 🔧 考えられる原因
- 💡 対処方法

## トラブルシューティング

### Cookieの有効期限切れ

Cookieは**30〜90日程度**で期限切れになります。エラーが発生した場合:

1. `auth_helper.py`を再実行してCookieを再取得
2. GitHub Secretsの`TWITTER_COOKIES_JSON`を更新
3. ワークフローを手動で再実行

**推奨**: 月1回程度、定期的にCookieを更新

### レート制限エラー

X APIのレート制限に引っかかった場合、自動的にリトライされます。それでも失敗する場合は、次回の実行を待ってください。

### 認証エラー

```
⚠ 環境変数TWITTER_COOKIES_JSONが設定されていません
```

→ GitHub Secretsが正しく設定されているか確認してください。**Repository secrets**として設定する必要があります。

### Discord通知が届かない

1. `DISCORD_WEBHOOK_URL`が正しく設定されているか確認
2. Webhook URLが有効か確認（削除されていないか）
3. ワークフローログで通知ステップを確認

## プロジェクト構成

```
IkizuLive-bot/
├── .github/
│   └── workflows/
│       └── weekly_post.yml      # GitHub Actionsワークフロー
├── src/
│   ├── __init__.py
│   ├── config.py                # 設定（メンバーリスト、待機時間など）
│   ├── auth.py                  # twikit認証
│   ├── collector.py             # ツイート収集（twikit使用）
│   ├── summarizer.py            # 要約生成（Groq使用）
│   └── poster.py                # 投稿（twikit使用、リトライ機能付き）
├── auth_helper.py               # Cookie取得ツール
├── main.py                      # メインスクリプト
├── pyproject.toml               # プロジェクト設定
├── .gitignore
└── README.md
```

## 技術スタック

- **Python**: 3.12
- **パッケージマネージャー**: uv
- **ツイート収集**: twikit（無料、非公式API）
- **ツイート投稿**: twikit（無料、非公式API）
- **LLM**: Groq（無料）
- **CI/CD**: GitHub Actions（無料）
- **通知**: Discord Webhook（無料）

## 注意事項

⚠️ **非公式APIの使用**: twikitは非公式APIを使用しているため、アカウントがロック/凍結されるリスクがあります。週1回の投稿であればリスクは低いですが、自己責任でご使用ください。

⚠️ **Cookie管理**: Cookieには認証情報が含まれるため、厳重に管理してください。GitHub Secretsに保存し、公開リポジトリにコミットしないでください。