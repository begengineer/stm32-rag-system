#!/usr/bin/env python3
"""
最小限のテストスクリプト - 必要な依存関係をテスト
"""

print("=== Python Import Test ===")

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

# LangChain
try:
    import langchain
    from langchain.schema import Document
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    print("✓ langchain: OK")
except ImportError as e:
    print(f"✗ langchain: {e}")

# ChromaDB
try:
    import chromadb
    print("✓ chromadb: OK")
except ImportError as e:
    print(f"✗ chromadb: {e}")

# Sentence Transformers
try:
    from sentence_transformers import SentenceTransformer
    print("✓ sentence_transformers: OK")
except ImportError as e:
    print(f"✗ sentence_transformers: {e}")

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