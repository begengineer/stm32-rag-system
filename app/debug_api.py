"""
OpenAI API キーのデバッグツール
"""
import streamlit as st
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_openai_api():
    """OpenAI APIの動作確認"""
    st.title("🔧 OpenAI API デバッグツール")
    
    # API キーの取得と表示
    try:
        api_key = st.secrets.get("api_keys", {}).get("openai_api_key", "")
        if api_key:
            masked_key = api_key[:8] + "..." + api_key[-8:] if len(api_key) > 16 else "短すぎます"
            st.success(f"✅ API キーが見つかりました: {masked_key}")
            
            # APIキーの長さチェック
            if len(api_key) < 20:
                st.error("❌ APIキーが短すぎます。正しいキーを設定してください。")
                return
                
        else:
            st.error("❌ API キーが見つかりません")
            return
    except Exception as e:
        st.error(f"❌ Secrets読み取りエラー: {e}")
        return
    
    # OpenAI クライアントのテスト
    if st.button("🧪 OpenAI API テスト"):
        try:
            with st.spinner("APIテスト中..."):
                client = OpenAI(api_key=api_key)
                
                # シンプルなテストリクエスト
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "Hello! 日本語で短く挨拶してください。"}
                    ],
                    max_tokens=50,
                    temperature=0.7
                )
                
                st.success("✅ OpenAI API テスト成功！")
                st.write("**応答:**", response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"❌ OpenAI API テスト失敗: {e}")
            logger.error(f"OpenAI API test failed: {e}")
    
    # 設定情報の表示
    st.subheader("📋 現在の設定")
    
    try:
        secrets_info = {
            "api_keys": "✅ あり" if st.secrets.get("api_keys") else "❌ なし",
            "auth": "✅ あり" if st.secrets.get("auth") else "❌ なし",
        }
        st.json(secrets_info)
    except Exception as e:
        st.error(f"設定確認エラー: {e}")
    
    # 簡易修正案の提示
    st.subheader("🔧 推奨修正案")
    st.markdown("""
    **APIキーが無効な場合の対処法：**
    
    1. **新しいAPIキーを生成**
       - https://platform.openai.com/api-keys にアクセス
       - 新しいAPIキーを作成
    
    2. **Streamlit Cloud Secretsを更新**
       ```toml
       [api_keys]
       openai_api_key = "新しいAPIキー"
       ```
    
    3. **アプリを再起動**
       - 「Reboot app」を実行
    """)

if __name__ == "__main__":
    debug_openai_api()