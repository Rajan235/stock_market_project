from db.db_utils import get_connection
from scripts.strategies.strategy_1 import generate_signal

def run_strategy(company_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT fp.period_name, ar.sales, fr.roce_percentage
        FROM annual_results ar
        JOIN financial_periods fp ON ar.period_id = fp.period_id
        JOIN financial_ratios fr ON ar.company_id = fr.company_id AND ar.period_id = fr.period_id
        WHERE ar.company_id = %s
        ORDER BY fp.period_name
    """, (company_id,))
    rows = cur.fetchall()
    prev_sales = None
    position= False
    print("Period | Sales | ROCE | Sales Growth (%) | Signal | Action")
    for period, sales, roce in rows:
        sales_growth = None
        if prev_sales is not None and prev_sales > 0:
            sales_growth = ((sales - prev_sales) / prev_sales) * 100
        signal = generate_signal(sales_growth, roce)
        action = "Hold"
        if signal == "Buy" and not position:
            action = "Buy"
            position = True
        elif signal == "Sell" and position:
            action = "Sell"
            position = False
        elif position:
            action = "Hold"
        else:
            action = "No Action"
        print(f"{period} | {sales} | {roce} | {sales_growth if sales_growth is not None else 'N/A'} | {signal} | {action}")
        prev_sales = sales
    conn.close()

if __name__ == "__main__":
    # Replace with your actual company_id
    run_strategy(company_id=1)