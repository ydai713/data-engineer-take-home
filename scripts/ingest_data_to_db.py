import psycopg2
import os


DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "yang"
DB_PASSWORD = ""
SQL_FILES_PATH = "token_data"


def execute_sql_files(kind):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        sql_files = sorted(
            [
                f for f in os.listdir(SQL_FILES_PATH) 
                if f.endswith(".sql") and f.startswith(kind)
            ]
        )

        for file in sql_files:
            file_path = os.path.join(SQL_FILES_PATH, file)
            print(f"Executing {file_path}...")

            with open(file_path, "r") as sql_file:
                sql_content = sql_file.read()

                # Execute the SQL file
                cursor.execute(sql_content)
                connection.commit()
                print(f"Executed {file_path} successfully.")

    except Exception as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    execute_sql_files(kind="log")
    execute_sql_files(kind="txs")
