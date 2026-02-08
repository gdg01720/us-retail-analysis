# コントリビューションガイド

このプロジェクトへの貢献を歓迎します！

## 開発環境のセットアップ

1. リポジトリをフォーク
2. ローカルにクローン
```bash
git clone https://github.com/your-username/us-retail-analysis.git
cd us-retail-analysis
```

3. 仮想環境の作成（推奨）
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

4. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

5. テストデータの配置
```bash
# data/financial_data_us.xlsx を配置
```

6. アプリケーションの起動
```bash
streamlit run app.py
```

## コントリビューションの流れ

1. **Issue を作成**
   - バグ報告、機能リクエスト、質問など
   - 既存のIssueを確認して重複を避ける

2. **ブランチを作成**
```bash
git checkout -b feature/your-feature-name
# または
git checkout -b fix/your-bug-fix
```

3. **変更を実装**
   - コードスタイルを統一
   - コメントを適切に追加
   - 必要に応じてドキュメントを更新

4. **テスト**
   - アプリケーションが正常に動作することを確認
   - エラーが発生しないことを確認

5. **コミット**
```bash
git add .
git commit -m "Add: 機能の説明"
# または
git commit -m "Fix: バグの説明"
```

6. **プッシュ**
```bash
git push origin feature/your-feature-name
```

7. **プルリクエスト作成**
   - 変更内容の説明を記載
   - スクリーンショットを追加（UI変更の場合）
   - 関連するIssueをリンク

## コーディング規約

### Python
- PEP 8 に準拠
- 関数にdocstringを追加
- 変数名は分かりやすく

### コミットメッセージ
- **Add:** 新機能追加
- **Fix:** バグ修正
- **Update:** 既存機能の更新
- **Refactor:** コードのリファクタリング
- **Docs:** ドキュメントの更新
- **Style:** コードスタイルの修正

例：
```
Add: キャッシュフロー分析タブを追加
Fix: データ読み込み時のエラーを修正
Update: チャートのカラーパレットを変更
```

## 機能リクエスト

以下のような機能追加を歓迎します：

- 新しい財務指標の追加
- チャートタイプの追加
- データエクスポート機能の拡張
- パフォーマンスの改善
- UIの改善

## バグ報告

バグを見つけた場合は、以下の情報を含めてIssueを作成してください：

- 再現手順
- 期待される動作
- 実際の動作
- エラーメッセージ（あれば）
- 環境情報（OS、Pythonバージョンなど）

## 質問・サポート

- GitHub Issuesで質問を投稿
- Discussions を活用（有効化されている場合）

## ライセンス

このプロジェクトに貢献することで、あなたの貢献がMITライセンスの下でライセンスされることに同意したものとみなされます。

---

ご協力ありがとうございます！🙏
