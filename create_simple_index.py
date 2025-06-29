#!/usr/bin/env python3
"""
シンプルなドキュメントインデックス作成スクリプト
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

from app.services.document_processor import DocumentProcessor
from app.models.simple_vector_db import SimpleVectorDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """シンプルなドキュメントインデックスを作成"""
    logger.info("シンプルなドキュメントインデックス作成を開始...")
    
    # ドキュメントフォルダのパス
    base_path = "/mnt/c/Users/anpan/OneDrive/デスクトップ/WorkSpace/RAGSystem"
    
    # ドキュメント処理器とベクトルDBを初期化
    doc_processor = DocumentProcessor()
    vector_db = SimpleVectorDatabase()
    
    # 処理するドキュメントリスト（重要なファイルから開始）
    priority_files = [
        f"{base_path}/nucleo-f767zi.pdf",
        f"{base_path}/um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf",
        f"{base_path}/um1727-getting-started-with-stm32-nucleo-board-software-development-tools-stmicroelectronics.pdf",
        f"{base_path}/tn1235-overview-of-stlink-derivatives-stmicroelectronics.pdf",
    ]
    
    # ANフォルダ内の重要なドキュメント（GPIO、Timer、UART関連を優先）
    important_an_files = [
        "an4899-stm32-microcontroller-gpio-hardware-settings-and-low-power-consumption-stmicroelectronics-ja.pdf",
        "an4776-general-purpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics-ja.pdf",
        "an3155-usart-protocol-used-in-the-stm32-bootloader-stmicroelectronics-en.pdf",
        "an4013-introduction-to-timers-for-stm32-mcus-stmicroelectronics-en.pdf",
        "an4661-getting-started-with-stm32f7-series-mcu-hardware-development-stmicroelectronics-en.pdf",
        "an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics-ja.pdf",
    ]
    
    an_folder = f"{base_path}/AN"
    if os.path.exists(an_folder):
        for file in important_an_files:
            full_path = os.path.join(an_folder, file)
            if os.path.exists(full_path):
                priority_files.append(full_path)
    
    # 存在するファイルのみをフィルター
    existing_files = [f for f in priority_files if os.path.exists(f)]
    logger.info(f"処理対象ファイル数: {len(existing_files)}")
    
    if not existing_files:
        logger.error("処理対象のファイルが見つかりません")
        return
    
    # ドキュメントを処理
    try:
        documents = doc_processor.create_documents(existing_files, "NUCLEO-F767ZI")
        logger.info(f"作成されたドキュメントチャンク数: {len(documents)}")
        
        if documents:
            # ベクトルDBに追加
            success = vector_db.add_documents(documents, "NUCLEO-F767ZI")
            
            if success:
                logger.info("シンプルなドキュメントインデックス作成完了！")
                
                # 統計情報を表示
                stats = vector_db.get_collection_stats()
                logger.info(f"ベクトルDB統計: {stats}")
                
                # テスト検索
                logger.info("\\n=== テスト検索 ===")
                test_queries = [
                    "GPIO LED制御",
                    "UART通信",
                    "タイマー PWM",
                    "STM32F767ZI",
                ]
                
                for query in test_queries:
                    results = vector_db.search_similar_documents(query, k=2)
                    logger.info(f"クエリ: '{query}' -> {len(results)}件の結果")
                    for i, (doc, score) in enumerate(results):
                        source = doc.metadata.get("filename", "不明")
                        logger.info(f"  {i+1}. {source} (スコア: {score:.3f})")
                        
            else:
                logger.error("ベクトルDBへの追加に失敗しました")
        else:
            logger.error("ドキュメントの処理に失敗しました")
            
    except Exception as e:
        logger.error(f"インデックス作成中にエラーが発生: {e}")
        raise

if __name__ == "__main__":
    main()