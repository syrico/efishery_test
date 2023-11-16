SET time zone 'Asia/Jakarta' ;
truncate table dwh_efishery.fact_order_accumulating ;

insert into dwh_efishery.fact_order_accumulating
select * from efisheri.v_fact_order_accumulating vf ;
