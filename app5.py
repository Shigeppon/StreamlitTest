import traceback
import tiktoken
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# models
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

SUMMARIZE_PROMPT = """以下のコンテンツについて、内容を300文字程度でわかりやすく要約してください。

========

{content}

========

日本語で書いてね！
"""

MODEL_PRICES = {
    "input": {
        "gpt-3.5-turbo": 0.5 / 1_000_000,
        "gpt-4o": 5 / 1_000_000,
        "claude-3-5-sonnet-20240620": 3 / 1_000_000,
        "gemini-1.5-pro-latest": 3.5 / 1_000_000,
    },
    "output": {
        "gpt-3.5-turbo": 1.5 / 1_000_000,
        "gpt-4o": 15 / 1_000_000,
        "claude-3-5-sonnet-20240620": 15 / 1_000_000,
        "gemini-1.5-pro-latest": 10.5 / 1_000_000,
    },
}


def init_page():
    st.set_page_config(page_title="Website Summarizer")
    st.header("Website Summarizer")
    st.sidebar.title("Options")


def select_model(temperature=0):
    models = ("GPT-3.5", "GPT-4", "Claude 3.5 Sonnet", "Gemini 1.5 Pro")
    model = st.sidebar.radio("Choose a model:", models)
    if model == "GPT-3.5":
        st.session_state.model_name = "gpt-3.5-turbo"
        return ChatOpenAI(
            temperature=temperature, model_name=st.session_state.model_name
        )
    elif model == "GPT-4":
        st.session_state.model_name = "gpt-4o"
        return ChatOpenAI(
            temperature=temperature, model_name=st.session_state.model_name
        )
    elif model == "Claude 3.5 Sonnet":
        st.session_state.model_name = "claude-3-5-sonnet-20240620"
        return ChatAnthropic(
            temperature=temperature, model_name=st.session_state.model_name
        )
    elif model == "Gemini 1.5 Pro":
        st.session_state.model_name = "gemini-1.5-pro-latest"
        return ChatGoogleGenerativeAI(
            temperature=temperature, model=st.session_state.model_name
        )


def init_chain():
    st.session_state.llm = select_model()
    prompot = ChatPromptTemplate.from_messages([("user", SUMMARIZE_PROMPT)])
    output_parser = StrOutputParser()
    return prompot | st.session_state.llm | output_parser


def validate_url(url):
    """URLが有効かどうかを判定する関数"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_content(url):
    try:
        with st.spinner("Fetching Website ..."):
            response = requests.get(url)
            st.write(response)
            soup = BeautifulSoup(response.text, "html.parser")

            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            else:
                return soup.body.get_text()
    except:
        st.write(traceback.format_exc())
        return None


def get_message_counts(text):
    if "gemini" in st.session_state.model_name:
        return st.session_state.llm.get_num_tokens(text)
    else:
        if "gpt" in st.session_state.model_name:
            encoding = tiktoken.encoding_for_model(st.session_state.model_name)
        else:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))


def calc_and_display_costs():
    output_count = 0
    input_count = 0
    for role, message in st.session_state.message_history:
        token_count = get_message_counts(message)
        if role == "ai":
            output_count += token_count
        else:
            input_count += token_count
    if len(st.session_state.message_history) == 1:
        return

    input_cost = MODEL_PRICES["input"][st.session_state.model_name] * input_count
    output_cost = MODEL_PRICES["output"][st.session_state.model_name] * output_count
    if (
        "gemini" in st.session_state.model_name
        and (input_count + output_count) > 128000
    ):
        input_cost *= 2
        output_cost *= 2

    cost = input_cost + output_cost

    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${cost:.5f}")
    st.sidebar.markdown(f"- Input cost: ${input_cost:.5f}")
    st.sidebar.markdown(f"- Outpu cost: ${output_cost:.5f}")


def main():
    init_page()
    chain = init_chain()

    if url := st.chat_input("URL: ", key="input"):
        is_valid_url = validate_url(url)
        if not is_valid_url:
            st.write("Please input valid url")
        else:
            if content := get_content(url):
                st.markdown("## Summary")
                st.write_stream(chain.stream({"content": content}))
                st.markdown("---")
                st.markdown("## Original Text")
                st.write(content)

    # calc_and_display_costs()


if __name__ == "__main__":
    main()
