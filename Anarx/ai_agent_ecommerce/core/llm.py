import sqlite3
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

def query_llm(question: str):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    q = question.lower()

    try:
        if 'total sales' in q:
            cursor.execute('SELECT SUM(total_sales) FROM product_total_sales')
            result = cursor.fetchone()[0] or 0
            return {"answer": f"Total sales: ₹{result:.2f}"}
        elif 'units ordered' in q or 'units sold' in q or 'total units' in q:
            cursor.execute('SELECT SUM(total_units_ordered) FROM product_total_sales')
            result = cursor.fetchone()[0] or 0
            return {"answer": f"Total units ordered: {int(result)}"}
        elif 'highest total sales' in q:
            cursor.execute('SELECT item_id, total_sales FROM product_total_sales ORDER BY total_sales DESC LIMIT 1')
            result = cursor.fetchone()
            return {"answer": f"Highest Total Sales: ₹{result[1]:.2f} by Product {result[0]}"}
        elif 'most ordered' in q:
            cursor.execute('SELECT item_id, total_units_ordered FROM product_total_sales ORDER BY total_units_ordered DESC LIMIT 1')
            result = cursor.fetchone()
            return {"answer": f"Most Units Ordered: {int(result[1])} by Product {result[0]}"}
        elif 'total ad spend' in q:
            cursor.execute('SELECT SUM(ad_spend) FROM product_ad_sales')
            result = cursor.fetchone()[0] or 0
            return {"answer": f"Total Ad Spend: ₹{result:.2f}"}
        elif 'total ad sales' in q:
            cursor.execute('SELECT SUM(ad_sales) FROM product_ad_sales')
            result = cursor.fetchone()[0] or 0
            return {"answer": f"Total Ad Sales: ₹{result:.2f}"}
        elif 'highest ad sales' in q:
            cursor.execute('SELECT item_id, ad_sales FROM product_ad_sales ORDER BY ad_sales DESC LIMIT 1')
            result = cursor.fetchone()
            return {"answer": f"Highest Ad Sales: ₹{result[1]:.2f} by Product {result[0]}"}
        elif 'roas' in q:
            cursor.execute('SELECT SUM(ad_sales) FROM product_ad_sales')
            revenue = cursor.fetchone()[0] or 0
            cursor.execute('SELECT SUM(ad_spend) FROM product_ad_sales')
            spend = cursor.fetchone()[0] or 0
            roas = revenue / spend if spend else 0
            return {"answer": f"RoAS (Return on Ad Spend): {roas:.2f}"}
        elif 'highest cpc' in q:
            cursor.execute('SELECT item_id, MAX(ad_spend * 1.0 / clicks) FROM product_ad_sales WHERE clicks > 0')
            result = cursor.fetchone()
            return {"answer": f"Product with highest CPC: {result[0]} at ₹{result[1]:.2f}"}
        elif 'most ad impressions' in q:
            cursor.execute('SELECT item_id, impressions FROM product_ad_sales ORDER BY impressions DESC LIMIT 1')
            result = cursor.fetchone()
            return {"answer": f"Product with most ad impressions: {result[0]} ({int(result[1])} impressions)"}
        elif 'eligible products count' in q:
            cursor.execute("SELECT COUNT(*) FROM eligibility_table WHERE eligibility = 'Eligible'")
            result = cursor.fetchone()[0] or 0
            return {"answer": f"Number of eligible products: {result}"}
        elif 'ineligible products count' in q:
            cursor.execute("SELECT COUNT(*) FROM eligibility_table WHERE eligibility = 'Ineligible'")
            result = cursor.fetchone()[0] or 0
            return {"answer": f"Number of ineligible products: {result}"}

        sql = generate_sql_from_llm(question)
        if not sql:
            return {"answer": "I couldn't understand the question."}
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return {"answer": "No results found."}
        if len(rows) == 1 and len(rows[0]) == 1:
            return {"answer": str(rows[0][0])}
        return {"answer": str(rows)}
    except Exception as e:
        return {"answer": f"Error: {e}"}
    finally:
        conn.close()

def generate_sql_from_llm(question: str) -> str:
    if not GEMINI_API_KEY:
        return None
    prompt = f"""
You are a data analyst. Use these SQLite tables:
- product_ad_sales(item_id, ad_sales, ad_spend, clicks, impressions, units_sold)
- product_total_sales(item_id, total_sales, total_units_ordered)
- eligibility_table(item_id, eligibility)
Generate a single SQLite SQL query to answer: '{question}'.
Only output the SQL query.
"""
    try:
        response = httpx.post(
            GEMINI_API_URL,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=20
        )
        data = response.json()
        sql = data['candidates'][0]['content']['parts'][0]['text']
        return sql.strip().replace("```sql", "").replace("```", "").strip()
    except Exception:
        return None
