import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from tools import visit_webpage, transcript_tool_langchain, read_file_contents, google_serper_search, python_repl_tool, youtube_transcript_tool, wikipedia


load_dotenv()


BASE_URL = os.getenv("BASE_URL")
OKTA_ACCESS_TOKEN = os.getenv("OKTA_ACCESS_TOKEN")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")

chat = ChatOpenAI(
    api_key=OKTA_ACCESS_TOKEN,
    base_url=BASE_URL,
    model="GPT_4_1",
    default_headers={"Subscription-Key": SUBSCRIPTION_KEY},
)


def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    file_path = config["configurable"].get("file_path", "")
    system_msg = (
        f"You are an AI assistant evaluated on the GAIA benchmark. "
        f"Answer questions using only verified information. "
        f"Use the available tools to find answers when needed. "
        f"If you do not have enough information, reply: 'I do not have enough information to answer the question.' "
        f"Provide only the direct answer, with no extra explanation, formatting, or restating the question. "
        f"For example, if asked 'What is the capital of France?', answer 'Paris'. "
        f"When returning comma separated lists as answer, provide a space after each comma (e.g., 'item1, item2, item3'). "
    )
    if file_path:
        system_msg += (
            f" If the question refers to a file, use the file path provided in your context to access the file, "
            f"and do not use the file name mentioned in the question. Use only the file path variable for file operations."
            f" The file path is: {file_path}."
        )
    return [{"role": "system", "content": system_msg}] + state["messages"]

react_agent = create_react_agent(
    model=chat,
    tools=[wikipedia, visit_webpage, transcript_tool_langchain, read_file_contents, google_serper_search, python_repl_tool, youtube_transcript_tool],
    prompt=prompt,
)
