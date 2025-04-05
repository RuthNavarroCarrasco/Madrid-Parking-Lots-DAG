from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from datetime import datetime
import json
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
import pandas as pd
from io import StringIO


def extract_access_url(**kwargs):
    ti = kwargs['ti']
    calles_ser_json_str = ti.xcom_pull(task_ids='get_calles_ser')
    calles_ser_json = json.loads(calles_ser_json_str)

    if not calles_ser_json:
        raise ValueError("No se encontró respuesta en XCom de 'get_calles_ser'")
    
    distribution = calles_ser_json["result"]["items"][0]["distribution"]
    yearly_parking_lots_data = []

    for yearly_parking_data in distribution:
        year = int(yearly_parking_data["title"])
        access_url = yearly_parking_data["accessURL"]
        if 'csv' in access_url and year == 2024:
            yearly_parking_lots_data.append({"Year": year, "Access URL": access_url})

    if not yearly_parking_lots_data:
        raise ValueError("No se encontró distribución CSV")
    
    ti.xcom_push(key="calles_ser_json", value=yearly_parking_lots_data)

    return yearly_parking_lots_data

def normalize_column(col: str) -> str:
    return (col.strip()
               .lower()
               .replace(' ', '_')
               .replace('á', 'a')
               .replace('é', 'e')
               .replace('í', 'i')
               .replace('ó', 'o')
               .replace('ú', 'u')
               .replace('ñ', 'n')
               .replace('/', '_')
               .replace('º', 'o')
               .replace('°', 'o'))

def download_and_store_csv(**kwargs):
    ti = kwargs['ti']
    yearly_parking_lots_data = ti.xcom_pull(task_ids='extract_access_url')
    if not yearly_parking_lots_data:
        raise ValueError("No se encontró información en XCom.")

    pg_hook = PostgresHook(postgres_conn_id='postgres_madrid_parking_lots')
    engine = pg_hook.get_sqlalchemy_engine()
    insertion_date = datetime.utcnow().date()

    for entry in yearly_parking_lots_data:
        year = entry["Year"]
        url = entry["Access URL"]

        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text

        df = pd.read_csv(StringIO(csv_data), sep=';', decimal=',')
        df.columns = [normalize_column(col) for col in df.columns]

        df['year'] = year
        df['insertion_date'] = insertion_date
        print(f"Año {year} insertado con {len(df)} registros. Columnas: {df.columns.tolist()}")
        try:
            df.head(0).to_sql('calles_zona_ser_raw_prueba', engine, if_exists='append', index=False)
        except ValueError:
            pass  # Ya existe

        df.to_sql('calles_zona_ser_raw_prueba', engine, if_exists='append', index=False)


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
        task_id="get_calles_ser",
        method="GET",
        http_conn_id="datos_madrid_http",
        endpoint="egob/catalogo/title/SER-calles.json",
        headers={"Accept": "application/json"},
        log_response=True,
        do_xcom_push=True,
    )

    extract_access_url = PythonOperator(
        task_id='extract_access_url',
        python_callable=extract_access_url,
    )

    download_and_store_csv = PythonOperator(
        task_id='download_and_store_csv',
        python_callable=download_and_store_csv,
    )

    get_calles_ser >> extract_access_url >> download_and_store_csv
