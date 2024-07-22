import streamlit as st

# $B%F%-%9%H(B($B%^!<%/%@%&%s$G=q$1$^$9!#(B)
st.write("# title")

# $BCm<a(B
st.caption("$BCm<a(B")

# $B2hA|(B
st.image("https://ul.h3z.jp/tbfgZLSX.webp")

# $B%F!<%V%k(B
import pandas as pd
df = pd.DataFrame(
        {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
        }
    )
st.write(df)

# $B%A%c!<%H(B
st.line_chart(df)
