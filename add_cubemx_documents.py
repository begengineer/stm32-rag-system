#!/usr/bin/env python3
"""
CubeMX関連ドキュメントを追加インデックス
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
    """CubeMX関連ドキュメントを追加"""
    logger.info("CubeMX関連ドキュメントをインデックスに追加...")
    
    # ドキュメントフォルダのパス
    base_path = "/mnt/c/Users/anpan/OneDrive/デスクトップ/WorkSpace/RAGSystem"
    
    # ドキュメント処理器とベクトルDBを初期化
    doc_processor = DocumentProcessor()
    vector_db = SimpleVectorDatabase()
    
    # 現在のドキュメント数を確認
    current_stats = vector_db.get_collection_stats()
    logger.info(f"現在のドキュメント統計: {current_stats}")
    
    # CubeMX関連ドキュメント
    cubemx_files = [
        f"{base_path}/CudeMX.pdf",
        f"{base_path}/flstm32nucleo.pdf",  # STM32 Nucleoボード関連
    ]
    
    # STM32Cube関連ドキュメントも追加
    cube_docs_path = f"{base_path}/サンプルコード/STM32Cube_FW_F7_V1.17.0/Documentation"
    if os.path.exists(cube_docs_path):
        for file in os.listdir(cube_docs_path):
            if file.endswith(".pdf"):
                cubemx_files.append(os.path.join(cube_docs_path, file))
    
    # CubeMX関連のApplication Noteも追加
    an_folder = f"{base_path}/AN"
    cubemx_related_an = [
        "an4731-stm32cube-mcu-package-examples-for-stm32f7-series-stmicroelectronics-en.pdf",
    ]
    
    for file in cubemx_related_an:
        full_path = os.path.join(an_folder, file)
        if os.path.exists(full_path):
            cubemx_files.append(full_path)
    
    # 存在するファイルのみをフィルター
    existing_files = [f for f in cubemx_files if os.path.exists(f)]
    logger.info(f"CubeMX関連ファイル数: {len(existing_files)}")
    
    for file in existing_files:
        logger.info(f"  - {os.path.basename(file)}")
    
    if not existing_files:
        logger.error("CubeMX関連ファイルが見つかりません")
        return
    
    # ドキュメントを処理
    try:
        documents = doc_processor.create_documents(existing_files, "NUCLEO-F767ZI")
        logger.info(f"作成されたCubeMX関連チャンク数: {len(documents)}")
        
        if documents:
            # カテゴリをCubeMXに設定
            for doc in documents:
                if "cubemx" in doc.metadata.get("filename", "").lower() or "cube" in doc.metadata.get("filename", "").lower():
                    doc.metadata["category"] = "cubemx_tool"
                elif "nucleo" in doc.metadata.get("filename", "").lower():
                    doc.metadata["category"] = "hardware"
            
            # ベクトルDBに追加
            success = vector_db.add_documents(documents, "NUCLEO-F767ZI")
            
            if success:
                logger.info("CubeMX関連ドキュメントの追加完了！")
                
                # 更新後の統計情報を表示
                updated_stats = vector_db.get_collection_stats()
                logger.info(f"更新後のドキュメント統計: {updated_stats}")
                
                # CubeMX関連のテスト検索
                logger.info("\\n=== CubeMXテスト検索 ===")
                test_queries = [
                    "CubeMX",
                    "STM32CubeMX",
                    "プロジェクト作成",
                    "ピン設定",
                    "コード生成",
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
        else:
            logger.error("ドキュメントの処理に失敗しました")
            
    except Exception as e:
        logger.error(f"インデックス追加中にエラーが発生: {e}")
        raise

if __name__ == "__main__":
    main()