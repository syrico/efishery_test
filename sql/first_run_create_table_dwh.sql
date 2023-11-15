CREATE TABLE if not exists dwh_efishery.customers (
	id int4 NOT NULL,
	"name" varchar NULL,
	CONSTRAINT customers_pk PRIMARY KEY (id)
);

CREATE TABLE if not exists  dwh_efishery.dimdates (
    dateid varchar PRIMARY KEY,
    calendar_date DATE,
    day_of_week INTEGER,
    day_name VARCHAR(20),
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
);

truncate table dwh_efishery.dimdates cascade ;

INSERT INTO dwh_efishery.dimdates (
dateid,    
calendar_date,
    day_of_week,
    day_name,
    day_of_month,
    day_of_year,
    week_of_year,
    month,
    month_name,
    quarter,
    year,
    is_weekend
)
SELECT
    to_char(d,'yyyymmdd') dateid,
	d::DATE,
    EXTRACT(DOW FROM d)::INTEGER AS day_of_week,
    TO_CHAR(d, 'Day') AS day_name,
    EXTRACT(DAY FROM d)::INTEGER AS day_of_month,
    EXTRACT(DOY FROM d)::INTEGER AS day_of_year,
    EXTRACT(WEEK FROM d)::INTEGER AS week_of_year,
    EXTRACT(MONTH FROM d)::INTEGER AS month,
    TO_CHAR(d, 'Month') AS month_name,
    EXTRACT(QUARTER FROM d)::INTEGER AS quarter,
    EXTRACT(YEAR FROM d)::INTEGER AS year,
    EXTRACT(DOW FROM d)::INTEGER IN (0, 6) AS is_weekend
FROM generate_series('2019-01-01'::DATE, '2023-12-31'::DATE, '1 day'::INTERVAL) d;

CREATE TABLE if not exists dwh_efishery.fact_order_accumulating (
	id text NOT NULL,
	order_date text NULL,
	inv_date text NULL,
	pay_date text NULL,
	customer_id int4 NULL,
	order_number text NULL,
	invoice_number text NULL,
	payment_number text NULL,
	total_order_qty int4 NULL,
	total_order_usd float8 NULL,
	order_to_inv_lag_days int4 NULL,
	inv_to_pay_lag_days int4 NULL,
	step text NULL,
	updated_timestamp timestamp NULL,
	CONSTRAINT fact_order_accumulating_pk PRIMARY KEY (id),
	CONSTRAINT fact_order_accumulating_un UNIQUE (id),
	CONSTRAINT id_customer_fk FOREIGN KEY (customer_id) REFERENCES dwh_efishery.customers(id),
	CONSTRAINT inv_date_fk FOREIGN KEY (inv_date) REFERENCES dwh_efishery.dimdates(dateid),
	CONSTRAINT order_date_fk FOREIGN KEY (order_date) REFERENCES dwh_efishery.dimdates(dateid),
	CONSTRAINT pay_date_fk FOREIGN KEY (pay_date) REFERENCES dwh_efishery.dimdates(dateid)
);