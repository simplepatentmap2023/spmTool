import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm


class TGraph():

    def barPlot(self, df):
        fig = plt.figure()

        # top
        for i in range(3):
            start = i * 10
            end = start + 9
            df[start:end].plot(ax=axes[i])



        # show plots
        # フォントをfontManagerに追加
        # FONT_PATH = "./ipam00303/ipam.ttf"
        FONT_PATH = './IPAexfont00401/ipaexg.ttf'
        fm.fontManager.addfont(FONT_PATH)

        # FontPropertiesオブジェクト生成（名前の取得のため）
        font_prop = fm.FontProperties(fname=FONT_PATH)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 8

        fig.tight_layout()
        fig.show()




        # df = df[0:9]
        # df.plot.barh()
        # plt.gca().invert_yaxis()
        # plt.tight_layout()
        #
        #
        # plt.show()
        # # step1 データの作成
        # labels = ['G1', 'G2', 'G3', 'G4', 'G5']
        # x = np.arange(len(labels))
        # men_means = [20, 34, 30, 35, 27]
        # women_means = [25, 32, 34, 20, 25]
        #
        # # step2 グラフフレームの作成
        # fig, ax = plt.subplots()
        # # step3 棒グラフの描画
        # ax.bar(x, men_means, label='Men', tick_label=labels)
        #
        # ax.set_xlabel('X label')
        # ax.set_ylabel('Y label')
        # ax.set_title('Basic Bar')
        # ax.legend()
        #
        # plt.show()
        #


        # #日本語ファイルの場所
        # font = 'https://github.com/simplepatentmap2023/spmTool/blob/main/IPAexfont00401/ipaexg.ttf'
        # fp = FontProperties(fname=font, size=9)
        #
        # #df.plot.bar(fontproperties=fp)
        # df.plot.bar()

        # plt.xlabel(fontproperties=fp)
        # plt.ylabel(fontproperties=fp)


        #plt.show()


        # plt.plot(x, np.sin(x))
        # plt.plot(x, np.cos(x))
        #
        # plt.show()

        #ipc データフレームをmatplotlibでバープロット化

        return 0


def main():
    #test dataの読み込み
    df = pd.read_csv('testDataInStud.csv')
    df = df['出願人/権利者'].value_counts()
    tg = TGraph()
    tg.barPlot(df=df)

    return 0

if __name__ == '__main__':
    main()