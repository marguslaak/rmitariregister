import os
from io import BytesIO
from typing import List
from zipfile import ZipFile

from django.conf import settings
import duckdb
import requests


def pull_files() -> None:
    """
    Tõmbame avaandmed äriregistrist

    Ettevõtte osanikud: https://avaandmed.ariregister.rik.ee/sites/default/files/avaandmed/ettevotja_rekvisiidid__osanikud.json.zip
    Ettevõtte varad: https://avaandmed.ariregister.rik.ee/sites/default/files/4.2023_aruannete_elemendid_kuni_31032024.zip
    Varade: https://avaandmed.ariregister.rik.ee/sites/default/files/1.aruannete_yldandmed_kuni_31032024.zip

    Seotud piletid: VP-45

    :return: Mitte midagi, salvestab fail(id) kataloogi `rawdata`
    """
    rawdata_dir_path: str = f'{settings.BASE_DIR}/rawdata'

    if not os.path.exists(rawdata_dir_path):
        os.mkdir(rawdata_dir_path)

    rawdata_urls: List[str] = [
        'https://avaandmed.ariregister.rik.ee/sites/default/files/avaandmed/ettevotja_rekvisiidid__osanikud.json.zip',
        'https://avaandmed.ariregister.rik.ee/sites/default/files/4.2023_aruannete_elemendid_kuni_31032024.zip',
        'https://avaandmed.ariregister.rik.ee/sites/default/files/1.aruannete_yldandmed_kuni_31032024.zip'
    ]

    for url in rawdata_urls:  # NB! Downloaded urls are all zip files
        response: requests.Response = requests.get(url)

        response.raise_for_status()

        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(rawdata_dir_path)


def process_companies():
    """
    Loome ettevõtete tabeli
    :return:
    """
    duckdb.query("COPY (SELECT ariregistri_kood, nimi FROM 'rawdata/ettevotja_rekvisiidid__osanikud.json') TO 'companies.parquet' (FORMAT PARQUET)")

def process_company_ownerships():
    """
    Loome omandisuhete tabeli
    :return:
    """

    duckdb.query("COPY (SELECT cast(b.ariregistri_kood as string) as company_number, b.nimi as company_name, unnest.osanikud.isiku_tyyp as owner_type, unnest.osanikud.nimi_arinimi as owner_name, unnest.osanikud.isikukood_registrikood as owner_number, unnest.osanikud.osaluse_protsent as ownership_size  FROM 'rawdata/ettevotja_rekvisiidid__osanikud.json' b, unnest(b.osanikud)) TO 'company_ownerships.parquet' (FORMAT PARQUET)")


def process_company_assets():
    """
    Loome ettevõtte varade tabeli
    :return:
    """
    duckdb.query("COPY (SELECT B.registrikood, A.vaartus FROM \"rawdata/4.2022_aruannete_elemendid_kuni_31032024.csv\" "
                 "A join \"rawdata/1.aruannete_yldandmed_kuni_31032024.csv\" B ON A.report_id = B.report_id "
                 "WHERE A.tabel = 'Bilanss' and A.elemendi_label = 'Varad') TO 'company_assets.parquet' (FORMAT PARQUET)")


def process_company_with_assets():
    """
    Loome ettevõtte ja tema varade tabeli
    :return:
    """
    duckdb.query("COPY (select e.ariregistri_kood, e.nimi, a.assets as varad from \"ettevotted.parquet\" e join \"assets.parquet\" a on e.ariregistri_kood = a.registrikood) TO 'company_with_assets.parquet' (FORMAT PARQUET)")


def process_company_with_assets():
    """
    Loome ettevõtte ja tema varade tabeli
    :return:
    """
    os.environ['PGPASSWORD'] = 'root'
    os.environ['PGUSER'] = 'root'
    os.environ['PGHOST'] = 'localhost'
    os.environ['PGDATABASE'] = 'ariregister'

    connection = duckdb.connect()
    connection.query("ATTACH '' AS postgres_db (TYPE POSTGRES)")

    # Ettevõtted, mis tuleb kustutada
    del_df = connection.query("SELECT P.* FROM postgres_db.data_storage_company P FULL OUTER JOIN 'company_with_assets.parquet' A "
                              "ON A.ariregistri_kood = P.ariregistri_kood AND A.nimi = P.nimi AND A.varad = P.varad "
                              "WHERE A.ariregistri_kood IS NULL AND A.nimi IS NULL AND A.varad IS NULL").df()

    add_df = connection.query("SELECT A.* FROM 'company_with_assets.parquet' A FULL OUTER JOIN postgres_db.data_storage_company P "
                              "ON A.ariregistri_kood = P.ariregistri_kood AND A.nimi = P.nimi AND A.varad = P.varad  "
                              "WHERE P.ariregistri_kood IS NULL AND P.nimi IS NULL AND P.varad IS NULL").df()

    connection.query("DELETE FROM postgres_db.data_storage_company USING del_df "
                     "WHERE data_storage_company.ariregistri_kood = del_df.ariregistri_kood "
                     "AND data_storage_company.nimi = del_df.nimi "
                     "AND data_storage_company.varad = del_df.varad ")

    connection.query("INSERT INTO postgres_db.data_storage_company(ariregistri_kood, nimi, varad) "
                     "SELECT add_df.ariregistri_kood, add_df.nimi, add_df.varad FROM add_df")


