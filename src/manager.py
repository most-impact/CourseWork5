import psycopg2


class DBManager:
    def __init__(self, dbname, user, password, host="localhost"):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host
        )
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cursor.execute(
            """
            SELECT companies.name, COUNT(vacancies.id) AS vacancies_count
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name;
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute(
            """
            SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id;
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("SELECT AVG(salary) FROM vacancies;")
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT title, salary, url
            FROM vacancies
            WHERE salary > %s;
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute(
            """
            SELECT title, salary, url
            FROM vacancies
            WHERE title LIKE %s;
        """,
            (f"%{keyword}%",),
        )
        return self.cursor.fetchall()
