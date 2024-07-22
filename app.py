import streamlit as st

# ワイドレイアウト
st.set_page_config(layout="wide")

# テキスト(マークダウンで書けます。)
st.write("# title")

# 注釈
st.caption("注釈")

# 画像
st.image("https://ul.h3z.jp/tbfgZLSX.webp")

# テーブル
import pandas as pd
df = pd.DataFrame(
        {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
        }
    )
st.write(df)

# チャート
st.line_chart(df)


# テキスト入力
name = st.text_input("名前")

# 数値入力
age = st.number_input("年齢",step=1)

st.write(f"名前: {name}")
st.write(f"年齢: {age}")

## ボタン
if st.button("Push"):
    st.write("ボタンを押しました")

# プルダウン
select = st.selectbox("好きな果物",options=["りんご","ばなな","いちご"])
st.write(select)

# プルダウン(複数選択)
multi_select = st.multiselect("好きな色",options=["赤","青","黄"])
st.write(multi_select)

# チェックボックス
check = st.checkbox("OK")
st.write(f"チェック：{check}")

# ラジオボタン
radio = st.radio("選択", ["猫", "犬"])
st.write(f"ラジオ：{radio}")

# ファイルアップロード
uploaded_file=st.file_uploader("Upload",type=["csv"])
if uploaded_file:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)


# ワイドレイアウト
# st.set_page_config(layout="wide")

# 横に並べる
cols = st.columns(2)
with cols[0]:
    st.write("列1")
with cols[1]:
    st.write("列2")

# タブ
tabs = st.tabs(["タブ1","タブ2"])
with tabs[0]:
    st.write("タブ1")
with tabs[1]:
    st.write("タブ2")
    
# アコーディオン
with st.expander("開きます"):
    st.write("開きました")

# サイドバー
with st.sidebar:
    st.write("サイドバー内に表示されます")