from io import BytesIO

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import zipfile
from Tspm import SimplePatentMap
from TGraph import DrawGraph

# import matplotlib.pyplot as plt
# from matplotlib import font_manager
# from PIL import Image, ImageDraw
# import japanize_matplotlib
import xlsxwriter

st.subheader('シンプルパテントマップ')

with st.sidebar:
    st.markdown("[YouTube](https://www.youtube.com/@simplepatentmap)")
    st.markdown("[ブログ](https://simplepm.jp/)")
    st.markdown("[データセット](https://github.com/simplepatentmap2023/dataset)")
    st.markdown("[J-PlatPat](https://www.j-platpat.inpit.go.jp/)")

uploaded_files = st.file_uploader("CSVファイルを選択して下さい", accept_multiple_files=True)
df = pd.DataFrame()
for uploaded_file in uploaded_files:
    df = pd.concat([df, pd.read_csv(uploaded_file)])
if st.button('sample'):
    df = pd.read_csv('sampleInStud.csv')


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

    #imageグラフの作成
    dg = DrawGraph()
    appTOP = formattedDF['筆頭出願人/権利者'].value_counts() #appTOP30はSeriesオブジェクト
    appTOPimg = dg.drawBarH(series=appTOP, rank=30, barColor='#ffa07a', title = '筆頭出願人')
    appTOPimg
    appTOPimg.savefig('appTOP.png')

    ipcTOP = formattedDF['主分類'].value_counts()  # appTOP30はSeriesオブジェクト
    ipcTOPimg = dg.drawBarH(series=ipcTOP, rank=30, barColor='gray', title='主分類')
    ipcTOPimg



    #ipcTOP30 = formattedDF['主分類'].value_counts()
    #ipcTOP30img = dg.drawBarH(df=ipcTOP30, rank=2, barColor='gray', title='主分類')

    #Downloadボタンの追加
    # formattedDF.to_excel(buf := BytesIO(), index=False)
    st.download_button(
        label="ダウンロード",
        # buf.getvalue(),
        data=buffer,
        file_name="SimplePatentMap.xlsx",
        mime='application/vnd.ms-excel'
    )


