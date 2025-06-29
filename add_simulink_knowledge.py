#!/usr/bin/env python3
"""
Simulink関連ナレッジを追加するスクリプト
"""
import os
import sys
import logging
from pathlib import Path

# パス設定
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")
sys.path.insert(0, app_dir)
sys.path.insert(0, current_dir)

from app.models.simple_vector_db import SimpleVectorDatabase
from langchain.schema import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_simulink_knowledge():
    """Simulink関連ナレッジをベクトルDBに追加"""
    logger.info("Simulink関連ナレッジを追加中...")
    
    # ベクトルDBを初期化
    vector_db = SimpleVectorDatabase()
    
    # Simulink関連のドキュメントを作成
    simulink_docs = [
        Document(
            page_content="""
STM32 NUCLEO-F767ZIでのSimulink開発環境セットアップ

1. 必要なソフトウェア：
- MATLAB/Simulink (R2019b以降推奨)
- Simulink Coder Support Package for STMicroelectronics Nucleo boards
- STM32CubeMX (オプション、統合使用時)

2. Support Packageインストール手順：
- MATLABのAdd-On Explorerを開く
- "Simulink Coder Support Package for STMicroelectronics Nucleo boards"を検索
- インストールボタンをクリック
- ハードウェアセットアップでNUCLEO-F767ZIを選択

3. 開発環境設定：
- ARM GCCコンパイラの設定
- ST-LINKドライバのインストール
- ボード接続の確認
            """,
            metadata={
                "filename": "simulink_setup_guide.md",
                "category": "simulink_setup",
                "microcontroller": "NUCLEO-F767ZI",
                "chunk_id": "simulink_setup_001"
            }
        ),
        Document(
            page_content="""
Simulinkでのブロック配置とモデル作成

1. 新規モデル作成：
- Simulink Start Pageから「Blank Model」を選択
- モデル名を設定（例：STM32_Model）

2. ライブラリブラウザからのブロック選択：
- Simulink Library Browserを開く
- STM32 Nucleoライブラリを展開
- 以下のブロックが利用可能：
  * Digital Input: デジタル入力読み取り
  * Digital Output: デジタル出力制御
  * Analog Input: ADC入力
  * PWM Output: PWM信号出力
  * UART Config/Send/Receive: シリアル通信
  * I2C Master Read/Write: I2C通信
  * SPI Master Transfer: SPI通信

3. ブロックパラメータ設定：
- ピン番号の指定
- サンプル時間の設定
- 通信パラメータの設定
            """,
            metadata={
                "filename": "simulink_block_placement.md",
                "category": "simulink_modeling",
                "microcontroller": "NUCLEO-F767ZI",
                "chunk_id": "simulink_modeling_001"
            }
        ),
        Document(
            page_content="""
Simulinkモデル設定とコード生成

1. Configuration Parameters設定：
- Ctrl+E でConfiguration Parametersを開く
- Solver設定：
  * Type: Fixed-step
  * Solver: discrete (no continuous states)
  * Fixed-step size: 0.001 (1ms推奨)

- Code Generation設定：
  * System target file: ert.tlc
  * Language: C
  * Build process: Build

2. ハードウェア設定：
- Hardware Implementation → Device type: STMicroelectronics STM32
- Device vendor: STMicroelectronics
- Device type: STM32F7xx

3. コード生成手順：
- Ctrl+B でビルド実行
- 生成されるファイル：
  * モデル名.c: メイン処理
  * モデル名.h: ヘッダファイル
  * rtwtypes.h: データ型定義

4. 自動プログラミング：
- ビルド成功後、自動的にボードに書き込み
- External Modeでリアルタイム監視可能
            """,
            metadata={
                "filename": "simulink_code_generation.md",
                "category": "simulink_codegen",
                "microcontroller": "NUCLEO-F767ZI",
                "chunk_id": "simulink_codegen_001"
            }
        ),
        Document(
            page_content="""
SimulinkでのSTM32デバッグとモニタリング

1. External Mode使用方法：
- モデルでExternal Modeを有効化
- Connect to Targetボタンでボード接続
- リアルタイムでの信号監視が可能
- パラメータのオンライン調整が可能

2. Connected I/O機能：
- Simulinkから直接ハードウェア制御
- リアルタイムでのI/O操作
- プロトタイピングに最適

3. PIL (Processor-in-the-Loop)テスト：
- 実際のプロセッサ上でのアルゴリズム検証
- 処理時間の測定
- メモリ使用量の確認

4. Signal Monitoring：
- Scopeブロックでの波形観測
- Displayブロックでの数値表示
- To Workspaceブロックでのデータ保存

5. デバッグのベストプラクティス：
- 適切なサンプル時間の設定
- ハードウェア制約の考慮
- リアルタイム性の確保
            """,
            metadata={
                "filename": "simulink_debugging.md",
                "category": "simulink_debug",
                "microcontroller": "NUCLEO-F767ZI",
                "chunk_id": "simulink_debug_001"
            }
        ),
        Document(
            page_content="""
Simulinkサンプルアプリケーション集

1. LED点滅制御モデル：
設計：[Pulse Generator] → [Digital Output]
- Pulse Generator: 周期1秒、デューティ比50%
- Digital Output: PIN指定（例：GPIOB Pin 0）

2. ADC読み取りモデル：
設計：[Analog Input] → [Gain] → [Display]
- Analog Input: ADC1 Channel 0
- Gain: 電圧変換係数
- Display: 読み取り値表示

3. PWMモーター制御：
設計：[Signal Generator] → [Saturation] → [PWM Output]
- Signal Generator: 制御信号生成
- Saturation: PWM範囲制限（0-100%）
- PWM Output: Timer3 Channel 1

4. UART通信モデル：
送信：[Constant] → [UART Send]
受信：[UART Receive] → [Display]

5. CAN通信モデル：
送信：[Signal Builder] → [CAN Pack] → [CAN Transmit]
受信：[CAN Receive] → [CAN Unpack] → [Scope]

6. センサーデータ処理：
設計：[ADC] → [Moving Average] → [Threshold] → [LED Control]
- Moving Average: ノイズフィルタリング
- Threshold: しきい値判定
- LED Control: 結果表示
            """,
            metadata={
                "filename": "simulink_samples.md",
                "category": "simulink_examples",
                "microcontroller": "NUCLEO-F767ZI",
                "chunk_id": "simulink_examples_001"
            }
        )
    ]
    
    logger.info(f"作成されたSimulinkドキュメント数: {len(simulink_docs)}")
    
    # ベクトルDBに追加
    success = vector_db.add_documents(simulink_docs, "NUCLEO-F767ZI")
    
    if success:
        logger.info("Simulink関連ナレッジの追加完了！")
        
        # 更新後の統計情報を表示
        updated_stats = vector_db.get_collection_stats()
        logger.info(f"更新後のドキュメント統計: {updated_stats}")
        
        # Simulink関連のテスト検索
        logger.info("\n=== Simulinkテスト検索 ===")
        test_queries = [
            "Simulink",
            "ブロック配置",
            "モデル作成",
            "コード生成",
            "External Mode",
            "PWMモデル",
        ]
        
        for query in test_queries:
            results = vector_db.search_similar_documents(query, k=3, score_threshold=0.05)
            logger.info(f"クエリ: '{query}' -> {len(results)}件の結果")
            for i, (doc, score) in enumerate(results):
                source = doc.metadata.get("filename", "不明")
                category = doc.metadata.get("category", "一般")
                logger.info(f"  {i+1}. {source} ({category}) - スコア: {score:.3f}")
                
    else:
        logger.error("ベクトルDBへの追加に失敗しました")

if __name__ == "__main__":
    add_simulink_knowledge()