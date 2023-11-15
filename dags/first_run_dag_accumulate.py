from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from datetime import datetime, timedelta

import pendulum
local_tz = pendulum.timezone("Asia/Jakarta")

default_args = {
    'owner': 'Syrico',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 13, 23, 0, tzinfo=local_tz),
    'email': ['syricoarindamo@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG('First_run_accumate', 
        default_args=default_args, 
        schedule_interval="@once", 
        catchup=False)

t_start = DummyOperator(task_id='start', dag=dag)

t_create_table_dwh = PostgresOperator(task_id = 'create_table_dwh', 
                                    sql = open('/home/syrico/airflow/sql/first_run_create_table_dwh.sql').read(),
                                    postgres_conn_id="postgres_local",
                                    dag=dag)

t_create_view = PostgresOperator(task_id = 'create_view_acumulative', 
                                    sql = open('/home/syrico/airflow/sql/first_run_v_fact_order_accumulating.sql').read(),
                                    postgres_conn_id="postgres_local",
                                    dag=dag)

t_create_mview = PostgresOperator(task_id = 'create_mview_acumulative', 
                                    sql = open('/home/syrico/airflow/sql/first_run_mv_fact_order_accumulating.sql').read(),
                                    postgres_conn_id="postgres_local",
                                    dag=dag)                                    

t_insert_into_tabel_fact = PostgresOperator(task_id = 'insert_into_fact_tbl', 
                                    sql = open('/home/syrico/airflow/sql/first_run_insert_into_table_fact_order.sql').read(),
                                    postgres_conn_id="postgres_local",
                                    dag=dag)                              

t_trigger_refresh_mv = PostgresOperator(task_id = 'refresh_mv', 
                                    sql = 'REFRESH MATERIALIZED VIEW efisheri.mv_fact_order_accumulating;',
                                    postgres_conn_id="postgres_local",
                                    dag=dag)  

t_end = DummyOperator(task_id='end', dag=dag)                                    

t_start >>t_create_table_dwh >> t_create_view  >> t_create_mview >>  t_insert_into_tabel_fact >>t_trigger_refresh_mv >> t_end                       

