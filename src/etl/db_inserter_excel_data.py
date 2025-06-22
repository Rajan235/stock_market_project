def safe_val(val):
    import math
    if val is None:
        return None
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    return val

# ----------------- Annual Results -----------------

#done 
def insert_annual_results(all_sections, conn, company_id):

    annual_df = all_sections["Profit & Loss"]
    derived_df = all_sections.get("Derived", None)
    derived_map = {}
    if derived_df is not None:
        derived_map = dict(zip(derived_df['year'], derived_df.iloc[:, 2]))

    for _, row in annual_df.iterrows():
        year = row['year']
        conn.execute("SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'annual'", (year,))
        period = conn.fetchone()
        if not period:
            continue
        period_id = period[0]
        
        # Parse base metrics safely
        sales = safe_val(row.get("Sales"))
        tax = safe_val(row.get("Tax"))
        pbt = safe_val(row.get("Profit before tax"))
        net_profit = safe_val(row.get("Net profit"))
        depreciation = safe_val(row.get("Depreciation"))
        interest = safe_val(row.get("Interest"))
        other_income = safe_val(row.get("Other Income"))
        dividend = safe_val(row.get("Dividend Amount"))
        equity_shares = safe_val(derived_map.get(year))

        # Calculate expenses from subfields
        expense_fields = [
            "Raw Material Cost", "Change in Inventory", "Power and Fuel",
            "Other Mfr. Exp", "Employee Cost", "Selling and admin", "Other Expenses"
        ]
        missing_expenses = []
        total_expenses = 0
        for expense_name in expense_fields:
            amount = safe_val(row.get(expense_name))
            if amount is not None:
                conn.execute("""
                    INSERT INTO annual_expenses (
                        company_id, period_id, expense_type, amount
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (company_id, period_id, expense_type) DO NOTHING
                """, (company_id, period_id, expense_name, amount))
                total_expenses += amount
            else:
                missing_expenses.append(expense_name)

        if missing_expenses:
            print(f"Year {year} missing expense fields: {missing_expenses}")
        # Operating Profit = Sales - Expenses
        operating_profit = sales - total_expenses if sales is not None else None

        # calculate total expennsis and also fill expensis table 
        opm_percentage = (operating_profit / sales) * 100 if operating_profit and sales else None
        tax_percentage = (tax / pbt) * 100 if tax and pbt else None
        dividend_payout_percentage = (dividend / net_profit) * 100 if dividend and net_profit else None
        eps_rs = net_profit / (equity_shares ) if net_profit and equity_shares else None 
        # Print all values before inserting
        print(f"Inserting annual_results for year {year}:")
        print(f"  sales={safe_val(sales)}, expenses={total_expenses}, operating_profit={operating_profit}, opm_percentage={opm_percentage}")
        print(f"  other_income={safe_val(other_income)}, interest={safe_val(interest)}, depreciation={safe_val(depreciation)}, profit_before_tax={safe_val(pbt)}, tax={safe_val(tax)}, tax_percentage={tax_percentage}")
        print(f"  net_profit={safe_val(net_profit)}, dividend_amount={safe_val(dividend)}, dividend_payout_percentage={dividend_payout_percentage}, eps_rs={eps_rs}")


        # Insert into annual_results
        conn.execute("""
            INSERT INTO annual_results (
                company_id, period_id, sales, expenses, operating_profit, opm_percentage,
                other_income, interest, depreciation, profit_before_tax, tax, tax_percentage,
                net_profit, dividend_amount, dividend_payout_percentage, eps_rs
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING
        """, (
            company_id, period_id,
            sales, total_expenses, operating_profit, opm_percentage,
            other_income, interest, depreciation, pbt, tax, tax_percentage,
            net_profit, dividend, dividend_payout_percentage, eps_rs
        ))


#done       

# ----------------- Cash Flow -----------------
def insert_cash_flow(all_sections, conn, company_id):
    cash_df = all_sections.get("Cash Flow")
    if cash_df is None:
        return

    for _, row in cash_df.iterrows():
        year = row['year']
        conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'annual'",
            (year,)
        )
        period=conn.fetchone()
        if not period:
            continue
        period_id = period[0]

        cash_ops = safe_val(row.get("Cash from Operating Activity"))
        cash_inv = safe_val(row.get("Cash from Investing Activity"))
        cash_fin = safe_val(row.get("Cash from Financing Activity"))
        net_cash = safe_val(row.get("Net Cash Flow"))

        conn.execute("""
            INSERT INTO cash_flow (
                company_id, period_id, cash_from_operating_activity,
                cash_from_investing_activity, cash_from_financing_activity, net_cash_flow
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING
        """, (company_id, period_id, cash_ops, cash_inv, cash_fin, net_cash))

