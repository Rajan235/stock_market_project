-- Companies table to store company information
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    company_code VARCHAR(50),
    sector VARCHAR(100),
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Financial periods/years master table
CREATE TABLE financial_periods (
    period_id SERIAL PRIMARY KEY,
    period_name VARCHAR(20) NOT NULL UNIQUE, -- 'Mar 2025', 'Jun 2024', etc.
    period_type VARCHAR(20) NOT NULL, -- 'quarterly', 'annual'
    period_date DATE NOT NULL,
    financial_year VARCHAR(10) NOT NULL, -- 'FY2025', 'FY2024'
    quarter_number INTEGER, -- 1,2,3,4 for quarterly data, NULL for annual
    calendar_year INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quarterly financial results
CREATE TABLE quarterly_results (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    sales DECIMAL(15,2),
    expenses DECIMAL(15,2),
    operating_profit DECIMAL(15,2),
    opm_percentage DECIMAL(8,2), --/Operating Profit Margin %
    other_income DECIMAL(15,2),
    interest DECIMAL(15,2),
    depreciation DECIMAL(15,2),
    profit_before_tax DECIMAL(15,2),
    tax_percentage DECIMAL(8,2),--tax is ther in csv
    net_profit DECIMAL(15,2),
    eps_rs DECIMAL(10,2), -- Earnings Per Share in Rs not in csv
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id)
);

-- Annual financial results (Year-over-Year)
CREATE TABLE annual_results (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    sales DECIMAL(15,2),
    expenses DECIMAL(15,2),-- not directly
    operating_profit DECIMAL(15,2),--no
    opm_percentage DECIMAL(8,2),--no
    other_income DECIMAL(15,2),
    interest DECIMAL(15,2),
    depreciation DECIMAL(15,2),
    profit_before_tax DECIMAL(15,2),
    tax_percentage DECIMAL(8,2),-- tax is there
    net_profit DECIMAL(15,2),
    eps_rs DECIMAL(10,2),--no
    dividend_payout_percentage DECIMAL(8,2),--divedend amount is there 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id)
);

 
-- Balance sheet data -- things in csv balance sheet which are not in this recievables inventory cash &bank no of equity shares new bonus shares face value
CREATE TABLE balance_sheet (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    equity_capital DECIMAL(15,2),--equity share capital
    reserves DECIMAL(15,2),
    borrowings DECIMAL(15,2),
    other_liabilities DECIMAL(15,2),
    total_liabilities DECIMAL(15,2),
    fixed_assets DECIMAL(15,2),-net block
    cwip DECIMAL(15,2), -- Capital Work in Progress
    investments DECIMAL(15,2),
    other_assets DECIMAL(15,2),
    total_assets DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id)
);

 
-- Cash flow statement csv contain price also
CREATE TABLE cash_flow (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    cash_from_operating_activity DECIMAL(15,2),
    cash_from_investing_activity DECIMAL(15,2),
    cash_from_financing_activity DECIMAL(15,2),
    net_cash_flow DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id)
);
-- csv contain Adjusted Equity Shares in Cr other things to be calculated
-- data is till here every other thing needs to be calculated 

-- Financial ratios
CREATE TABLE financial_ratios (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    debtor_days DECIMAL(8,2),
    inventory_days DECIMAL(8,2),
    days_payable DECIMAL(8,2),
    cash_conversion_cycle DECIMAL(8,2),
    working_capital_days DECIMAL(8,2),
    roce_percentage DECIMAL(8,2), -- Return on Capital Employed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id)
);


-- Shareholding pattern data (works for both quarterly and annual)
CREATE TABLE shareholding_pattern (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    promoters_percentage DECIMAL(8,2),
    fiis_percentage DECIMAL(8,2), -- Foreign Institutional Investors
    diis_percentage DECIMAL(8,2), -- Domestic Institutional Investors
    public_percentage DECIMAL(8,2),
    others_percentage DECIMAL(8,2),
    number_of_shareholders BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id)
);



