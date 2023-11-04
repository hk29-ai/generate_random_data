# 概要  
次の４つの方法にて、乱数を生成するpythonスクリプトです。  
下記1,2については、pythonライブラリ「lhsmdu」を使用して、3,4については「numpy」を使用しています。  
1.モンテカルロ法　…　lhsmdu.createRandomStandardUniformMatrix(dimension, sampling_num)  
2.ラテン超方格法　…　lhsmdu.sample(dimension, sampling_num)  
3.正規分布　…　np.random.normal(0.5, 0.16, sampling_num)  
4.ベータ分布　…　np.random.beta(5, 2, sampling_num)  

# ライブラリのインストール  
pythonライブラリ「lhsmdu」については、次のようにpipでインストールします。  
pip install lhsmdu  

# 使い方  
## 入力因子について、キーは因子名でバリューはその乱数の生成範囲の下限と上限をタプルです。  
例)  
   input_factors = {
        "height": (50, 200),
        "width": (0.06, 0.1),
        "density": (1e15, 9e15),
        "temp": (-50, 250)
    }
  
## サンプル数について、次のように指定します。
例）  
sampling_num = 200
