from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys 
import os 
sys.path.append('/opt/airflow/scripts') 
from extract_helpers import extract_csv, extract_sql_db, load_to_dw

default_args = {
    'owner': 'Paulo',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='banvic_etl', # Identificador no Airflow
    default_args=default_args,
    start_date=datetime(2025, 9, 1),
    schedule_interval='35 4 * * *',   # 04:35 diário
    catchup=False, # Sem catchup
    tags=['banvic'],
) as dag:

    t_extract_csv = PythonOperator(
        task_id='extract_csv',
        python_callable=extract_csv,
        provide_context=True
    )

    t_extract_sql = PythonOperator(
        task_id='extract_sql_db',
        python_callable=extract_sql_db,
        provide_context=True
    )

    t_load = PythonOperator(
        task_id='load_to_dw',
        python_callable=load_to_dw,
        provide_context=True,
        trigger_rule='all_success'
    )

    [t_extract_csv, t_extract_sql] >> t_load