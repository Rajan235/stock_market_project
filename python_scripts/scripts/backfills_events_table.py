import json
from db.db_utils import get_connection
import psycopg2
from sqlalchemy import create_engine

# ...existing code...
def is_number(val):
    try:
        float(val)
        return True
    except (TypeError, ValueError):
        return False


conn = get_connection()
cursor = conn.cursor()
engine = create_engine("postgresql+psycopg2://", creator=lambda: conn)
# ✅ Step 2: Set Constants// instead of this take metric from actual tables in db like annual_results balanmce_sheet, quarterly_results, cash_flow
# METRICS = ["sales", "net_profit", "eps_rs", "operating_profit", "expenses", "other_income", "interest", "depreciation", "profit_before_tax", "tax", "tax_percentage", "opm_percentage"]
# EVENT_TYPE_NAME = "quarterly_results_announced"  # or annual_results_announced

# cursor.execute("""
#     SELECT column_name 
#     FROM information_schema.columns 
#     WHERE table_name = 'quarterly_results'
#       AND column_name NOT IN ('id', 'company_id', 'period_id', 'created_at', 'updated_at')
# """)
# METRICS = [row[0] for row in cursor.fetchall()]

def get_table_metrics(table_name, exclude=None):
    exclude = exclude or ['id', 'company_id', 'period_id', 'created_at', 'updated_at']
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = %s
    """, (table_name,))
    return [row[0] for row in cursor.fetchall() if row[0] not in exclude]

def backfill_events_for_table(table_name, event_type_name,metrics,period_type='quarterly'):
    
    # ✅ Step 3: Get event_type_id
    cursor.execute("SELECT id FROM event_type WHERE name = %s", (event_type_name,))
    event_type_id = cursor.fetchone()[0]

    select_cols = ", ".join([f"{table_name}.{col}" for col in metrics])

    sql = f"""
    SELECT 
        {table_name}.company_id,
        fp.period_id,
        fp.period_date,
        fp.financial_year,
        fp.quarter_number,
        {select_cols}
    FROM {table_name}
    JOIN financial_periods fp ON {table_name}.period_id = fp.period_id
    WHERE fp.period_type = %s
    ORDER BY {table_name}.company_id, fp.period_date
    """
    cursor.execute(sql, (period_type,))
    results = cursor.fetchall()


    # # ✅ Step 4: Fetch all quarterly results with their financial periods
    # cursor.execute("""
    # SELECT 
    #     qr.company_id,
    #     fp.period_id as period_id,
    #     fp.period_date,
    #     fp.financial_year,
    #     fp.quarter_number,
    #     qr.sales, qr.net_profit, qr.eps_rs, qr.operating_profit, qr.expenses, 
    #     qr.other_income, qr.interest, qr.depreciation, qr.profit_before_tax, 
    #     qr.tax, qr.tax_percentage, qr.opm_percentage
    # FROM quarterly_results qr
    # JOIN financial_periods fp ON qr.period_id = fp.period_id
    # ORDER BY qr.company_id, fp.period_date
    # """)
    # results = cursor.fetchall()
    print(results)

    # ✅ Step 5: Organize into dict for lookup
    from collections import defaultdict

    company_history = defaultdict(list)
    for row in results:
        record = dict(zip(
            ["company_id", "period_id", "period_end", "year", "quarter"] + metrics,
            row
        ))
        company_history[record["company_id"]].append(record)

    # ✅ Step 6: Loop through each company and create events
    for company_id, periods in company_history.items():
        for i in range(1, len(periods)):
            current = periods[i]
            previous = periods[i - 1]

            # Step 6.1: Build metrics dictionaries
            # curr_metrics = {k: float(current[k]) if current[k] is not None else None for k in metrics}
            # prev_metrics = {k: float(previous[k]) if previous[k] is not None else None for k in metrics}
            # ...existing code...
            curr_metrics = {k: float(current[k]) if is_number(current[k]) else current[k] for k in metrics}
            prev_metrics = {k: float(previous[k]) if is_number(previous[k]) else previous[k] for k in metrics}
