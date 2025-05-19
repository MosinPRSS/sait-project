import dotenv
import asyncio
from crewai import Agent, Crew, Task, LLM
from tools.Searchers import ThesaurusRuWordNetSearch

dotenv.load_dotenv()

async def main():
    RWN_search_tool = ThesaurusRuWordNetSearch()

    model = LLM(
        model="ollama/llama3.1",
        temperature=0.7,
        url="http://localhost:11434"
    )

    agent = Agent(
        role="Суммарайзер-поисковик по тезаурусам",
        goal="""
        # DONT USE ANY JSON, DICTIONARY OR UNICODE SEQUENCE WHEN USING A TOOL
        WHILE SEARCHING SEND QUERIES ONLY OF RUSSIAN TERMINS WHICH USERS SUGGEST TO FIND
        For example if user provide: "найди значение термина корова" you must provide to query: "корова" or write it in URL-format.
        For example, "корова" -> "%D0%BA%D0%BE%D1%80%D0%BE%D0%B2%D0%B0".
        """,
        backstory="Опытный лингвист с большим стажем в работе с лингвистическими базами",
        llm=model,
        verbose=True,
        tools=[RWN_search_tool],
    )

    task = Task(
        description="Найди значение слова молот",
        expected_output="Summarize with meanings which you got from thesaurus. IT MUST BE ON RUSSIAN!!!",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
        output_log_file=True
    )

    result = await crew.kickoff()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
