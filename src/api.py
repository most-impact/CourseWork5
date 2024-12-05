import requests


class HHApi:
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_employer_data(employer_id):
        """Receives information about the employer using an ID card"""
        url = f"{HHApi.BASE_URL}/employers/{employer_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_vacancies(employer_id):
        """Receives data about company vacancies"""
        url = f"{HHApi.BASE_URL}/vacancies"
        params = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
