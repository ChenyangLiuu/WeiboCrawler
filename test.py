import re

import pandas  as pd
from snownlp import SnowNLP

from mongo import connect_to_mongo

comments = 'comments'
collection = connect_to_mongo(comments)


def analysis_by_keyword(keyword):
    results=[]
    for u in collection.find({'comment_text':re.compile(keyword)}):
        results.append(u)
    result= [result[ 'comment_text' ] for result in results]
    score = []

    for i in range(len(result)):
        try:
            blob = SnowNLP(result[i])

            score.append(blob.sentiments)
        except Exception:
            pass

    data = pd.DataFrame(score)

    data.to_csv('sentiment.csv', header=False, index=False, mode='w')
    result = pd.DataFrame(result)
    result.to_csv('comments.csv', encoding='utf_8_sig')




if __name__ =="__main__":
    keyword=input()
    analysis_by_keyword(keyword)