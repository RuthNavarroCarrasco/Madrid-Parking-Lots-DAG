from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='madrid_parking_lots',
    default_args=default_args,
    schedule_interval='@yearly',
    catchup=False,
    tags=['madrid', 'api'],
) as dag:

    get_calles_ser = HttpOperator(
        task_id="get_ser_calles",
        method="GET",
        http_conn_id="datos_madrid_http",
        endpoint="egob/catalogo/title/SER-calles.json",
        headers={"Accept": "application/json"},
        log_response=True,
    )

    get_calles_ser
