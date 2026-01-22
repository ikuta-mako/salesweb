import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["sales_db"]


tenpo_col = db["tenpo"]
uriage_col = db["uriage"]

def get_sales_data():
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