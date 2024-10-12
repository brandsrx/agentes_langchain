## la forma en la que se emplea wikipedia con langchain
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


response = wikipedia.run("HUNTER X HUNTER")

print(response)