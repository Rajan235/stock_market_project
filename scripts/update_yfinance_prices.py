import yfinance as yf
import pandas as pd
from db.db_utils import get_connection
from sqlalchemy import create_engine, text
from datetime import datetime

##need to cange for all companies in db

# PostgreSQL connection
conn = get_connection()
engine = create_engine("postgresql+psycopg2://", creator=lambda: conn)

# Load companies
# companies = pd.read_sql("""
#     SELECT company_id, company_name, company_code 
#     FROM companies 
#     WHERE company_code IS NOT NULL
# """, conn)
companies = [{"company_code": "ADANIPORTS", "screener_id": "6594426", "excel_file": "Adani Ports.xlsx"}]

# Helper function to insert latest price
def insert_latest_price(symbol, company_id):
    try:
        df = yf.download(symbol, period="1d", interval="1d", progress=False,auto_adjust=True)
        if df.empty:
            print(f"⚠️ No latest price data for {symbol}")
            return

        # latest_price = df['Close'].iloc[-1]
        latest_price = float(df['Close'].iloc[-1])

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO latest_prices (company_id, date, close_price)
                VALUES (:company_id, CURRENT_DATE, :price)
                ON CONFLICT (company_id, date)
                DO UPDATE SET close_price = EXCLUDED.close_price, updated_at = CURRENT_TIMESTAMP
            """), {"company_id": company_id, "price": latest_price})

        print(f"✅ Latest price updated for {symbol}: ₹{latest_price:.2f}")

    except Exception as e:
        print(f"❌ Error updating latest price for {symbol}: {e}")


# Helper function to insert historical prices
def insert_historical_prices(symbol, company_id, start="2010-01-01"):
    try:
        df = yf.download(symbol, start=start, interval="1d", progress=False, auto_adjust=False)
        if df.empty:
            print(f"⚠️ No historical data for {symbol}")
            return

        # Reset index to make 'Date' a column
       # df.reset_index(inplace=True)

        with engine.begin() as conn:
            for _, row in df.iterrows():
                try:
                    date_value = pd.to_datetime(row.name).date()  # Ensure it's a date object

                    # Prepare record
                    record = {
                        "company_id": company_id,
                        "date": date_value,
                        # "open": float(row.get("Open", 0.0)),
                        # "high": float(row.get("High", 0.0)),
                        # "low": float(row.get("Low", 0.0)),
                        # "close": float(row.get("Close", 0.0)),
                        # "adj_close": float(row.get("Adj Close", row.get("Close", 0.0))),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        #"adj_close": float(row["Adj Close"]) if "Adj Close" in df.columns and pd.notnull(row["Adj Close"]) else float(row["Close"]),
                        "adj_close": float(row.get("Adj Close", row.get("Close", 0.0))),
                        "volume": int(row.get("Volume", 0)),
                        "dividends": float(row.get("Dividends", 0.0)) if "Dividends" in row else 0.0,
                        "splits": float(row.get("Stock Splits", 0.0)) if "Stock Splits" in row else 0.0
                    }

                    conn.execute(text("""
                        INSERT INTO historical_prices (
                            company_id, date, open_price, high_price, low_price,
                            close_price, adj_close_price, volume, dividends, stock_splits
                        )
                        VALUES (
                            :company_id, :date, :open, :high, :low,
                            :close, :adj_close, :volume, :dividends, :splits
                        )
                        ON CONFLICT (company_id, date)
                        DO UPDATE SET
                            open_price = EXCLUDED.open_price,
                            high_price = EXCLUDED.high_price,
                            low_price = EXCLUDED.low_price,
                            close_price = EXCLUDED.close_price,
                            adj_close_price = EXCLUDED.adj_close_price,
                            volume = EXCLUDED.volume,
                            dividends = EXCLUDED.dividends,
                            stock_splits = EXCLUDED.stock_splits,
                            created_at = CURRENT_TIMESTAMP
                    """), record)
                    #print(f"Inserting: {record}")


                except Exception as row_err:
                    print(f"⚠️ Error on row for {symbol} at {row['Date']}: {row_err}")

        print(f"✅ Historical prices inserted for {symbol} ({len(df)} days)")

    except Exception as e:
        print(f"❌ Error inserting historical prices for {symbol}: {e}")
# def financials_yfinance(companies):
#     for row in companies:
#         symbol = row['company_code'] + ".NS"
#         print("=" * 80)
#         print(f"\n📈 Processing: {row['company_code']} ({symbol})")

#         try:
#             ticker = yf.Ticker(symbol)

#             # ✅ Basic Company Info
#             info = ticker.info
#             print("\n🔍 Basic Info:")
#             print({k: info.get(k) for k in ['longName', 'sector', 'industry', 'marketCap', 'website']})

#             # ✅ Annual Income Statement
#             print("\n📊 Annual Income Statement:")
#             print(ticker.financials.to_string())

#             # ✅ Quarterly Income Statement
#             print("\n📊 Quarterly Income Statement:")
#             print(ticker.quarterly_financials.to_string())

#             # ✅ TTM Income Statement (if available)
#             ttm_income = getattr(ticker, "ttm_income_stmt", None)
#             if isinstance(ttm_income, pd.DataFrame):
#                 print("\n📊 TTM Income Statement:")
#                 print(ttm_income.to_string())

#             # ✅ Annual Balance Sheet
#             print("\n📄 Annual Balance Sheet:")
#             print(ticker.balance_sheet.to_string())

#             # ✅ Quarterly Balance Sheet
#             print("\n📄 Quarterly Balance Sheet:")
#             print(ticker.quarterly_balance_sheet.to_string())

#             # ✅ TTM Balance Sheet (if available)
#             ttm_balance = getattr(ticker, "ttm_balance_sheet", None)
#             if isinstance(ttm_balance, pd.DataFrame):
#                 print("\n📄 TTM Balance Sheet:")
#                 print(ttm_balance.to_string())

#             # ✅ Annual Cash Flow Statement
#             print("\n💵 Annual Cash Flow:")
#             print(ticker.cashflow.to_string())

#             # ✅ Quarterly Cash Flow Statement
#             print("\n💵 Quarterly Cash Flow:")
#             print(ticker.quarterly_cashflow.to_string())

#             # ✅ TTM Cash Flow (if available)
#             ttm_cashflow = getattr(ticker, "ttm_cashflow", None)
#             if isinstance(ttm_cashflow, pd.DataFrame):
#                 print("\n💵 TTM Cash Flow:")
#                 print(ttm_cashflow.to_string())

#         except Exception as e:
#             print(f"❌ Error fetching financials for {symbol}: {e}")

# Example input list of companies

def insert_yfinance_statement(df, company_id, period_type, table_name):
    if df is None or df.empty:
        return
    # df: index = field_name, columns = period_end (datetime or string)
    with engine.begin() as conn:
        for field_name, row in df.iterrows():
            for period_end, value in row.items():
                if pd.isnull(value):
                    continue
                # Try to find period_id from financial_periods
                period_end_date = pd.to_datetime(period_end).date()
                period_id = conn.execute(
                    text("SELECT period_id FROM financial_periods WHERE period_name = :period_name"),
                    {"period_name": str(period_end_date)}
                ).scalar()
                if not period_id:
                    # Optionally, insert new period if not found
                    continue
                conn.execute(
                    text(f"""
                        INSERT INTO {table_name} (company_id, period_id, period_type, field_name, value)
                        VALUES (:company_id, :period_id, :period_type, :field_name, :value)
                        ON CONFLICT (company_id, period_id, period_type, field_name)
                        DO UPDATE SET value = EXCLUDED.value, created_at = CURRENT_TIMESTAMP
                    """),
                    {
                        "company_id": company_id,
                        "period_id": period_id,
                        "period_type": period_type,
                        "field_name": field_name,
                        "value": value
                    }
                )

def insert_yfinance_company_info(info, company_id):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO yfinance_company_info (company_id, long_name, sector, industry, market_cap, website)
                VALUES (:company_id, :long_name, :sector, :industry, :market_cap, :website)
                ON CONFLICT (company_id)
                DO UPDATE SET long_name = EXCLUDED.long_name, sector = EXCLUDED.sector,
                              industry = EXCLUDED.industry, market_cap = EXCLUDED.market_cap,
                              website = EXCLUDED.website, created_at = CURRENT_TIMESTAMP
            """),
            {
                "company_id": company_id,
                "long_name": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap"),
                "website": info.get("website"),
            }
        )

