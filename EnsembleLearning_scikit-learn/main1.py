# -*- coding:utf-8 -*-
# Anaconda 4.3.0 環境

import numpy
import pandas
import matplotlib.pyplot as plt

# scikit-learn ライブラリ関連
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler        # scikit-learn の preprocessing モジュールの StandardScaler クラス
from sklearn.model_selection import StratifiedKFold     #
from sklearn.model_selection import cross_val_score     #

from sklearn.pipeline import Pipeline

# 自作クラス
import EnsembleLearningClassifier
import DataPreProcess
import Plot2D

def main():
    """
    アンサンブル学習
    
    """
    print("Enter main()")
    
    ensemble_clf = EnsembleLearningClassifier.EnsembleLearningClassifier( n_classifier = 1 )

    # データの読み込み

    #===========================================
    # 前処理 [PreProcessing]
    #===========================================
    # 欠損データへの対応
    #prePro.meanImputationNaN()

    # ラベルデータをエンコード
    #prePro.encodeClassLabelByLabelEncoder( colum = 1 )
    #prePro.print( "Breast Cancer Wisconsin dataset" )

    # データをトレードオフデータとテストデータに分割
    #X_train, X_test, y_train, y_test \
    #= DataPreProcess.DataPreProcess.dataTrainTestSplit( X_input = dat_X, y_input = dat_y, ratio_test = 0.2 )

    #-------------------------------------------
    # Pipeline の設定
    #-------------------------------------------
    # パイプラインに各変換器、推定器を設定
    """
    pipe_logReg = Pipeline(
                      steps = [                                           # タプル (任意の識別文字, 変換器 or 推定器のクラス) で指定
                                  ( "scl", StandardScaler() ),            # スケーリング：　変換器のクラス（fit() 関数を持つ）
                                  ( "pca", PCA( n_components=2 ) ),       # PCA でデータの次元削除
                                  ( "clf", LogisticRegression( random_state=1 ) ) # ロジスティクス回帰：推定器のクラス（preddict()関数を持つ）
                              ]
                  )
    """

    # パイプラインに設定した変換器の fit() 関数を実行
    #pipe_logReg.fit( X_train, y_train )

    # 
    #print( "Test Accuracy: %.3f" % pipe_logReg.score( X_test, y_test ) )

    #============================================
    # Learning Process
    #===========================================
    # パイプラインに設定した推定器の predict() 実行
    #y_predict = pipe_logReg.predict(X_test)
    #print("predict : ", y_predict )
    
    # pipeline オブジェクトの内容確認
    #print( "pipe_logReg.get_params() : \n", pipe_logReg.get_params( deep = True ) )
    #print( "pipe_logReg.get_params() : \n", pipe_logReg.get_params( deep = False ) )

    #===========================================
    # 汎化性能の確認
    #===========================================
    

    plt.savefig("./EnsembleLearning_scikit-learn_1.png", dpi = 300, bbox_inches = 'tight' )
    plt.show()
    
    print("Finish main()")
    return
    
if __name__ == '__main__':
     main()