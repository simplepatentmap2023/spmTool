import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import subplots
import japanize_matplotlib  # 日本語化matplotlib


class DrawGraph():
    # import seaborn as sns
    # sns.set(font="IPAexGothic")  # 日本語フォント設定

    def drawBarH(self, df, rank,  barColor, title):
        fig, axes = plt.subplots(rank, 1, sharex=True, figsize=(6, 8))
        for i in range(rank):
            axes[i].set_title(f'{title} TOP{i*10+1}-{i*10+10}')
            axes[i].barh(df[i:i+10].index, df[i:i+10].values, label=df[i:i+10].values, color=barColor)
            axes[i].invert_yaxis()
        return fig