# ...existing code...
            variance_metrics = {}

            for k in metrics:
                try:
                    if is_number(curr_metrics[k]) and is_number(prev_metrics[k]):
                        variance_metrics[k] = float(curr_metrics[k]) - float(prev_metrics[k])
                    else:
                        variance_metrics[k] = None
                except Exception:
                    variance_metrics[k] = None

            # Step 6.2: For each metric, insert a financial_event
            for metric in metrics:
                # if curr_metrics[metric] is None or prev_metrics[metric] is None:
                #     continue

                previous_value = prev_metrics[metric]
                current_value = curr_metrics[metric]
                if is_number(current_value) and is_number(previous_value):
                    prev_val_to_insert = float(previous_value)
                    curr_val_to_insert = float(current_value)
                    variance = curr_val_to_insert - prev_val_to_insert
                else:
                    prev_val_to_insert = None
                    curr_val_to_insert = None
                    variance = None

                details = {
                    "report_period": f"Q{current['quarter']} {current['year']}",
                    "source": "screener_backfill",
                    "metrics": curr_metrics,
                    "previous_metrics": prev_metrics,
                    "variance_metrics": variance_metrics
                }

                # Step 6.3: Insert into financial_events
                cursor.execute("""
                    INSERT INTO financial_events (
                        company_id, event_type_id, event_timestamp,
                        main_metric, previous_value, current_value, variance, details
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (company_id, event_type_id, event_timestamp, main_metric) DO NOTHING
                """, (
                    company_id,
                    event_type_id,
                    current["period_end"],  # Use financial period end as event date
                    metric,
                    prev_val_to_insert,
                    curr_val_to_insert,
                    variance,
                    json.dumps(details)
                ))

# Example usage for quarterly_results
backfill_events_for_table(
    table_name='quarterly_results',
    event_type_name='quarterly_results_announced',
    metrics=[
        "sales", "net_profit", "eps_rs", "operating_profit", "expenses", "other_income",
        "interest", "depreciation", "profit_before_tax", "tax", "tax_percentage", "opm_percentage"
    ],
    period_type='quarterly'
)
print("✅ Backfilled quarterly results events.")
# Example usage for annual_results
backfill_events_for_table(
    table_name='annual_results',
    event_type_name='annual_results_announced',
    metrics=[
        "sales", "net_profit", "eps_rs", "operating_profit", "expenses", "other_income",
        "interest", "depreciation", "profit_before_tax", "tax", "tax_percentage", "opm_percentage",
        "dividend_payout_percentage", "dividend_amount"
    ],
    period_type='annual'
)

print("✅ Backfilled annual results events.")
backfill_events_for_table(
    table_name='balance_sheet',
    event_type_name='annual_results_announced',
    metrics=[
        "equity_capital", "reserves", "borrowings", "other_liabilities", "total_liabilities",
        "fixed_assets", "cwip", "investments", "other_assets", "total_assets"
    ],
    period_type='annual'  # or 'quarterly' if you have quarterly balance sheets
)

print("✅ Backfilled balance sheet events.")
backfill_events_for_table(
    table_name='cash_flow',
    event_type_name='annual_results_announced',
    metrics=[
        "cash_from_operating_activity", "cash_from_investing_activity",
        "cash_from_financing_activity", "net_cash_flow"
    ],
    period_type='annual'  # or 'quarterly' if you have quarterly cash flows
)
print("✅ Backfilled cash flow events.")
backfill_events_for_table(
    table_name='financial_ratios',
    event_type_name='annual_results_announced',
    metrics=[
        "debtor_days", "inventory_days", "days_payable", "cash_conversion_cycle",
        "working_capital_days", "roce_percentage"
    ],
    period_type='annual'  # or 'quarterly' if you have quarterly ratios
)
print("✅ Backfilled financial ratios events.")
backfill_events_for_table(
    table_name='performance_metrics',
    event_type_name='annual_results_announced',
    metrics=[
        "metric_type", "period_duration", "value_percentage"
    ],
    period_type='annual'  # or as appropriate for your data
)
print("✅ Backfilled performance metrics events.")
# ✅ Step 7: Commit and close
conn.commit()
cursor.close()
conn.close()
print("✅ Backfill complete.")