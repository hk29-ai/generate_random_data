#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lhsmdu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
now = datetime.datetime.now()
now = now.strftime("%y%m%d")

class RandomSampler:
    # インスタンスの生成
    def __init__(self, factors, sampling_num, save_file_name, plot_color):
        self.factors = factors # 入力データ
        self.factors_column_names = list(factors.keys()) # 因子名をリスト化
        self.sampling_num = sampling_num # 生成するサンプル数
        self.save_file_name = save_file_name # 保存するファイル名
        self.plot_color = plot_color # グラフにプロットする点の色

    # データ生成
    def generate_random_data(self, random_data):
        # データの逆正規化
        fixed_data_np = self._normalize_data(random_data)
        
        # pandasデータフレームにする
        random_df = pd.DataFrame(fixed_data_np.T, columns=self.factors_column_names)
        
        # csvファイルへ出力する
        random_df.to_csv(f"{self.save_file_name}.csv", sep=",", index=False, encoding="utf-8")
        
        # グラフへプロット
        self.plot_matrix_scatter(random_df)
        
        return random_df

    # データの逆正規化。生成されたデータは区間0～1の乱数データのため、指定した最小値～最大値の区間へ変換する
    def _normalize_data(self, data):
        for i, key in enumerate(self.factors_column_names):
            my_min, my_max = self.factors[key]
            data[i] = ((my_max - my_min) * data[i] + my_min)
        return np.array(data)

    # 行列散布図
    def plot_matrix_scatter(self, df):
        sns.set(style="ticks", font_scale=1.2, palette=self.plot_color, color_codes=True)
        g = sns.pairplot(df, diag_kind="hist")
        g.fig.suptitle(self.save_file_name)
        g.fig.subplots_adjust(top=0.9)
        plt.savefig(f"{self.save_file_name}.png")
        plt.close()

# モンテカロ法によるデータ生成
class MonteCarlo(RandomSampler):
    def __init__(self, factors, sampling_num, save_file_name, plot_color):
        super().__init__(factors, sampling_num, save_file_name, plot_color)

    def generate_samples(self):
        monte_carlo = lhsmdu.createRandomStandardUniformMatrix(len(self.factors), self.sampling_num)
        return self.generate_random_data(monte_carlo)

# ラテン超方格法によるデータ生成
class LatinHypercube(RandomSampler):
    def __init__(self, factors, sampling_num, save_file_name, plot_color):
        super().__init__(factors, sampling_num, save_file_name, plot_color)

    def generate_samples(self):
        latin_hypercube = lhsmdu.sample(len(self.factors), self.sampling_num)
        return self.generate_random_data(latin_hypercube)

# 正規乱数によるデータ生成
class NormalRandom(RandomSampler):
    def __init__(self, factors, sampling_num, save_file_name, plot_color):
        super().__init__(factors, sampling_num, save_file_name, plot_color)

    def generate_samples(self):
        buf=[]
        for cnt in range(len(self.factors)):
            buf.append(np.random.normal(0.5, 0.16, self.sampling_num))
        normal_random = np.array(buf)
        return self.generate_random_data(normal_random)

# ベータ関数によるデータ生成
class BetaRandom(RandomSampler):
    def __init__(self, factors, sampling_num, save_file_name, plot_color):
        super().__init__(factors, sampling_num, save_file_name, plot_color)

    def generate_samples(self):
        buf=[]
        for cnt in range(len(self.factors)):
            buf.append(np.random.beta(5, 2, self.sampling_num))
        beta_random = np.array(buf)
        return self.generate_random_data(beta_random)

def main():
    # モンテカルロ法
    monte_carlo = MonteCarlo(input_factors, sampling_num, f'{now}_monte_carlo', 'winter')
    df1 = monte_carlo.generate_samples()
    print(df1)

    # ラテン超方格法
    latin_hypercube  = LatinHypercube(input_factors, sampling_num, f'{now}_latin_hypercube', 'autumn')
    df2 = latin_hypercube.generate_samples()
    print(df2)

    # 正規乱数
    normal_random = NormalRandom(input_factors, sampling_num, f'{now}_normal_random', 'gray')
    df3 = normal_random.generate_samples()
    print(df3)

    # ベータ乱数
    beta_random = BetaRandom(input_factors, sampling_num, f'{now}_beta_random', 'summer')
    df4 = beta_random.generate_samples()
    print(df4)
    
if __name__ == "__main__":
    # 作成するランダムデータを辞書型で作成する
    # キーは因子名、バリューはタプルで生成データの下限と上限を指定する
    input_factors = {
        "height": (50, 200),
        "width": (0.06, 0.1),
        "density": (1e15, 9e15),
        "temp": (-50, 250)
    }
    
    # 生成するサンプル数
    sampling_num = 200

    main()
