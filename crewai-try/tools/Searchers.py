from crewai.tools import BaseTool
from pydantic import BaseModel
from bs4 import BeautifulSoup
from typing import Type
import requests

class WordQuery(BaseModel):
    term: str

class ThesaurusRuWordNetSearch(BaseTool):
    name: str = "RuWordNet Searcher"
    description: str = (
        "Поиск значений слова в RuWordNet. Передавай одно русское слово через параметр 'term'."
    )
    args_schema: Type[BaseModel] = WordQuery

    def _run(self, term: str) -> str:
        url = f"https://ruwordnet.ru/ru/search/{term}"

        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        print(f"[DEBUG] URL: {url}")
        print("[DEBUG] Response status:", res.status_code)

        results = []
        for block in soup.find_all("div", class_="relation"):
            title_tag = block.find("h4", class_="relations-title")
            sense_lists = block.find_all("div", class_="sense-list")

            senses = []
            for sense_list in sense_lists:
                sense_items = sense_list.find_all("div", class_="sense")
                for item in sense_items:
                    a_tag = item.find("a")
                    if a_tag:
                        senses.append(a_tag.text.strip())

            if title_tag and senses:
                title = title_tag.text.strip()
                results.append(f"{title}: {', '.join(senses)}")

        return "\n".join(results) if results else "Результаты не найдены."