-- Growth metrics and performance statistics
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id), -- Latest period for which metrics are calculated
    metric_type VARCHAR(50) NOT NULL, -- 'compounded_sales_growth', 'compounded_profit_growth', 'stock_price_cagr', 'roe'
    period_duration VARCHAR(20) NOT NULL, -- '10_years', '5_years', '3_years', 'ttm', 'last_year'
    value_percentage VARCHAR(10), -- Store as string to handle formats like "13%", "-20%"
    calculated_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id, metric_type, period_duration)
);

-- Indexes for better query performance
CREATE INDEX idx_financial_periods_date ON financial_periods(period_date);
CREATE INDEX idx_financial_periods_year ON financial_periods(financial_year);
CREATE INDEX idx_financial_periods_type ON financial_periods(period_type);

CREATE INDEX idx_quarterly_results_company_period ON quarterly_results(company_id, period_id);
CREATE INDEX idx_annual_results_company_period ON annual_results(company_id, period_id);
CREATE INDEX idx_balance_sheet_company_period ON balance_sheet(company_id, period_id);
CREATE INDEX idx_cash_flow_company_period ON cash_flow(company_id, period_id);
CREATE INDEX idx_financial_ratios_company_period ON financial_ratios(company_id, period_id);
CREATE INDEX idx_shareholding_pattern_company_period ON shareholding_pattern(company_id, period_id);
CREATE INDEX idx_performance_metrics_company_period ON performance_metrics(company_id, period_id);

-- Constraints to ensure data integrity
ALTER TABLE quarterly_results ADD CONSTRAINT chk_quarterly_opm_range CHECK (opm_percentage >= -100 AND omp_percentage <= 100);
ALTER TABLE annual_results ADD CONSTRAINT chk_annual_opm_range CHECK (opm_percentage >= -100 AND opm_percentage <= 100);
ALTER TABLE balance_sheet ADD CONSTRAINT chk_balance_sheet_equality CHECK (ABS(total_assets - total_liabilities) < 1); -- Allow minor rounding differences
ALTER TABLE shareholding_pattern ADD CONSTRAINT chk_shareholding_total CHECK 
    (ABS((promoters_percentage + fiis_percentage + diis_percentage + public_percentage + others_percentage) - 100) < 0.1);

-- Ensure quarterly data only links to quarterly periods and annual data to annual periods
ALTER TABLE quarterly_results ADD CONSTRAINT chk_quarterly_period_type 
    CHECK ((SELECT period_type FROM financial_periods WHERE period_id = quarterly_results.period_id) = 'quarterly');
ALTER TABLE annual_results ADD CONSTRAINT chk_annual_period_type 
    CHECK ((SELECT period_type FROM financial_periods WHERE period_id = annual_results.period_id) = 'annual');

-- Comments for better documentation
COMMENT ON TABLE companies IS 'Master table for company information';
COMMENT ON TABLE financial_periods IS 'Master table for all financial periods/years';
COMMENT ON TABLE quarterly_results IS 'Quarterly financial performance data';
COMMENT ON TABLE annual_results IS 'Annual financial performance data with year-over-year metrics';
COMMENT ON TABLE balance_sheet IS 'Balance sheet data showing assets, liabilities and equity';
COMMENT ON TABLE cash_flow IS 'Cash flow statement data';
COMMENT ON TABLE financial_ratios IS 'Various financial ratios and efficiency metrics';
COMMENT ON TABLE shareholding_pattern IS 'Shareholding pattern data (quarterly and annual)';
COMMENT ON TABLE performance_metrics IS 'Growth metrics and performance statistics';

-- Sample trigger for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to main tables
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_financial_periods_updated_at BEFORE UPDATE ON financial_periods FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_quarterly_results_updated_at BEFORE UPDATE ON quarterly_results FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_annual_results_updated_at BEFORE UPDATE ON annual_results FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_balance_sheet_updated_at BEFORE UPDATE ON balance_sheet FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cash_flow_updated_at BEFORE UPDATE ON cash_flow FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_financial_ratios_updated_at BEFORE UPDATE ON financial_ratios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_shareholding_pattern_updated_at BEFORE UPDATE ON shareholding_pattern FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_performance_metrics_updated_at BEFORE UPDATE ON performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample data for financial_periods table (you would populate this with your actual periods) need to have ttm as well
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

