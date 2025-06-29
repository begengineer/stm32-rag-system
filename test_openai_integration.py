#!/usr/bin/env python3
"""
OpenAI統合テストスクリプト
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

def test_openai_integration():
    """OpenAI統合テスト"""
    logger.info("=== OpenAI統合テスト開始 ===")
    
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
        logger.warning("OpenAI APIが利用できません。テンプレートベースで動作します。")
        if not status["openai_available"]:
            logger.error("OpenAIライブラリがインストールされていません。")
        elif not status["openai_configured"]:
            logger.error("OpenAI API keyが設定されていません。")
        return False
    
    # 3. Q&Aテスト
    logger.info("\n=== Q&Aテスト ===")
    test_questions = [
        "LEDを点滅させる方法を教えてください",
        "CubeMXの使い方を教えてください",
        "PWMでモーター制御をするには？"
    ]
    
    for question in test_questions:
        logger.info(f"\n質問: {question}")
        try:
            result = rag_engine.answer_question(question, microcontroller="NUCLEO-F767ZI")
            logger.info(f"回答生成成功:")
            logger.info(f"  信頼度: {result['confidence']:.2f}")
            logger.info(f"  ソース数: {result['num_sources']}")
            logger.info(f"  回答: {result['answer'][:200]}...")
        except Exception as e:
            logger.error(f"回答生成エラー: {e}")
    
    # 4. コード生成テスト
    logger.info("\n=== コード生成テスト ===")
    test_requests = [
        "LEDを点滅させる",
        "ボタンでLEDを制御する"
    ]
    
    for request in test_requests:
        logger.info(f"\n要求: {request}")
        try:
            result = rag_engine.generate_code(request, microcontroller="NUCLEO-F767ZI")
            logger.info(f"コード生成成功:")
            logger.info(f"  説明: {result['explanation'][:100]}...")
            logger.info(f"  コード長: {len(result['code'])} 文字")
        except Exception as e:
            logger.error(f"コード生成エラー: {e}")
    
    logger.info("\n=== OpenAI統合テスト完了 ===")
    return True

if __name__ == "__main__":
    test_openai_integration()