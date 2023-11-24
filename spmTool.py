import streamlit as st
import pandas as pd
import numpy as np

#sampleファイルの読み込みに利用
import glob
# 正規表現のマッチに利用
import re

#データのグラフ化に利用
import matplotlib.pyplot as plt
import japanize_matplotlib

#エクセルファイルの出力に利用
from io import BytesIO

#WordCloudに利用
import unicodedata

# janomeを使った形態素解析
from janome.tokenizer import Tokenizer

# ワードクラウドによる頻出単語の可視化
from wordcloud import WordCloud


# import shutil
# import io
# import os
# import tempfile
#------import文の終了------


class SimplePatentMap:
    def __init__(self, df):
        self.df = df

    def IPCs(self, series):
        regEXP = re.compile('(([A-H]\d\d[A-Z]\d+/)\d+)')

        mainIPCmg = []
        mainIPCsg = []
        othersMg = ''
        othersSg = ''

        for FIs in series:
            # FI列の処理
            ipcs = regEXP.findall(FIs)
            # IPCのフォーマットにマッチしたFIがあった場合
            if ipcs:
                # 主分類を取得
                mainIPC = ipcs.pop(0)
                mainIPCmg.append(mainIPC[1])
                mainIPCsg.append(mainIPC[0])

                # 主分類以外のIPCの処理
                # 主分類以外のIPCの取得

                otherIPCmg = []
                otherIPCsg = []
#                print(ipcs)
                for other in ipcs:

                    otherIPCmg.append(other[1])
                    otherIPCsg.append(other[0])

                # 重複したIPCの削除
                otherIPCmg = list(dict.fromkeys(otherIPCmg))
                otherIPCsg = list(dict.fromkeys(otherIPCsg))

                otherIPCmg = ';'.join(otherIPCmg)
                otherIPCsg = ';'.join(otherIPCsg)
#                print(otherIPCmg)

            else:
                print("result",len(ipcs))
                mainIPCmg.append('not FI')
                mainIPCsg.append('not FI')
                othersMg = 'not FI'
                othersSg = 'not FI'

        return mainIPCmg, mainIPCsg, otherIPCmg, otherIPCsg


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

        #indexになっているcolumnsを列にする（筆頭出願人の場合、indexになっている筆頭出願人を列の値にする
        rankingDF.reset_index(inplace=True)
        rankingDF = rankingDF.reindex(columns=['ランキング', columns, '件数'])

        #indexを1から振り直す
#        rankingDF.index = np.arange(1, len(rankingDF) + 1)
        rankingDF.index = rankingDF.index + 1
        return rankingDF

    def drawBarh(self, df, title, to, barColor='b', BGColor='w'):
        df = df.query('ランキング < @to')
        xticks = []
        for i, rank in enumerate(df['ランキング']):
            xticks.append(':'.join([str(int(rank)), df[title][i+1]]))
        xticks.reverse()
        value = df['件数'][::-1]
        fig = plt.figure(figsize=(12, 8), tight_layout = True)  # ...1
        ax = fig.add_subplot(111)  # ...2
        graph = ax.barh(xticks, value, label=title, color=barColor)  # ...3
        ax.bar_label(graph, labels=value, padding=3, fontsize=8)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.title(title)

        return fig

    def drawWordCloud(self, df, columns):
        text = df[columns].values.tolist()
        text = ''.join(map(str, text))
        text = re.sub('、', '', text)
        text = re.sub('‐', '', text)
        text = re.sub('「', '', text)
        text = re.sub('」', '', text)
        text = re.sub('（', '', text)
        text = re.sub('）', '', text)
        text = re.sub('【', '', text)
        text = re.sub('】', '', text)
        text = re.sub('<BR>', '', text)

        text = unicodedata.normalize('NFKC', text)
#        st.write('UNICODEの正規化後：{}'.format(text))

        # 対象のテキストをtokenizeする
        t = Tokenizer()
        tokenized_text = t.tokenize(text)
        words_list = []

        # tokenizeされたテキストをfor文を使ってhinshiとhinshi2に格納する。
        for token in tokenized_text:
            tokenized_word = token.surface
            hinshi = token.part_of_speech.split(',')[0]
            hinshi2 = token.part_of_speech.split(',')[1]
            # 抜き出す品詞を指定する
            if hinshi == "名詞":
                if (hinshi2 != "数") and (hinshi2 != "代名詞") and (hinshi2 != "非自立"):
                    words_list.append(tokenized_word)

        words_wakachi = " ".join(words_list)
