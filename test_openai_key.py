#!/usr/bin/env python3
"""
OpenAI API key テスト
"""
import os
from dotenv import load_dotenv

# .envを読み込み
load_dotenv("/mnt/c/Users/anpan/OneDrive/デスクトップ/WorkSpace/RAGSystem/rag_system/.env")

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {api_key is not None}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"API Key starts with: {api_key[:10] if api_key else 'None'}...")

try:
    import openai
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    
    # 簡単なテスト
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    
    print("✓ OpenAI API key is valid!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"✗ OpenAI API key test failed: {e}")
    print("API keyが無効または期限切れの可能性があります")