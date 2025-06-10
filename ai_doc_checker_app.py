import streamlit as st
import time
import os
from openai import OpenAI

# 追加: 横幅を広げるカスタムCSS
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1980px !important;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- OpenAIクライアント初期化 ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- タイトル・説明 ---
st.title("📘 AI検証ツール")
st.markdown("""PlantUML/テキストで記述された仕様ドキュメントをAIが検証します。""")

# --- ドキュメントファイルパス定義 ---
usecase = ["./ユースケース図/自動販売機_ユースケース図_レビュー後.wsd",]

usecase_description = ["./ユースケース記述/お金を投入する.md",
                       "./ユースケース記述/機械の状態を確認する.md",
                       "./ユースケース記述/故障対応を行う.md",
                       "./ユースケース記述/商品を選択し購入する.md",
                       "./ユースケース記述/商品を補充する.md",
                       "./ユースケース記述/商品一覧を表示する.md",
                       "./ユースケース記述/釣銭・返金を受け取る.md",
                       "./ユースケース記述/釣銭を補充する.md",
                       "./ユースケース記述/売上金を回収する.md",
                       "./ユースケース記述/販売商品を変更する.md",
                       ]

activiry_usecase = [   "./アクティビティ図_ユースケース/お金を投入する.wsd",
                       "./アクティビティ図_ユースケース/機械の状態を確認する.wsd",
                       "./アクティビティ図_ユースケース/故障対応を行う.wsd",
                       "./アクティビティ図_ユースケース/商品を選択し購入する.wsd",
                       "./アクティビティ図_ユースケース/商品を補充する.wsd",
                       "./アクティビティ図_ユースケース/商品一覧を表示する.wsd",
                       "./アクティビティ図_ユースケース/釣銭_返金を受け取る.wsd",
                       "./アクティビティ図_ユースケース/釣銭を補充する.wsd",
                       "./アクティビティ図_ユースケース/売上金を回収する.wsd",
                       "./アクティビティ図_ユースケース/販売商品を変更する.wsd",
                    ]

statemachine = ["./ステートマシン図/自動販売機_メイン.wsd",
                "./ステートマシン図/自動販売機_メンテナンスモード.wsd",
                "./ステートマシン図/自動販売機_故障中.wsd",
                "./ステートマシン図/自動販売機_故障中.wsd"]

activity_function = ["./アクティビティ図_機能/お金投入を監視する.wsd",
                    "./アクティビティ図_機能/合計投入金額を表示する.wsd",
                    "./アクティビティ図_機能/商品ボタン押下を監視する.wsd",
                    "./アクティビティ図_機能/商品一覧を表示する.wsd",
                    "./アクティビティ図_機能/商品在庫を確認する.wsd",
                    "./アクティビティ図_機能/投入金または釣銭を返金する.wsd",
                    "./アクティビティ図_機能/購入可能な商品ボタンを選択可能にする.wsd",
                    "./アクティビティ図_機能/購入商品を払いだす.wsd",
                    "./アクティビティ図_機能/釣銭を確認する.wsd",
                    "./アクティビティ図_機能/釣銭有無を表示する.wsd"]

sequence = ["./シーケンス図_機能/機能検証.wsd",]

request = ["./要求図/自動販売機_要求図.wsd",]

system = ["./システム構成図/自動販売機_システム構成図.wsd",]

glossary = ["./用語集/用語集.md"]

# --- 検証オプション ---
options = ["",
           "図間整合性チェック 用語_ID整合性チェック",
           "図間整合性チェック 要求図とユースケース図",
           "図間整合性チェック ユースケース記述内のフローとアクティビティ図（ユースケース）",
           "図間整合性チェック ステートマシン図と関連ドキュメント",
           "図間整合性チェック システム構成図とシーケンス図",
           "網羅性チェック 要求カバレッジ",
           "網羅性チェック フローカバレッジ",
           "網羅性チェック 状態・遷移カバレッジ",
           "網羅性チェック リスク対応カバレッジ",
           "シミュレーションベースの検証 シーケンス図の妥当性検証 (シナリオ生成とシミュレーション実行)",
           "シミュレーションベースの検証 ステートマシン図の動的検証 (イベントシーケンス生成と動的解析)"
        ]

# --- メイン処理 ---
choice = st.selectbox("検証項目を指定してください", options)
files = []
txt_content = ""

# プロンプトを読み出す
if choice and os.path.exists("./プロンプト/" + choice + ".txt"):
    with open("./プロンプト/" + choice + ".txt", "r", encoding="utf-8") as f:
        txt_content = f.read()
else:
    if choice:
        st.info(f"{choice}.txt ファイルが見つかりません。")

# コンテキストファイル選択
if choice == "図間整合性チェック 用語_ID整合性チェック":
    files = request + usecase + usecase_description + system + statemachine + glossary

if choice == "図間整合性チェック 要求図とユースケース図":
    files =  request + usecase

if choice == "図間整合性チェック ユースケース記述内のフローとアクティビティ図（ユースケース）":
    files =  usecase_description + activiry_usecase

if choice == "図間整合性チェック ステートマシン図と関連ドキュメント":
    files =  statemachine + usecase_description + activity_function

if choice == "図間整合性チェック システム構成図とシーケンス図":
    files =  system + sequence

# --- AI検証 ---
if st.button("🔍 AI検証を実行"):
    if not files:
        st.warning("検証対象のファイルが選択されていません。")
        st.stop()
    if not txt_content:
        st.warning("プロンプトファイルが読み込まれていません。")
        st.stop()
    with st.spinner("AIが仕様ドキュメントを分析中..."):
        try:
            context = ""
            st.markdown("#### 検証対象ファイル一覧")
            l = ""
            for f in files:
                l = l + f + "\n"
            st.code(l)
               
            for file_name in files:
                if os.path.exists(file_name):
                    with open(file_name, "r", encoding="utf-8") as f:
                        content = f.read()
                        context += f"\n### ドキュメント: {file_name}\n{content}\n"
                else:
                    st.markdown(f"""ファイルがありません
                    {file_name}
                    """)
            prompt = f"{txt_content}\n\n---\n\n{context}"
            result = ""
            response = client.chat.completions.create(
                model="gpt-4.1",
                #model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたはMBSE仕様ドキュメントの整合性検証を支援するAIです。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10000
            )
            result = response.choices[0].message.content
            st.success("✅ AI検証の結果")
            with st.expander("AI検証の詳細結果", expanded=True):
                st.markdown(result)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
