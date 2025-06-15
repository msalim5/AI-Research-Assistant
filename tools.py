from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool

search = DuckDuckGoSearchResults()
search_tool = Tool(
  name = "search",
  func = search.run,
  description="Search for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_result=1 , doc_content_chars_max = 100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
