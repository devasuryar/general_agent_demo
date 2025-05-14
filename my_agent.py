import yaml
from smolagents import OpenAIServerModel, VisitWebpageTool
from smolagents import CodeAgent, FinalAnswerTool, WikipediaSearchTool, Tool
from langchain_community.tools import DuckDuckGoSearchRun

import os

# Load environment variables from .env file
with open('.env') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value



model = OpenAIServerModel(
    model_id="GEMINI_15_PRO",  # Replace with the desired model ID
    api_base=os.getenv("BASE_URL"),  # Base URL for the API
    api_key=os.getenv("OKTA_ACCESS_TOKEN"),  # API key for authentication
    custom_role_conversions=None,
    temperature=0.5,
    client_kwargs={
        "default_headers": {"Subscription-Key": os.getenv("SUBSCRIPTION_KEY")},  # Additional headers,
    },
    web_search_options={
        "enabled": True,
        "dynamic_threshold": 0.5
    }
)

# Load system prompt from prompt.yaml file
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

final_answer = FinalAnswerTool()

ddg_tool = Tool.from_langchain(DuckDuckGoSearchRun())

agent = CodeAgent(
    tools=[final_answer, VisitWebpageTool(), WikipediaSearchTool(), ddg_tool],
    add_base_tools=True,
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
    model=model)



#
# res = agent.run("Can you find any information about the latest news on AI?")
# print(res)