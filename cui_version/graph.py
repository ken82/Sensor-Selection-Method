#/usr/bin/python3
#_*_coding:utf-8_*_
#sensor_selection.pyの実験結果グラフ
import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5])  # 横軸は判別器の数
y = np.array([1, 2, 3, 4, 5])  # 縦軸は精度

plt.plot(x, y)  # グラフを準備
#plt.title("")  # グラフタイトル
plt.xlabel("Number of Discriminator")  # x軸の名前
plt.ylabel("Precision")  # y軸の名前
plt.show()  # グラフの表示