-- Sample queries to demonstrate the power of this schema:

-- Query 1: Get all metrics for a specific financial year
/*
SELECT 
    c.company_name,
    fp.financial_year,
    fp.period_name,
    ar.sales as annual_sales,
    ar.net_profit as annual_profit,
    bs.total_assets,
    cf.net_cash_flow,
    fr.roce_percentage,
    sp.promoters_percentage
FROM companies c
JOIN financial_periods fp ON fp.financial_year = 'FY2025'
LEFT JOIN annual_results ar ON c.company_id = ar.company_id AND fp.period_id = ar.period_id
LEFT JOIN balance_sheet bs ON c.company_id = bs.company_id AND fp.period_id = bs.period_id  
LEFT JOIN cash_flow cf ON c.company_id = cf.company_id AND fp.period_id = cf.period_id
LEFT JOIN financial_ratios fr ON c.company_id = fr.company_id AND fp.period_id = fr.period_id
LEFT JOIN shareholding_pattern sp ON c.company_id = sp.company_id AND fp.period_id = sp.period_id
WHERE fp.period_type = 'annual'
ORDER BY c.company_name;
*/

-- Query 2: Get quarterly progression for a specific year
/*
SELECT 
    c.company_name,
    fp.period_name,
    fp.quarter_number,
    qr.sales,
    qr.operating_profit,
    qr.net_profit,
    qr.eps_rs
FROM companies c
JOIN financial_periods fp ON fp.financial_year = 'FY2025' AND fp.period_type = 'quarterly'
JOIN quarterly_results qr ON c.company_id = qr.company_id AND fp.period_id = qr.period_id
ORDER BY c.company_name, fp.quarter_number;
*/

-- Query 3: Year-over-year comparison
/*
SELECT 
    c.company_name,
    fp1.financial_year as current_year,
    ar1.sales as current_sales,
    fp2.financial_year as previous_year,
    ar2.sales as previous_sales,
    ROUND(((ar1.sales - ar2.sales) / ar2.sales * 100), 2) as sales_growth_percentage
FROM companies c
JOIN financial_periods fp1 ON fp1.financial_year = 'FY2025' AND fp1.period_type = 'annual'
JOIN financial_periods fp2 ON fp2.financial_year = 'FY2024' AND fp2.period_type = 'annual'
JOIN annual_results ar1 ON c.company_id = ar1.company_id AND fp1.period_id = ar1.period_id
JOIN annual_results ar2 ON c.company_id = ar2.company_id AND fp2.period_id = ar2.period_id
ORDER BY sales_growth_percentage DESC;
*/


-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.annual_expenses
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    expense_type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    amount numeric(15, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT annual_expenses_pkey PRIMARY KEY (id),
    CONSTRAINT annual_expenses_company_id_period_id_expense_type_key UNIQUE (company_id, period_id, expense_type)
);

CREATE TABLE IF NOT EXISTS public.annual_results
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    sales numeric(15, 2),
    expenses numeric(15, 2),
    operating_profit numeric(15, 2),
    opm_percentage numeric(8, 2),
    other_income numeric(15, 2),
    interest numeric(15, 2),
    depreciation numeric(15, 2),
    profit_before_tax numeric(15, 2),
    tax_percentage numeric(8, 2),
    net_profit numeric(15, 2),
    eps_rs numeric(10, 2),
    dividend_payout_percentage numeric(8, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tax numeric(15, 2),
    dividend_amount numeric(15, 2),
    CONSTRAINT annual_results_pkey PRIMARY KEY (id),
    CONSTRAINT annual_results_company_id_period_id_key UNIQUE (company_id, period_id)
);

COMMENT ON TABLE public.annual_results
    IS 'Annual financial performance data with year-over-year metrics';

CREATE TABLE IF NOT EXISTS public.balance_sheet
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    equity_capital numeric(15, 2),
    reserves numeric(15, 2),
    borrowings numeric(15, 2),
    other_liabilities numeric(15, 2),
    total_liabilities numeric(15, 2),
    fixed_assets numeric(15, 2),
    cwip numeric(15, 2),
    investments numeric(15, 2),
    other_assets numeric(15, 2),
    total_assets numeric(15, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT balance_sheet_pkey PRIMARY KEY (id),
    CONSTRAINT balance_sheet_company_id_period_id_key UNIQUE (company_id, period_id)
);

