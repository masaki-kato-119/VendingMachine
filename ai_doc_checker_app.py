import streamlit as st
import os
from openai import OpenAI

# OpenAIクライアント（v1以降のインターフェース）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📘 AIドキュメント一貫性チェッカー")
st.markdown("PlantUML/テキストで記述された仕様ドキュメント間の用語・IDの一貫性をAIが検証します。")

uploaded_files = st.file_uploader(
    "📂 要求図 / ユースケース図 / ステートマシン図 / 用語集などを複数アップロードしてください",
    type=["wsd", "md"],
    accept_multiple_files=True
)

if st.button("🔍 一貫性チェックを実行"):

    if not uploaded_files:
        st.warning("少なくとも1つ以上のファイルをアップロードしてください。")
    else:
        with st.spinner("AIが仕様ドキュメントを分析中..."):
            try:
                context = ""
                for f in uploaded_files:
                    content = f.read().decode("utf-8")
                    context += f"\n### ドキュメント: {f.name}\n{content}\n"

                prompt = f"""
以下のPlantUMLで記述された要求図、ユースケース図、ユースケース記述（テキスト）、システム構成図、ステートマシン図、および用語集のテキストを入力とします。

これらのドキュメント間で、以下の用語およびIDの一貫性を検証してください。

表記揺れ（例：大文字・小文字の違い、スペースの有無、略語とフルネームの混在、送り仮名の違い）、および、あるドキュメントで使用されている用語/IDが他の関連ドキュメントで定義されていない、または異なる意味で定義・使用されている不整合を自動検出してください。

検証対象の用語・IDの例：

- アクター名
- ユースケース名
- コンポーネント名
- 状態名
- 要求ID
- ユースケースID

検出した不整合箇所、その内容（例：「要求図のREQ_001とユースケース記述のreq_001は表記揺れの可能性」）、および該当するドキュメント名をリスト形式で報告してください。

---

{context}
"""

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "あなたはMBSE仕様ドキュメントの整合性検証を支援するAIです。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=2000
                )

                result = response.choices[0].message.content
                st.success("✅ 一貫性チェック結果")
                st.markdown(result)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
