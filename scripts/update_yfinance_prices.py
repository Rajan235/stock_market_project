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
companies = pd.read_sql("""
    SELECT company_id, company_name, company_code 
    FROM companies 
    WHERE company_code IS NOT NULL
""", conn)

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

# Loop over companies and run updates
for _, row in companies.iterrows():
    company_id = row['company_id']
    symbol = row['company_code'] + ".NS"

    print(f"\n📈 Processing: {row['company_name']} ({symbol})")
    insert_latest_price(symbol, company_id)
    insert_historical_prices(symbol, company_id, start="2010-01-01")
