from langchain import LLMMathChain, OpenAI
from langchain.agents import Tool, initialize_agent

from wwwml.tools.sysstat import iostat, mpstat, vmstat


def load_tools(llm, verbose=False):
    return [
        Tool(
            name="Calculator",
            func=LLMMathChain.from_llm(llm=llm, verbose=verbose).run,
            description="useful for when you need to answer questions about math",
        ),
        iostat,
        vmstat,
        mpstat,
    ]
