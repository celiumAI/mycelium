from .model import Repository
from .note.model import Note
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.llms import Ollama
from crewai import Agent, Task, Crew, Process


repo_notes = Repository(node_type=Note)
repo_questions = Repository(node_type=Note, path=repo_notes.path.parent / 'concepts')
repo_questions.ensure_exists()

llm = Ollama(model="mistral:instruct")


notes = repo_notes.nodes
for note in notes:
    = Agent(
    role='research manager',
    goal="find an insteresting research question that could result in someone writing the following text",
    backstory="""You are a Senior Research Analyst at a leading tech think tank.
  Your expertise lies in identifying emerging trends from plain text dumps. You have a knack for dissecting complex data and presenting
  actionable insights.""",
    tools=[],
    llm=llm,
    verbose=True
    )
    prompt_find_question = """find an insteresting research question that could result in someone writing the following text: """

    messages = [
        SystemMessage(content=""),
        HumanMessage(content=prompt_find_question + note.read()),
    ]

    response = llm(messages)
    message_ai = AIMessage(content=response)
    print(message_ai.content)
    

    prompt_find_solution = """propose a better solution to the problem and how it could be implemented in a agile framework that contains 5 or less levels of abstraction from the main idea down to specific function definitions."""
    prompt_improve_solution = """improve the solution. you must think outside of the box and find non mainstream solutions. the goal is to replace programmers with large language models. so now first read the text"""
    exit()
