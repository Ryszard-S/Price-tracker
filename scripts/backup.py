import subprocess
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

# psql connection String
connectionString = "postgres://postgres:postgres@localhost:5432/postgres"

R_DB_MAIN = os.environ.get('R_DB_MAIN')
R_DB_USER = os.environ.get('R_DB_USER')
R_DB_PASSWORD = os.environ.get('R_DB_PASSWORD')
R_DB_HOST = os.environ.get('R_DB_HOST')
R_DB_PORT = os.environ.get('R_DB_PORT')
R_DB = os.environ.get('R_DB')

L_DB_MAIN = os.environ.get('L_DB_MAIN')
L_DB_USER = os.environ.get('L_DB_USER')
L_DB_PASSWORD = os.environ.get('L_DB_PASSWORD')
L_DB_HOST = os.environ.get('L_DB_HOST')
L_DB_PORT = os.environ.get('L_DB_PORT')
L_DB = os.environ.get('L_DB')


def backup_postgres_db(host, database_name, port, user, password, dest_file):
    """
    Backup postgres db to a file.
    """

    try:
        process = subprocess.run(
            ["pwsh", "-Command", 'pg_dump',
             '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database_name),
             '-Fc',
             '-f', dest_file,
             '-v'],
            stdout=subprocess.PIPE
        )
        # output = process.communicate()[0]
        if int(process.returncode) != 0:
            print('Command failed. Return code : {}'.format(process.returncode))
            exit(1)
        # return output
    except Exception as e:
        print(e)
        exit(1)


def create_db(db_host, database, user_name, user_password, db_main):
    try:
        con = psycopg2.connect(dbname=db_main,
                               user=user_name, host=db_host,
                               password=user_password)

    except Exception as e:
        print(e)
        exit(1)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("DROP DATABASE {} WITH(FORCE) ;".format(database))
        print('DB dropped with FORCE')
    except Exception as e:
        print('DB does not exist, nothing to drop')
    cur.execute("CREATE DATABASE {} ;".format(database))
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE {} TO {} ;".format(database, user_name))
    return database


def restore_postgres_db(db_host, db, port, user, password, backup_file):
    """
    Restore postgres db from a file.
    """

    try:
        print(user, password, db_host, port, db)
        process = subprocess.Popen(
            ['pg_restore',
             '--no-owner',
             '--dbname=postgresql://{}:{}@{}/{}'.format(user, password, db_host, db),
             '-v',
             backup_file],
            stdout=subprocess.PIPE
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            print('Command failed. Return code : {}'.format(process.returncode))

        return output
    except Exception as e:
        print("Issue with the db restore : {}".format(e))


if __name__ == "__main__":
    # LOCAL BACKUP

    backup_postgres_db(L_DB_HOST, L_DB, L_DB_PORT, L_DB_USER, L_DB_PASSWORD, "pricetracker07-04.sql")

    # LOCAL RESTORE

    # L_DB='pricetracker'
    # create_db(L_DB_HOST, L_DB, L_DB_USER, L_DB_PASSWORD, L_DB_MAIN)
    # restore_postgres_db(L_DB_HOST, L_DB, L_DB_PORT, L_DB_USER, L_DB_PASSWORD, "pricetracker22-001-03.sql")

    # REMOTE RESTORE

    create_db(R_DB_HOST, R_DB, R_DB_USER, R_DB_PASSWORD, R_DB_MAIN)
    restore_postgres_db(R_DB_HOST, R_DB, R_DB_PORT, R_DB_USER, R_DB_PASSWORD, "pricetracker07-04.sql")
