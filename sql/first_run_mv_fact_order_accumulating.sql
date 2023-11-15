SET time zone 'Asia/Jakarta' ;

create MATERIALIZED VIEW efisheri.mv_fact_order_accumulating as 
select 
concat(o.customer_id,'-',o.order_number) id,
max(to_char(o."date",'yyyymmdd')) order_date, 
max(to_char(i."date",'yyyymmdd'))  inv_date,
max(to_char(p."date",'yyyymmdd')) pay_date,
max(o.customer_id) as customer_id,  
o.order_number, 
i.invoice_number, 
p.payment_number,
--ol.product_id, 
sum(ol.quantity) as total_order_qty,
sum(ol.usd_amount) as total_order_usd,
max(abs(extract (doy from o."date") - extract (doy from i."date"))) as order_to_inv_lag_days,
max(abs(extract (doy from i."date") - extract (doy from p."date"))) as inv_to_pay_lag_days,
case when (i."date" is null and p.date is null ) then 'order'
	 when (i."date" is not null and p."date" is null) then 'on payment'
	 else 'completed'
	end as "step",
now()::timestamp as updated_timestamp
from efisheri.orders o 
left join efisheri.order_lines ol 
on o.order_number = ol.order_number 
left join efisheri.invoices i 
on i.order_number = o.order_number 
left join efisheri.payments p
on p.invoice_number =i.invoice_number
group by o.order_number, i.invoice_number, p.payment_number 