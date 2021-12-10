import pandas  as pd
from snownlp import SnowNLP

from mongo import connect_to_mongo

comments = 'comments'
collection = connect_to_mongo(comments)


result = pd.DataFrame(list(collection.find()))

result.to_csv('comments.csv', encoding='utf_8_sig')

df = pd.read_csv("comments.csv")
result = list(df["comment_text"])
score = []

for i in range(len(result)):
    try:
        blob = SnowNLP(result[i])

        score.append(blob.sentiments)
    except Exception:
        pass

data = pd.DataFrame(score)

data.to_csv('sentiment.csv', header=False, index=False, mode='a+')
