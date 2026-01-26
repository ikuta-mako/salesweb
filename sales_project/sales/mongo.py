# sales/mongo.py
from django.conf import settings
from pymongo import MongoClient

def get_db():
    # 5秒で諦める（Renderのタイムアウト回避）
    client = MongoClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
    )
    return client[settings.MONGO_DB]

def get_tenpo_col():
    return get_db()["tenpo"]

def get_uriage_col():
    return get_db()["uriage"]

def get_sales_data():
    tenpo_col = get_tenpo_col()
    uriage_col = get_uriage_col()

    tenpos = list(tenpo_col.find({}, {"_id": 0}))
    uriages = list(uriage_col.find({}, {"_id": 0}))

    tenpo_dict = {t["tenpo_id"]: t["name"] for t in tenpos}

    result = []
    for u in uriages:
        result.append({
            "tenpo_id": u["tenpo_id"],
            "tenpo_name": tenpo_dict.get(u["tenpo_id"], "不明"),
            "date": u["date"],
            "amount": u["amount"],
        })

    return result
