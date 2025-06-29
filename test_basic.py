#!/usr/bin/env python3
"""
STマイクロマイコン RAGシステム 基本テスト
"""

import sys
import os
import traceback

def test_imports():
    """基本的なインポートテスト"""
    print("🧪 基本インポートテスト...")
    
    try:
        # 標準ライブラリ
        import json
        import re
        import hashlib
        print("  ✅ 標準ライブラリ")
        
        # アプリケーションモジュール
        sys.path.append('app')
        from config import Config
        print("  ✅ 設定ファイル")
        
        from services.microcontroller_selector import MicrocontrollerSelector
        print("  ✅ マイコン選択サービス")
        
        from services.code_generator import CodeGenerator
        print("  ✅ コード生成サービス")
        
        from utils.helpers import sanitize_filename, format_file_size
        print("  ✅ ヘルパー関数")
        
        return True
        
    except Exception as e:
        print(f"  ❌ インポートエラー: {e}")
        traceback.print_exc()
        return False

def test_config():
    """設定ファイルテスト"""
    print("⚙️ 設定ファイルテスト...")
    
    try:
        from config import Config
        
        # 基本設定の確認
        assert hasattr(Config, 'SUPPORTED_MICROCONTROLLERS')
        assert 'NUCLEO-F767ZI' in Config.SUPPORTED_MICROCONTROLLERS
        assert hasattr(Config, 'SYSTEM_PROMPT')
        assert hasattr(Config, 'QA_PROMPT_TEMPLATE')
        
        print("  ✅ 設定ファイルの構造が正しい")
        return True
        
    except Exception as e:
        print(f"  ❌ 設定ファイルエラー: {e}")
        return False

def test_microcontroller_selector():
    """マイコン選択機能テスト"""
    print("🎯 マイコン選択機能テスト...")
    
    try:
        from services.microcontroller_selector import MicrocontrollerSelector
        
        selector = MicrocontrollerSelector()
        
        # 利用可能なマイコンの取得
        available = selector.get_available_microcontrollers()
        assert len(available) > 0
        assert 'NUCLEO-F767ZI' in available
        
        # マイコン情報の取得
        info = selector.get_microcontroller_info('NUCLEO-F767ZI')
        assert info is not None
        assert info.name == 'NUCLEO-F767ZI'
        
        # 現在の選択
        selector.set_current_microcontroller('NUCLEO-F767ZI')
        current = selector.get_current_microcontroller()
        assert current == 'NUCLEO-F767ZI'
        
        print("  ✅ マイコン選択機能が正常動作")
        return True
        
    except Exception as e:
        print(f"  ❌ マイコン選択機能エラー: {e}")
        traceback.print_exc()
        return False

def test_code_generator():
    """コード生成機能テスト"""
    print("⚡ コード生成機能テスト...")
    
    try:
        from services.code_generator import CodeGenerator
        
        generator = CodeGenerator()
        
        # 利用可能なテンプレートの取得
        templates = generator.get_available_templates()
        assert len(templates) > 0
        assert 'LED_CONTROL' in templates
        
        # テンプレート情報の取得
        template_info = generator.get_template_info('LED_CONTROL')
        assert template_info is not None
        assert 'name' in template_info
        assert 'description' in template_info
        
        # コード生成
        result = generator.generate_code_from_template('LED_CONTROL')
        assert result['success'] == True
        assert 'code' in result
        assert len(result['code']) > 100  # 生成されたコードが十分な長さ
        
        print("  ✅ コード生成機能が正常動作")
        return True
        
    except Exception as e:
        print(f"  ❌ コード生成機能エラー: {e}")
        traceback.print_exc()
        return False

def test_helper_functions():
    """ヘルパー関数テスト"""
    print("🔧 ヘルパー関数テスト...")
    
    try:
        from utils.helpers import (
            sanitize_filename,
            format_file_size,
            clean_text_for_search,
            validate_microcontroller_name
        )
        
        # ファイル名サニタイズ
        clean_name = sanitize_filename("test<>file.txt")
        assert '<' not in clean_name
        assert '>' not in clean_name
        
        # ファイルサイズフォーマット
        size_str = format_file_size(1024)
        assert '1.0KB' == size_str
        
        # テキストクリーニング
        clean_text = clean_text_for_search("  test\n\ntext  ")
        assert clean_text == "test text"
        
        # マイコン名バリデーション
        assert validate_microcontroller_name("NUCLEO-F767ZI") == True
        assert validate_microcontroller_name("invalid_name") == False
        
        print("  ✅ ヘルパー関数が正常動作")
        return True
        
    except Exception as e:
        print(f"  ❌ ヘルパー関数エラー: {e}")
        traceback.print_exc()
        return False

def test_directory_structure():
    """ディレクトリ構造テスト"""
    print("📁 ディレクトリ構造テスト...")
    
    try:
        required_dirs = [
            'app',
            'app/models',
            'app/services', 
            'app/utils',
            'app/ui',
            'data',
            'docs'
        ]
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                print(f"  ❌ ディレクトリが見つかりません: {directory}")
                return False
        
        required_files = [
            'app/main.py',
            'app/config.py',
            'app/services/document_processor.py',
            'app/services/microcontroller_selector.py',
            'app/services/code_generator.py',
            'app/models/vector_db.py',
            'app/models/rag_engine.py',
            'requirements.txt',
            'setup.py'
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                print(f"  ❌ ファイルが見つかりません: {file_path}")
                return False
        
        print("  ✅ ディレクトリ構造が正しい")
        return True
        
    except Exception as e:
        print(f"  ❌ ディレクトリ構造エラー: {e}")
        return False

def test_document_detection():
    """ドキュメント検出テスト"""
    print("📄 ドキュメント検出テスト...")
    
    try:
        base_path = "../"
        pdf_files = [
            "nucleo-f767zi.pdf",
            "um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf"
        ]
        
        found_count = 0
        for pdf_file in pdf_files:
            full_path = os.path.join(base_path, pdf_file)
            if os.path.exists(full_path):
                print(f"  ✅ 見つかりました: {pdf_file}")
                found_count += 1
            else:
                print(f"  ⚠️  見つかりません: {pdf_file}")
        
        if found_count > 0:
            print(f"  ✅ {found_count}/{len(pdf_files)} のドキュメントが利用可能")
            return True
        else:
            print("  ⚠️  ドキュメントが見つかりませんが、システムは動作可能")
            return True
        
    except Exception as e:
        print(f"  ❌ ドキュメント検出エラー: {e}")
        return False

def main():
    """メインテスト関数"""
    print("🚀 STマイクロマイコン RAGシステム 基本テスト開始")
    print("=" * 60)
    
    tests = [
        test_directory_structure,
        test_imports,
        test_config,
        test_microcontroller_selector,
        test_code_generator,
        test_helper_functions,
        test_document_detection
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"  ❌ テスト実行エラー: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 テスト結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 全てのテストが成功しました！")
        print("\n次のステップ:")
        print("1. .envファイルでOpenAI API keyを設定")
        print("2. 以下のコマンドでアプリケーションを起動:")
        print("   streamlit run app/main.py")
        return True
    else:
        print("⚠️  一部のテストが失敗しました")
        print("   エラーを確認して修正してください")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)