# ----------------- Balance Sheet -----------------

#done 
def insert_balance_sheet(all_sections, conn, company_id):
    bs_df = all_sections.get("Balance Sheet")
    if bs_df is None:
        return

    for _, row in bs_df.iterrows():
        year = row['year']
        conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'annual'",
            (year,)
        )
        period=conn.fetchone()
        if not period:
            continue
        period_id = period[0]

        equity = safe_val(row.get("Equity Share Capital"))
        reserves = safe_val(row.get("Reserves"))
        borrowings = safe_val(row.get("Borrowings"))
        liabilities = safe_val(row.get("Other Liabilities"))
        total_liab = safe_val(row.get("Total"))
        net_block = safe_val(row.get("Net Block"))
        cwip = safe_val(row.get("CWIP"))
        invest = safe_val(row.get("Investments"))
        other_assets = safe_val(row.get("Other Assets"))
        total_assets = safe_val(row.get("Total"))
        receivables = safe_val(row.get("Receivables"))
        inventory = safe_val(row.get("Inventory"))
        cashAndBank = safe_val(row.get("Cash & Bank"))
        Num_of_Equity_Shares = safe_val(row.get("No. of Equity Shares"))
        New_Bonus_Shares = safe_val(row.get("New Bonus Shares"))
        Face_value = safe_val(row.get("Face value"))


        conn.execute("""
            INSERT INTO balance_sheet (
                company_id, period_id, equity_capital, reserves, borrowings,
                other_liabilities, total_liabilities, fixed_assets, cwip,
                investments, other_assets, total_assets
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING
        """, (
            company_id, period_id, equity, reserves, borrowings, liabilities,
            total_liab, net_block, cwip, invest, other_assets, total_assets
        ))

# ----------------- Quarterly Results -----------------
def insert_quarterly_results(all_sections, conn, company_id):
    q_df = all_sections.get("Quarterly")
    if q_df is None:
        return

    for _, row in q_df.iterrows():
        year = row['year']
        conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'quarterly'",
            (year,)
        )
        period=conn.fetchone()
        if not period:
            continue
        period_id = period[0]

        sales = safe_val(row.get("Sales"))
        expenses = safe_val(row.get("Expenses"))
        op = safe_val(row.get("Operating Profit"))
        other_income = safe_val(row.get("Other Income"))
        interest = safe_val(row.get("Interest"))
        dep = safe_val(row.get("Depreciation"))
        pbt = safe_val(row.get("Profit before tax"))
        tax = safe_val(row.get("Tax"))
        np = safe_val(row.get("Net Profit"))
        opm_percentage = (op / sales * 100) if op and sales else None
        tax_percentage = (tax / pbt) * 100 if tax and pbt else None
        #eps=need to be calculated 

        conn.execute("""
            INSERT INTO quarterly_results (
                company_id, period_id, sales, expenses, operating_profit,
                opm_percentage, other_income, interest, depreciation,
                profit_before_tax, tax,tax_percentage, net_profit
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING
        """, (
            company_id, period_id, sales, expenses, op, opm_percentage, other_income,
            interest, dep, pbt, tax,tax_percentage, np
        ))

