import re
import pandas as pd
import numpy as np
import streamlit as st


class SimplePatentMap():

    def makeYearDF(self, df):
        year_df = pd.DataFrame()
        year_df['出願年'] = df['出願日'].str[:4]
        year_df['公知年'] = df['公知日'].str[:4]
        return year_df

    def makeApplicantDF(self, df):
        applicant_df = pd.DataFrame()
        applicants_series = df['出願人/権利者'].fillna('-')
        for index, value in applicants_series.items():
            applicants = value.split(',')
            applicant_df.at[index, '筆頭出願人/権利者'] = applicants.pop(0)
            coapplicants = ('単独' if len(applicants) == 0 else ';'.join(applicants))
            applicant_df.at[index, '共同出願人/権利者'] = coapplicants
        return applicant_df

    def makeIPCsDF(self, df):
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
    def format(_self, df):
        df.index = np.arange(1, len(df) + 1)
        year_df = _self.makeYearDF(df)
        applicants_df = _self.makeApplicantDF(df)
        IPCsDF = _self.makeIPCsDF(df)
#        st.write(df[['文献番号', '出願番号', '出願日', '公知日']])
        return pd.concat([df[['文献番号', '出願番号', '出願日', '公知日']],
                          year_df,
                          applicants_df,
                          IPCsDF,
                          df[['公開番号', '公告番号', '登録番号', '審判番号', 'その他', '文献URL']]
                          ], axis=1)
