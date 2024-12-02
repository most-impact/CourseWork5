import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config


def create_database():
    params = config()
    conn = psycopg2.connect(
        dbname='postgres',
        user=params['user'],
        password=params['password'],
        host=params['host']
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        cursor.execute('CREATE DATABASE your_database_name')
        print('Database created successfully.')
    except psycopg2.errors.DuplicateDatabase:
        print('Database already exists.')
    finally:
        cursor.close()
        conn.close()


def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            vacancies_url VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255),
            company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE
        );
        """
    ]

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        conn.commit()
        print('Tables created successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_company(conn, name, description, vacancies_url):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO companies (name, description, vacancies_url)
        VALUES (%s, %s, %s) RETURNING id;
    """,
        (name, description, vacancies_url),
    )
    company_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return company_id


def add_vacancy(conn, title, salary, url, company_id):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO vacancies (title, salary, url, company_id)
        VALUES (%s, %s, %s, %s);
    """,
        (title, salary, url, company_id),
    )
    conn.commit()
    cursor.close()
