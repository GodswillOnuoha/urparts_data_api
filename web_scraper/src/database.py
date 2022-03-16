import psycopg2
from config import db_config


def create_datbase():
    conn = psycopg2.connect(
        host=db_config["host"], user=db_config["user"], password=db_config["password"]
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {db_config['database']}")
            cur.execute(f"CREATE DATABASE {db_config['database']}")
    finally:
        conn.close()


def create_tables():
    conn = None
    try:
        with psycopg2.connect(**db_config) as conn:
            print("db connection successful")

            # Cursor
            with conn.cursor() as cur:

                cur.execute("DROP TABLE IF EXISTS machine_parts")
                cur.execute("DROP TABLE IF EXISTS machine_models")

                create_table_script = """
                    CREATE TABLE IF NOT EXISTS machine_models (
                        id              integer PRIMARY KEY,
                        manufacturer    varchar(50) NOT NULL,
                        machine_type    varchar(50) NOT NULL,
                        machine_model   varchar(50) NOT NULL
                    )
                """
                cur.execute(create_table_script)

                create_parts_table_script = """
                    CREATE TABLE IF NOT EXISTS machine_parts (
                        id              SERIAL,
                        model_id        integer REFERENCES machine_models (id),
                        part_number     varchar(50) NOT NULL,
                        category        varchar(100)
                    )
                """
                cur.execute(create_parts_table_script)

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def save_rows(rows_list):
    conn = None
    insert_model_script = "INSERT INTO machine_models (id, manufacturer, machine_type, machine_model) VALUES (%s, %s, %s, %s)"
    try:
        with psycopg2.connect(**db_config) as conn:
            # Cursor
            with conn.cursor() as cur:
                model_id, manufacturer, machine_type, machine_model, parts = rows_list

                # Insert machine model
                cur.execute(
                    insert_model_script,
                    (model_id, manufacturer, machine_type, machine_model),
                )

                # Insert machine parts
                if parts:
                    args_str = ",".join(
                        cur.mogrify("(%s,%s,%s)", part).decode("utf-8")
                        for part in parts
                    )
                    cur.execute(
                        "INSERT INTO machine_parts (model_id, part_number, category) VALUES "
                        + args_str
                    )

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_datbase()
create_tables()
