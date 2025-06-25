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

    # to insert screener data in db
    insert_annual_results(all_sections, cur, company_id)
    insert_balance_sheet(all_sections, cur, company_id)
    insert_cash_flow(all_sections, cur, company_id)
    insert_quarterly_results(all_sections, cur, company_id)
    insert_financial_ratios(all_sections, cur, company_id)
    insert_performance_metrics(all_sections, cur, company_id)
    conn.commit()

    # to back fill events table
    # Example usage for quarterly_results
    # backfill_events_for_table(
    #     table_name='quarterly_results',
    #     event_type_name='quarterly_results_announced',
    #     metrics=[
    #         "sales", "net_profit", "eps_rs", "operating_profit", "expenses", "other_income",
    #         "interest", "depreciation", "profit_before_tax", "tax", "tax_percentage", "opm_percentage"
    #     ],
    #     period_type='quarterly'
    # )

    # # Example usage for annual_results
    # backfill_events_for_table(
    #     table_name='annual_results',
    #     event_type_name='annual_results_announced',
    #     metrics=[
    #         "sales", "net_profit", "eps_rs", "operating_profit", "expenses", "other_income",
    #         "interest", "depreciation", "profit_before_tax", "tax", "tax_percentage", "opm_percentage",
    #         "dividend_payout_percentage", "dividend_amount"
    #     ],
    #     period_type='annual'
    # )
    # backfill_events_for_table(
    #     table_name='balance_sheet',
    #     event_type_name='balance_sheet_announced',
    #     metrics=[
    #         "equity_capital", "reserves", "borrowings", "other_liabilities", "total_liabilities",
    #         "fixed_assets", "cwip", "investments", "other_assets", "total_assets"
    #     ],
    #     period_type='annual'  # or 'quarterly' if you have quarterly balance sheets
    # )
    # backfill_events_for_table(
    #     table_name='cash_flow',
    #     event_type_name='cash_flow_announced',
    #     metrics=[
    #         "cash_from_operating_activity", "cash_from_investing_activity",
    #         "cash_from_financing_activity", "net_cash_flow"
    #     ],
    #     period_type='annual'  # or 'quarterly' if you have quarterly cash flows
    # )

    # backfill_events_for_table(
    #     table_name='financial_ratios',
    #     event_type_name='financial_ratios_announced',
    #     metrics=[
    #         "debtor_days", "inventory_days", "days_payable", "cash_conversion_cycle",
    #         "working_capital_days", "roce_percentage"
    #     ],
    #     period_type='annual'  # or 'quarterly' if you have quarterly ratios
    # )

    # backfill_events_for_table(
    #     table_name='performance_metrics',
    #     event_type_name='performance_metrics_announced',
    #     metrics=[
    #         "metric_type", "period_duration", "value_percentage"
    #     ],
    #     period_type='annual'  # or as appropriate for your data
    # )

cur.close()
conn.close()
print("Data processing completed successfully.")




