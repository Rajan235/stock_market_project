# Stock Market Project

This project helps you build and populate a financial database using data from Screener and Yahoo Finance for the top Nifty 50 companies.

---

## **Step 1: Prepare Reference Data**

**Before running any scripts, make sure you have inserted the required periods and event types:**

```sql
-- Annual periods
INSERT INTO financial_periods (period_name, period_type, period_date, financial_year, quarter_number, calendar_year) VALUES
('Mar 2014', 'annual', '2014-03-31', 'FY2014', NULL, 2014),
...
('Mar 2025', 'annual', '2025-03-31', 'FY2025', NULL, 2025),

-- Quarterly periods
('Mar 2022', 'quarterly', '2022-03-31', 'FY2022', 4, 2022),
...
('Mar 2025', 'quarterly', '2025-03-31', 'FY2025', 4, 2025);

-- TTM period (latest)
INSERT INTO financial_periods (period_name, period_type, period_date, financial_year, quarter_number, calendar_year)
VALUES ('Mar 2025', 'ttm', '2025-03-31', 'FY2025', NULL, 2025)
ON CONFLICT (period_name, period_type) DO NOTHING;

-- Event types
INSERT INTO event_type (name, description, category)
VALUES
  ('quarterly_results_announced', 'Quarterly financials declared', 'fundamental'),
  ('annual_results_announced', 'Annual financials declared', 'fundamental');
```

---

## **Step 2: Download Excel Files from Screener**

1. **Run the Java Selenium Utility:**
   ```sh
   cd java_fetcher/selenium_download
   mvn exec:java -Dexec.mainClass="App"
   ```
   This will download all company Excel files into the `data/downloads` directory.

---

## **Step 3: Prepare Company Mapping**

- The `company_mapping` file contains all Nifty 50 companies and their corresponding Excel file paths.
- **Cross-check** that all downloaded Excel files are present and mapped correctly.

---

## **Step 4: Populate the Database**

1. **Go to your project root:**

   ```sh
   cd finance_project
   ```

2. **Run the main ETL script:**
   ```sh
   python -m src.main
   ```
   This will:
   - Parse all Excel files.
   - Populate the following tables:
     - `annual_results`
     - `balance_sheet`
     - `cash_flow`
     - `quarterly_results`
     - `financial_ratios`
     - `performance_metrics`

---

## **Step 5: Update Yahoo Finance Data**

- To fetch and update Yahoo Finance prices, run:
  ```sh
  python -m scripts.update_yfinance_prices
  ```

---

## **Step 6: Backfill Events Table**

- To backfill the `financial_events` table, run:
  ```sh
  python -m scripts.backfills_events_table
  ```

---

## **Database Schema**

- The full schema is in `db/schema.sql`.
- An ERD diagram is also provided as a PNG.
- You can restore a backup of the database from `data/finance_project_db.backup` if needed.

---

## **Tips**

- Always insert the reference data (`financial_periods`, `event_type`) before running the ETL scripts.
- If you want to recreate the database, use the schema file or the backup provided.

---

## **Troubleshooting**

- If you encounter missing data, check that all Excel files are present and mapped.
- Ensure all required periods and event types are inserted before running scripts.
- For any schema changes, update both the schema and your ETL scripts accordingly.

---

## **Contact**

For questions or issues, refer to the schema or open an issue in this repository.
