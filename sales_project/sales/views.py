from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from . import mongo
import os
from django.conf import settings
import json


#トップページ
def top(request):
     try:
        tenpos = list(mongo.get_tenpo_col().find({}))
        tenpo_list = [
            {"id": t["tenpo_id"], "name": t["name"]}
            for t in tenpos
        ]
        return render(
            request,
            "sales/index.html",
            {"tenpo_list": tenpo_list}
        )
    except Exception as e:
        return render(
            request,
            "sales/index.html",
            {
                "tenpo_list": [],
                "error": f"DB接続エラー: {e}"
            }
        )

#売上一覧
def tenpo_detail(request, tenpo_id):
    tenpo_id = int(tenpo_id)

    tenpo = tenpo_col.find_one({"tenpo_id": tenpo_id})

    start = request.GET.get("start")
    end = request.GET.get("end")

    query = {"tenpo_id": tenpo_id}
    if start and end:
        query["date"] = {"$gte": start, "$lte": end}

    uriage_list = list(uriage_col.find(query))

    tenpo_obj = {
        "id": tenpo_id,
        "name": tenpo["name"]
    }

    return render(request, "sales/detail.html", {
       "tenpo": tenpo_obj,
       "uriage_list": uriage_list,
    })

#グラフ作成
def tenpo_graph(request, tenpo_id):
    tenpo_id = int(tenpo_id)
    mode = request.GET.get("mode", "amount")

    data = list(
        uriage_col.find({"tenpo_id": tenpo_id}).sort("date", 1)
    )

    tenpo = tenpo_col.find_one({"tenpo_id": tenpo_id})

    if not data:
        return render(request, "sales/graph.html", {
            "tenpo_name": tenpo["name"],
            "error": "売上データがありません"
        })

    labels = [str(d["date"]) for d in data]

    if mode == "visitors":
        values = [d["visitors"] for d in data]
        graph_label = "来客数"
    else:
        values = [d["amount"] for d in data]
        graph_label = "売上金額"

    return render(request, "sales/graph.html", {
        "tenpo_name": tenpo["name"],
        "labels": labels,
        "values": values,
        "graph_label": graph_label,
        "mode": mode,
    })





#ローカルLLMによる売り上げ要約
from django.shortcuts import render
from .mongo import get_sales_data
from .llm import call_llm


def dashboard(request, tenpo_id):
    """
    売上データを取得し、
    LLMに簡単な分析コメントを書かせる画面
    """

    # MongoDBから売上データ取得
    sales_data = get_sales_data()
    tenpo_sales = [s for s in sales_data if s["tenpo_id"] == tenpo_id]

    # LLM用プロンプト
    prompt = f"""
以下は店舗ID{tenpo_id}の売上データです。

{tenpo_sales}

このデータから分かる特徴を、
日本語で3〜4文で簡潔に説明してください。
"""

    # LLM呼び出し
    try:
        ai_comment = call_llm(prompt)
    except Exception as e:
        ai_comment = f"AIコメントの生成に失敗しました: {e}"

    return render(
        request,
        "sales/dashboard.html",
        {
            "sales_data": sales_data,
            "ai_comment": ai_comment,
             "tenpo_id": tenpo_id,
        }
    )















