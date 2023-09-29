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
            # if display_rank > rank:
            #     break
            value = series.values[count]
            if value != previous_value:
                display_rank = count + 1
                previous_value = value

            if display_rank > rank:
                break

            appNames.append(f'{display_rank} {applicant}')
            values.append(value)

#        for appName in appNames:
#            print(appName)

        appNames.reverse()
        values.reverse()

        # 出願人名の最大文字数を確認
        length = math.ceil(len(max(appNames, key=lambda x: len(x))) / 10)

        #fig, ax = plt.subplots(tight_layout = True)
        fig = plt.figure(figsize=(6 + length,rank /3), tight_layout=True)
        fig.suptitle(f'{title} TOP 1-{rank}')
        ax = fig.add_subplot(111)

        plt.rcParams['font.size'] = 8

        graph = ax.barh(appNames, values, color = barColor)
        ax.bar_label(graph, labels=values, padding=3, fontsize = 10)
#        plt.show()
        return fig


if __name__ == "__main__":
    df = pd.read_csv('sampleInStud.csv')
    series = df['出願人/権利者'].value_counts()

    dg = DrawGraph()
    dg.drawBarH(series, rank=20, barColor='gray', title='')