# ----------------- Financial Ratios -----------------
def insert_financial_ratios(all_sections, conn, company_id):
    # Prepare annual_results and balance_sheet as dicts by period_id
    annual_df = all_sections.get("Profit & Loss")
    bs_df = all_sections.get("Balance Sheet")
    if annual_df is None or bs_df is None:
        return
    
    # Build period_id lookup
    period_ids = {}
    for _, row in annual_df.iterrows():
        year = row['year']
        period = conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'annual'",
            (year,)
        ).fetchone()
        if period:
            period_ids[year] = period[0]

    # Build dicts for quick access
    annual_map = {row['year']: row for _, row in annual_df.iterrows()}
    bs_map = {row['year']: row for _, row in bs_df.iterrows()}

    for year, period_id in period_ids.items():
        annual_result = annual_map.get(year, {})
        balance_sheet = bs_map.get(year, {})

        sales = safe_val(annual_result.get('Sales'))
        receivables = safe_val(balance_sheet.get('Receivables'))
        inventory = safe_val(balance_sheet.get('Inventory'))
        payables = safe_val(balance_sheet.get('Payables'))
        total_assets = safe_val(balance_sheet.get('Total'))
        current_assets = safe_val(balance_sheet.get('Current Assets'))
        current_liabilities = safe_val(balance_sheet.get('Current Liabilities'))
        operating_profit = safe_val(annual_result.get('Operating Profit'))
        other_income = safe_val(annual_result.get('Other Income'))
        net_profit = annual_result.get('net_profit')
        interest = annual_result.get('interest')
        tax = annual_result.get('tax')

        # Debtor Days
        debtor_days = round((receivables / sales) * 365, 2) if receivables and sales else None
        # Inventory Days
        inventory_days = round((inventory / sales) * 365, 2) if inventory and sales else None
        # Days Payable
        days_payable = round((payables / sales) * 365, 2) if payables and sales else None
        # Working Capital Days
        working_capital = (current_assets - current_liabilities) if current_assets and current_liabilities else None
        working_capital_days = round((working_capital / sales) * 365, 2) if working_capital and sales else None
        # Cash Conversion Cycle
        cash_conversion_cycle = (debtor_days or 0) + (inventory_days or 0) - (days_payable or 0) if debtor_days is not None and inventory_days is not None and days_payable is not None else None
        # ROCE
        EBIT = (operating_profit or 0) + (other_income or 0)
        capital_employed = (total_assets - current_liabilities) if total_assets and current_liabilities else None
        roce = round((EBIT / capital_employed) * 100, 2) if EBIT and capital_employed else None

        conn.execute("""
            INSERT INTO financial_ratios (
                company_id, period_id, debtor_days, inventory_days, days_payable,
                cash_conversion_cycle, working_capital_days, roce_percentage
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING
        """, (
            company_id, period_id, debtor_days, inventory_days, days_payable,
            cash_conversion_cycle, working_capital_days, roce
        ))
    
# ----------------- Performance Metrics -----------------
def calculate_cagr(start_value, end_value, years):
    if start_value is None or end_value is None or start_value == 0 or years <= 0:
        return None
    return round(((end_value / start_value) ** (1 / years) - 1) * 100, 2)

def insert_performance_metrics(all_sections, conn, company_id):
    annual_df = all_sections.get("Profit & Loss")
    bs_df = all_sections.get("Balance Sheet")
    if annual_df is None or bs_df is None:
        return

    # Build period_id lookup
    period_ids = []
    for _, row in annual_df.iterrows():
        year = row['year']
        period = conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'annual'",
            (year,)
        ).fetchone()
        if period:
            period_ids.append((year, period[0]))

    # Sort by year for CAGR
    period_ids = sorted(period_ids, key=lambda x: x[0])
    annual_map = {row['year']: row for _, row in annual_df.iterrows()}
    bs_map = {row['year']: row for _, row in bs_df.iterrows()}
    # annual_results: list of dicts, each with 'period_id', 'sales', 'net_profit', 'equity'
    years = 5
    if len(period_ids) >= years + 1:
        start_year, _ = period_ids[-(years+1)]
        end_year, end_period_id = period_ids[-1]
        start = annual_map[start_year]
        end = annual_map[end_year]
        cagr_sales = calculate_cagr(safe_val(start.get('Sales')), safe_val(end.get('Sales')), years)
        cagr_profit = calculate_cagr(safe_val(start.get('Net profit')), safe_val(end.get('Net profit')), years)
        conn.execute("""
            INSERT INTO performance_metrics (company_id, period_id, metric_type, period_duration, value_percentage)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id, metric_type, period_duration) DO NOTHING
        """, (company_id, end_period_id, 'compounded_sales_growth', f'{years}_years', f"{cagr_sales}%"))
        conn.execute("""
            INSERT INTO performance_metrics (company_id, period_id, metric_type, period_duration, value_percentage)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id, metric_type, period_duration) DO NOTHING
        """, (company_id, end_period_id, 'compounded_profit_growth', f'{years}_years', f"{cagr_profit}%"))

    # ROE for last year
    if period_ids:
        last_year, last_period_id = period_ids[-1]
        last = annual_map[last_year]
        last_bs = bs_map.get(last_year, {})
        equity = safe_val(last_bs.get('Equity Share Capital'))
        net_profit = safe_val(last.get('Net profit'))
        if equity and net_profit:
            roe = round((net_profit / equity) * 100, 2)
            conn.execute("""
                INSERT INTO performance_metrics (company_id, period_id, metric_type, period_duration, value_percentage)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (company_id, period_id, metric_type, period_duration) DO NOTHING
            """, (company_id, last_period_id, 'roe', 'last_year', f"{roe}%"))