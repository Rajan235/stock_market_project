from src.etl.excel_parser import parse_financial_excel
from src.etl.db_inserter_excel_data import (insert_annual_results,insert_balance_sheet,insert_cash_flow,insert_quarterly_results,insert_financial_ratios,insert_performance_metrics)
import psycopg2
from db.db_utils import get_connection
from sqlalchemy import create_engine

import os 

from src.etl.company_mapping import companies




conn = get_connection()
cur = conn.cursor()
engine = create_engine("postgresql+psycopg2://", creator=lambda: conn)
# company_name = "Wipro"
# company_code = "WIPRO"  # From your symbol mapping
# Insert if not exists


for company in companies:
    excel_file = company["excel_file"]
    company_name = os.path.splitext(excel_file)[0] if excel_file else company["company_code"]
    company_code = company["company_code"]

    if not excel_file or not os.path.exists(os.path.join("data/downloads", excel_file)):
        print(f"Skipping {company_code}: Excel file not found.")
        continue

    print(f"\nProcessing {company_name} ({company_code}) ...")

    # Insert company if not exists
    cur.execute("""
        INSERT INTO companies (company_name, company_code)
        VALUES (%s, %s)
        ON CONFLICT (company_name) DO NOTHING
    """, (company_name, company_code))

    cur.execute("SELECT company_id FROM companies WHERE company_name = %s", (company_name,))
    company_id = cur.fetchone()[0]

    file_path = os.path.join("data/downloads", excel_file)
    print(f"Parsing financial data from {file_path} ...")
    all_sections = parse_financial_excel(file_path)
    #print(all_sections)

    insert_annual_results(all_sections, cur, company_id)
    insert_balance_sheet(all_sections, cur, company_id)
    insert_cash_flow(all_sections, cur, company_id)
    insert_quarterly_results(all_sections, cur, company_id)
    insert_financial_ratios(all_sections, cur, company_id)
    insert_performance_metrics(all_sections, cur, company_id)
    conn.commit()

cur.close()
conn.close()




