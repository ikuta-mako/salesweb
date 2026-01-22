from pymongo import MongoClient
from datetime import date, timedelta
import random

# MongoDB接続
client = MongoClient("mongodb://localhost:27017/")
db = client["sales_db"]

tenpo_col = db["tenpo"]
uriage_col = db["uriage"]

# 既存売上データ削除（入れ直し）
uriage_col.delete_many({})

# 日付設定
start_date = date(2025, 1, 1)
days = 30  # 30日分

tenpo_list = list(tenpo_col.find())

uriage_data = []

for tenpo in tenpo_list:
    tenpo_id = tenpo["tenpo_id"]

    for i in range(days):
        d = start_date + timedelta(days=i)

        visitors = random.randint(20, 80)
        amount = visitors * random.randint(1800, 3200)

        uriage_data.append({
            "tenpo_id": tenpo_id,
            "date": d.strftime("%Y-%m-%d"),
            "amount": amount,
            "visitors": visitors
        })

uriage_col.insert_many(uriage_data)

print("売上データ自動生成 完了")
