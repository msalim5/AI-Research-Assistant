from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from yarl import Query
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool


load_dotenv()

class Response(BaseModel):
  topic: str
  summary:str
  sources: list[str]
  tools_used: list[str]


##Set up LLM via an agent
llm = ChatAnthropic(model = "claude-3-5-sonnet-20241022")
parser = PydanticOutputParser(pydantic_object=Response)

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system,"
      """
      You are a research assistant that will help generate a research paper. Answer the user querry and use neccassary tools.
      Wrap the output in the format provided and do not provide additional text\n{format_instructions}
      """
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
  ]
).partial(format_instructions = parser.get_format_instructions())

tools = [search_tool, wiki_tool]
agent = create_tool_calling_agent(
  llm = llm,
  prompt= prompt,
  tools = tools
)

agent_executor = AgentExecutor(agent=agent, tools = tools)
query = input("What can I assist you with? Please type quit to exit: ")

while 'quit' not in query: 
  raw_response = agent_executor.invoke({"query":query})

  try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
  except Exception as e:
    print("Error Parsing Response", e, "Raw Response: ", raw_response)
  
  query = input("What can I assist you with? Please type quit to exit: ")

  
print('Glad I could help assit!')





