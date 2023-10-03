import codecs
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
import re


class WordCloudMaker:
    def __init__(self, text=None, font_path=None, width=800, height=600, min_font_size=15):
        """
        コンストラクタ
        """
#        self.font_path = font_path  # フォントのパス
        self.text = text  # クラウド化したいテキスト
        self.background_color = 'white'  # 画像の背景色
        self.width = width  # 画像の横ピクセル数
        self.height = height  # 画像の縦ピクセル数
        self.min_font_size = min_font_size  # 最小のフォントサイズ

    def create(self, path, exclusion=[]):
        """
          ワードクラウドの画像生成

        Parameters:
            path : str         画像の出力パス
            exclusion : [str]  除外ワードのリスト
        """
        # 名詞の抽出
        words = self.extract_words(self.text, exclusion)
        # ワードクラウドの画像生成
        words = self.generate_wordcloud(path, words)

    def generate_wordcloud(self, path, words):
        """
        ワードクラウドの画像生成

        Parameters:
            path : str        画像の出力パス
            words : [str]     ワードクラウド化したい名詞リスト
        """
        # ワードクラウドの画像生成
        wordcloud = WordCloud(
            background_color=self.background_color,  # 背景色
            font_path=self.font_path,  # フォントのパス
            width=self.width,  # 画像の横ピクセル数
            height=self.width,  # 画像の縦ピクセル数
            min_font_size=self.min_font_size  # 最小のフォントサイズ
        )
        # ワードクラウドの作成
        wordcloud.generate(words)
        # 画像保存
        wordcloud.to_file(path)

    def extract_words(self, text, exclusion=[]):
        """
        形態素解析により一般名詞と固有名詞のリストを作成
        ---------------
        Parameters:
            text : str         テキスト
            exclusion : [str]  除外したいワードのリスト
        """
        token = Tokenizer().tokenize(text)
        words = []

        for line in token:
            tkn = re.split('\t|,', str(line))
            # 名詞のみ対象
            if tkn[0] not in exclusion and tkn[1] in ['名詞'] and tkn[2] in ['一般', '固有名詞']:
                words.append(tkn[0])

        return ' '.join(words)

    def read_file(self, filename):
        '''
        ファイルの読み込み

        Parameters:
        --------
            filename : str   要約したい文書が書かれたファイル名
        '''
        with codecs.open(filename, 'r', 'utf-8', 'ignore') as f:
            self.read_text(f.read())

    def read_text(self, text):
        '''
        テキストの読み込み
        '''
        self.text = text
