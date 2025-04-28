import json
from crewai.tools import BaseTool
class SerializerJSON(BaseTool):
    name: str = "Сериализатор JSON"
    description: str = """
    Сериализируй для некоторых поисковиков запросы, переводя с unicode-формата на русский язык.
    """

    def _run(self, line: str) -> str:
        decoded_line = bytes(line, "utf-8").decode("unicode-escape")
        return decoded_line

print(SerializerJSON())