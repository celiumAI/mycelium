import os

from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

API_KEY = os.environ.get("API_KEY", "something")

def get_branch_prompt(name: str):
    with open(f"./prompts/{name}.pt", "r") as f:
        return f.read()


def simple(seed: str, target: str) -> str:
    prompt = get_branch_prompt(target)
    prompt_template = ChatPromptTemplate.from_template(prompt)
    model = ChatOllama()
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({"seed": seed})
    return response


if __name__ == "__main__":
    print(simple("test string", "story"))
