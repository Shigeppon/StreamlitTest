import base64
import streamlit as st
from langchain_openai import ChatOpenAI


def init_page():
    st.set_page_config(page_title="Image Recognizer")
    st.header("Image Recognizer")
    st.sidebar.title("Options")


def main():
    init_page()

    llm = ChatOpenAI(temperature=0, model="gpt-4o", max_tokens=512)

    uploaded_file = st.file_uploader(
        label="Upload your Image here", type=["png", "jpg", "webp", "gif"]
    )

    if uploaded_file:
        if user_input := st.chat_input("聞きたいことを入力してね！"):
            image_base64 = base64.b64encode(uploaded_file.read()).decode()
            image = f"data:image/jpeg;base64,{image_base64}"

            query = [
                (
                    "user",
                    [
                        {"type": "text", "text": user_input},
                        {
                            "type": "image_url",
                            "image_url": {"url": image, "detail": "auto"},
                        },
                    ],
                )
            ]
            st.markdown("### Question")
            st.write(user_input)
            st.image(uploaded_file)
            st.markdown("### Answer")
            st.write_stream(llm.stream(query))
        else:
            st.write("まずは画像をアップロードしてね")


if __name__ == "__main__":
    main()
