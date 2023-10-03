# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
# import matplotlib as mpl
# from matplotlib.pyplot import subplots
import japanize_matplotlib  # 日本語化matplotlib


class DrawGraph():

    def drawBarH(self, series, rank,  barColor, title):
        appNames = []
        values = []
        display_rank = 0
        previous_value = 0

        for count, applicant in enumerate(series.index):
            value = series.values[count]
            if value != previous_value:
                display_rank = count + 1
                previous_value = value

            if display_rank > rank:
                break

            appNames.append(f'{display_rank} {applicant}')
            values.append(value)

        #グラフを降順に表示するためにreverseする。
        appNames.reverse()
        values.reverse()

        # 出願人名（y軸のフォントサイズの設定のため）の最大文字数を確認
        length = math.ceil(len(max(appNames, key=lambda x: len(x))) / 10)

        fig = plt.figure(figsize=(8+length, rank/4), tight_layout=True)
        #fig, ax = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True)
        ax = fig.add_subplot(111)


        #fig.suptitle(f'{title} TOP 1-{rank}')
        ax.set_title(f'{title} TOP 1-{rank}')

        # plt.subplots_adjust(top=0.85, hspace=0.6)
        # ax = fig.add_subplot(111)

#        plt.rcParams['font.size'] = 8

        graph = ax.barh(appNames, values, color = barColor)
        ax.bar_label(graph, labels=values, padding=2, fontsize = 8)
#        plt.show()
        return fig


if __name__ == "__main__":
    df = pd.read_csv('sampleInStud.csv')
    series = df['出願人/権利者'].value_counts()

    dg = DrawGraph()
    dg.drawBarH(series, rank=20, barColor='gray', title='')

