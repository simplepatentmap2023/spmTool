from io import BytesIO
import pandas as pd
import streamlit as st
from Tspm import SimplePatentMap

st.subheader('シンプルパテントマップ')

with st.sidebar:
#    st.markdown("[マニュアル](https://github.com/SimplePatentMap/tool/blob/main/spmTool_manual.pdf)")
    st.markdown("[データセット](https://github.com/simplepatentmap2023/dataset)")
    st.markdown("[J-PlatPat](https://www.j-platpat.inpit.go.jp/)")
#    st.markdown("[使い方](https://www.j-platpat.inpit.go.jp/)")

uploaded_files = st.file_uploader("CSVファイルを選択して下さい", accept_multiple_files=True)
df = pd.DataFrame()
for uploaded_file in uploaded_files:
    df = pd.concat([df, pd.read_csv(uploaded_file)])

if len(df) > 1:
    spm = SimplePatentMap()
    formatted_df = spm.format(df)

    st.write(formatted_df)


    #Downloadボタンの追加
    formatted_df.to_excel(buf := BytesIO(), index=False)
    st.download_button(
        "ダウンロード",
        buf.getvalue(),
        "SimplePatentMap.xlsx",
    )


