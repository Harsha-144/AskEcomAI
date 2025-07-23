import pandas as pd
import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, '../../data')

def main():
    conn = sqlite3.connect('ecommerce.db')
    try:
        product_ad_sales = pd.read_csv(os.path.join(data_dir, 'Product-Level Ad Sales and Metrics (mapped).csv'))
        eligibility_table = pd.read_csv(os.path.join(data_dir, 'Product-Level Eligibility Table (mapped).csv'))
        product_total_sales = pd.read_csv(os.path.join(data_dir, 'Product-Level Total Sales and Metrics (mapped).csv'))

        product_ad_sales.to_sql('product_ad_sales', conn, if_exists='replace', index=False)
        product_total_sales.to_sql('product_total_sales', conn, if_exists='replace', index=False)
        eligibility_table.to_sql('eligibility_table', conn, if_exists='replace', index=False)

        print("Database setup completed successfully.")
    except Exception as e:
        print(f"Error during database setup: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 