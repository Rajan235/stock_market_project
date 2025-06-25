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


