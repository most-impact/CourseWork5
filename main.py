import psycopg2

from src.api import HHApi
from src.manager import DBManager
from src.setup_db import add_company, add_vacancy, create_database, create_tables


def main():
    create_database()
    create_tables()

    conn = psycopg2.connect(
        dbname="hh_vacancies",
        user="postgres",
        password="simplepassword123",
        host="localhost",
    )

    employer_ids = [1455, 1740, 78638]

    for employer_id in employer_ids:
        employer_data = HHApi.get_employer_data(employer_id)
        vacancies = HHApi.get_vacancies(employer_id)

        company_id = add_company(
            conn,
            employer_data["name"],
            employer_data.get("description", ""),
            employer_data.get("vacancies_url", ""),
        )

        for vacancy in vacancies:
            salary_info = vacancy.get("salary")
            salary = salary_info.get("from") if salary_info else None

            add_vacancy(
                conn, vacancy["name"], salary, vacancy.get("alternate_url"), company_id
            )

    db_manager = DBManager(
        dbname="hh_vacancies", user="postgres", password="simplepassword123"
    )

    print("Выберите действие:")
    print("1: Посмотреть количество вакансий по компаниям")
    print("2: Посмотреть все вакансии")
    print("3: Средняя заработная плата")
    print("4: Вакансии с зарплатой выше средней")
    print("5: Поиск вакансий по ключевому слову")

    number = input("Введите номер действия: ")
    if number == "1":
        print(db_manager.get_companies_and_vacancies_count())
    elif number == "2":
        print(db_manager.get_all_vacancies())
    elif number == "3":
        print(db_manager.get_avg_salary())
    elif number == "4":
        print(db_manager.get_vacancies_with_higher_salary())
    elif number == "5":
        keyword = input("Введите ключевое слово: ")
        print(db_manager.get_vacancies_with_keyword(keyword))
    else:
        print("Неверное действие. Попробуйте снова.")

    conn.close()


if __name__ == "__main__":
    main()
