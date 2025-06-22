def safe_val(val):
    import math
    if val is None:
        return None
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    return val



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
            safe_val(sales), safe_val(total_expenses), safe_val(operating_profit), safe_val(opm_percentage),
            safe_val(other_income), safe_val(interest), safe_val(depreciation), safe_val(pbt), safe_val(tax), safe_val(tax_percentage),
            safe_val(net_profit), safe_val(dividend), safe_val(dividend_payout_percentage), safe_val(eps_rs)
        ))


#done       
def insert_cash_flow(all_sections, conn, company_id):
    cash_df = all_sections.get("Cash Flow")
    if cash_df is None:
        return

    for _, row in cash_df.iterrows():
        year = row['year']
        period = conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'annual'",
            (year,)
        ).fetchone()
        if not period:
            continue
        period_id = period[0]

        cash_ops = row.get("Cash from Operating Activity")
        cash_inv = row.get("Cash from Investing Activity")
        cash_fin = row.get("Cash from Financing Activity")
        net_cash = row.get("Net Cash Flow")

        conn.execute("""
            INSERT INTO cash_flow (
                company_id, period_id, cash_from_operating_activity,
                cash_from_investing_activity, cash_from_financing_activity, net_cash_flow
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, period_id) DO NOTHING
        """, (company_id, period_id, cash_ops, cash_inv, cash_fin, net_cash))

#done 
def insert_balance_sheet(all_sections, conn, company_id):
    bs_df = all_sections.get("Balance Sheet")
    if bs_df is None:
        return

    for _, row in bs_df.iterrows():
        year = row['year']
        period = conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'annual'",
            (year,)
        ).fetchone()
        if not period:
            continue
        period_id = period[0]

        equity = row.get("Equity Share Capital")
        reserves = row.get("Reserves")
        borrowings = row.get("Borrowings")
        liabilities = row.get("Other Liabilities")
        total_liab = row.get("Total Liabilities")
        net_block = row.get("Net Block")
        cwip = row.get("CWIP")
        invest = row.get("Investments")
        other_assets = row.get("Other Assets")
        total_assets = row.get("Total Assets")
        # Optional fields, might not be present in all rows but get them may use in future 
        receivables = row.get("Receivables")
        inventory = row.get("Inventory")
        cashAndBank =row.get("Cash & Bank")
        Num_of_Equity_Shares =row.get("No. of Equity Shares")
        New_Bonus_Shares = row.get("New Bonus Shares")
        Face_value = row.get("Face value")


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


def insert_quarterly_results(all_sections, conn, company_id):
    q_df = all_sections.get("Quarterly")
    if q_df is None:
        return

    for _, row in q_df.iterrows():
        year = row['year']
        period = conn.execute(
            "SELECT period_id FROM financial_periods WHERE period_date = %s AND period_type = 'quarterly'",
            (year,)
        ).fetchone()
        if not period:
            continue
        period_id = period[0]

        sales = row.get("Sales")
        expenses = row.get("Expenses")
        op = row.get("Operating Profit")
        other_income = row.get("Other Income")
        interest = row.get("Interest")
        dep = row.get("Depreciation")
        pbt = row.get("Profit before tax")
        tax = row.get("Tax")
        np = row.get("Net Profit")
        opm_percentage= op / sales * 100 if op and sales else None
        #eps=need to be calculated 


        tax_percentage = (tax / pbt) * 100, 2 if tax and pbt else None

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