#        st.write(words_wakachi)

        font = 'ipaexg.ttf'

        # 意味なさそうな単語（ストップワード）を除去する。
        stopWords = ['ので', 'そう', 'から', 'ため']
        stopWords += ['方法', '装置', '構造', '材料', '手段', '含有', '選択']
        # stopWords += ['型', '器', '機', '基', '具', '材', '式', '図', '性', '物', '用', '体', '治', '部', '品', '剤']
        stopWords += ['型', '基', '具', '式', '図', '性', '物', '用', '体', '治', '部', '品', '剤']
        stopWords += ['(57)', '要約', '課題', '解決手段', '特徴とする', '本発明の課題は', '選択図', '図','前記', '解決','提供','上記', 'なし']

        # WordCloudを表示

        word_cloud =  WordCloud(font_path=font, width=1500, height=900,
                               stopwords=set(stopWords), min_font_size=5,
                               collocations=False, background_color='white',
                               max_words=400).generate(words_wakachi)
        fig = plt.figure(figsize=(15, 10))
        fig.suptitle(f"{columns}に含まれる主なキーワード", size=18, y=0.90)
        plt.imshow(word_cloud)
        plt.tick_params(labelbottom=False, labelleft=False)
        plt.xticks([])
        plt.yticks([])
        # plt.show()
        # figure.savefig("Word_Cloud.png")

        return fig



#------画面の描画------
st.subheader('シンプルパテントマップ')
df = pd.DataFrame()

with st.sidebar:
    st.markdown("[YouTube](https://www.youtube.com/@simplepatentmap)")
    st.markdown("[ブログ](https://simplepm.jp/)")
    st.markdown("[データセット](https://github.com/simplepatentmap2023/dataset)")
    st.markdown("[J-PlatPat](https://www.j-platpat.inpit.go.jp/)")

uploaded_files = st.file_uploader("CSVファイルを選択して下さい", type='csv', accept_multiple_files=True)
for uploaded_file in uploaded_files:
    df = pd.concat([df, pd.read_csv(uploaded_file)])


st.text('CO2の吸収分離に関する特許情報（20010101-20221231）をサンプルとして表示します。')
if st.button('sample'):
    for sample in glob.glob('./sample/*.csv'):
        df = pd.concat([df, pd.read_csv(sample)])


if len(df) > 1:
    spm = SimplePatentMap(df)
    formattedDF = spm.format(df)
    appRankingDF = spm.ranking(formattedDF, '筆頭出願人/権利者')
    IPCmgRankingDF = spm.ranking(formattedDF, '主分類（mg）')
    IPCsgRankingDF = spm.ranking(formattedDF, '主分類（sg）')

    excelBuffer = BytesIO()
    with pd.ExcelWriter(excelBuffer, engine='xlsxwriter') as writer:

        appRankingDF.to_excel(writer, sheet_name='筆頭出願人', index=False)
        IPCmgRankingDF.to_excel(writer, sheet_name='主分類（mg）', index=False)
        IPCsgRankingDF.to_excel(writer, sheet_name='主分類（sg）', index=False)
        # heatmapDF.to_excel(writer, sheet_name='ヒートマップ', index=False)
        formattedDF.to_excel(writer, sheet_name='データセット', index=False)
        writer._save()

        xlsx = excelBuffer.getvalue()

    #ランキングデータフレームを可視化
    fig1 = spm.drawBarh(df=appRankingDF, title='筆頭出願人/権利者', to=20,barColor='navajowhite', BGColor='oldlace')
    fig2 = spm.drawBarh(df=IPCmgRankingDF, title='主分類（mg）', to=20, barColor='darkgrey', BGColor='whitesmoke')
    fig3 = spm.drawWordCloud(df = df, columns = '発明の名称')

    fig1
    fig2
    fig3

    if '要約' in df.columns:
        fig4 = spm.drawWordCloud(df = df, columns = '要約')
        fig4

    st.download_button(
        label="ダウンロード",
        data=xlsx,
        file_name="SimplePatentMap.xlsx",
        mime='application/octet-stream'
    )
