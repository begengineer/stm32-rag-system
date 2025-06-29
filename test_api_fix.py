#!/usr/bin/env python3
"""
修正版API統合テストスクリプト
"""
import os
import sys
import logging

# パス設定
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")
sys.path.insert(0, app_dir)
sys.path.insert(0, current_dir)

from app.models.simple_rag_engine import SimpleRAGEngine
from app.models.simple_vector_db import SimpleVectorDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api_fix():
    """API修正テスト"""
    logger.info("=== API修正テスト開始 ===")
    
    # 1. システム初期化
    logger.info("システム初期化中...")
    vector_db = SimpleVectorDatabase()
    rag_engine = SimpleRAGEngine(vector_db=vector_db, use_openai=True)
    
    # 2. システム状態確認
    status = rag_engine.get_system_status()
    logger.info("システム状態:")
    for key, value in status.items():
        logger.info(f"  {key}: {value}")
    
    if not status["llm_available"]:
        logger.error("OpenAI APIが利用できません")
        if not status["openai_available"]:
            logger.error("OpenAIライブラリがインストールされていません")
        elif not status["openai_configured"]:
            logger.error("OpenAI API keyが設定されていません")
        return False
    
    # 3. 簡単な質問テスト
    logger.info("\n=== 簡単なテスト ===")
    test_question = "LEDを点滅させる方法は？"
    logger.info(f"質問: {test_question}")
    
    try:
        result = rag_engine.answer_question(test_question, microcontroller="NUCLEO-F767ZI")
        logger.info(f"回答生成成功:")
        logger.info(f"  信頼度: {result['confidence']:.2f}")
        logger.info(f"  ソース数: {result['num_sources']}")
        logger.info(f"  回答: {result['answer'][:100]}...")
        return True
    except Exception as e:
        logger.error(f"回答生成エラー: {e}")
        return False

if __name__ == "__main__":
    success = test_api_fix()
    if success:
        print("\n✅ API修正成功 - OpenAI統合が正常に動作しています")
    else:
        print("\n❌ API修正失敗 - 問題が残っています")