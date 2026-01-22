#データ入れる用
from pymongo import MongoClient

# MongoDB接続
client = MongoClient("mongodb://localhost:27017/")
db = client["sales_db"]

tenpo_col = db["tenpo"]
uriage_col = db["uriage"]

# 既存削除（入れ直し用）
tenpo_col.delete_many({}) 
uriage_col.delete_many({})

# 店舗データ 
tenpo_data = [
    {"tenpo_id": 1, "name": "渋谷店"},
    {"tenpo_id": 2, "name": "新宿店"},
    {"tenpo_id": 3, "name": "池袋店"},
    {"tenpo_id": 4, "name": "秋葉原店"},
    {"tenpo_id": 5, "name": "上野店"},
    {"tenpo_id": 6, "name": "東京駅前店"},
    {"tenpo_id": 7, "name": "品川店"},
    {"tenpo_id": 8, "name": "横浜店"}
]

tenpo_col.insert_many(tenpo_data)

print("データ投入完了")
