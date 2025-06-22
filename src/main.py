# from db.db_utils import get_connection
# from scripts.fetch_data import fetch_data
# from utils.insert_data_fromApi import (
#     insert_company, get_period_id, insert_quarterly_results, insert_annual_results,
#     insert_balance_sheet, insert_cash_flow, insert_financial_ratios,
#     insert_shareholding_pattern, insert_performance_metrics
# )

# if __name__ == "__main__":
#     STOCK_NAME = "SEQUENT"
#     COMPANY_NAME = "Sequent Scientific"
#     COMPANY_CODE = "SEQUENT"

#     data = fetch_data(STOCK_NAME)
#     if not data:
#         exit()

#     conn = get_connection()
#     company_id = insert_company(conn, COMPANY_NAME, COMPANY_CODE)

#      # Insert quarterly results
#     quarter_results = data.get("quarter_results", {})
#     for period_name in quarter_results.get("Sales", {}):
#         period_id = get_period_id(conn, period_name, "quarterly")
#         if not period_id:
#             print(f"Quarterly period {period_name} not found in financial_periods table.")
#             continue
#         metrics = {k: v.get(period_name) for k, v in quarter_results.items()}
#         insert_quarterly_results(conn, company_id, period_id, metrics)

#     # Insert annual results
#     yoy_results = data.get("yoy_results", {})
#     for period_name in yoy_results.get("Sales", {}):
#         period_id = get_period_id(conn, period_name, "annual")
#         if not period_id:
#             print(f"Annual period {period_name} not found in financial_periods table.")
#             continue
#         metrics = {k: v.get(period_name) for k, v in yoy_results.items()}
#         insert_annual_results(conn, company_id, period_id, metrics)

#     # Insert balance sheet
#     balancesheet = data.get("balancesheet", {})
#     for period_name in balancesheet.get("Equity Capital", {}):
#         period_id = get_period_id(conn, period_name, "annual")
#         if not period_id:
#             print(f"Balance sheet period {period_name} not found in financial_periods table.")
#             continue
#         metrics = {k: v.get(period_name) for k, v in balancesheet.items()}
#         insert_balance_sheet(conn, company_id, period_id, metrics)

#     # Insert cash flow
#     cashflow = data.get("cashflow", {})
#     for period_name in cashflow.get("Net Cash Flow", {}):
#         period_id = get_period_id(conn, period_name, "annual")
#         if not period_id:
#             print(f"Cash flow period {period_name} not found in financial_periods table.")
#             continue
#         metrics = {k: v.get(period_name) for k, v in cashflow.items()}
#         insert_cash_flow(conn, company_id, period_id, metrics)

#     # Insert ratios
#     ratios = data.get("ratios", {})
#     for period_name in ratios.get("Debtor Days", {}):
#         period_id = get_period_id(conn, period_name, "annual")
#         if not period_id:
#             print(f"Ratios period {period_name} not found in financial_periods table.")
#             continue
#         metrics = {k: v.get(period_name) for k, v in ratios.items()}
#         insert_financial_ratios(conn, company_id, period_id, metrics)

#     # Insert shareholding pattern (quarterly)
#     shp_quarterly = data.get("shareholding_pattern_quarterly", {})
#     for period_name in shp_quarterly.get("Promoters", {}):
#         period_id = get_period_id(conn, period_name, "quarterly")
#         if not period_id:
#             print(f"Shareholding quarterly period {period_name} not found in financial_periods table.")
#             continue
#         metrics = {k: v.get(period_name) for k, v in shp_quarterly.items()}
#         insert_shareholding_pattern(conn, company_id, period_id, metrics)

#     # Insert shareholding pattern (yearly)
#     shp_yearly = data.get("shareholding_pattern_yearly", {})
#     for period_name in shp_yearly.get("Promoters", {}):
#         period_id = get_period_id(conn, period_name, "annual")
#         if not period_id:
#             print(f"Shareholding annual period {period_name} not found in financial_periods table.")
#             continue
#         metrics = {k: v.get(period_name) for k, v in shp_yearly.items()}
#         insert_shareholding_pattern(conn, company_id, period_id, metrics)

#     # Insert performance metrics (profit_loss_stats)
#     profit_loss_stats = data.get("profit_loss_stats", {})
#     # Use the latest annual period for period_id
#     if yoy_results.get("Sales", {}):
#         latest_annual_period = max(yoy_results.get("Sales", {}).keys(), key=lambda x: int(x.split()[-1]))
#         period_id = get_period_id(conn, latest_annual_period, "annual")
#         if period_id:
#             insert_performance_metrics(conn, company_id, period_id, profit_loss_stats)

#     conn.close()
#     print("All data inserted successfully.")

from src.etl.excel_parser import parse_financial_excel
from src.etl.db_inserter_excel_data import (insert_annual_results,insert_balance_sheet,insert_cash_flow,insert_quarterly_results)
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
    excel_file = company.get("excel_file")
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
    all_sections = parse_financial_excel(file_path)

    insert_annual_results(all_sections, cur, company_id)
    insert_balance_sheet(all_sections, cur, company_id)
    insert_cash_flow(all_sections, cur, company_id)
    insert_quarterly_results(all_sections, cur, company_id)
    conn.commit()

cur.close()
conn.close()




