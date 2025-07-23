from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3
from ai_agent_ecommerce.core.llm import query_llm

router = APIRouter()
DB_PATH = 'ecommerce.db'

class Query(BaseModel):
    question: str

@router.post("/ask")
def ask_route(q: Query):
    return query_llm(q.question)

# Utility
def query_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Chart endpoints
@router.get("/chart/total_sales")
def total_sales_chart():
    rows = query_db("SELECT item_id, total_sales FROM product_total_sales ORDER BY total_sales DESC LIMIT 10")
    return {"labels": [r[0] for r in rows], "data": [r[1] for r in rows]}

@router.get("/chart/units_ordered")
def units_ordered_chart():
    rows = query_db("SELECT item_id, total_units_ordered FROM product_total_sales ORDER BY total_units_ordered DESC LIMIT 10")
    return {"labels": [r[0] for r in rows], "data": [r[1] for r in rows]}

@router.get("/chart/ad_spend_vs_sales")
def ad_spend_vs_sales_chart():
    rows = query_db("SELECT item_id, ad_spend, ad_sales FROM product_ad_sales ORDER BY ad_spend DESC LIMIT 10")
    return {
        "labels": [r[0] for r in rows],
        "ad_spend": [r[1] for r in rows],
        "ad_sales": [r[2] for r in rows],
    }

@router.get("/chart/ad_clicks")
def ad_clicks_chart():
    rows = query_db("SELECT item_id, clicks FROM product_ad_sales ORDER BY clicks DESC LIMIT 10")
    return {"labels": [r[0] for r in rows], "data": [r[1] for r in rows]}

@router.get("/chart/eligibility")
def eligibility_chart():
    eligible = query_db("SELECT COUNT(*) FROM eligibility_table WHERE eligibility = 'Eligible'")
    ineligible = query_db("SELECT COUNT(*) FROM eligibility_table WHERE eligibility = 'Ineligible'")
    return {
        "labels": ["Eligible", "Ineligible"],
        "data": [eligible[0][0], ineligible[0][0]]
    }
