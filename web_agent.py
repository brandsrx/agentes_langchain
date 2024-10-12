from langchain_community.agent_toolkits import PlayWrightBrowserToolkit 
from langchain_community.tools.playwright.utils import create_sync_playwright_browser


from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

# Crear un navegador Playwright sincronizado                             
sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
tools = toolkit.get_tools()

# Elegir el LLM que impulsará el agente (usando Ollama)
llm = OllamaLLM(model="llama3.2:1b", temperature=0)

# Definir un prompt utilizando PromptTemplate
prompt_template = PromptTemplate(
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
    template="""Eres un asistente de IA que puede usar herramientas para responder preguntas. Tu tarea es responder la pregunta del usuario siguiendo un formato específico que permite a tu agente analizar la respuesta.

**Acceso a las herramientas:**
{tools}

**Acciones que puedes realizar:**
{tool_names}

**Formato para usar una herramienta:**
Si decides que necesitas usar una herramienta, tu salida debe seguir este formato:
'''
Pensamiento: ¿Necesito usar una herramienta? Sí
Acción: [Nombre de la herramienta que deseas usar]
Entrada de acción: [Especifica la entrada necesaria para la acción]
Observación: [Describe el resultado de la acción]
'''

**Formato para no usar una herramienta:**
Si decides que no necesitas usar una herramienta, tu salida debe seguir este formato:
'''
Pensamiento: ¿Necesito usar una herramienta? No
Respuesta final: [Escribe tu respuesta aquí]
'''

**Pregunta:** {input}
{agent_scratchpad}

Asegúrate de que la respuesta contenga solo un conjunto de "Pensamiento", "Acción", "Entrada de acción", "Observación" o "Respuesta final". No debes repetir las secciones y asegúrate de ser claro y conciso en tus respuestas.
"""
)

# Crear un agente que utiliza herramientas de Playwright
agent = create_react_agent(llm, tools, prompt_template)

# Crear un ejecutor de agente pasando el agente y las herramientas
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)

# Definir el comando para el agente
command = {
    "input": "Vaya a https://python.langchain.com/docs/integrations/tools/playwright/ y deme un resumen de todas las herramientas mencionadas en la página que aparece. Imprima la URL en cada paso"
}

# Invocar el agente
response = agent_executor.invoke(command)
print(response)  # Imprimir la respuesta del agente
