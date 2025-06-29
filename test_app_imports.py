#!/usr/bin/env python3
"""
アプリケーション固有のインポートテスト
"""

import os
import sys

# パス設定 - main.pyと同じ
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")
sys.path.insert(0, app_dir)
sys.path.insert(0, current_dir)

print("=== App Import Test ===")
print(f"Current dir: {current_dir}")
print(f"App dir: {app_dir}")
print(f"Python path: {sys.path[:3]}")

# Config
try:
    sys.path.insert(0, app_dir)
    from config import Config
    print("✓ config.Config: OK")
    print(f"  OpenAI API Key present: {bool(Config.OPENAI_API_KEY)}")
    print(f"  Embedding model: {Config.EMBEDDING_MODEL}")
except ImportError as e:
    print(f"✗ config.Config: {e}")

# Models
try:
    from models.vector_db import VectorDatabase
    print("✓ models.vector_db.VectorDatabase: OK")
except ImportError as e:
    print(f"✗ models.vector_db.VectorDatabase: {e}")

try:
    from models.rag_engine import RAGEngine
    print("✓ models.rag_engine.RAGEngine: OK")
except ImportError as e:
    print(f"✗ models.rag_engine.RAGEngine: {e}")

# Services
try:
    from services.document_processor import DocumentProcessor
    print("✓ services.document_processor.DocumentProcessor: OK")
except ImportError as e:
    print(f"✗ services.document_processor.DocumentProcessor: {e}")

try:
    from services.microcontroller_selector import MicrocontrollerSelector
    print("✓ services.microcontroller_selector.MicrocontrollerSelector: OK")
except ImportError as e:
    print(f"✗ services.microcontroller_selector.MicrocontrollerSelector: {e}")

try:
    from services.code_generator import CodeGenerator
    print("✓ services.code_generator.CodeGenerator: OK")
except ImportError as e:
    print(f"✗ services.code_generator.CodeGenerator: {e}")

# UI Components
try:
    from ui.components import *
    print("✓ ui.components: OK")
except ImportError as e:
    print(f"✗ ui.components: {e}")

print("\n=== Test Complete ===")