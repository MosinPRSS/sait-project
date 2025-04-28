from crewai import Agent, Crew, Task, LLM
import dotenv, os
from tools.Searchers import ThesaurusRuWordNetSearch
dotenv.load_dotenv()

RWN_search_tool = ThesaurusRuWordNetSearch()
serializer_tool = None
API_KEY = os.getenv("openai_key")

model = LLM(
    model="openai/gpt-4",
    api_key=API_KEY,
    temperature=0.7,
    stop=["END"]
)

agent = Agent(
    role="Суммарайзер-поисковик по тезаурусам",
    goal="""
    # DONT USE ANY JSON, DICTIONARY OR UNICODE SEQUENCE WHEN USING A TOOL
    WHILE SEARCHING SEND QUERIES ONLY OF RUSSIAN TERMINS WHICH USERS SUGGEST TO FIND
    For example if user provide: "найди значение термина корова" you must provide to query: "корова" or write it in URI-format.
    For example, "корова" -> "%D0%BA%D0%BE%D1%80%D0%BE%D0%B2%D0%B0".
    """,
    backstory="Опытный лингвист с большим стажем в работе с лингвистическими базами",
    llm=model,
    verbose=True,
    tools=[RWN_search_tool],
)

task = Task(
    description="Найди значение слова слон",
    expected_output="Summarize with meanings which you got from tesaurus. IT MUST BE ON RUSSIAN!!!",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    output_log_file=True
)

result = crew.kickoff()
print(result)

