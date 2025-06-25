import streamlit as st
import os
from typing import List, Tuple, Any, Optional
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import tiktoken

# --- 定数 ---
DEFAULT_MAX_TOKENS = 500
DEFAULT_N_RESULTS = 5

# --- OpenAIクライアントとEmbedding関数の初期化 ---
def init_openai_client() -> Tuple[OpenAI, Any]:
    """
    OpenAIクライアントとEmbeddingFunctionを初期化する

    Returns:
        Tuple[OpenAI, Any]: OpenAIクライアントとEmbeddingFunction
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEYが設定されていません。")
        st.stop()
    client = OpenAI(api_key=api_key)
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )
    return client, embedding_fn

client, openai_ef = init_openai_client()

# --- トークナイザのキャッシュ ---
@st.cache_resource(show_spinner="テキスト分割・ベクトル化用のエンコーダを準備しています...")
def get_tokenizer() -> Any:
    """
    tiktokenのエンコーダをキャッシュして返す

    Returns:
        tiktoken.Encoding: tiktokenのエンコーダオブジェクト
    """
    return tiktoken.get_encoding("cl100k_base")

# --- テキスト分割 ---
def split_text_into_chunks(
    text: str, tokenizer: Any, max_tokens: int = DEFAULT_MAX_TOKENS
) -> List[str]:
    """
    テキストを意味のある塊（チャンク）に分割する

    Args:
        text (str): 分割対象のテキスト
        tokenizer (Any): tiktokenのエンコーダ
        max_tokens (int): 1チャンクあたりの最大トークン数

    Returns:
        List[str]: 分割されたテキストチャンクのリスト
    """
    sentences = text.split('\n')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(tokenizer.encode(current_chunk + sentence + "\n")) > max_tokens:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence + "\n"
        else:
            current_chunk += sentence + "\n"
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# --- ファイル読み込み ---
def read_file_content(file_path: str) -> Optional[str]:
    """
    ファイルを読み込んで内容を返す

    Args:
        file_path (str): ファイルパス

    Returns:
        Optional[str]: ファイル内容（失敗時はNone）
    """
    if not os.path.exists(file_path):
        st.warning(f"ファイルが見つかりません: {file_path}")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.warning(f"ファイル読み込みエラー: {file_path}, {e}")
        return None

# --- ベクトルDB構築 ---
@st.cache_resource(show_spinner="関連ドキュメントのベクトルDBを構築中...")
def create_vector_store_from_files(
    file_paths: Tuple[str, ...], _embedding_fn: Any
) -> Any:
    """
    指定されたファイルリストからChromaDBコレクションを構築する

    Args:
        file_paths (Tuple[str, ...]): ドキュメントファイルのパスのタプル
        _embedding_fn (Any): EmbeddingFunction

    Returns:
        chromadb.api.models.Collection.Collection: 構築されたChromaDBコレクション
    """
    chroma_client = chromadb.Client()
    collection_name = f"rag_collection_{hash(file_paths)}"
    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=_embedding_fn
    )

    tokenizer = get_tokenizer()
    all_chunks: List[str] = []
    all_metadatas: List[dict] = []
    all_ids: List[str] = []

    for file_path in file_paths:
        content = read_file_content(file_path)
        if content is None:
            continue
        chunks = split_text_into_chunks(content, tokenizer)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({"source": file_path})
            all_ids.append(f"{file_path}_{i}")

    if all_chunks:
        collection.add(
            ids=all_ids,
            documents=all_chunks,
            metadatas=all_metadatas
        )
    return collection

# --- ベクトルDB検索 ---
def retrieve_relevant_docs(
    query: str, collection: Any, n_results: int = DEFAULT_N_RESULTS
) -> List[str]:
    """
    ベクトルDBから関連性の高いドキュメントチャンクを取得する

    Args:
        query (str): 検索クエリ
        collection (chromadb.api.models.Collection.Collection): 検索対象のコレクション
        n_results (int): 取得するドキュメント数

    Returns:
        List[str]: 関連性の高いドキュメントチャンクのリスト
    """
    if not collection or collection.count() == 0:
        return []
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results['documents'][0] if results and results['documents'] else []

# --- ドキュメントファイルパス定義 ---
def get_all_file_paths() -> List[str]:
    """全ての仕様関連ファイルパスをまとめて返す"""
    usecase = ["./ユースケース図/自動販売機_ユースケース図_レビュー後.wsd"]
    usecase_description = [
        "./ユースケース記述/お金を投入する.md",
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
    activiry_usecase = [
        "./アクティビティ図_ユースケース/お金を投入する.wsd",
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
    statemachine = [
        "./ステートマシン図/自動販売機_メイン.wsd",
        "./ステートマシン図/自動販売機_メンテナンスモード.wsd",
        "./ステートマシン図/自動販売機_管理モード.wsd",
        "./ステートマシン図/自動販売機_故障中.wsd"
    ]
    activity_function = [
        "./アクティビティ図_機能/お金投入を監視する.wsd",
        "./アクティビティ図_機能/合計投入金額を表示する.wsd",
        "./アクティビティ図_機能/商品ボタン押下を監視する.wsd",
        "./アクティビティ図_機能/商品一覧を表示する.wsd",
        "./アクティビティ図_機能/商品在庫を確認する.wsd",
        "./アクティビティ図_機能/投入金または釣銭を返金する.wsd",
        "./アクティビティ図_機能/購入可能な商品ボタンを選択可能にする.wsd",
        "./アクティビティ図_機能/購入商品を払いだす.wsd",
        "./アクティビティ図_機能/釣銭を確認する.wsd",
        "./アクティビティ図_機能/釣銭有無を表示する.wsd"
    ]
    sequence = ["./シミュレーション_機能/自動販売機.wsd"]
    request = ["./要求図/自動販売機_要求図.wsd"]
    system = ["./システム構成図/自動販売機_システム構成図.wsd"]
    glossary = ["./用語集/用語集.md"]
    fmea = ["./リスク評価/FMEA.md"]
    fta = [
        "./リスク評価/FTA_商品が出ない_誤表示.wsd",
        "./リスク評価/FTA_釣銭不足_返金不可.wsd",
        "./リスク評価/FTA_投入不可_金額誤認識.wsd"
    ]
    return (
        request + usecase + usecase_description + system + statemachine +
        activity_function + glossary + sequence + fmea + fta
    )

# --- メイン処理 ---
def main() -> None:
    """
    Streamlitアプリのメイン処理。
    ユーザーからの問い合わせを受け付け、RAGによる仕様検索・AI回答を行う。
    """
    st.title("🔍 RAG対応 仕様検索エンジン")
    st.markdown(
        "仕様ドキュメントをRAG (Retrieval-Augmented Generation)技術を用いてAIが参照します。\n"
        "顧客、エンジニアは仕様に対して確認事項、懸念点などの質問を行うことで、AIが仕様ドキュメントを参照して回答します。"
    )
    st.text_area("仕様書の内容について問い合わせる", "", height=150, key="prompt_text_area")
    run_button = st.button("問い合わせる")
    files_to_load = get_all_file_paths()

    if run_button and st.session_state.prompt_text_area:
        try:
            vector_store = create_vector_store_from_files(tuple(files_to_load), openai_ef)
            retrieved_context_docs = retrieve_relevant_docs(
                st.session_state.prompt_text_area, vector_store
            )
            if not retrieved_context_docs:
                st.error("関連情報をドキュメントから見つけられませんでした。ファイルの内容を確認してください。")
                st.stop()

            context_for_ai = "\n---\n".join(retrieved_context_docs)
            final_prompt = (
                "以下の「検証指示」に従って、「参考ドキュメント」の内容を検証し、結果を報告してください。\n"
                "# 検証指示\n"
                f"{st.session_state.prompt_text_area}\n\n"
                "# 参考ドキュメント\n"
                f"{context_for_ai}\n"
            )
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはシステムアナリストのスペシャリストです。提供されたドキュメントの断片のみに基づいて、厳密に検証を実行してください。"},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.0,
                max_tokens=4000
            )
            result = response.choices[0].message.content

            st.success("✅ AI検索が完了しました。")
            st.subheader("検索結果")
            st.markdown(result)
            st.subheader("AIが参照した情報")
            st.info("AIは以下のドキュメントの断片を重点的に参照して回答を生成しました。")
            with st.expander("参照したドキュメント断片"):
                st.markdown("---")
                st.code(context_for_ai, language='text')

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()