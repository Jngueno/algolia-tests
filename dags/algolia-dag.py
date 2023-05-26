import sys
sys.path.append('')

import pendulum
import boto3
import psycopg2

import pandas as pd

from botocore import UNSIGNED
from botocore.config import Config
from sqlalchemy import create_engine

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from datetime import datetime, timedelta
from airflow.hooks.base_hook import BaseHook

from common.transform import alg_transform



@dag(
    schedule='@daily',
    start_date=pendulum.datetime(2019, 4, 1, tz='UTC'),
    end_date=pendulum.datetime(2019, 4, 7, tz='UTC'),
    catchup=True,
    tags=["etl"],
)
def algolia_test():
    @task()
    def download_csv_file():
        context = get_current_context()
        exec_date = context.get('execution_date').to_date_string()
        s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
        src_bucket = 'alg-data-public'
        src_client = s3.Bucket(src_bucket)
        object_key = f'{exec_date}.csv'
        src_client.download_file(object_key, f'/tmp/{object_key}')

    @task()
    def transform():
        context = get_current_context()
        exec_date = context.get('execution_date').to_date_string()
        data = pd.read_csv(f'/tmp/{exec_date}.csv')
        new_df = alg_transform(data)
        new_df.to_csv(f'/tmp/{exec_date}_new.csv', sep=',', index=False)
    
    @task()
    def load():
        postgres_conn = BaseHook.get_connection("postgresql_conn")
        context = get_current_context()
        exec_date = context.get('execution_date').to_date_string()
        df = pd.read_csv(f'/tmp/{exec_date}_new.csv')
        engine = create_engine(f'postgresql://{postgres_conn.login}:{postgres_conn.password}@{postgres_conn.host}:{postgres_conn.port}/{postgres_conn.schema}')
        df.to_sql('algolia_tests', engine, if_exists='append')
    download_csv_file() >> transform() >> load()

algolia_test()