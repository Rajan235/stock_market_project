# Stock Market Project

This project helps you build and populate a financial database using data from Screener and Yahoo Finance for the top Nifty 50 companies.

---

## **Step 1: Prepare Reference Data**

**Before running any scripts, make sure you have inserted the required periods and event types:**

```sql
INSERT INTO financial_periods (period_name, period_type, period_date, financial_year, quarter_number, calendar_year) VALUES
-- Annual periods
('Mar 2014', 'annual', '2014-03-31', 'FY2014', NULL, 2014),
('Mar 2015', 'annual', '2015-03-31', 'FY2015', NULL, 2015),
('Mar 2016', 'annual', '2016-03-31', 'FY2016', NULL, 2016),
('Mar 2017', 'annual', '2017-03-31', 'FY2017', NULL, 2017),
('Mar 2018', 'annual', '2018-03-31', 'FY2018', NULL, 2018),
('Mar 2019', 'annual', '2019-03-31', 'FY2019', NULL, 2019),
('Mar 2020', 'annual', '2020-03-31', 'FY2020', NULL, 2020),
('Mar 2021', 'annual', '2021-03-31', 'FY2021', NULL, 2021),
('Mar 2022', 'annual', '2022-03-31', 'FY2022', NULL, 2022),
('Mar 2023', 'annual', '2023-03-31', 'FY2023', NULL, 2023),
('Mar 2024', 'annual', '2024-03-31', 'FY2024', NULL, 2024),
('Mar 2025', 'annual', '2025-03-31', 'FY2025', NULL, 2025),

-- Quarterly periods
('Mar 2022', 'quarterly', '2022-03-31', 'FY2022', 4, 2022),
('Jun 2022', 'quarterly', '2022-06-30', 'FY2023', 1, 2022),
('Sep 2022', 'quarterly', '2022-09-30', 'FY2023', 2, 2022),
('Dec 2022', 'quarterly', '2022-12-31', 'FY2023', 3, 2022),
('Mar 2023', 'quarterly', '2023-03-31', 'FY2023', 4, 2023),
('Jun 2023', 'quarterly', '2023-06-30', 'FY2024', 1, 2023),
('Sep 2023', 'quarterly', '2023-09-30', 'FY2024', 2, 2023),
('Dec 2023', 'quarterly', '2023-12-31', 'FY2024', 3, 2023),
('Mar 2024', 'quarterly', '2024-03-31', 'FY2024', 4, 2024),
('Jun 2024', 'quarterly', '2024-06-30', 'FY2025', 1, 2024),
('Sep 2024', 'quarterly', '2024-09-30', 'FY2025', 2, 2024),
('Dec 2024', 'quarterly', '2024-12-31', 'FY2025', 3, 2024),
('Mar 2025', 'quarterly', '2025-03-31', 'FY2025', 4, 2025);

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
