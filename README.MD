# Efishery Technical Test

## 1. Scheduling Airflow

Given table from production as ![Alt text](image.png) that want to be analyzed, so we were created datawarehouse that get data from production daily at 07.00 WIB. We need accumulation of transaction that aggregation by date, customer, order, payment and invoice. 
![Alt text](image-1.png). 

On table fact_order_accumulating we add id as primary key that usefull for upsert the data, because **just only data not completed (no payment and no invoice)from production that we insert into datawarehouse**.
We use Apache Airflow to schedule and Orchastre the pipeline, we provide 2 DAGS, for first run that get all data from production to datawarehouse and another is to get not completed data(no payment, no invoice) daily at 07.00 WIB
![Alt text](image-2.png)
Only data not completed was updated 
![Alt text](image-5.png)

Directory Tree:

├── dags
│   ├── daily_acummulate_dag.py
│   ├── first_run_dag_accumulate.py
├── image-1.png
├── image-2.png
├── image-3.png
├── image-4.png
├── image.png
├── n.ipynb
├── README.MD
├── soal_2
│   └── transform_json.py
└── sql
    ├── daily_upsert_into_table_fact_order.sql
    ├── first_run_create_table_dwh.sql
    ├── first_run_insert_into_table_fact_order.sql
    ├── first_run_mv_fact_order_accumulating.sql
    └── first_run_v_fact_order_accumulating.sql