"""
STマイクロマイコン RAGシステム セットアップスクリプト
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Python バージョンをチェック"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 以上が必要です")
        print(f"現在のバージョン: {sys.version}")
        return False
    
    print(f"✅ Python バージョン: {sys.version.split()[0]}")
    return True

def install_requirements():
    """必要なパッケージをインストール"""
    print("📦 必要なパッケージをインストール中...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ パッケージのインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ パッケージのインストールに失敗しました: {e}")
        return False

def setup_directories():
    """必要なディレクトリを作成"""
    print("📁 ディレクトリを作成中...")
    
    directories = [
        "data/documents",
        "data/vector_store", 
        "data/microcontrollers",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ 作成: {directory}")
    
    return True

def setup_environment_file():
    """環境変数ファイルを設定"""
    env_file = ".env"
    env_example = ".env.example"
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            shutil.copy(env_example, env_file)
            print(f"✅ {env_file} を作成しました")
            print(f"⚠️  {env_file} ファイルを編集してOpenAI API keyを設定してください")
        else:
            print(f"❌ {env_example} が見つかりません")
            return False
    else:
        print(f"✅ {env_file} は既に存在します")
    
    return True

def check_openai_key():
    """OpenAI API keyの設定をチェック"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API keyが設定されていません")
        print("   .envファイルでOPENAI_API_KEYを設定してください")
        return False
    
    print("✅ OpenAI API keyが設定されています")
    return True

def create_sample_documents():
    """サンプルドキュメントを配置"""
    print("📄 ドキュメント配置をチェック中...")
    
    # 実際のPDFファイルの存在確認
    base_path = Path("../")
    required_docs = [
        "nucleo-f767zi.pdf",
        "um1974-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf"
    ]
    
    found_docs = 0
    for doc in required_docs:
        if (base_path / doc).exists():
            print(f"  ✅ 見つかりました: {doc}")
            found_docs += 1
        else:
            print(f"  ⚠️  見つかりません: {doc}")
    
    if found_docs > 0:
        print(f"✅ {found_docs}/{len(required_docs)} のドキュメントが見つかりました")
        return True
    else:
        print("⚠️  必要なドキュメントが見つかりません")
        print("   PDFファイルを適切な場所に配置してください")
        return False

def test_system():
    """システムテスト"""
    print("🧪 システムテスト中...")
    
    try:
        # 基本的なインポートテスト
        from app.config import Config
        from app.models.vector_db import VectorDatabase
        print("  ✅ モジュールのインポート成功")
        
        # 設定テスト
        if hasattr(Config, 'SUPPORTED_MICROCONTROLLERS'):
            print("  ✅ 設定ファイル読み込み成功")
        
        return True
        
    except Exception as e:
        print(f"  ❌ システムテスト失敗: {e}")
        return False

def main():
    """メインセットアップ関数"""
    print("🚀 STマイクロマイコン RAGシステム セットアップ開始")
    print("=" * 60)
    
    success = True
    
    # 1. Python バージョンチェック
    if not check_python_version():
        success = False
    
    # 2. パッケージインストール
    if success and not install_requirements():
        success = False
    
    # 3. ディレクトリ作成
    if success and not setup_directories():
        success = False
    
    # 4. 環境ファイル設定
    if success and not setup_environment_file():
        success = False
    
    # 5. OpenAI key チェック（警告のみ）
    check_openai_key()
    
    # 6. ドキュメント配置チェック（警告のみ）
    create_sample_documents()
    
    # 7. システムテスト
    if success and not test_system():
        success = False
    
    print("=" * 60)
    
    if success:
        print("🎉 セットアップが正常に完了しました！")
        print()
        print("次のステップ:")
        print("1. .envファイルでOpenAI API keyを設定")
        print("2. 必要なドキュメントファイルを配置")
        print("3. 以下のコマンドでアプリケーションを起動:")
        print("   streamlit run app/main.py")
    else:
        print("❌ セットアップ中にエラーが発生しました")
        print("   エラーを修正してから再度実行してください")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)