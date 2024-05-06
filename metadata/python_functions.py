from io import StringIO
from typing import List, Dict, Optional

from duckdb import DuckDBPyConnection, connect
from pandas import DataFrame

from metadata.models import StepExecution


def _retrieve_parquet_cols(
        con: DuckDBPyConnection,
        parquet_filename: str
) -> List[str]:
    """
    Given a DuckDB connection object and a parquet filename, return a list of column names for the mentioned parquet file.

    :param con: DuckDB connection object
    :param parquet_filename: Parquet filename
    :return: List of column names for the mentioned parquet file
    """
    # Describe returns per column:
    # column_name column_type null key default extra
    return [
        col[0]
        for col in con.execute(
            f"DESCRIBE SELECT * FROM '{parquet_filename}'"
        ).fetchall()
    ]


def _map_column_values_with_fk(con: DuckDBPyConnection,
                               parquet_columns: List[str],
                               mapping: Dict[str, str],
                               parquet_filename: str) -> str:
    # We need to join the parquet file with the foreign key table and save new parquet
    """
    Example:
    foreign_table.field=local_column
    :param con:
    :param parquet_columns:
    :param mapping:
    :param parquet_filename:
    :return:
    """
    new_parqet_name = parquet_filename
    parquet_col_fields = parquet_columns.copy()
    print("The fields", parquet_col_fields)
    pidx = 1

    # iterate over fk mappings and build a joined query one-by-one
    for key, value in mapping.items():
        if "CAST INTO" in key:
            key_cast = '::'+key.split("CAST INTO")[1].strip()
            key = key.split("CAST INTO")[0].strip()
        else:
            key_cast = ''

        foreign_table, foreign_field = value.rsplit(".", 1)
        remote_field_name, local_field_name = foreign_field.split("=")

        print("Remove",key)
        parquet_col_fields.remove(key)
        parquet_col_fields.append("id as " + local_field_name)

        q = f"""
        SELECT {", ".join(parquet_col_fields)} FROM '{new_parqet_name}' P 
        JOIN {foreign_table} ON {remote_field_name} = P.{key}{key_cast}
        """

        print(q)
        parquet_col_fields.remove("id as " + local_field_name)
        parquet_col_fields.append(local_field_name)

        new_parqet_name = parquet_filename.rsplit(".", 1)[0] + f"_{pidx}.parquet"
        con.query(q).write_parquet(new_parqet_name) # noqa

        pidx += 1

    return new_parqet_name


def sync_with_postgres(
        table_name: str,
        parquet_filename: str,
        mapping: Dict[str, str] = None,
        add_only: bool = False,
        step_execution: Optional[StepExecution] = None
) -> None:
    con = connect()
    con.query(f"ATTACH '' AS postgres_db (TYPE POSTGRES)")

    # Describe returns per column:
    # column_name column_type null key default extra
    parquet_cols: List[str] = _retrieve_parquet_cols(con=con, parquet_filename=parquet_filename)

    if mapping:
        # We need to  make value to foreign key values
        parquet_filename = _map_column_values_with_fk(con, parquet_cols, mapping, parquet_filename)

        parquet_cols = _retrieve_parquet_cols(con=con, parquet_filename=parquet_filename)

    def build_metadata(*dataframes: DataFrame) -> str:
        metadata: str = ''

        for dataframe in dataframes:
            buffer = StringIO()

            dataframe.info(buf=buffer)

            metadata += f'{getattr(dataframe, "_name", "")}\n' + '\n'.join(buffer.getvalue().split('\n')[1:]) + '\n'

        return metadata

    def build_del_select_query() -> str:
        return f"""
        SELECT 
            P.* 
        FROM {table_name} P 
        FULL OUTER JOIN '{parquet_filename}' A
        ON {' AND '.join(f' P.{col} IS NOT DISTINCT FROM A.{col}' for col in parquet_cols)}
        WHERE {' AND '.join(f' A.{col} IS NULL' for col in parquet_cols)}
        """

    def build_add_select_query() -> str:
        return f"""
        SELECT 
            A.* 
        FROM '{parquet_filename}' A
        FULL OUTER JOIN {table_name} P 
        ON {' AND '.join(f'P.{col} IS NOT DISTINCT FROM A.{col}' for col in parquet_cols)}
        WHERE {' AND '.join(f'P.{col} IS NULL' for col in parquet_cols)}
        """

    def build_del_query(df_name: str) -> str:
        return f"""
        DELETE FROM {table_name} P using {df_name} AS A
        WHERE {' AND '.join(f'P.{col} IS NOT DISTINCT FROM A.{col}' for col in parquet_cols)}
        """

    def build_add_query(df_name: str) -> str:
        return f"""
        INSERT INTO {table_name}({', '.join(parquet_cols)})
        SELECT {', '.join(f'{df_name}.{col}' for col in parquet_cols)} FROM {df_name}
        """

    # We need to compare the data in the parquet file with the data in the postgres table
    del_df = None
    if not add_only:
        query = build_del_select_query()
        #print("Del query select:", query)
        del_df = con.query(query).df() # noqa

    query = build_add_select_query()
    #print("Add query select:", query)
    add_df = con.query(query).df() # noqa

    # First we delete the rows that are not present in the parquet file
    if not add_only:
        query = build_del_query(df_name='del_df')
        #print("Del query:", query)
        con.query(query)

    query = build_add_query(df_name='add_df')
    #print("Add query:", query)
    con.query(query)

    if step_execution:
        setattr(add_df, '_name', 'Adding rows from parquet')
        if isinstance(del_df, DataFrame):
            setattr(del_df, '_name', 'Remove rows from db')

        step_execution.metadata = build_metadata(*[df for df in [add_df, del_df] if isinstance(df, DataFrame)])
        step_execution.save(update_fields=['metadata'])

    con.commit()
