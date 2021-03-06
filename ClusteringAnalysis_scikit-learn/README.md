## クラスター分析 [Clustering Analysis]

### 項目 [Contents]

1. [使用するライブラリ](#使用するライブラリ)
1. [使用するデータセット](#使用するデータセット)
1. [コードの実行結果](#コードの実行結果)
    1. [k-mean 法によるクラスタリング](#クラスタリング)
    1. [エルボー法を用いた最適なクラスター数](#エルボー法を用いた最適なクラスター数)
    1. [シルエット図を用いたクラスタリング性能の数値化](#シルエット図を用いたクラスタリング性能の数値化)
1. [背景理論](#背景理論)
    1. [ベクトル量子化](#ベクトル量子化)
    1. [k-mean 法](#k-mean法)
    1. [学習ベクトル量子化](#学習ベクトル量子化)
    1. [ウォード法](#ウォード法)
    1. [EMアルゴリズム](#EMアルゴリズム)

</br>

<a name="#使用するライブラリ"></a>

### 使用するライブラリ：

> scikit-learn ライブラリ </br>
>> データセット Dataset loading utilities : `sklearn.datasets`</br>
>> http://scikit-learn.org/stable/datasets/index.html </br>
>>> ガウス分布に従った各クラスター生成 : `sklearn.datasets.make_blobs()` : </br>
http://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_blobs.html#sklearn.datasets.make_blobs

>> クラスタリング : `sklearn.cluster`</br>
http://scikit-learn.org/stable/modules/clustering.html#clustering </br>
>>> k-means 法 : `sklearn.cluster.KMeans` </br>
http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html </br>

> その他ライブラリ
>>

</br>

<a name="#使用するデータセット"></a>

### 使用するデータセット

> ガウス分布に従った各クラスター生成 : `sklearn.datasets.make_blobs()`

</br>

<a name="#コードの実行結果"></a>

## コードの実行結果

<a name="#クラスタリング"></a>

## k-mean 法によるクラスタリング : `main1.py`

### ① ガウス分布に従った各クラスターの散布図

- ガウス分布に従った各クラスターを `sklearn.datasets.make_blobs()` 関数を使用して生成
- クラスター数 5 個 : `centers = 5`
- 各クラスターのサンプル数 100 個（合計 500 個） `n_samples = 500`
- 特徴量 2 個 : `n_features = 2`

> ガウス分布に従った各クラスターの散布図
![clutterringanalysis_scikit-learn_1-1](https://user-images.githubusercontent.com/25688193/29921505-c2d7b696-8e8c-11e7-9ef9-84abad420f7a.png)


### ② k-means法でのセントロイドと各クラスターの散布図

- k-meas 法として `sklearn.cluster.KMeans` クラスを使用
- クラスター数 5 個 : `n_clusters = 5`
- クラスターの個数（５個）の都度、異なるランダムな初期値を使用して, </br>k-means 法によるクラスタリングを 10 回行う : `n_init = 10`
- １回の k-means 法の最大イテレーション回数 300 回 : `max_iter = 300`
- k-means 法において、収束と判定する為の相対的な許容誤差値 0.0001 : `tol = 1e-04`
- fitting 処理 `sklearn.cluster.KMeans.fit()` する特徴行列 `X_features` は、
    - 各クラスターのサンプル数 100 個（合計 500 個） `X_features[0:500,:]`
    - 特徴量 2 個 : `X_features[:,0], X_features[:,1]`

</br>

> k-means 法でのセントロイドと各クラスターの散布図
>> セントロイドをまとめて描写した散布図
![clutterringanalysis_scikit-learn_1-2](https://user-images.githubusercontent.com/25688193/29921508-c476719a-8e8c-11e7-8470-95cfd511ab69.png)

>> セントロイドを個別に描写した散布図
![clutterringanalysis_scikit-learn_1-3](https://user-images.githubusercontent.com/25688193/29921350-38ef44bc-8e8c-11e7-98d8-b96e7782aae3.png)

</br>

<a name="#エルボー法を用いた最適なクラスター数"></a>

## エルボー法を用いた、最適なクラスター数 : `main2.py`

|クラスター数|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Distortion (SSE)</br>小数点以下切り捨て|13693|3694|1535|676|**238**</br>値が急速に低下（エルボー）|218|201|185|168|153|141|129|120|110|

> kmeans ++ 法による、クラスター数と SSE 値の関係図（エルボー法）。</br>図より、クラスター数が、5 個のときみエルボー（肘）部分となっており、最適なクラスター数は 5 個であることが分かる。
![clutterringanalysis_scikit-learn_2-1](https://user-images.githubusercontent.com/25688193/29934439-283e1a2e-8eb6-11e7-9382-f5d41ccbf4ff.png)


</br>

<a name="#シルエット図を用いたクラスタリング性能の数値化"></a>

## シルエット図を用いた、クラスタリング性能の数値化 : `main3.py`

> コード実装中...

</br>

---

<a name="#背景理論"></a>

## 背景理論

<a name="#ベクトル量子化"></a>

## ベクトル量子化

![twitter_ _ _9-3_170623](https://user-images.githubusercontent.com/25688193/29883660-f317784c-8deb-11e7-95f2-36758cc39a98.png)

<a name="#k-mean法"></a>

## k-mean 法

![twitter_ _ _9-4_170623](https://user-images.githubusercontent.com/25688193/29883665-f521bbd4-8deb-11e7-8d72-5f67a511e32f.png)

<a name="#学習ベクトル量子化"></a>

## 学習ベクトル量子化 [LQV]

![twitter_ _ _9-5_170623](https://user-images.githubusercontent.com/25688193/29883666-f554559e-8deb-11e7-8e70-62068f41afa7.png)

<a name="#ウォード法"></a>

## ウォード法

<a name="#EMアルゴリズム"></a>

## EM アルゴリズム

![twitter_ _ _11-6_170701](https://user-images.githubusercontent.com/25688193/29933249-f4078546-8eb1-11e7-8ae1-83861e2cefd8.png)
![twitter_ _ _11-8_170701](https://user-images.githubusercontent.com/25688193/29933253-f40b7390-8eb1-11e7-8006-8eeed89f613e.png)
![twitter_ _ _11-9_170701](https://user-images.githubusercontent.com/25688193/29933250-f40824e2-8eb1-11e7-995a-bfbd9f0415d4.png)
![twitter_ _ _11-10_170701](https://user-images.githubusercontent.com/25688193/29933251-f40a4e7a-8eb1-11e7-9643-b1c99e0096db.png)
![twitter_ _ _11-7 _170701](https://user-images.githubusercontent.com/25688193/29933252-f40a45c4-8eb1-11e7-9afa-7335ce8f1123.png)
