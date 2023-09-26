import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import subplots
import japanize_matplotlib  # 日本語化matplotlib


class DrawGraph():
    # import seaborn as sns
    # sns.set(font="IPAexGothic")  # 日本語フォント設定

    def drawBarH(self, df, barColor):
        fig, axes = plt.subplots(3, 1, sharex=True, figsize=(9, 6))

        top10 = df[0:9].sort_values(ascending=True)
        top20 = df[10:19].sort_values(ascending=True)
        top30 = df[20:29].sort_values(ascending=True)

        axes[0].barh(top10.index[0: 9:], top10.values[0: 9], color=barColor)
        axes[0].set_title('筆頭出願人TOP 1-10')
        axes[1].barh(top20.index[0: 9], top20.values[0: 9], color=barColor)
        axes[1].set_title('筆頭出願人TOP11-20')
        axes[2].barh(top30.index[0: 9], top30.values[0: 9], color=barColor)
        axes[2].set_title('筆頭出願人TOP21-30')


        return fig

    # df = pd.read_csv('/content/drive/MyDrive/明細書：スタッド溶接、公知日20010101-20221231.csv')
    # series = df['出願人/権利者'].value_counts()
    # img = drawBarH(series=series, barColor='#ffa07a', title='筆頭出願人')
    # img
    #
    # series = df['FI'].value_counts()
    # img2 = drawBarH(series=series, barColor='gray', title='FI')
    # img