import pylab as plt
import pandas as pd

import matplotlib.pyplot as plt
import os


HOUSING_PATH=r"D:\WORKPLACE\WeiboCrawler"
#导入数据
def load_housing_data(housing_path=HOUSING_PATH):
    csv_path=os.path.join(housing_path,"sentiment.csv")
    return pd.read_csv(csv_path)

housing=load_housing_data()

#绘制直方图
housing.hist(bins=100,figsize=(15,10))  #bins表示直方图中柱子的数量，figsize是每张图的大小
plt.title(" ")
plt.xlabel('point')
plt.ylabel('count')

plt.savefig(r"D:\WORKPLACE\WeiboCrawler\static\assets\img\zhifangtu.png")