COMMENT ON TABLE public.balance_sheet
    IS 'Balance sheet data showing assets, liabilities and equity';

CREATE TABLE IF NOT EXISTS public.cash_flow
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    cash_from_operating_activity numeric(15, 2),
    cash_from_investing_activity numeric(15, 2),
    cash_from_financing_activity numeric(15, 2),
    net_cash_flow numeric(15, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cash_flow_pkey PRIMARY KEY (id),
    CONSTRAINT cash_flow_company_id_period_id_key UNIQUE (company_id, period_id)
);

COMMENT ON TABLE public.cash_flow
    IS 'Cash flow statement data';

CREATE TABLE IF NOT EXISTS public.companies
(
    company_id serial NOT NULL,
    company_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    company_code character varying(50) COLLATE pg_catalog."default",
    sector character varying(100) COLLATE pg_catalog."default",
    industry character varying(100) COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT companies_pkey PRIMARY KEY (company_id),
    CONSTRAINT unique_company_code UNIQUE (company_code),
    CONSTRAINT unique_company_name UNIQUE (company_name)
);

COMMENT ON TABLE public.companies
    IS 'Master table for company information';

-- CREATE TABLE IF NOT EXISTS public.event_type
-- (
--     id serial NOT NULL,
--     name character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     CONSTRAINT event_type_pkey PRIMARY KEY (id),
--     CONSTRAINT event_type_name_key UNIQUE (name)
-- );

CREATE TABLE IF NOT EXISTS public.event_type (
    id serial PRIMARY KEY,
    name varchar(50) UNIQUE NOT NULL,          -- e.g., 'quarterly_results_announced'
    description text,                          -- e.g., 'Quarterly earnings released'
    category varchar(50),                      -- e.g., 'fundamental', 'technical', etc.
    expression text,                           -- Optional logic (e.g., 'revenue_growth > 15')
    active boolean DEFAULT true                -- For enabling/disabling event types
);

CREATE TABLE IF NOT EXISTS public.financial_events (
    id serial PRIMARY KEY,

    company_id integer NOT NULL,              -- FK to your company table
    event_type_id integer NOT NULL REFERENCES event_type(id), -- Type of event
    event_timestamp timestamp NOT NULL,       -- When this event happened

    main_metric varchar(50) NOT NULL,         -- e.g., 'revenue', 'eps', 'net_profit'
    previous_value numeric,                   -- e.g., revenue in previous Q4
    current_value numeric,                    -- e.g., revenue in current Q4
    variance numeric,                         -- current - previous

    details jsonb NOT NULL,                   -- Full snapshot (all metrics, metadata)

    CONSTRAINT unique_event_per_metric UNIQUE (
        company_id, event_type_id, event_timestamp, main_metric
    )
);

-- CREATE TABLE IF NOT EXISTS public.financial_events
-- (
--     id serial NOT NULL,
--     company_id integer,
--     event_type_id integer,
--     event_timestamp timestamp without time zone NOT NULL,
--     details jsonb NOT NULL,
--     CONSTRAINT financial_events_pkey PRIMARY KEY (id),
--     CONSTRAINT financial_events_company_id_event_type_id_event_timestamp_key UNIQUE (company_id, event_type_id, event_timestamp)
-- );

CREATE TABLE IF NOT EXISTS public.financial_periods
(
    period_id serial NOT NULL,
    period_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    period_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    period_date date NOT NULL,
    financial_year character varying(10) COLLATE pg_catalog."default" NOT NULL,
    quarter_number integer,
    calendar_year integer NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT financial_periods_pkey PRIMARY KEY (period_id),
    CONSTRAINT unique_period_type_name UNIQUE (period_name, period_type)
);

COMMENT ON TABLE public.financial_periods
    IS 'Master table for all financial periods/years';

