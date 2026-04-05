import requests
from app.core.encryption import *
from typing import Dict, Any, List, Optional

import time

def get_vacancy_details(vacancy_id: str, headers: Dict) -> Optional[Dict]:
    """
    Получает детальную информацию о конкретной вакансии
    """
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except:
        return None
    
def getCountryList() -> List[Dict]:
    base_url = "https://api.hh.ru/areas/countries"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        countries = []
        # Парсим регионы первого уровня (области, края, республики и крупные города)
        for country in data:
            countries.append({
                'id': country['id'],
                'name': country['name']
            })
        return countries
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")

def getRegionByCountry(CountryID) -> List[Dict]:
    base_url = f"https://api.hh.ru/areas/{CountryID}"
    params = {
        "countryId": CountryID
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        regions = []
        # Парсим регионы первого уровня (области, края, республики и крупные города)
        for region in data['areas']:
            regions.append({
                'id': region['id'],
                'name': region['name']
            })
        return regions
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")

def getCityByRegion(CountryID: int, RegionID: int) -> List[Dict]:
    base_url = f"https://api.hh.ru/areas/{CountryID}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        cities = []
        # Парсим регионы первого уровня (области, края, республики и крупные города)
        for region in data['areas']:
            if int(region["id"]) == RegionID:
                for city in region['areas']:
                    cities.append({
                        'id': city['id'],
                        'name': city['name']
                    })
        return cities
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")

def getCurrentVacancies(
        token: str,
    ) -> List[Dict[str, Any]]:
    url = "https://api.hh.ru/vacancies"
    userData = decodeJWTToken(token=token)
    queryText = str.replace(userData['hardSkills'], ",", " OR ")
    queryText += " OR " + userData['eduDirection']
    print(queryText)
    params = {
        "area": userData['cityId'],
        "text": queryText,
        "per_page": 20,  # Максимум на странице
        "page": 0,
        "order_by": "publication_time"
    }

    headers = {
        "User-Agent": "MyVacancyParser/1.0"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        vacancies = data.get("items", [])

        return vacancies

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return []
    
def hashPassword(password: str) -> str:
    return hasher.hash(password)

