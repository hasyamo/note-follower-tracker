# note フォロワー推移トラッカー

noteのフォロワー数を毎日自動取得し、GitHub Pages でダッシュボード表示するツール。

## 🚀 セットアップ

### 1. リポジトリの設定

1. このリポジトリをフォークまたはテンプレートとして使用
2. **Settings** → **Variables** → **Repository variables** で以下を設定:
   - `NOTE_CREATOR_ID`: あなたのnoteクリエイターID（URLの `https://note.com/xxx` の `xxx` 部分）

### 2. GitHub Pages の有効化

1. **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. Save

### 3. Actions の権限設定

1. **Settings** → **Actions** → **General**
2. Workflow permissions: **Read and write permissions** を選択
3. Save

## 💻 ローカルでの実行

```bash
# .env ファイルを作成
cp .env.example .env
# NOTE_CREATOR_ID を自分のIDに編集

# 依存パッケージをインストール（オプション）
pip install python-dotenv

# 実行
python scripts/fetch_followers.py
```

## 📊 機能

- 毎日 JST 23:00 に自動でフォロワー数を取得
- GitHub Pages でダッシュボード表示
  - 現在のフォロワー数
  - 前日比・週間・月間の増減
  - フォロワー推移グラフ
  - 日次増減グラフ
  - 直近14日間の記録テーブル

## 🔧 手動実行

Actions タブから「Fetch Note Followers」を手動実行することも可能。

## 📁 ファイル構成

```
├── .github/workflows/
│   └── fetch-followers.yml   # GitHub Actions ワークフロー
├── scripts/
│   └── fetch_followers.py    # フォロワー取得スクリプト
├── data/
│   └── followers.json        # 取得データ（自動更新）
├── index.html                # ダッシュボード
└── README.md
```

## ⚠️ 注意事項

- noteの非公式APIを使用しています。仕様変更により動作しなくなる可能性があります。
- 1日1回の実行を推奨。頻繁なアクセスは避けてください。

## 📝 ライセンス

MIT