CREATE TABLE IF NOT EXISTS public.financial_ratios
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    debtor_days numeric(8, 2),
    inventory_days numeric(8, 2),
    days_payable numeric(8, 2),
    cash_conversion_cycle numeric(8, 2),
    working_capital_days numeric(8, 2),
    roce_percentage numeric(8, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT financial_ratios_pkey PRIMARY KEY (id),
    CONSTRAINT financial_ratios_company_id_period_id_key UNIQUE (company_id, period_id)
);

COMMENT ON TABLE public.financial_ratios
    IS 'Various financial ratios and efficiency metrics';

CREATE TABLE IF NOT EXISTS public.historical_prices
(
    id serial NOT NULL,
    company_id integer,
    date date NOT NULL,
    open_price numeric(10, 2),
    high_price numeric(10, 2),
    low_price numeric(10, 2),
    close_price numeric(10, 2),
    adj_close_price numeric(10, 2),
    volume bigint,
    dividends numeric(10, 2),
    stock_splits numeric(10, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT historical_prices_pkey PRIMARY KEY (id),
    CONSTRAINT historical_prices_company_id_date_key UNIQUE (company_id, date)
);

CREATE TABLE IF NOT EXISTS public.latest_prices
(
    id serial NOT NULL,
    company_id integer,
    date date DEFAULT CURRENT_DATE,
    close_price numeric(10, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT latest_prices_pkey PRIMARY KEY (id),
    CONSTRAINT latest_prices_company_id_date_key UNIQUE (company_id, date)
);

CREATE TABLE IF NOT EXISTS public.performance_metrics
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    metric_type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    period_duration character varying(20) COLLATE pg_catalog."default" NOT NULL,
    value_percentage character varying(10) COLLATE pg_catalog."default",
    calculated_date date DEFAULT CURRENT_DATE,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT performance_metrics_pkey PRIMARY KEY (id),
    CONSTRAINT performance_metrics_company_id_period_id_metric_type_period_key UNIQUE (company_id, period_id, metric_type, period_duration)
);

COMMENT ON TABLE public.performance_metrics
    IS 'Growth metrics and performance statistics';

CREATE TABLE IF NOT EXISTS public.quarterly_results
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    sales numeric(15, 2),
    expenses numeric(15, 2),
    operating_profit numeric(15, 2),
    opm_percentage numeric(8, 2),
    other_income numeric(15, 2),
    interest numeric(15, 2),
    depreciation numeric(15, 2),
    profit_before_tax numeric(15, 2),
    tax_percentage numeric(8, 2),
    net_profit numeric(15, 2),
    eps_rs numeric(10, 2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tax numeric(15, 2),
    CONSTRAINT quarterly_results_pkey PRIMARY KEY (id),
    CONSTRAINT quarterly_results_company_id_period_id_key UNIQUE (company_id, period_id)
);

COMMENT ON TABLE public.quarterly_results
    IS 'Quarterly financial performance data';

CREATE TABLE IF NOT EXISTS public.shareholding_pattern
(
    id serial NOT NULL,
    company_id integer NOT NULL,
    period_id integer NOT NULL,
    promoters_percentage numeric(8, 2),
    fiis_percentage numeric(8, 2),
    diis_percentage numeric(8, 2),
    public_percentage numeric(8, 2),
    others_percentage numeric(8, 2),
    number_of_shareholders bigint,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT shareholding_pattern_pkey PRIMARY KEY (id),
    CONSTRAINT shareholding_pattern_company_id_period_id_key UNIQUE (company_id, period_id)
);

COMMENT ON TABLE public.shareholding_pattern
    IS 'Shareholding pattern data (quarterly and annual)';

ALTER TABLE IF EXISTS public.annual_expenses
    ADD CONSTRAINT annual_expenses_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.annual_expenses
    ADD CONSTRAINT annual_expenses_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.annual_results
    ADD CONSTRAINT annual_results_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.annual_results
    ADD CONSTRAINT annual_results_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.balance_sheet
    ADD CONSTRAINT balance_sheet_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.balance_sheet
    ADD CONSTRAINT balance_sheet_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.cash_flow
    ADD CONSTRAINT cash_flow_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.cash_flow
    ADD CONSTRAINT cash_flow_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.financial_events
    ADD CONSTRAINT financial_events_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.financial_events
    ADD CONSTRAINT financial_events_event_type_id_fkey FOREIGN KEY (event_type_id)
    REFERENCES public.event_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.financial_ratios
    ADD CONSTRAINT financial_ratios_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.financial_ratios
    ADD CONSTRAINT financial_ratios_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.historical_prices
    ADD CONSTRAINT historical_prices_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.latest_prices
    ADD CONSTRAINT latest_prices_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.performance_metrics
    ADD CONSTRAINT performance_metrics_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.performance_metrics
    ADD CONSTRAINT performance_metrics_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.quarterly_results
    ADD CONSTRAINT quarterly_results_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.quarterly_results
    ADD CONSTRAINT quarterly_results_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.shareholding_pattern
    ADD CONSTRAINT shareholding_pattern_company_id_fkey FOREIGN KEY (company_id)
    REFERENCES public.companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.shareholding_pattern
    ADD CONSTRAINT shareholding_pattern_period_id_fkey FOREIGN KEY (period_id)
    REFERENCES public.financial_periods (period_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;

TRUNCATE TABLE 
    annual_expenses,
    annual_results,
    balance_sheet,
    cash_flow,
    companies,
    event_type,
    financial_periods,
    financial_ratios,
    historical_prices,
    latest_prices,
    performance_metrics,
    quarterly_results,
    shareholding_pattern,
    yfinance_cash_flow,
    yfinance_company_info,
    yfinance_balance_sheet,
    yfinance_income_statement,
    financial_events
RESTART IDENTITY CASCADE;

CREATE TABLE yfinance_income_statement (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    period_type VARCHAR(20) NOT NULL, -- 'annual', 'quarterly', 'ttm'
    field_name VARCHAR(100) NOT NULL,
    value NUMERIC(20, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id, period_type, field_name)
);

CREATE TABLE yfinance_balance_sheet (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    period_type VARCHAR(20) NOT NULL, -- 'annual', 'quarterly', 'ttm'
    field_name VARCHAR(100) NOT NULL,
    value NUMERIC(20, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id, period_type, field_name)
);
CREATE TABLE yfinance_cash_flow (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    period_type VARCHAR(20) NOT NULL, -- 'annual', 'quarterly', 'ttm'
    field_name VARCHAR(100) NOT NULL,
    value NUMERIC(20, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, period_id, period_type, field_name)
);

CREATE TABLE yfinance_company_info (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    long_name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap BIGINT,
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id)
);

ALTER TABLE annual_results DROP CONSTRAINT IF EXISTS chk_annual_opm_range;

CREATE TABLE IF NOT EXISTS yfinance_cash_flow (
    company_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    free_cash_flow NUMERIC,
    repurchase_of_capital_stock NUMERIC,
    repayment_of_debt NUMERIC,
    issuance_of_debt NUMERIC,
    issuance_of_capital_stock NUMERIC,
    capital_expenditure NUMERIC,
    end_cash_position NUMERIC,
    beginning_cash_position NUMERIC,
    effect_of_exchange_rate_changes NUMERIC,
    changes_in_cash NUMERIC,
    financing_cash_flow NUMERIC,
    net_other_financing_charges NUMERIC,
    interest_paid_cff NUMERIC,
    cash_dividends_paid NUMERIC,
    common_stock_dividend_paid NUMERIC,
    net_common_stock_issuance NUMERIC,
    common_stock_payments NUMERIC,
    common_stock_issuance NUMERIC,
    net_issuance_payments_of_debt NUMERIC,
    net_short_term_debt_issuance NUMERIC,
    short_term_debt_issuance NUMERIC,
    net_long_term_debt_issuance NUMERIC,
    long_term_debt_payments NUMERIC,
    long_term_debt_issuance NUMERIC,
    investing_cash_flow NUMERIC,
    net_other_investing_changes NUMERIC,
    interest_received_cfi NUMERIC,
    dividends_received_cfi NUMERIC,
    net_investment_purchase_and_sale NUMERIC,
    sale_of_investment NUMERIC,
    purchase_of_investment NUMERIC,
    net_business_purchase_and_sale NUMERIC,
    sale_of_business NUMERIC,
    purchase_of_business NUMERIC,
    net_ppe_purchase_and_sale NUMERIC,
    sale_of_ppe NUMERIC,
    purchase_of_ppe NUMERIC,
    operating_cash_flow NUMERIC,
    taxes_refund_paid NUMERIC,
    change_in_working_capital NUMERIC,
    change_in_other_current_liabilities NUMERIC,
    change_in_other_current_assets NUMERIC,
    change_in_payable NUMERIC,
    change_in_inventory NUMERIC,
    change_in_receivables NUMERIC,
    other_non_cash_items NUMERIC,
    stock_based_compensation NUMERIC,
    provisionand_write_offof_assets NUMERIC,
    depreciation_and_amortization NUMERIC,
    amortization_cash_flow NUMERIC,
    depreciation NUMERIC,
    gain_loss_on_investment_securities NUMERIC,
    net_foreign_currency_exchange_gain_loss NUMERIC,
    gain_loss_on_sale_of_ppe NUMERIC,
    gain_loss_on_sale_of_business NUMERIC,
    net_income_from_continuing_operations NUMERIC,
    PRIMARY KEY (company_id, period_id, period_type)
);

CREATE TABLE yfinance_balance_sheet (
    company_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    cash_and_cash_equivalents NUMERIC,
    short_term_investments NUMERIC,
    net_receivables NUMERIC,
    inventory NUMERIC,
    other_current_assets NUMERIC,
    total_current_assets NUMERIC,
    property_plant_equipment NUMERIC,
    goodwill NUMERIC,
    intangible_assets NUMERIC,
    other_assets NUMERIC,
    total_assets NUMERIC,
    accounts_payable NUMERIC,
    short_term_debt NUMERIC,
    other_current_liabilities NUMERIC,
    total_current_liabilities NUMERIC,
    long_term_debt NUMERIC,
    other_liabilities NUMERIC,
    total_liabilities NUMERIC,
    common_stock NUMERIC,
    retained_earnings NUMERIC,
    treasury_stock NUMERIC,
    other_equity NUMERIC,
    total_equity NUMERIC,
    total_liabilities_and_equity NUMERIC,
    PRIMARY KEY (company_id, period_id, period_type)
);

CREATE TABLE yfinance_income_statement (
    company_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    total_revenue NUMERIC,
    cost_of_revenue NUMERIC,
    gross_profit NUMERIC,
    research_and_development NUMERIC,
    selling_general_and_admin NUMERIC,
    operating_income NUMERIC,
    total_other_income_expense_net NUMERIC,
    ebit NUMERIC,
    interest_expense NUMERIC,
    income_before_tax NUMERIC,
    income_tax_expense NUMERIC,
    net_income NUMERIC,
    net_income_to_common NUMERIC,
    basic_eps NUMERIC,
    diluted_eps NUMERIC,
    weighted_average_shares_outstanding NUMERIC,
    weighted_average_shares_diluted NUMERIC,
    PRIMARY KEY (company_id, period_id, period_type)
);

CREATE TABLE IF NOT EXISTS yfinance_income_statement (
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    period_type VARCHAR(20) NOT NULL, -- 'annual', 'quarterly', 'ttm'
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id, period_id, period_type)
);
CREATE TABLE IF NOT EXISTS yfinance_balance_sheet (
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    period_type VARCHAR(20) NOT NULL, -- 'annual', 'quarterly', 'ttm'
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id, period_id, period_type)
);
CREATE TABLE IF NOT EXISTS yfinance_cash_flow (
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    period_id INTEGER NOT NULL REFERENCES financial_periods(period_id),
    period_type VARCHAR(20) NOT NULL, -- 'annual', 'quarterly', 'ttm'
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id, period_id, period_type)
);

INSERT INTO event_type (name, description, category)
VALUES 
  ('quarterly_results_announced', 'Quarterly financials declared', 'fundamental'),
  ('annual_results_announced', 'Annual financials declared', 'fundamental');
