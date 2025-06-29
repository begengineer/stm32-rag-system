#!/usr/bin/env python3
"""
最小限のテストスクリプト - OpenAI embeddingsを使った軽量版
"""

print("=== Minimal Import Test ===")

# 基本的なライブラリ
try:
    import sys
    import os
    print("✓ sys, os: OK")
except ImportError as e:
    print(f"✗ sys, os: {e}")

# OpenAI
try:
    import openai
    print("✓ openai: OK")
except ImportError as e:
    print(f"✗ openai: {e}")

# LangChain - 新しい正しいインポート
try:
    from langchain.schema import Document
    from langchain_community.vectorstores import Chroma
    from langchain_openai.embeddings import OpenAIEmbeddings
    from langchain_openai.chat_models import ChatOpenAI
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.prompts import PromptTemplate
    print("✓ langchain (updated imports): OK")
except ImportError as e:
    print(f"✗ langchain (updated imports): {e}")

# ChromaDB
try:
    import chromadb
    print("✓ chromadb: OK")
except ImportError as e:
    print(f"✗ chromadb: {e}")

# PDF処理
try:
    import PyPDF2
    import pdfplumber
    print("✓ PDF libraries: OK")
except ImportError as e:
    print(f"✗ PDF libraries: {e}")

# Streamlit
try:
    import streamlit
    print("✓ streamlit: OK")
except ImportError as e:
    print(f"✗ streamlit: {e}")

print("\n=== Environment Info ===")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

print("\n=== Test Complete ===")