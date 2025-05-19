from crewai.tools import BaseTool
from pydantic import BaseModel
from bs4 import BeautifulSoup
from typing import Type
import asyncio, httpx

class WordQuery(BaseModel):
    term: str

class ThesaurusRuWordNetSearch(BaseTool):
    name: str = "RuWordNet Searcher"
    description: str = (
        "Поиск значений слова в RuWordNet. Передавай одно русское слово через параметр 'term'."
    )
    args_schema: Type[BaseModel] = WordQuery

    async def _run(self, term: str) -> str:
        url = f"https://ruwordnet.ru/ru/search/{term}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(url, headers=headers)
                res.raise_for_status()
        except httpx.RequestError as e:
            return f"Ошибка подключения к RuWordNet: {e}"

        soup = BeautifulSoup(res.text, 'html.parser')

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
        
        if results:
            return await self._summary(results)
        else:
            return "Результаты не найдены, попробуйте иначе подобрать слово или измените его"
    
    async def _summary(self, lst: list) -> str:
        prompt = (
            "Here is collected content which you need to summary into one sentence:\n"
            f"{', '.join(lst)}\n"
            "You must return answer in russian only."
        )

        json_query = {
            "model": "qwen3",
            "content": prompt,
            "options": {
                "temperature": 0.7,
            },
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=200) as client:
                res = await client.post("http://localhost:11434/api/generate", json=json_query)
                res.raise_for_status()
                return res.text.strip()
        except httpx.RequestError as e:
            return f"Ошибка при генерации саммари: {e}"

