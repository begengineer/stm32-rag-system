#!/usr/bin/env python3
"""
Streamlit Secrets デバッグスクリプト
"""
import os
import sys

# パス設定
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")
sys.path.insert(0, app_dir)
sys.path.insert(0, current_dir)

try:
    import streamlit as st
    print("✓ Streamlitインポート成功")
    
    # Streamlit secretsテスト
    try:
        api_key = st.secrets.get("api_keys", {}).get("openai_api_key", "")
        if api_key:
            print(f"✓ Streamlit SecretsからAPIキー取得成功: {api_key[:10]}...")
        else:
            print("❌ Streamlit SecretsからAPIキー取得失敗")
            
        # Secretsの中身を確認
        print("\nStreamlit Secrets内容:")
        for key in st.secrets.keys():
            print(f"  {key}: {type(st.secrets[key])}")
            
    except Exception as e:
        print(f"❌ Streamlit Secrets読み取りエラー: {e}")
        
except ImportError:
    print("❌ Streamlitインポート失敗")

# 環境変数確認
from app.config import Config
print(f"\nConfig.get_openai_api_key(): {Config.get_openai_api_key()[:10] if Config.get_openai_api_key() else 'None'}...")

# .streamlit/secrets.tomlファイル確認
secrets_path = os.path.join(current_dir, ".streamlit", "secrets.toml")
print(f"\nSecrets file path: {secrets_path}")
print(f"Secrets file exists: {os.path.exists(secrets_path)}")

if os.path.exists(secrets_path):
    with open(secrets_path, 'r') as f:
        content = f.read()
        print(f"Secrets file content length: {len(content)}")
        print("Secrets file structure:")
        for line in content.split('\n')[:10]:  # 最初の10行のみ表示
            if line.strip() and not line.startswith('sk-'):
                print(f"  {line}")