SET time zone 'Asia/Jakarta' ;

insert into dwh_efishery.fact_order_accumulating
select * from efisheri.v_fact_order_accumulating vf
where vf.id in (select mvf.id 
				from efisheri.mv_fact_order_accumulating mvf
				where mvf.step <> 'completed')
on conflict (id)    
do update            
set 
order_date = EXCLUDED.order_date,
inv_date = EXCLUDED.inv_date,
pay_date = EXCLUDED.pay_date,
customer_id = EXCLUDED.customer_id,
order_number = EXCLUDED.order_number,
invoice_number = EXCLUDED.invoice_number,
payment_number = EXCLUDED.payment_number,
total_order_qty = EXCLUDED.total_order_qty,
total_order_usd = EXCLUDED.total_order_usd,
order_to_inv_lag_days = EXCLUDED.order_to_inv_lag_days,
inv_to_pay_lag_days = EXCLUDED.inv_to_pay_lag_days,
step = EXCLUDED.step,
updated_timestamp = EXCLUDED.updated_timestamp;