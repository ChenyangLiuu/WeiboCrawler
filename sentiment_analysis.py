import pandas  as pd
from snownlp import SnowNLP

from mongo import connect_to_mongo

comments = 'comments'
collection = connect_to_mongo(comments)

def get_comment_text():
    results = list(collection.find({},{'_id':0,'comment_text':1}))
    result= [result[ 'comment_text' ] for result in results]
    return result

results = get_comment_text()
score=[]

for i in range(len(results)):
    try:
        blob = SnowNLP(results[i])
        print(blob.sentiments)
        score.append(blob.sentiments)
    except Exception:
        pass

data = pd.DataFrame(score)

data.to_csv('sentiment.csv', header=False, index=False, mode='a+')