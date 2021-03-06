<a name="DataPreProcess_scikit-learn"></a>
# DataPreProcess_scikit-learn

機械学習における、データの前処理のサンプルコード集。（練習プログラム）

pandas ライブラリ、scikit-learn ライブラリを使用。

1. [Practice 1 : 欠損値 NaN への対応](#Practice1)
1. [Practice 2 : カテゴリデータ（名義 [nominal] 特徴量、順序 [ordinal] 特徴量）の処理](#Practice2)
1. [Practice 3 : データセットの分割](#Practice3)
1. [Practice 4 : 特徴量のスケーリング](#Practice4)
1. [Practice 5 : 有益な特徴量の選択](#Practice5)

<a name="Practice1"></a>
## Practice 1 : 欠損値 NaN への対応

#### ・欠損値 NaNの補完（平均値）

csv data (欠損値 NaN を含むデータ)

||A|B|C|D|
|:--:|:--:|:--:|:--:|:--:|
|0|1.0|2.0|3.0|4.0|
|1|5.0|6.0|NaN|8.0|
|2|10.0|11.0|12.0|NaN|

欠損値 NaN の平均値補完

||A|B|C|D|
|:--:|:--:|:--:|:--:|:--:|
|0|1.0|2.0|3.0|4.0|
|1|5.0|6.0|7.5|8.0|
|2|10.0|11.0|12.0|6.0|

```
# 関連箇所コード抜粋
import numpy
import pandas
....
from sklearn.preprocessing import Imputer

class DataPreProcess( object ):
    ....
    
    def meanImputationNaN( self, axis = 0 ):
        """
        欠損値 [NaN] を平均値で補完する
        [Input]
            axis : int
                0 : NaN を列の平均値で補完
                1 : NaN を行の平均値で補完
        """
        imputer = Imputer( 
                      missing_values = 'NaN', 
                      strategy = 'mean', 
                      axis = axis       # 0 : 列の平均値, 1 : 行の平均値
                  )
        
    imputer.fit( self.df_ )         # self.df_ は１次配列に変換されることに注意
    self.df_ = imputer.transform( self.df_ )
    return self

def main():
    ....
    #-----------------------------------------
    # Practice 1 : 欠損値 NaN の補完
    #-----------------------------------------
    prePro1 = DataPreProcess.DataPreProcess()

    csv_data = '''
                  A,B,C,D
                  1.0,2.0,3.0,4.0
                  5.0,6.0,,8.0
                  10.0,11.0,12.0,
               '''
    
    prePro1.setDataFrameFromCsvData( csv_data )
    prePro1.print( "csv data" )

    prePro1.meanImputationNaN()
    prePro1.print( "欠損値 NaN の平均値補完" )
```

<a name="Practice2"></a>
## Practice 2 : カテゴリデータ（名義 [nominal] 特徴量、順序 [ordinal] 特徴量）の処理

#### ・名義 [nominal] 特徴量の map(directionary) での整数化
#### ・クラスラベルのエンコーディング（ディクショナリマッピング方式）

list から pandas データフレームを作成

||0|1|2|3|
|---|---|---|---|---|
|0 |green |M   |10.1  |class1|
|1 |red   |L   |13.5  |class2|
|2 |blue  |XL  |15.3  |class1|

pandas データフレームにコラム（列）を追加

||color |size  |price |classlabel|
|---|---|---|---|---|
|0  |green |M   |10.1 |class1|
|1  |red   |L   |13.5 |class2|
|2  |blue  |XL  |15.3 |class1|

順序特徴量 size の map(directionary) を作成し、作成した map で順序特徴量を整数化

||color  |size  |price |classlabel|
|---|---|---|---|---|
|0  |green  |1 |10.1  |class1 |
|1  |red    |2 |13.5  |class2 |
|2  |blue   |3 |15.3  |class1 |

```
# 関連箇所コード抜粋
import numpy
import pandas
...

class DataPreProcess( object ):
    ....
    def setDataFrameFromList( self, list ):
        """
        [Input]
            dataFrame : list

        """
        self.df_ = pandas.DataFrame( list )

        return self
        
    def setColumns( self, columns ):
        """
        データフレームにコラム（列）を設定する。
        """
        self.df_.columns = columns
        
        return self
        
    def encodeClassLabel( self, key ):
        """
        クラスラベルを表す文字列を 0,1,2,.. の順に整数化する.（ディクショナリマッピング方式）
        [Input]
            key : string
                整数化したいクラスラベルの文字列
        """
        mapping = { label: idx for idx, label in enumerate( numpy.unique( self.df_[key]) ) }
        self.df_[key] = self.df_[key].map( mapping )

        return self

def main():
    ....
    #--------------------------------------------------
    # Practice 2 : カテゴリデータの処理
    # 名義 [nominal] 特徴量、順序 [ordinal] 特徴量
    #--------------------------------------------------
    prePro2 = DataPreProcess.DataPreProcess()

    # list から pandas データフレームを作成
    prePro2.setDataFrameFromList(
        list = [ 
                  ['green', 'M', 10.1, 'class1'], 
                  ['red', 'L', 13.5, 'class2'], 
                  ['blue', 'XL', 15.3, 'class1'] 
               ]
    )

    prePro2.print( "list から pandas データフレームを作成" )

    # pandas データフレームにコラム（列）を追加
    prePro2.setColumns( ['color', 'size', 'price', 'classlabel'] )
    prePro2.print( "pandas データフレームにコラム（列）を追加" )
    
    # 順序特徴量 size の map(directionary) を作成
    dict_size = {
        'XL': 3,
        'L': 2,
        'M': 1
    }
    # 作成した map で順序特徴量を整数化
    prePro2.mappingOrdinalFeatures( key = 'size', input_dict = dict_size )
    prePro2.print( "順序特徴量 size の map(directionary) を作成し、作成した map で順序特徴量を整数化" )
    
    # クラスラベルのエンコーディング（ディクショナリマッピング方式）
    prePro2.encodeClassLabel("classlabel")
    prePro2.print( "クラスラベルのエンコーディング（ディクショナリマッピング方式" )
    ....
```

#### ・カテゴリデータの one-hot encoding

|size|price|color_blue|color_green|color_red|
|---|---|---|---|---|
|0|1|10.1|0|1|0|
|1|2|13.5|0|0|1|
|2|3|15.3|1|0|0|

```
# 関連箇所コード抜粋
....
from sklearn.preprocessing import OneHotEncoder         # One-hot encoding 用に使用

class DataPreProcess( object ): 
    ....
    
    def oneHotEncode( self, categories, col ):
        """
        カテゴリデータ（名義特徴量, 順序特徴量）の One-hot Encoding を行う.

        [Input]
            categories : list
                カテゴリデータの list

            col : int
                特徴行列の変換する変数の列位置 : 0 ~

        """
        X_values = self.df_[categories].values    # カテゴリデータ（特徴行列）を抽出
        #print( X_values )
        #print( self.df_[categories] )

        # one-hot Encoder の生成
        ohEncode = OneHotEncoder( 
                      categorical_features = [col],    # 変換する変数の列位置：[0] = 特徴行列 X_values の最初の列
                      sparse = False                   # ?  False : 通常の行列を返すようにする。
                   )

        # one-hot Encoding を実行
        #self.df_ = ohEncode.fit_transform( X_values ).toarray()   # ? sparse = True の場合の処理
        self.df_ = pandas.get_dummies( self.df_[categories] )     # 文字列値を持つ行だけ数値に変換する
        
        return self
        
def main():
    ....
    # カテゴリデータのone-hot encoding
    prePro2.oneHotEncode( categories = ['color', 'size', 'price'], col = 0 )
    prePro2.print( "カテゴリデータのone-hot encoding" )
    ....
``` 

<a name="Practice3"></a>
## Practice 3 : データセットの分割

#### ・トレーニングデータとテストデータへの分割とその割合

 Wine データセット (https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data)

||Class label  |Alcohol  |Malic acid   |Ash  |Alcalinity of ash|Magnesium |Total phenols|Flavanoids|Nonflavanoid phenols|Proanthocyanins|Color intensity|Hue|OD280/OD315 of diluted wines|Proline|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0 |1 |14.23 |1.71  |2.43 |15.6 |127 |2.80|3.06|0.28|2.29|5.640000|1.04|3.92|1065|
|1 |1 |13.20 |1.78  |2.14 |11.2 |100 |2.65|2.76|0.26|1.28|4.380000|1.05|3.40|1050|
|2 |1 |13.16 |2.36  |2.67 |18.6 |101 |2.80|3.24|0.30|2.81|5.680000|1.03|3.17|1185|
|3 |1 |14.37 |1.95  |2.50 |16.8 |113 |3.85|3.49|0.24|2.18|7.800000|0.86|3.45|1480|
|4 |1 |13.24 |2.59  |2.87 |21.0 |118 |2.80|2.69|0.39|1.82|4.320000|1.04|2.93|735|  
|5 |1 |14.20 |1.76  |2.45 |15.2 |112 |3.27|3.39|0.34|1.97|6.750000|1.05|2.85|1450|
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|
|170|3|12.20|3.03|2.32|19.0|96 |1.25|0.49|0.40|0.73|5.500000  |0.66|1.83|510|   
|171|3|12.77|2.39|2.28|19.5|86 |1.39|0.51|0.48|0.64|9.899999  |0.57|1.63|470|  
|172|3|14.16|2.51|2.48|20.0|91 |1.68|0.70|0.44|1.24|9.700000  |0.62|1.71|660|  
|173|3|13.71|5.65|2.45|20.5|95 |1.68|0.61|0.52|1.06|7.700000  |0.64|1.74|740|  
|174|3|13.40|3.91|2.48|23.0|102|1.80|0.75|0.43|1.41|7.300000  |0.70|1.56|750|  
|175|3|13.27|4.28|2.26|20.0|120|1.59|0.69|0.43|1.35|10.200000 |0.59|1.56|835|  
|176|3|13.17|2.59|2.37|20.0|120|1.65|0.68|0.53|1.46|9.300000  |0.60|1.62|840| 
|177|3|14.13|4.10|2.74|24.5|96 |2.05|0.76|0.56|1.35|9.200000  |0.61|1.60|560| 

```
# 関連箇所コード抜粋
import pandas
from sklearn.model_selection import train_test_split    # scikit-learn の train_test_split関数の new-version
....

class DataPreProcess( object ):
    ....
    def setDataFrameFromCsvFile( self, csv_fileName ):
        """
        csv ファイルからデータフレームを構築する

        [Input]
            csv_fileName : string
                csvファイルパス＋ファイル名
        """
        self.df_ = pandas.read_csv( csv_fileName, header = None )
        return self

    def setColumns( self, columns ):
        """
        データフレームにコラム（列）を設定する。
        """
        self.df_.columns = columns
        
        return self

    #---------------------------------------------------------
    # データセットの分割を行う関数群
    #---------------------------------------------------------
    @staticmethod
    def dataTrainTestSplit( X_input, y_input, ratio_test = 0.3 ):
        """
        データをトレーニングデータとテストデータに分割する。
        分割は, ランダムサンプリングで行う.

        [Input]
            X_input : Matrix (行と列からなる配列)
                特徴行列

            y_input : 配列
                教師データ

            ratio_test : float
                テストデータの割合 (0.0 ~ 1.0)

        [Output]
            X_train : トレーニングデータ用の Matrix (行と列からなる配列)
            X_test  : テストデータの Matrix (行と列からなる配列)
            y_train : トレーニングデータ用教師データ配列
            y_test  : テストデータ用教師データ配列
        """        
        X_train, X_test, y_train, y_test \
        = train_test_split(
            X_input,  y_input, 
            test_size = ratio_test, 
            random_state = 0             # 
          )
        
        return X_train, X_test, y_train, y_test

def main():
    ....
    #--------------------------------------------------
    # Practice 3 : データセットの分割
    # トレーニングデータとテストデータへの分割
    #--------------------------------------------------
    prePro3 = DataPreProcess.DataPreProcess()

    # Wine データセットの読み込み
    prePro3.setDataFrameFromCsvFile( "https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data" )
    
    # 列名をセット
    prePro3.setColumns( 
        [
            'Class label', 'Alcohol', 'Malic acid', 'Ash',
            'Alcalinity of ash', 'Magnesium', 'Total phenols',
            'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins',
            'Color intensity', 'Hue', 'OD280/OD315 of diluted wines',
            'Proline'
        ] 
    )
    
    X_train, X_test, y_train, y_test \
    = DataPreProcess.DataPreProcess.dataTrainTestSplit( 
        X_input = prePro3.df_.iloc[:, 1:].values,   # iloc : 行、列を番号で指定（先頭が 0）。df_.iloc[:, 1:] = 全行、1~の全列
        y_input = prePro3.df_.iloc[:, 0].values,    #
        ratio_test = 0.3
    )

    # 分割データ（トレーニングデータ、テストデータ）を出力
    print( "トレーニングデータ : \n", X_train )
    print("テストデータ : \n", X_test )
    print("トレーニング用教師データ : \n", y_train )
    print("テスト用教師データ : \n", y_test )
    ....
``` 

<a name="Practice4"></a>
## Practice 4 : 特徴量のスケーリング

#### ・正規化 [nomalization]（min-max スケーリング <0~1>）

トレーニングデータ [normalized] :

||[ Alcohol, Malic acid, Ash, Alcalinity of ash, Magnesium, Total phenols, Flavanoids, Nonflavanoid phenols, Proanthocyanins, Color intensity, Hue, OD280/OD315 of diluted wines,  Proline ] |
|---|:---|
|0|[ 0.72043011,  0.20378151,  0.53763441, ...,  0.48717949,  1.,          0.5854251 ]|
|1|[ 0.31989247,  0.08403361,  0.31182796, ...,  0.27350427,  0.64102564,  0.        ]|
|2|[ 0.60215054,  0.71218487,  0.48387097, ...,  0.04273504,  0.10622711,  0.42348178]|
|...| [...] |

テストデータ [normalized] : 

||[ Alcohol, Malic acid, Ash, Alcalinity of ash, Magnesium, Total phenols, Flavanoids, Nonflavanoid phenols, Proanthocyanins, Color intensity, Hue, OD280/OD315 of diluted wines,  Proline ] |
|---|:---|
|0|[ 0.72849462,  0.16386555,  0.47849462,  0.29896907,  0.52173913,  0.53956835 ,0.74311927, 0.13461538, 0.37974684,  0.4364852,   0.32478632,  0.70695971, 0.60566802 ]|
|1| [ 0.47311828  0.37394958  0.60215054  0.58762887  0.45652174  0.13669065, 0.27217125  0.19230769  0.26582278  0.90926457 -0.05128205  0.07326007, 0.13603239 ] |
|2| [ 0.36021505,  0.05042017,  0.43010753,  0.43298969,  0.18478261,  0.86330935, 0.80428135,  0.09615385,  0.45886076,  0.30276982,  0.58119658,  0.58608059,0.08744939 ] |
|...| [ ... ] |

#### ・標準化 [standardization]（平均値：０、分散値：１）


トレーニングデータ [standardized] :

||[ Alcohol, Malic acid, Ash, Alcalinity of ash, Magnesium, Total phenols, Flavanoids, Nonflavanoid phenols, Proanthocyanins, Color intensity, Hue, OD280/OD315 of diluted wines,  Proline ] |
|---|:---|
|0| [ 0.91083058, -0.46259897, -0.01142613, ...,  0.65706596,  1.94354495, 0.93700997 ] |
|1| [ -0.95609928, -0.96608672, -1.53725357, ..., -0.40859506,  0.58118003, -1.41336684 ] |
|2| [ 0.35952243,  1.67501572, -0.37471838, ..., -1.55950896, -1.44846566, 0.28683658 ] |
|...| [...] |

テストデータ [standardized] :

|| [ Alcohol, Malic acid, Ash, Alcalinity of ash, Magnesium, Total phenols, Flavanoids, Nonflavanoid phenols, Proanthocyanins, Color intensity, Hue, OD280/OD315 of diluted wines,  Proline ] |
|---|:---|
|0| [ 0.94841977, -0.63042822, -0.4110476,  -0.87677804,  1.22679643,  0.57147571, 0.95620726, -1.24682729,  0.01258759,  0.36299992, -0.15283642,  0.83141032, 1.01828164 ] |
|1| [ -0.24190464,  0.25288364,  0.42452457,  0.69400284,  0.81583896, -1.30214437, -0.62636631, -1.00437054, -0.59161664,  2.47674005, -2.02839981, -1.57358081, -0.86722119 ] |
|2| [ -0.76815332, -1.10741662, -0.73801062, -0.14748691, -0.89648384,  2.07706327, 1.16173629, -1.40846512,  0.43217386, -0.23482557, 1.1259568,   0.37265479, -1.06227321 ] |
|...| [ ... ] |

```
# 関連箇所コード抜粋
....
from sklearn.preprocessing import MinMaxScaler          # scikit-learn の preprocessing モジュールの MinMaxScaler クラス
from sklearn.preprocessing import StandardScaler        # scikit-learn の preprocessing モジュールの StandardScaler クラス
....

class DataPreProcess( object ):
    ....
    #---------------------------------------------------------
    # データのスケーリングを行う関数群
    #---------------------------------------------------------
    @staticmethod
    def normalizedTrainTest( X_train, X_test ):
        """
        指定したトレーニングデータ, テストにデータ（データフレーム）を正規化する.
        ここでの正規化は, min-maxスケーリング [0,1] 範囲を指す.
        トレーニングデータは正規化だけでなく欠損値処理も行う.
        テストデータは,トレーニングデータに対するfit()の結果で,transform()を行う必要

        [Input]
            X_train : トレーニングデータ用の Matrix (行と列からなる配列)
            X_test  : テストデータの Matrix (行と列からなる配列)

        [Output]
            X_train_norm : 正規化されたトレーニングデータ用の Matrix (行と列からなる配列)
            X_test_norm  : 正規化されたテストデータの Matrix (行と列からなる配列)
        """
        mms = MinMaxScaler()

        # fit_transform() : fit()を実施した後に、同じデータに対してtransform()を実施する。
        # トレーニングデータの場合は、それ自体の統計を基に正規化や欠損値処理を行っても問題ないので、fit_transform()を使って構わない。
        X_train_norm = mms.fit_transform( X_train )

        # transform() :  fit()で取得した統計情報を使って、渡されたデータを実際に書き換える。
        # テストデータの場合は、比較的データ数が少なく、トレーニングデータの統計を使って正規化や欠損値処理を行うべきなので、トレーニングデータに対するfit()の結果で、transform()を行う必要がある。
        X_test_norm = mms.transform( X_test )

        return X_train_norm, X_test_norm
        
    @staticmethod
    def standardizeTrainTest( X_train, X_test ):
        """
        指定したトレーニングデータ, テストにデータ（データフレーム）を標準化 [standardize] する.
        ここでの標準化は, 平均値 : 0 , 分散値 : 1 への変換指す.
        トレーニングデータは標準化だけでなく欠損値処理も行う.
        テストデータは,トレーニングデータに対する fit() の結果で, transform() を行う.

        [Input]
            X_train : トレーニングデータ用の Matrix (行と列からなる配列)
            X_test  : テストデータの Matrix (行と列からなる配列)

        [Output]
            X_train_std : 標準化された [standardized] トレーニングデータ用の Matrix (行と列からなる配列)
            X_test_std  : 標準化された [standardized] テストデータの Matrix (行と列からなる配列)
        """
        stdsc = StandardScaler()

        # fit_transform() : fit() を実施した後に, 同じデータに対して transform() を実施する。
        # トレーニングデータの場合は, それ自体の統計を基に標準化や欠損値処理を行っても問題ないので, fit_transform() を使って構わない。
        X_train_std = stdsc.fit_transform( X_train )

        # transform() :  fit() で取得した統計情報を使って, 渡されたデータを実際に書き換える.
        # テストデータの場合は, 比較的データ数が少なく, トレーニングデータの統計を使って標準化や欠損値処理を行うべきなので,
        # トレーニングデータに対する fit() の結果で、transform() を行う必要がある。
        X_test_std = stdsc.transform( X_test )

        return X_train_std, X_test_std    
    ....

def main():
    ....
    #--------------------------------------------------
    # Practice 4 : 特徴量のスケーリング
    # 正規化 [normalization], 標準化 [standardization]
    #--------------------------------------------------
    # 正規化
    X_train_norm, X_test_norm \
    = DataPreProcess.DataPreProcess.normalizedTrainTest( X_train, X_test )
    
    # 正規化後のデータを出力
    print( "トレーニングデータ [normalized] :\n", X_train_norm )
    print("テストデータ [normalized] : \n", X_test_norm )

    # 標準化
    X_train_std, X_test_std \
    = DataPreProcess.DataPreProcess.standardizeTrainTest( X_train, X_test )

    # 標準化後のデータを出力
    print( "トレーニングデータ [standardized] :\n", X_train_std )
    print("テストデータ [standardized] : \n", X_test_std )
    ....
```

<a name="Practice5"></a>
## Practice 5 : 有益な特徴量の選択

Theory : バイアス・分散トレードオフと過学習、及び正則化による過学習への対応

![twitter_ _3-1_160924](https://user-images.githubusercontent.com/25688193/28652178-310a6984-72c1-11e7-994c-d28390cd000b.png)
![twitter_ _3-2_160924](https://user-images.githubusercontent.com/25688193/28652185-381f5356-72c1-11e7-8fae-37e7f77b4e30.png)
![twitter_ _3-3_160924](https://user-images.githubusercontent.com/25688193/28652189-3da74482-72c1-11e7-8050-866a21cba355.png)
![twitter_ _3-4_170727](https://user-images.githubusercontent.com/25688193/28652195-456e0480-72c1-11e7-96c4-c2d9ee8ba273.png)
![twitter_ _3-5_170810](https://user-images.githubusercontent.com/25688193/29157553-5ed3f980-7de2-11e7-9d74-6bd33193dd0f.png)

![twitter_ 18-19_170727](https://user-images.githubusercontent.com/25688193/28652198-4b09b560-72c1-11e7-8053-a9e00b280ef8.png)

### ・L1正則化による疎な解

＜Teory＞ L1正則化による過学習への対応、及び疎な解 [Sparseness] と次元圧縮

L2正則化が重みベクトルの２乗和 ∑w^2 で与えられるのに対し、L1正則化は単に重みベクトルの絶対和 ∑w で与えられる。
この L1 正則化による重みの変化の制限（正則化最小２乗法）を幾何学的に考えると、重みベクトル空間において、L1正則化による制限がひし形な形状となる。
その結果、コスト関数とL1正則化による制限双方を満たす最適解（最小値）は、特定の特徴の重み軸で最小化が行われることになり、他の特徴量に対しては疎な解（ほとんどの特徴量の重みが０になるような解）が得られる。

![twitter_ _3-8_170810](https://user-images.githubusercontent.com/25688193/29160054-ccc1b816-7deb-11e7-8fc4-2ba7380ce9f0.png)


#### プログラムの実行結果 : ロジスティクス回帰モデル（１対他 [OvR] アプローチ）での 使用例（ワインデータ）

|正解率|値 (0~1)|
|---|---|
|Training accuracy|0.983870967742|
|Test accuracy|0.981481481481|

L1 正則化によるモデルの切片の値

|１対他 [OvR] アプローチ|切片値|
|---|---|
|0 : class 1 vs class 2/3 |-0.38376074|
|1 : class 2 vs class 1/3 |-0.15810964|
|2 : class 3 vs class 1/2|-0.70042452|

L1 正則化による特徴の重み係数値の表

|１対他 [OvR] アプローチ|Alcohol|Malic acid|Ash|Alcalinity of ash|Magnesium|Total phenols|Flavanoids|Nonflavanoid phenols|Proanthocyanins|Color intensity|Hue|OD280/OD315 of diluted wines|Proline|
|:------------------------|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0 : class 1 vs class 2/3 |0.27988583|0|0|-0.02809465|0|0|0.70993117|0|0|0|0|0|1.23653338|
|1 : class 2 vs class 1/3 |-0.64383223|-0.06887207|-0.05718404|0|0|0|0|0|0|-0.92699913|0.05997951|0|-0.37104588|
|2 : class 3 vs class 1/2 |0|0.06149544|0|0|0|0|-0.63611754|0|0|0.49810234|-0.35820078|-0.57121725|0|

特徴の重みの変化の図

![datapreprocess_scikit-learn_1](https://user-images.githubusercontent.com/25688193/29161716-3e730c8e-7df2-11e7-8e03-be01c29b3841.png)

```
....
from sklearn.linear_model import LogisticRegression

# 関連箇所コード抜粋
def main():
    ....
    #--------------------------------------------------------
    # Practice 5 : 有益な特徴量の選択
    # L1正則化による疎な解（ロジスティクス回帰モデルで検証）
    #--------------------------------------------------------
    logReg = LogisticRegression(
        penalty = 'l1',     # L1正則化
        C = 0.1             # 逆正則化パラメータ
    )

    logReg.fit( X_train_std, y_train )
    
    print( 'Training accuracy:', logReg.score( X_train_std, y_train ) )
    print( 'Test accuracy:', logReg.score( X_test_std, y_test ) )

    print("切片 :",logReg.intercept_ )
    print("重み係数 : \n",logReg.coef_ )

    #----------------------------------------
    # 図の作図
    fig = plt.figure()
    ax = plt.subplot(1, 1, 1)
    
    # 各係数（特徴）の色のリスト
    colors = [
                 'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 
                 'pink', 'lightgreen', 'lightblue', 'gray', 'indigo', 'orange'
             ]

    # 重み係数のリスト、逆正則化パラメータのリスト（空のリストで初期化）
    weights = [] 
    params = []

    # 逆正則化パラメータの値毎に処理を繰り返す
    for c in numpy.arange(-4., 6.):
        lr = LogisticRegression( penalty = 'l1', C = 10.**c, random_state = 0 )
        lr.fit( X_train_std, y_train )
        weights.append( lr.coef_[1] )
        params.append( 10.**c )

    weights = numpy.array( weights )    # 重み係数を Numpy 配列に変換

    # 各重み係数をプロット
    for column, color in zip( range(weights.shape[1]), colors ):
        # 折れ線グラフ
        plt.plot(
            params, weights[:, column],
            label = prePro3.df_.columns[column + 1],
            color = color
        )
    
    plt.grid()
    plt.axhline( 0, color = 'black', linestyle = '--', linewidth = 3 )
    plt.xlim( [10**(-5), 10**5] )
    plt.ylabel('weight coefficient')
    plt.xlabel('C [Reverse regularization parameter] (log scale)')
    plt.xscale('log')   # x 軸を log スケール化
    plt.legend(loc='lower left')
    plt.tight_layout()

    plt.savefig( 'DataPreProcess_scikit-learn_1.png', dpi=300, bbox_inches = 'tight' )
    plt.show()
    ....
```
