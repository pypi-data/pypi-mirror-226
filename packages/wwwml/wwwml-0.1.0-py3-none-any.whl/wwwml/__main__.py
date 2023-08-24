from os import environ

import openai
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI

from wwwml.tools import load_tools

INIT_PROMPT = "My Linux server is slow. Use providered function to check the server."

if __name__ == "__main__":
    if "WWWML_DEPLOYMENT" in environ:
        llm = ChatOpenAI(temperature=0, deployment_id=environ["WWWML_DEPLOYMENT"])
    else:
        llm = ChatOpenAI(
            temperature=0, model=environ.get("WWWML_MODEL", "gpt-3.5-turbo")
        )
    agent = initialize_agent(
        load_tools(llm), llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
    )
    agent.run(INIT_PROMPT)
