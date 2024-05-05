from io import BytesIO
from typing import Tuple
from zipfile import ZipFile

import requests
from django.db import connection as django_connection
from duckdb import DuckDBPyConnection
from duckdb.typing import VARCHAR


def add_duckdb_functions(connection: DuckDBPyConnection) -> None:
    connection.query("ATTACH '' AS postgres_db (TYPE POSTGRES)")
    connection.create_function(name='pull_file', function=pull_file, parameters=[VARCHAR, VARCHAR], return_type='NULL')
    connection.create_function(name='grant_privileges', function=grant_privileges, return_type='NULL')


def pull_file(url: str, filename: str) -> None:
    response: requests.Response = requests.get(url)

    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as zip_file:
        if filename not in zip_file.namelist():
            raise RuntimeError('File not present in zip file!')

        zip_file.extract(filename)


def grant_privileges(*tables: Tuple[str]) -> None:
    with django_connection.cursor() as cursor:
        for table in tables:
            cursor.execute(f'GRANT SELECT ON public.{table} TO web_anon')  # NB! Currently, hard-coded user
