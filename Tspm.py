import re
import pandas as pd
import numpy as np

# import streamlit as st
df = pd.DataFrame()


class SimplePatentMap():


    @staticmethod
    def makeYearDF(df):
        year_df = pd.DataFrame()
        year_df['出願年'] = df['出願日'].str[:4]
        year_df['公知年'] = df['公知日'].str[:4]
        return year_df

    @staticmethod
    def makeApplicantDF(df):
        applicant_df = pd.DataFrame()
        applicants_series = df['出願人/権利者'].fillna('-')
        for index, value in applicants_series.items():
            applicants = value.split(',')
            applicant_df.at[index, '筆頭出願人/権利者'] = applicants.pop(0)
            coapplicants = ('単独' if len(applicants) == 0 else ';'.join(applicants))
            applicant_df.at[index, '共同出願人/権利者'] = coapplicants
        return applicant_df

    @staticmethod
    def makeIPCsDF(df):
        IPCsDF = pd.DataFrame()
        fi_series = df['FI'].fillna('-')
        regEXP = re.compile('[A-H]\d\d[A-Z]\d+/\d+')
        for index, FI in fi_series.items():
            try:
                IPCs = regEXP.findall(FI)
            except:
                df.at[index, '主分類'] = 'not FI(s)'
                df.at[index, '主分類以外'] = '-'
            else:
                IPCsDF.at[index, '主分類'] = IPCs.pop(0) if len(IPCs) > 0 else '-'
                # 重複を排除
                IPCs = dict.fromkeys(IPCs)
                IPCsDF.at[index, '主分類以外'] = ';'.join(IPCs)

        return IPCsDF

    #    @st.cache_data
    def format(self, df):
        df.index = np.arange(1, len(df) + 1)
        year_df = self.makeYearDF(df)
        applicants_df = self.makeApplicantDF(df)
        IPCsDF = self.makeIPCsDF(df)

        #        st.write(df[['文献番号', '出願番号', '出願日', '公知日']])
        return pd.concat([df[['文献番号', '出願番号', '出願日', '公知日']],
                          year_df,
                          df['発明の名称'],
                          applicants_df,
                          IPCsDF,
                          df[['公開番号', '公告番号', '登録番号', '審判番号', 'その他', '文献URL']]
                          ], axis=1)

    def applicants(self, formattedDF):
        app = pd.crosstab(index=formattedDF['筆頭出願人/権利者'],
                          columns=formattedDF['文献番号'],
                          margins=True,
                          margins_name='文献数')
        app = app.sort_values(by='文献数', ascending=False)
        app = app.iloc[:, -1]
        #なぜか出願人TOP10のインデックスが出力されない。
        app = app.reset_index()
        app = app.drop(index=0)
        return app

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

