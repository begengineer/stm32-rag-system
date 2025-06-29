#!/usr/bin/env python3
"""
Simulink統合テストスクリプト
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

def test_simulink_integration():
    """Simulink統合テスト"""
    logger.info("=== Simulink統合テスト開始 ===")
    
    # 1. システム初期化
    logger.info("システム初期化中...")
    vector_db = SimpleVectorDatabase()
    rag_engine = SimpleRAGEngine(vector_db=vector_db, use_openai=True)
    
    # 2. システム状態確認
    status = rag_engine.get_system_status()
    logger.info("システム状態:")
    logger.info(f"  総ドキュメント数: {status['total_documents']}")
    logger.info(f"  OpenAI API: {'利用可能' if status['llm_available'] else '利用不可'}")
    
    # 3. Simulink Q&Aテスト
    logger.info("\n=== Simulink Q&Aテスト ===")
    simulink_questions = [
        "SimulinkでSTM32を制御する方法を教えて",
        "Simulinkでブロックを配置する手順は？",
        "PWMをSimulinkで制御したい",
        "External Modeの使い方は？",
        "SimulinkでADC読み取りモデルを作りたい",
        "CAN通信をSimulinkで実装するには？"
    ]
    
    for question in simulink_questions:
        logger.info(f"\n質問: {question}")
        try:
            result = rag_engine.answer_question(question, microcontroller="NUCLEO-F767ZI")
            logger.info(f"回答生成成功:")
            logger.info(f"  信頼度: {result['confidence']:.2f}")
            logger.info(f"  ソース数: {result['num_sources']}")
            logger.info(f"  回答: {result['answer'][:200]}...")
            
            # Simulink関連の回答かチェック
            if any(keyword in result['answer'].lower() for keyword in ['simulink', 'matlab', 'ブロック', 'モデル']):
                logger.info("  ✓ Simulink関連の回答を確認")
            else:
                logger.warning("  ⚠ Simulink関連でない可能性")
                
        except Exception as e:
            logger.error(f"回答生成エラー: {e}")
    
    # 4. Simulinkコード生成テスト
    logger.info("\n=== Simulinkコード生成テスト ===")
    simulink_requests = [
        "SimulinkでLEDを点滅させる",
        "SimulinkでPWM制御",
        "SimulinkでADC読み取り"
    ]
    
    for request in simulink_requests:
        logger.info(f"\n要求: {request}")
        try:
            result = rag_engine.generate_code(request, microcontroller="NUCLEO-F767ZI")
            logger.info(f"コード生成成功:")
            logger.info(f"  説明: {result['explanation'][:100]}...")
            logger.info(f"  コード長: {len(result['code'])} 文字")
            
            # Simulink関連のコードかチェック
            if any(keyword in result['code'].lower() for keyword in ['model_step', 'simulink', 'rtw', 'model_initialize']):
                logger.info("  ✓ Simulink関連のコードを確認")
            else:
                logger.warning("  ⚠ 通常のCコードの可能性")
                
        except Exception as e:
            logger.error(f"コード生成エラー: {e}")
    
    # 5. ドキュメント検索テスト
    logger.info("\n=== Simulinkドキュメント検索テスト ===")
    search_queries = [
        "Simulink ブロック配置",
        "External Mode デバッグ",
        "PWM モデル Simulink",
        "コード生成 Simulink"
    ]
    
    for query in search_queries:
        logger.info(f"\n検索クエリ: {query}")
        try:
            results = rag_engine.search_documentation(query, num_results=3)
            logger.info(f"検索結果: {len(results)}件")
            for i, result in enumerate(results):
                source = result['source']
                category = result['category']
                relevance = result['relevance_score']
                logger.info(f"  {i+1}. {source} ({category}) - 関連度: {relevance:.3f}")
                
        except Exception as e:
            logger.error(f"検索エラー: {e}")
    
    logger.info("\n=== Simulink統合テスト完了 ===")
    return True

if __name__ == "__main__":
    test_simulink_integration()