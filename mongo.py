from pymongo import MongoClient


def connect_to_mongo(table_name):
    client = MongoClient(host='127.0.0.1', port=27017)
    # 选择数据库
    db = client[table_name]
    # 选择好数据库后我们需要指定要操作的集合，与数据库的选择类似
    collection = db[table_name]
    return collection

def save_to_mongo(collection,result):
    if collection.insert_one(result):
        pass

