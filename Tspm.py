import re
import pandas as pd
import numpy as np
# import streamlit as st
df = pd.DataFrame()


class SimplePatentMap():

    #筆頭出願人か共同出願人かを分ける
    def applicants(self, series):
        mainApp = []
        coApp = []
        for applicants in series:
            aPPList = applicants.split(',')
            mainApp.append(aPPList[0])
            coApp.append(';'.join(aPPList[1:]) if len(aPPList[1:]) > 0 else '単独')

        return mainApp, coApp

    #主分類、主分類以外をメイングループ、サブグループに分けて出力
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


    def format(self, df):
        #出願年、公知年の作成
        df['出願年'] = df['出願日'].str[:4]
        df['公知年'] = df['公知日'].str[:4]

        #筆頭出願人、共同出願人の作成
        df['筆頭出願人/権利者'], df['共同出願人/権利者'] = self.applicants(df['出願人/権利者'].fillna('-'))

        #IPCの作成
        df['主分類（mg）'], df['主分類（sg）'], df['主分類以外（mg）'], df['主分類以外（sg）'] = self.IPCs(df['FI'].fillna('-'))

        df = df.reindex(columns=['文献番号', '出願番号', '出願日', '公知日',
                            '出願年', '公知年', '発明の名称', '筆頭出願人/権利者', '共同出願人/権利者',
                            '主分類（mg）', '主分類（sg）', '主分類以外（mg）', '主分類以外（sg）', 'FI',
                            '公開番号', '公告番号', '登録番号', '審判番号', 'その他', '文献URL'])
        return df

    # def applicants(self, formattedDF):
    #     app = pd.crosstab(index=formattedDF['筆頭出願人/権利者'],
    #                       columns=formattedDF['文献番号'],
    #                       margins=True,
    #                       margins_name='文献数')
    #     app = app.sort_values(by='文献数', ascending=False)
    #     app = app.iloc[:, -1]
    #     #なぜか出願人TOP10のインデックスが出力されない。
    #     app = app.reset_index()
    #     app = app.drop(index=0)
    #     return app

    def ipc(self, formattedDF):
        ipc = pd.crosstab(index=formattedDF['主分類'],
                          columns=formattedDF['文献番号'],
                          margins=True,
                          margins_name='文献数')
        ipc = ipc.sort_values(by='文献数', ascending=False)
        ipc = ipc.iloc[:, -1]
        ipc = ipc.reset_index()
        ipc = ipc.drop(index=0)
        return ipc

    def heatmap(self, formattedDF):
        heatmap = pd.crosstab(index=formattedDF['主分類'],
                               columns=formattedDF['公知年'],
                               margins=True,
                               margins_name='合計')
        heatmap = heatmap.sort_values(by='合計', ascending=False)
#        ipc = ipc.iloc[:, -1]
        heatmap = heatmap.reset_index()
        heatmap = heatmap.drop(index=0)
        return heatmap

    def radarchart(self, formattedDF, num):
        TOPapplicants = self.applicants(formattedDF)
        TOPapplicants = TOPapplicants.iloc[:num]

        radarchart = pd.crosstab(index=formattedDF['主分類'],
                               columns=TOPapplicants['筆頭出願人/権利者'])
        radarchart = radarchart.iloc[:, :10]
        radarchart = radarchart.assign(合計=df.sum(axis=0))
        radarchart = radarchart.reset_index()
        return radarchart

