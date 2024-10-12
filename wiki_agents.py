from langchain_ollama import OllamaLLM
from langchain.agents import  AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

from pydantic import BaseModel,Field
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

class WikiInputs(BaseModel):
    """Entradas a la herramienta wikipedia."""
    query:str = Field(
        description="La consulta a buscar en Wikipedia debe tener 3 palabras o menos."
    )

llms = OllamaLLM(
    model="llama3.2:1b",
    temperature=0.2
)

wikipedia = WikipediaQueryRun(
    name="wiki-tool",
    description="busca cosas en wikipedia",
    args_schema=WikiInputs,
    api_wrapper=WikipediaAPIWrapper(),
    return_direct=True
)

tools = [wikipedia]

prompt_t = """Eres un asistente de IA que puede usar herramientas para responder preguntas. Tu tarea es responder la pregunta del usuario siguiendo un formato específico que permite a tu agente analizar la respuesta.

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

prompt = PromptTemplate.from_template(prompt_t)

agents = create_react_agent(
    llm=llms,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agents,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True  # Cambiado a True para manejar errores de análisis
)

response = agent_executor.invoke({"input": "busca en wikipedia 'HUNTER X HUNTER' y dame un resumen"})

print(response["output"])