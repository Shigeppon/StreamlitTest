import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# models
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

from urllib.parse import urlparse

from langchain_community.document_loaders import YoutubeLoader

SUMMARIZE_PROMPT = """以下のコンテンツについて、内容を300文字程度でわかりやすく要約してください。

========

{content}

========

日本語で書いてね！
"""


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
    """
    Document:
        - page_content: str
        - metadata: dict

            - source: str
            - title: str
            - description: Optional[str]
            - view_count: int
            - thumbnail_url: Optional[str]
            - publish_date: str
            - length: int
            - author: str
    """
    with st.spinner("Fetching Website ..."):
        loader = YoutubeLoader.from_youtube_url(
            url, add_video_info=True, language=["en", "ja"]
        )
        res = loader.load()

        try:
            if res:
                content = res[0].page_content
                title = res[0].metadata["title"]
                return f"Title: {title}\n\n{content}"
            else:
                return None
        except:
            st.write(traceback.format_exc())
            return None


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


if __name__ == "__main__":
    main()
