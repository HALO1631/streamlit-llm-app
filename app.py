from dotenv import load_dotenv
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数読み込み
load_dotenv()

# LLM インスタンスの初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

# 専門家タイプごとのシステムプロンプト設定
SYSTEM_PROMPTS = {
    "お金の悩み": (
        "あなたはお金の悩みに詳しい専門家です。投資、節約、資産運用などの観点から、"
        "ユーザーの質問に対して具体的かつ親切にアドバイスを提供してください。"
    ),
    "人間関係の悩み": (
        "あなたは人間関係の悩みに詳しいカウンセラーです。コミュニケーション、"
        "対人スキル、感情マネジメントなどの観点から、ユーザーの悩みに寄り添う形で回答してください。"
    )
}

# LLM 呼び出し用関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    ユーザーの入力と専門家タイプに基づいて LLM に問い合わせ、応答を返す
    :param user_input: ユーザーが入力したテキスト
    :param expert_type: ラジオボタンで選択された専門家タイプ
    :return: LLM からの回答テキスト
    """
    # まずシステムメッセージを設定
    system_prompt = SYSTEM_PROMPTS.get(expert_type, "You are a helpful assistant.")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    # LLM 呼び出し
    response = llm.invoke(messages)
    return response.content

# Streamlit アプリケーション
st.title("人生の悩みを専門家に質問してみよう！")

# ラジオボタンで専門家タイプを選択
expert_choice = st.radio(
    "相談したい悩みの種類を選んでください。",
    ["お金の悩み", "人間関係の悩み"]
)

st.divider()

# 入力フォームと実行ボタン
# 選択された専門家タイプによって例文を変える
if expert_choice == "お金の悩み" :
    example_query = "投資初心者ですが、どのように始めれば良いですか？"
else:
    example_query ="彼女と仲直りする方法を教えてください。"

user_query = st.text_input(f'あなたの悩みを入力してください。例: "{example_query}"')

if st.button("実行"):
    if user_query:
        with st.spinner("専門家が考え中…"):
            answer = get_llm_response(user_query, expert_choice)
        st.subheader("回答結果")
        st.write(answer)
    else:
        st.error("質問を入力してください。")