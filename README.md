# 🇺🇸 米国主要小売業 財務分析ダッシュボード

Streamlitを使用した、米国主要小売業の財務データを可視化・分析するインタラクティブなダッシュボードアプリケーションです。

## 📊 主な機能

### 5つの分析タブ
- **💰 損益計算書**: 売上構成、営業利益率の比較
- **📊 貸借対照表**: 総資産、自己資本比率の分析
- **📈 財務指標**: 在庫効率、総資産回転率などの財務指標
- **💵 キャッシュフロー**: 営業CF、投資CF、フリーCFの比較
- **👥 労働生産性**: 従業員1人当たりの売上高・営業利益

### その他の機能
- 📈 過去5年間のトレンド分析（オプション）
- 📥 HTMLレポートのダウンロード（全タブ対応）
- 🎨 企業ごとの一貫したカラーリング
- 💱 通貨単位の切り替え（10億ドル / 百万ドル）
- 🏢 業態別のカテゴリフィルター

## 🚀 セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/your-username/us-retail-analysis.git
cd us-retail-analysis
```

### 2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 3. データファイルの配置
`data/` フォルダに `financial_data_us.xlsx` を配置してください。

```
us-retail-analysis/
├── app.py
├── data/
│   └── financial_data_us.xlsx  ← ここに配置
├── fonts/
│   └── ipaexg.ttf             ← オプション（日本語フォント）
└── requirements.txt
```

### 4. アプリケーションの起動
```bash
streamlit run app.py
```

ブラウザが自動的に開き、ダッシュボードが表示されます（通常は http://localhost:8501）。

## 🌐 Streamlit Cloudへのデプロイ

### 方法1: GitHub経由（推奨）
1. このリポジトリをGitHubにプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
3. 「New app」をクリック
4. リポジトリとブランチを選択
5. Main file path: `app.py`
6. データファイルをアップロード（後述）
7. 「Deploy」をクリック

### データファイルのアップロード方法

**オプションA: GitHubに含める（小さいファイルの場合）**
```bash
git add data/financial_data_us.xlsx
git commit -m "Add financial data"
git push
```

**オプションB: Streamlit Cloudで直接アップロード**
1. デプロイ後、アプリの設定から「Secrets」を開く
2. ファイルマネージャーを使用してアップロード

**オプションC: 外部ストレージ（大きいファイルの場合）**
- Google Drive、Dropbox、S3などからダウンロードするコードを追加

## 📁 プロジェクト構成

```
us-retail-analysis/
├── app.py                      # メインアプリケーション
├── requirements.txt            # 依存パッケージ
├── README.md                   # このファイル
├── .gitignore                  # Git除外設定
├── data/                       # データフォルダ
│   ├── .gitkeep               # フォルダ保持用
│   └── financial_data_us.xlsx # 財務データ（要配置）
└── fonts/                      # フォントフォルダ
    ├── .gitkeep               # フォルダ保持用
    └── ipaexg.ttf             # 日本語フォント（オプション）
```

## 📊 データフォーマット

`financial_data_us.xlsx` は以下の列を含む必要があります：

### 必須列
- `企業名`: 企業名
- `決算年度`: 決算年度（数値）
- `売上高`: 売上高（ドル）
- `営業利益`: 営業利益（ドル）
- `営業利益率`: 営業利益率（%）

### 推奨列
- `売上原価`, `販管費`, `売上総利益`, `売上総利益率`, `販管費率`
- `総資産`, `流動資産`, `棚卸資産`, `純資産`, `有利子負債`, `自己資本比率`
- `営業CF`, `投資CF`, `フリーCF`
- `従業員数`, `棚卸資産回転率`, `総資産回転率`
- `全従業員1人当り売上高`, `全従業員1人当り営業利益`

### サンプルデータ形式

| 企業名 | 決算年度 | 売上高 | 営業利益 | 営業利益率 | ... |
|--------|----------|--------|----------|------------|-----|
| Walmart | 2024 | 648000000000 | 27670000000 | 4.27 | ... |
| Target | 2024 | 107410000000 | 5570000000 | 5.18 | ... |

## 🎨 カスタマイズ

### 業態カテゴリの追加・変更
`app.py` の `CATEGORY_GROUPS` を編集：

```python
CATEGORY_GROUPS = {
    'スーパー/BigBox': ['Walmart', 'Target', 'Kroger', ...],
    'ドラッグストア/医薬卸': ['CVS Health', 'McKesson', ...],
    # 新しいカテゴリを追加
    'あなたのカテゴリ': ['企業A', '企業B', ...],
}
```

### カラーパレットの変更
`COLORS['primary']` リストを編集：

```python
COLORS = {
    'primary': ['#2E86AB', '#A23B72', '#F18F01', ...],
}
```

## 🔧 トラブルシューティング

### データファイルが見つからない
```
⚠️ データファイルが見つかりません。
```
→ `data/financial_data_us.xlsx` が正しく配置されているか確認

### フォントが表示されない
日本語が文字化けする場合：
1. `fonts/ipaexg.ttf` を配置
2. システムフォントを使用（自動フォールバック）

### Streamlit Cloudでのメモリエラー
データサイズが大きい場合、以下を試してください：
1. データを必要な年度のみに絞る
2. 不要な列を削除
3. プランをアップグレード

## 📝 ライセンス

MIT License

## 🤝 コントリビューション

プルリクエストを歓迎します！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📧 お問い合わせ

質問やフィードバックがあれば、Issueを作成してください。

---

**Built with** ❤️ **using Streamlit**
