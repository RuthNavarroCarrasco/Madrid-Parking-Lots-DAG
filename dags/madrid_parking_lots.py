from airflow.decorators import dag
from airflow.providers.http.operators.http import HttpOperator
from datetime import datetime

@dag(
    dag_id='madrid_parking_lots',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@yearly',
    catchup=False,
    tags=['example'],
)
def madrid_parking_lots_dag():
    get_calles_ser = HttpOperator(
        task_id="get_op",
        method="GET",
        http_conn_id=None,
        endpoint="get",
        data={"title": "SER-calles", "fmt": "json"},
        headers={},
    )

    get_calles_ser

madrid_parking_lots_dag()
