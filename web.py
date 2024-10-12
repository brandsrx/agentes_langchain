##la forma en la que se emplea Langchain con langchain
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser

sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
tools = toolkit.get_tools()

tools_by_name = {tool.name: tool for tool in tools}
navigate_tool = tools_by_name["navigate_browser"]
get_elements_tool = tools_by_name["get_elements"]

# Navegar y obtener elementos de manera síncrona
def run_tasks():
    data = navigate_tool.run({"url": "https://docs.python.org/es/3.8/library/asyncio.html"})
    print(data)
    
    elements = get_elements_tool.run({"selector": ".document", "attributes": ["innerText"]})
    print(elements)

run_tasks()
