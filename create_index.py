#!/usr/bin/env python3
"""
ドキュメントインデックス作成スクリプト（オフライン版）
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
from app.models.vector_db_offline import OfflineVectorDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """ドキュメントインデックスを作成"""
    logger.info("ドキュメントインデックス作成を開始...")
    
    # ドキュメントフォルダのパス
    base_path = "/mnt/c/Users/anpan/OneDrive/デスクトップ/WorkSpace/RAGSystem"
    
    # ドキュメント処理器とベクトルDBを初期化
    doc_processor = DocumentProcessor()
    vector_db = OfflineVectorDatabase()
    
    # 処理するドキュメントリスト
    document_files = [
        f"{base_path}/nucleo-f767zi.pdf",
        f"{base_path}/tn1235-overview-of-stlink-derivatives-stmicroelectronics.pdf",
        f"{base_path}/um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf",
        f"{base_path}/um1727-getting-started-with-stm32-nucleo-board-software-development-tools-stmicroelectronics.pdf",
    ]
    
    # ANフォルダ内のドキュメント
    an_folder = f"{base_path}/AN"
    if os.path.exists(an_folder):
        for file in os.listdir(an_folder):
            if file.endswith(".pdf"):
                document_files.append(os.path.join(an_folder, file))
    
    # 存在するファイルのみをフィルター
    existing_files = [f for f in document_files if os.path.exists(f)]
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
                logger.info("ドキュメントインデックス作成完了！")
                
                # 統計情報を表示
                stats = vector_db.get_collection_stats()
                logger.info(f"ベクトルDB統計: {stats}")
            else:
                logger.error("ベクトルDBへの追加に失敗しました")
        else:
            logger.error("ドキュメントの処理に失敗しました")
            
    except Exception as e:
        logger.error(f"インデックス作成中にエラーが発生: {e}")
        raise

if __name__ == "__main__":
    main()