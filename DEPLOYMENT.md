# デプロイガイド

このアプリケーションをStreamlit Cloudにデプロイする手順を説明します。

## 事前準備

### 1. GitHubアカウント
- GitHubアカウントを作成（持っていない場合）
- https://github.com

### 2. Streamlit Cloudアカウント
- Streamlit Cloudアカウントを作成
- https://streamlit.io/cloud
- GitHubアカウントでログイン

## デプロイ手順

### ステップ1: GitHubにプッシュ

1. **新しいリポジトリを作成**
```bash
# GitHub上で新しいリポジトリを作成
# 例: us-retail-analysis
```

2. **ローカルリポジトリを初期化**
```bash
cd us-retail-analysis
git init
git add .
git commit -m "Initial commit"
```

3. **リモートリポジトリに接続**
```bash
git remote add origin https://github.com/your-username/us-retail-analysis.git
git branch -M main
git push -u origin main
```

### ステップ2: データファイルの準備

**オプションA: GitHubに含める（小サイズの場合）**
```bash
# .gitignore からデータファイルのコメントを外す
# data/financial_data_us.xlsx をリポジトリに追加
git add data/financial_data_us.xlsx
git commit -m "Add financial data"
git push
```

**オプションB: Streamlit Secrets（推奨）**
```bash
# データファイルはGitHubに含めない
# Streamlit Cloudの管理画面から直接アップロード
```

### ステップ3: Streamlit Cloudでデプロイ

1. **Streamlit Cloud にログイン**
   - https://share.streamlit.io

2. **新しいアプリを作成**
   - 「New app」ボタンをクリック

3. **リポジトリを選択**
   - Repository: `your-username/us-retail-analysis`
   - Branch: `main`
   - Main file path: `app.py`

4. **Advanced settings（必要に応じて）**
   - Python version: 3.11
   - Secrets: データファイルのパスなど

5. **Deploy!**
   - デプロイボタンをクリック
   - 数分待つ

### ステップ4: データファイルのアップロード

**データファイルがGitHubにない場合:**

1. アプリの設定を開く
2. 「Settings」→「Secrets」
3. ファイルマネージャーを使用してアップロード
4. または、外部ストレージからダウンロードするコードを追加

## データファイルの外部ストレージ対応

### Google Drive から読み込む例

`app.py` に以下を追加：

```python
import gdown

@st.cache_data
def download_data_from_gdrive():
    url = 'https://drive.google.com/uc?id=YOUR_FILE_ID'
    output = 'data/financial_data_us.xlsx'
    gdown.download(url, output, quiet=False)
    return output

# データ読み込み前に実行
if not os.path.exists('data/financial_data_us.xlsx'):
    download_data_from_gdrive()
```

### Dropbox から読み込む例

```python
import urllib.request

@st.cache_data
def download_from_dropbox():
    url = 'https://www.dropbox.com/s/YOUR_FILE_LINK?dl=1'
    output = 'data/financial_data_us.xlsx'
    urllib.request.urlretrieve(url, output)
    return output
```

## トラブルシューティング

### デプロイエラー: ModuleNotFoundError

**原因**: 必要なパッケージが `requirements.txt` にない

**解決策**:
```bash
# requirements.txt を確認
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### メモリエラー

**原因**: データサイズが大きい、または計算量が多い

**解決策**:
1. データを必要な範囲に絞る
2. キャッシュを活用 (`@st.cache_data`)
3. Streamlit Cloudのプランをアップグレード

### データファイルが見つからない

**原因**: データファイルのパスが正しくない

**解決策**:
```python
# 絶対パスを使用
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data", "financial_data_us.xlsx")
```

### フォントが表示されない

**原因**: Streamlit CloudにIPAフォントがない

**解決策**:
1. フォントファイルをリポジトリに含める
2. または、システムフォントにフォールバック（自動対応済み）

## カスタムドメイン設定

Streamlit Cloudは無料プランでもカスタムドメインを設定できます。

1. 設定から「Custom domain」を選択
2. ドメインを入力（例: `finance.yourdomain.com`）
3. DNSレコードを設定
4. 反映を待つ（最大48時間）

## セキュリティ設定

### 認証の追加

Streamlit Cloudには組み込みの認証機能があります：

1. 設定から「Sharing」を選択
2. 「Require viewers to log in」を有効化
3. 許可するメールアドレスを追加

### Secrets の管理

機密情報は `secrets.toml` で管理：

```toml
# .streamlit/secrets.toml
[data]
file_id = "YOUR_GOOGLE_DRIVE_FILE_ID"

[database]
username = "your_username"
password = "your_password"
```

アプリ内で使用：
```python
file_id = st.secrets["data"]["file_id"]
```

## 更新手順

1. **ローカルで変更**
```bash
# コードを編集
git add .
git commit -m "Update: 機能を追加"
git push
```

2. **自動デプロイ**
   - Streamlit Cloudが自動的に再デプロイ
   - 数分で反映

## モニタリング

Streamlit Cloudの管理画面で以下を確認：

- アプリのステータス
- ログ
- リソース使用状況
- アクセス統計

## バックアップ

定期的にバックアップを取ることをお勧めします：

1. GitHubリポジトリ（コード）
2. データファイル（外部ストレージ）
3. 設定ファイル

---

**デプロイ成功おめでとうございます！** 🎉

問題が発生した場合は、[Streamlit ドキュメント](https://docs.streamlit.io/)を参照してください。
