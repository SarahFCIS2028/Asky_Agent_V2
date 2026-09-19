import wikipedia
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia.set_user_agent(
    "ConnectX_Summer_Training_Project/1.0 (student_project)"
)
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=3000)
wikipedia_search = WikipediaQueryRun(api_wrapper=api_wrapper)

print(wikipedia.search("Roman Empire"))

print(wikipedia_search.invoke("Roman Empire"))