import os
import psycopg2

from dagster import asset, job
from dagster_dbt import DbtCliResource, load_assets_from_dbt_project

DB_HOST = os.environ["POSTGRES_DB_HOST"]
DB_NAME = os.environ["POSTGRES_DB_NAME"]
DB_USER = os.environ["POSTGRES_DB_USER"]
DB_PASSWORD = os.environ["POSTGRES_DB_PASSWORD"]


def ingest_data(context, kind):
    """Ingest data by executing SQL files."""
    connection = None
    cursor = None
    folder = "dagster_user_code/token_data"
    sql_file_batch_size = 6

    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = connection.cursor()

        sql_files = sorted(
            [f for f in os.listdir(folder) if f.endswith(".sql") and f.startswith(kind)]
        )

        cursor.execute("set search_path to dagster;")
        connection.commit()

        # Process files in batches
        files_to_process = sql_files[:sql_file_batch_size]
        if not files_to_process:
            context.log.info("No SQL files left to process.")
            return "No files processed."

        for file in files_to_process:
            file_path = os.path.join(folder, file)
            context.log.info(f"Executing {file_path}...")

            with open(file_path, "r") as sql_file:
                sql_content = sql_file.read()

                # Execute the SQL file
                cursor.execute(sql_content)
                connection.commit()
                context.log.info(f"Executed {file_path} successfully.")

        return f"Processed {len(files_to_process)} files."

    except Exception as e:
        if connection:
            connection.rollback()
        context.log.error(f"Error during ingestion: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@asset
def create_table(context):
    """create log and transaction tables if not exists"""
    connection = None
    cursor = None
    folder = "dagster_user_code/ddl"

    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = connection.cursor()

        cursor.execute("create schema dagster;")
        connection.commit()

        sql_files = [f for f in os.listdir(folder) if f.endswith(".sql")]


        for file in sql_files:
            file_path = os.path.join(folder, file)
            context.log.info(f"Executing {file_path}...")

            with open(file_path, "r") as sql_file:
                cursor.execute(sql_file.read())
                connection.commit()
                context.log.info(f"Executed {file_path} successfully.")

        return "Table created successfully"

    except Exception as e:
        if connection:
            connection.rollback()
        context.log.error(f"Error during ingestion: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@asset(deps=["create_table"])
def ingest_log_data(context):
    ingest_data(context, kind="log")


@asset(deps=["create_table"])
def ingest_transaction_data(context):
    ingest_data(context, kind="log")


@asset(deps=["ingest_log_data", "ingest_transaction_data"])
def create_dbt_manifest(context, dbt: DbtCliResource):
    """Run dbt commands to create manifest file"""
    dbt.cli(["deps"], context=context).wait()
    dbt.cli(["seed"], context=context).wait()
    return "Manifest created successfully"


@asset(deps=["create_dbt_manifest"])
def run_dbt(context, dbt: DbtCliResource):
    """Run dbt commands to create manifest file"""
    dbt.cli(["run"], context=context).wait()
    return "run successfully"


@asset(deps=["run_dbt"])
def test_dbt(context, dbt: DbtCliResource):
    """Run dbt commands to create manifest file"""
    dbt.cli(["test"], context=context).wait()
    return "test successfully"


@job
def dbt_pipeline():
    create_table()
    ingest_log_data()
    ingest_transaction_data()
    create_dbt_manifest()
    run_dbt()
    test_dbt()


# Explicitly specify the dbt_resource_key
dbt_assets = load_assets_from_dbt_project(
    project_dir="/opt/dagster/app/abs_dbt",
    profiles_dir="/root/.dbt",
    dbt_resource_key="dbt",
)

dbt_resource = DbtCliResource(
    project_dir="/opt/dagster/app/abs_dbt",
    profiles_dir="/root/.dbt",
)
