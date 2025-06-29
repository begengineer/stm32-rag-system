# STマイクロマイコン RAGシステム

マイコン初心者向けのQ&A・サンプルコード生成システムです。STマイクロエレクトロニクスのNUCLEO-F767ZIマイコンに関する質問に答え、実用的なサンプルコードを生成します。

## 🎯 主な機能

### 💬 Q&A システム
- マイコンの基本的な使い方
- CubeMXの操作方法  
- 回路設計のアドバイス
- トラブルシューティング
- 初心者向けの分かりやすい説明

### ⚡ サンプルコード生成
- LED制御、ボタン入力、PWM制御などの基本機能
- 詳細なコメント付きコード
- 初心者でも理解しやすい構造
- カスタム要求への対応

### 🔍 ドキュメント検索
- 技術文書からの情報検索
- アプリケーションノートの参照
- ユーザーマニュアルの検索
- 関連度による結果ランキング

### 📊 マイコン情報表示
- ハードウェア仕様
- ペリフェラル情報
- 開発ボード対応状況
- 用途別推奨情報

## 🏗️ システム構成

```
rag_system/
├── app/                     # アプリケーションコード
│   ├── main.py             # メインアプリケーション
│   ├── config.py           # 設定ファイル
│   ├── models/             # データモデル
│   │   ├── rag_engine.py   # RAGエンジン
│   │   └── vector_db.py    # ベクトルデータベース
│   ├── services/           # サービス層
│   │   ├── document_processor.py    # ドキュメント処理
│   │   ├── code_generator.py        # コード生成
│   │   └── microcontroller_selector.py # マイコン選択
│   ├── utils/              # ユーティリティ
│   └── ui/                 # UIコンポーネント
├── data/                   # データディレクトリ
│   ├── documents/          # 処理済みドキュメント
│   ├── vector_store/       # ベクトルデータベース
│   └── microcontrollers/   # マイコン別データ
└── docs/                   # ドキュメント
```

## 📋 システム要件

- **Python**: 3.8以上
- **メモリ**: 4GB以上推奨
- **ディスク容量**: 1GB以上の空き容量
- **インターネット接続**: OpenAI API利用のため必要

### 必要なライブラリ
- streamlit: Webアプリケーションフレームワーク
- langchain: RAGフレームワーク
- chromadb: ベクトルデータベース
- sentence-transformers: 埋め込みモデル
- openai: OpenAI API クライアント
- その他（requirements.txt参照）

## 🚀 セットアップ手順

### 1. プロジェクトの準備
```bash
cd rag_system
```

### 2. 自動セットアップの実行
```bash
python setup.py
```

### 3. 環境変数の設定
`.env`ファイルを編集してOpenAI API keyを設定:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 4. ドキュメントの配置
以下のファイルを適切な場所に配置:
- `nucleo-f767zi.pdf` (製品概要)
- `um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf` (ユーザーマニュアル)
- `um1727-getting-started-with-stm32-nucleo-board-software-development-tools-stmicroelectronics.pdf`
- `tn1235-overview-of-stlink-derivatives-stmicroelectronics.pdf`
- ANフォルダ内のアプリケーションノート

### 5. アプリケーションの起動
```bash
streamlit run app/main.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

## 💡 使用方法

### Q&A機能の使用
1. 左サイドバーでマイコンを選択
2. 「Q&A」タブで質問を入力
3. システムが関連ドキュメントを検索して回答を生成

**質問例:**
- "LEDを点滅させる方法を教えて"
- "PWM信号を生成するには？"
- "CubeMXでGPIOを設定する手順"
- "タイマー割り込みの使い方"

### コード生成機能の使用
1. 「コード生成」タブを選択
2. カスタム要求またはテンプレートを選択
3. 要求を入力して「コード生成」をクリック
4. 生成されたコードをコピーして使用

### ドキュメント検索機能
1. 「ドキュメント検索」タブを選択
2. 検索キーワードを入力
3. 必要に応じてフィルターを設定
4. 関連する文書セクションを確認

## 🔧 カスタマイズ

### 新しいマイコンの追加
`app/config.py`の`SUPPORTED_MICROCONTROLLERS`に新しいマイコン情報を追加:

```python
SUPPORTED_MICROCONTROLLERS = {
    "新しいマイコン名": {
        "name": "新しいマイコン名",
        "series": "STM32Fx",
        "core": "Cortex-Mx",
        "frequency": "xxx MHz",
        "flash": "xxx KB/MB", 
        "ram": "xxx KB",
        "description": "説明文"
    }
}
```

### 新しいコードテンプレートの追加
`app/services/code_generator.py`の`_load_templates()`メソッドに新しいテンプレートを追加します。

### プロンプトのカスタマイズ
`app/config.py`の各種プロンプトテンプレートを編集して、回答スタイルを調整できます。

## 📊 パフォーマンス

### 処理時間
- 質問応答: 通常3-10秒
- コード生成: 通常5-15秒
- ドキュメント検索: 通常1-3秒
- 初回ドキュメント処理: 数分（ファイル数による）

### メモリ使用量
- 基本動作: 約500MB-1GB
- ドキュメント処理時: 一時的に1-2GB増加

## 🐛 トラブルシューティング

### よくある問題

**Q: "OpenAI API keyが設定されていません"エラー**
A: `.env`ファイルで正しいAPI keyを設定してください

**Q: ドキュメントが見つからない**
A: PDFファイルが正しい場所に配置されているか確認してください

**Q: 回答が生成されない**
A: インターネット接続とAPI key、関連ドキュメントの登録状況を確認してください

**Q: パフォーマンスが遅い**
A: 埋め込みモデルをより軽量なものに変更するか、チャンクサイズを調整してください

### ログの確認
```bash
# アプリケーションログの確認
tail -f logs/app.log
```

### 設定のリセット
```bash
# ベクトルデータベースのリセット
rm -rf data/vector_store/*

# 設定ファイルのリセット  
cp .env.example .env
```

## 🤝 貢献

バグレポートや機能要求は、GitHubのIssuesで受け付けています。

### 開発環境のセットアップ
```bash
# 開発用追加パッケージのインストール
pip install -r requirements-dev.txt

# テストの実行
python -m pytest tests/

# コード品質チェック
flake8 app/
black app/
```

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

技術的な質問や問題については、以下の手順で対処してください：

1. このREADMEとトラブルシューティングセクションを確認
2. ログファイルでエラーメッセージを確認
3. GitHubのIssuesで類似の問題を検索
4. 新しいIssueを作成（再現手順とログを含める）

## 🔄 更新履歴

### v1.0.0 (2024-01-01)
- 初回リリース
- NUCLEO-F767ZI対応
- 基本的なRAG機能実装
- Q&A、コード生成、ドキュメント検索機能

## 🙏 謝辞

- STMicroelectronics: 技術文書の提供
- OpenAI: GPTモデルの提供
- LangChain: RAGフレームワークの提供
- オープンソースコミュニティ: 各種ライブラリの提供