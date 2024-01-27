import requests
from bs4 import BeautifulSoup
import json
import fake_useragent


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
}

results = []
ua = fake_useragent.UserAgent()
data = requests.get(
    url=f"https://spb.hh.ru/search/vacancy?text=python+django+flask&area=1&area=2&page=1",
    headers={'user-agent':ua.random}
)

soup = BeautifulSoup(data.content, 'lxml')

page_count = int(soup.find('div', attrs={'class':'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)

for page in range(page_count):
    url = f"https://spb.hh.ru/search/vacancy?text=python+django+flask&area=1&area=2&page={page}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        vacancies = soup.find_all("div", class_="vacancy-serp-item__layout")

        for vacancy in vacancies:
            company = vacancy.find(
                "a", {"data-qa": "vacancy-serp__vacancy-employer"}
            ).text.replace('\xa0', ' ')
            address = vacancy.find(
                "div", {"data-qa": "vacancy-serp__vacancy-address"}
            ).text
            city = address.split(",")[0]

            salary_element = vacancy.find(
                "span",
                {"data-qa": "vacancy-serp__vacancy-compensation"},
            )

            salary = salary_element.text.replace('\u202f', ' ') if salary_element else "Не указана"

            link = vacancy.find("a", class_="bloko-link")["href"]

            results.append(
                {
                    "company": company,
                    "city": city,
                    "salary": salary,
                    "link": link,
                }
            )

with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

