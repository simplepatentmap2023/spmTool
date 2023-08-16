from io import BytesIO

# import matplotlib
import pandas as pd
import streamlit as st
from Tspm import SimplePatentMap
# import matplotlib.pyplot as plt
# from matplotlib import font_manager
# from PIL import Image, ImageDraw
# import japanize_matplotlib
# import xlsxwriter

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
    formattedDF = spm.format(df)
    appDF = spm.applicants(formattedDF)
    ipcDF = spm.ipc(formattedDF)
    heatmapDF = spm.heatmap(formattedDF)
    #radarchartDF = spm.radarchart(formattedDF, 10)

    st.write(formattedDF)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        appDF.to_excel(writer, sheet_name='筆頭出願人', index=False)
        ipcDF.to_excel(writer, sheet_name='主分類', index=False)
        heatmapDF.to_excel(writer, sheet_name='ヒートマップ', index=False)
        formattedDF.to_excel(writer, sheet_name='データセット', index=False)

    #Downloadボタンの追加

    # formattedDF.to_excel(buf := BytesIO(), index=False)
    st.download_button(
        label="ダウンロード",
        # buf.getvalue(),
        data=buffer,
        file_name="SimplePatentMap.xlsx",
        mime='application/vnd.ms-excel'
    )


