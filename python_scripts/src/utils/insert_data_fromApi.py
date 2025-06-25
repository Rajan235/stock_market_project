import psycopg2
from db.db_utils import get_connection

def insert_company(conn, company_name, company_code):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO companies (company_name, company_code)
            VALUES (%s, %s)
            ON CONFLICT (company_name) DO NOTHING
            RETURNING company_id;
        """, (company_name, company_code))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            cur.execute("SELECT company_id FROM companies WHERE company_name=%s;", (company_name,))
            return cur.fetchone()[0]

def insert_financial_period(conn, period_name, period_type, period_date, financial_year, quarter_number, calendar_year):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO financial_periods
            (period_name, period_type, period_date, financial_year, quarter_number, calendar_year)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (period_name) DO NOTHING
            RETURNING period_id;
        """, (period_name, period_type, period_date, financial_year, quarter_number, calendar_year))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            cur.execute("SELECT period_id FROM financial_periods WHERE period_name=%s;", (period_name,))
            return cur.fetchone()[0]

def get_period_id(conn, period_name, period_type):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT period_id FROM financial_periods
            WHERE period_name=%s AND period_type=%s
        """, (period_name, period_type))
        result = cur.fetchone()
        return result[0] if result else None

def insert_quarterly_results(conn, company_id, period_id, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO quarterly_results (
                company_id, period_id, sales, expenses, operating_profit, opm_percentage,
                other_income, interest, depreciation, profit_before_tax, tax_percentage,
                net_profit, eps_rs
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING;
        """, (
            company_id, period_id,
            data.get("Sales"),
            data.get("Expenses"),
            data.get("Operating Profit"),
            data.get("OPM %"),
            data.get("Other Income"),
            data.get("Interest"),
            data.get("Depreciation"),
            data.get("Profit before tax"),
            data.get("Tax %"),
            data.get("Net Profit"),
            data.get("EPS in Rs")
        ))
    conn.commit()

def insert_annual_results(conn, company_id, period_id, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO annual_results (
                company_id, period_id, sales, expenses, operating_profit, opm_percentage,
                other_income, interest, depreciation, profit_before_tax, tax_percentage,
                net_profit, eps_rs, dividend_payout_percentage
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING;
        """, (
            company_id, period_id,
            data.get("Sales"),
            data.get("Expenses"),
            data.get("Operating Profit"),
            data.get("OPM %"),
            data.get("Other Income"),
            data.get("Interest"),
            data.get("Depreciation"),
            data.get("Profit before tax"),
            data.get("Tax %"),
            data.get("Net Profit"),
            data.get("EPS in Rs"),
            data.get("Dividend Payout %")
        ))
    conn.commit()
def insert_balance_sheet(conn, company_id, period_id, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO balance_sheet (
                company_id, period_id, equity_capital, reserves, borrowings, other_liabilities,
                total_liabilities, fixed_assets, cwip, investments, other_assets, total_assets
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING;
        """, (
            company_id, period_id,
            data.get("Equity Capital"),
            data.get("Reserves"),
            data.get("Borrowings"),
            data.get("Other Liabilities"),
            data.get("Total Liabilities"),
            data.get("Fixed Assets"),
            data.get("CWIP"),
            data.get("Investments"),
            data.get("Other Assets"),
            data.get("Total Assets")
        ))
    conn.commit()

def insert_cash_flow(conn, company_id, period_id, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO cash_flow (
                company_id, period_id, cash_from_operating_activity, cash_from_investing_activity,
                cash_from_financing_activity, net_cash_flow
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING;
        """, (
            company_id, period_id,
            data.get("Cash from Operating Activity"),
            data.get("Cash from Investing Activity"),
            data.get("Cash from Financing Activity"),
            data.get("Net Cash Flow")
        ))
    conn.commit()

def insert_financial_ratios(conn, company_id, period_id, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO financial_ratios (
                company_id, period_id, debtor_days, inventory_days, days_payable,
                cash_conversion_cycle, working_capital_days, roce_percentage
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING;
        """, (
            company_id, period_id,
            data.get("Debtor Days"),
            data.get("Inventory Days"),
            data.get("Days Payable"),
            data.get("Cash Conversion Cycle"),
            data.get("Working Capital Days"),
            data.get("ROCE %")
        ))
    conn.commit()

def insert_shareholding_pattern(conn, company_id, period_id, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO shareholding_pattern (
                company_id, period_id, promoters_percentage, fiis_percentage, diis_percentage,
                public_percentage, others_percentage, number_of_shareholders
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING;
        """, (
            company_id, period_id,
            data.get("Promoters"),
            data.get("FIIs"),
            data.get("DIIs"),
            data.get("Public"),
            data.get("Others"),
            data.get("No. of Shareholders")
        ))
    conn.commit()

def insert_performance_metrics(conn, company_id, period_id, stats):
    for metric_type, periods in stats.items():
        for period_label, value in periods.items():
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO performance_metrics (
                        company_id, period_id, metric_type, period_duration, value_percentage
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (company_id, period_id, metric_type, period_duration) DO NOTHING;
                """, (
                    company_id, period_id, metric_type.replace(" ", "_").lower(), period_label.replace(" ", "").replace(":", "").lower(), value
                ))
    conn.commit()