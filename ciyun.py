import jieba
import wordcloud
import os
import pandas as pd


#读取csv转化为txt
filePath = r'D:\WORKPLACE\WeiboCrawler'
files=os.listdir(filePath)
data = pd.read_csv(r'D:\WORKPLACE\WeiboCrawler\comments.csv')		# 使用pandas模块读取数据

print('开始写入txt文件...')
with open('11.txt','w', encoding='utf-8') as f:
    for line in data.values:
       print( f.write((str(line[1])+'\n')))#表示将第一列第二列和第三列进行转换




# 读取文本
with open("11.txt",encoding="utf-8") as f:
    s = f.read()

ls = jieba.lcut(s) # 生成分词列表
text = ' '.join(ls) # 连接成字符串


stopwords = ["的","是","了"] # 去掉不需要显示的词

wc = wordcloud.WordCloud(font_path="msyh.ttc",
                         width = 3000,
                         height = 1000,
                         background_color='white',
                         max_words=1000,stopwords=s)
# msyh.ttc电脑本地字体，写可以写成绝对路径
wc.generate(text) # 加载词云文本
wc.to_file(r"D:\WORKPLACE\WeiboCrawler\static\assets\img\词云.png") # 保存词云文件