def financials_yfinance(companies):
    for row in companies:
        symbol = row['company_code'] + ".NS"
        print("=" * 80)
        print(f"\n📈 Processing: {row['company_code']} ({symbol})")
        try:
            ticker = yf.Ticker(symbol)
            # Lookup company_id from your companies table
            company_id = engine.execute(
                text("SELECT company_id FROM companies WHERE company_code = :code"),
                {"code": row['company_code']}
            ).scalar()
            if not company_id:
                print(f"❌ Company {row['company_code']} not found in DB.")
                continue

            # Basic Info
            info = ticker.info
            insert_yfinance_company_info(info, company_id)

            # Income Statements
            insert_yfinance_statement(ticker.financials, company_id, "annual", "yfinance_income_statement")
            insert_yfinance_statement(ticker.quarterly_financials, company_id, "quarterly", "yfinance_income_statement")
            ttm_income = getattr(ticker, "ttm_income_stmt", None)
            if isinstance(ttm_income, pd.DataFrame):
                insert_yfinance_statement(ttm_income, company_id, "ttm", "yfinance_income_statement")

            # Balance Sheets
            insert_yfinance_statement(ticker.balance_sheet, company_id, "annual", "yfinance_balance_sheet")
            #insert_yfinance_statement(ticker.quarterly_balance_sheet, company_id, "quarterly", "yfinance_balance_sheet")
            ttm_balance = getattr(ticker, "ttm_balance_sheet", None)
            if isinstance(ttm_balance, pd.DataFrame):
                insert_yfinance_statement(ttm_balance, company_id, "ttm", "yfinance_balance_sheet")

            # Cash Flows
            insert_yfinance_statement(ticker.cashflow, company_id, "annual", "yfinance_cash_flow")
            insert_yfinance_statement(ticker.quarterly_cashflow, company_id, "quarterly", "yfinance_cash_flow")
            ttm_cashflow = getattr(ticker, "ttm_cashflow", None)
            if isinstance(ttm_cashflow, pd.DataFrame):
                insert_yfinance_statement(ttm_cashflow, company_id, "ttm", "yfinance_cash_flow")

            print(f"✅ yfinance data inserted for {symbol}")

        except Exception as e:
            print(f"❌ Error fetching financials for {symbol}: {e}")

financials_yfinance(companies)
# Run the function
