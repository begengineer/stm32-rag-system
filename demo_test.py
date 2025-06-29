#!/usr/bin/env python3
"""
STマイクロマイコン RAGシステム デモテスト
実際の質問でシステムの動作を確認
"""

import sys
import os

# アプリケーションモジュールを追加
sys.path.append('app')

def demo_microcontroller_info():
    """マイコン情報表示のデモ"""
    print("🎯 マイコン情報表示デモ")
    print("-" * 40)
    
    try:
        from services.microcontroller_selector import MicrocontrollerSelector
        
        selector = MicrocontrollerSelector()
        mc_info = selector.get_microcontroller_info('NUCLEO-F767ZI')
        
        print(f"📊 {mc_info.name} 仕様情報:")
        print(f"  シリーズ: {mc_info.series}")
        print(f"  コア: {mc_info.core}")
        print(f"  動作周波数: {mc_info.frequency}")
        print(f"  フラッシュ: {mc_info.flash}")
        print(f"  RAM: {mc_info.ram}")
        print(f"  説明: {mc_info.description}")
        
        if mc_info.features:
            print(f"\n🌟 主な特徴:")
            for i, feature in enumerate(mc_info.features[:5], 1):
                print(f"  {i}. {feature}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def demo_code_generation():
    """コード生成のデモ"""
    print("\n⚡ サンプルコード生成デモ")
    print("-" * 40)
    
    try:
        from services.code_generator import CodeGenerator
        
        generator = CodeGenerator()
        
        # 利用可能なテンプレート表示
        templates = generator.get_available_templates()
        print("📝 利用可能なテンプレート:")
        for template in templates:
            info = generator.get_template_info(template)
            if info:
                print(f"  • {info['name']}: {info['description']}")
        
        print(f"\n💡 LED制御コード生成例:")
        result = generator.generate_code_from_template('LED_CONTROL')
        
        if result['success']:
            code_preview = result['code'][:300] + "..." if len(result['code']) > 300 else result['code']
            print(f"説明: {result['explanation']}")
            print("生成されたコード（抜粋）:")
            print("```c")
            print(code_preview)
            print("```")
            
            if 'features' in result:
                print("\n特徴:")
                for feature in result['features']:
                    print(f"  • {feature}")
        else:
            print(f"❌ コード生成失敗: {result.get('error', '不明')}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def demo_document_processor():
    """ドキュメント処理のデモ"""
    print("\n📚 ドキュメント処理デモ")
    print("-" * 40)
    
    try:
        from services.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        
        # 利用可能なドキュメントをチェック
        base_path = "../"
        test_files = [
            "nucleo-f767zi.pdf",
            "um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf"
        ]
        
        available_files = []
        for file_name in test_files:
            file_path = os.path.join(base_path, file_name)
            if os.path.exists(file_path):
                available_files.append(file_path)
                print(f"  ✅ 利用可能: {file_name}")
            else:
                print(f"  ⚠️  見つかりません: {file_name}")
        
        if available_files:
            print(f"\n📖 ドキュメント処理テスト（{len(available_files)}ファイル）...")
            
            # 最初のファイルのみテスト（時間短縮のため）
            test_file = available_files[0]
            print(f"処理中: {os.path.basename(test_file)}")
            
            # テキスト抽出テスト
            text = processor.extract_text_from_file(test_file)
            
            if text:
                text_preview = text[:200] + "..." if len(text) > 200 else text
                print(f"抽出されたテキスト（抜粋）:")
                print(f'"{text_preview}"')
                print(f"総文字数: {len(text):,}")
                
                # ドキュメント作成テスト
                documents = processor.create_documents([test_file])
                if documents:
                    print(f"作成されたチャンク数: {len(documents)}")
                    print(f"最初のチャンク文字数: {len(documents[0].page_content)}")
                    
                    # 要約統計
                    summary = processor.get_document_summary(documents)
                    print(f"ドキュメント要約:")
                    for key, value in summary.items():
                        print(f"  {key}: {value}")
                else:
                    print("⚠️  ドキュメントチャンクが作成されませんでした")
            else:
                print(f"⚠️  {test_file} からテキストを抽出できませんでした")
        else:
            print("⚠️  処理可能なドキュメントが見つかりません")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_helper_functions():
    """ヘルパー関数のデモ"""
    print("\n🔧 ヘルパー関数デモ")
    print("-" * 40)
    
    try:
        from utils.helpers import (
            sanitize_filename,
            format_file_size,
            extract_code_blocks,
            parse_microcontroller_specs,
            detect_microcontroller_from_text
        )
        
        # ファイル名サニタイズ
        original = "STM32<project>file?.txt"
        sanitized = sanitize_filename(original)
        print(f"ファイル名サニタイズ:")
        print(f"  元: {original}")
        print(f"  後: {sanitized}")
        
        # ファイルサイズフォーマット
        sizes = [512, 1024, 1048576, 1073741824]
        print(f"\nファイルサイズフォーマット:")
        for size in sizes:
            formatted = format_file_size(size)
            print(f"  {size:>10} bytes = {formatted}")
        
        # コードブロック抽出
        sample_text = '''
        Here is some code:
        ```c
        int main() {
            return 0;
        }
        ```
        And some Python:
        ```python
        print("Hello")
        ```
        '''
        
        code_blocks = extract_code_blocks(sample_text)
        print(f"\nコードブロック抽出:")
        for i, block in enumerate(code_blocks, 1):
            print(f"  ブロック{i} ({block['language']}): {len(block['code'])}文字")
        
        # マイコン名検出
        test_texts = [
            "This is about NUCLEO-F767ZI development board",
            "Using STM32F746ZG microcontroller",
            "No microcontroller mentioned here"
        ]
        
        print(f"\nマイコン名検出:")
        for text in test_texts:
            detected = detect_microcontroller_from_text(text)
            result = detected if detected else "見つかりません"
            print(f"  '{text[:30]}...' -> {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def demo_recommendations():
    """推奨機能のデモ"""
    print("\n💡 推奨機能デモ")
    print("-" * 40)
    
    try:
        from services.microcontroller_selector import MicrocontrollerSelector
        
        selector = MicrocontrollerSelector()
        
        use_cases = ["general", "iot", "motor_control", "audio", "graphics"]
        
        print("用途別マイコン推奨:")
        for use_case in use_cases:
            recommendation = selector.get_recommended_microcontroller(use_case)
            print(f"  {use_case:15}: {recommendation['recommended']}")
            print(f"                   理由: {recommendation['reason']}")
        
        # 開発Tips
        tips = selector.get_development_tips('NUCLEO-F767ZI')
        print(f"\n🎯 NUCLEO-F767ZI 開発Tips:")
        for i, tip in enumerate(tips[:3], 1):
            print(f"  {i}. {tip}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    """メインデモ関数"""
    print("🎮 STマイクロマイコン RAGシステム デモテスト")
    print("=" * 60)
    
    demos = [
        ("マイコン情報表示", demo_microcontroller_info),
        ("コード生成", demo_code_generation),
        ("ドキュメント処理", demo_document_processor),
        ("ヘルパー関数", demo_helper_functions),
        ("推奨機能", demo_recommendations)
    ]
    
    results = []
    for demo_name, demo_func in demos:
        try:
            success = demo_func()
            results.append((demo_name, success))
        except Exception as e:
            print(f"❌ {demo_name}デモでエラー: {e}")
            results.append((demo_name, False))
    
    print("\n" + "=" * 60)
    print("📊 デモテスト結果:")
    
    success_count = 0
    for demo_name, success in results:
        status = "✅ 成功" if success else "❌ 失敗"
        print(f"  {demo_name:20}: {status}")
        if success:
            success_count += 1
    
    print(f"\n🎯 成功率: {success_count}/{len(results)} ({100*success_count/len(results):.0f}%)")
    
    if success_count == len(results):
        print("🎉 全デモが成功しました！")
        print("\n📚 RAGシステムは以下の機能が利用可能です:")
        print("  • マイコン情報表示と比較")
        print("  • サンプルコード生成（LED、ボタン、PWMなど）")
        print("  • ドキュメント処理とテキスト抽出")
        print("  • 用途別マイコン推奨")
        print("  • 開発Tipsの提供")
        print("\n🚀 Streamlitアプリケーションを起動してWebインターフェースをお試しください:")
        print("   streamlit run app/main.py")
        
    else:
        print("⚠️  一部のデモで問題が発生しました")
        print("   詳細なエラーメッセージを確認してください")
    
    return success_count == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)