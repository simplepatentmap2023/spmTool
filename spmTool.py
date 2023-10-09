from io import BytesIO
import os
import re

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


import zipfile
#import Tspm
from TGraph import DrawGraph



class SimplePatentMap:
    def __init__(self, df):
        self.df = df

    def IPCs(self, series):
        mainIPCmg = []
        mainIPCsg = []
        regEXP = re.compile('(([A-H]\d\d[A-Z]\d+/)\d+)')

        for FIs in series:

            try:
                IPCs = regEXP.findall(FIs)
            except: #FIが記載されていない場合
                a=0

            else: #FIが記載されている場合（通常処理）
                mainIPC = IPCs.pop(0)
                mainIPCmg.append(mainIPC[1])
                mainIPCsg.append(mainIPC[0])

                # df['主文類（mg）'] = mainIPCmg
                # df['主文類（sg）'] = mainIPCsg

                sg = []
                mg = []
                for list in IPCs:
                    sg.append(list[0])
                    mg.append(list[1])

                sg = ';'.join(sg)
                mg = ';'.join(mg)

                df['主文類以外（mg）'] = mg
                df['主文類以外（sg）'] = sg

        return mainIPCmg, mainIPCsg, mg, sg

    def applicants(self, series):
        mainApp = []
        coApp = []
        for applicants in series:
            aPPList = applicants.split(',')
            mainApp.append(aPPList[0])
            coApp.append(';'.join(aPPList[1:]) if len(aPPList[1:]) > 0 else '単独')

        return mainApp, coApp

    def format(self, df):
        # 出願年、公知年の作成
        df['出願年'] = df['出願日'].str[:4]
        df['公知年'] = df['公知日'].str[:4]

        # 筆頭出願人、共同出願人の作成
        df['筆頭出願人/権利者'], df['共同出願人/権利者'] = self.applicants(df['出願人/権利者'].fillna('-'))

        # IPCの作成
        df['主分類（mg）'], df['主分類（sg）'], df['主分類以外（mg）'], df['主分類以外（sg）'] = self.IPCs(df['FI'].fillna('-'))

        df = df.reindex(columns=['文献番号', '出願番号', '出願日', '公知日',
                                 '出願年', '公知年', '発明の名称', '筆頭出願人/権利者', '共同出願人/権利者',
                                 '主分類（mg）', '主分類（sg）', '主分類以外（mg）', '主分類以外（sg）', 'FI',
                                 '公開番号', '公告番号', '登録番号', '審判番号', 'その他', '文献URL'])
        df.index = np.arange(1, len(df) + 1)
        return df

    def ranking(self, df, columns):
        #元になるSeriesを作る
        df = df[columns].value_counts()

        #dfからランキング用のseriesを作成する
        rank = df.rank(method='min', ascending = False)

        #作成した二つのseriesをdataframeに変換
        df = pd.DataFrame(df).rename(columns={'count':'件数'})
        rank = pd.DataFrame(rank).rename(columns={'count':'ランキング'})

        #二つのdataframeを結合
        rankingDF = pd.merge(df, rank,on=columns)
        #rankingDF = pd.merge(df, rank, on=columns)

        #indexになっているcolumnsを列にする（筆頭出願人の場合、indexになっている筆頭出願人を列の値にする
        rankingDF.reset_index(inplace=True)
        rankingDF = rankingDF.reindex(columns=['ランキング', columns, '件数'])

        #indexを1から振り直す
        rankingDF.index = np.arange(1, len(rankingDF) + 1)

        return rankingDF

st.subheader('シンプルパテントマップ')
df = pd.DataFrame()

with st.sidebar:
    st.markdown("[YouTube](https://www.youtube.com/@simplepatentmap)")
    st.markdown("[ブログ](https://simplepm.jp/)")
    st.markdown("[データセット](https://github.com/simplepatentmap2023/dataset)")
    st.markdown("[J-PlatPat](https://www.j-platpat.inpit.go.jp/)")

    sample_btn = st.button('sample', key='sample_btn')
    if sample_btn:
        df = pd.read_csv('sampleInStud.csv')

uploaded_files = st.file_uploader("CSVファイルを選択して下さい", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    df = pd.concat([df, pd.read_csv(uploaded_file)])

if len(df) > 1:
    spm = SimplePatentMap(df)
    formattedDF = spm.format(df)
    appRankingDF = spm.ranking(formattedDF, '筆頭出願人/権利者')
    IPCmgRankingDF = spm.ranking(formattedDF, '主分類（mg）')
    IPCsgRankingDF = spm.ranking(formattedDF, '主分類（sg）')

    st.write(formattedDF)

    subjects = np.array(["math", "physics", "chemistry", "earth science"])
    scores = np.array([80, 95, 45, 65])
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.2)
    ax.barh(subjects, scores)
    plt.show()

    #イメージファイルの作成（出願人TOP30、IPC(mg)TOP30）
    subjects = np.array(["math", "physics", "chemistry", "earth science"])
    scores = np.array([80, 95, 45, 65])

    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.2)

    ax.barh(subjects, scores)

    plt.show()



    #ダウンロードファイル（エクセル）の書き出し準備
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        appRankingDF.to_excel(writer, sheet_name='筆頭出願人', index=False)
        IPCmgRankingDF.to_excel(writer, sheet_name='主分類（mg）', index=False)
        IPCsgRankingDF.to_excel(writer, sheet_name='主分類（sg）', index=False)
        # heatmapDF.to_excel(writer, sheet_name='ヒートマップ', index=False)
        formattedDF.to_excel(writer, sheet_name='データセット', index=False)



    #    Downloadボタンの追加
    #spm.formattedDF.to_excel(buf := BytesIO(), index=False)
    st.download_button(
        label="ダウンロード",
        # buf.getvalue(),
        data=buffer,
        file_name="SimplePatentMap.xlsx",
        mime='application/vnd.ms-excel'
    )


