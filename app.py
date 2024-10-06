#para poder crear se necesita los siguientes modulos 
from langchain_ollama import OllamaLLM
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

# Inicializar el modelo de Ollama
llm = OllamaLLM(model="llama3.2:1b",temperature=0)

def sumar_numeros(numx: int, numy: int) -> str:
    """ Suma de números."""
    resultado = numx + numy
    return f"Action: sumar_numeros\nAction Input: numx={numx}, numy={numy}\nObservation: La suma entre {numx} y {numy} es: {resultado}\nFinal Answer: {resultado}"

def restar_numeros(numx: int, numy: int) -> str:
    """ Resta de números."""

    resultado = numx - numy
    return f"Action: restar_numeros\nAction Input: numx={numx}, numy={numy}\nObservation: La resta entre {numx} y {numy} es: {resultado}\nFinal Answer: {resultado}"

# Definir las herramientas
tools = [
    Tool(
        name="sumar_numeros",
        func=sumar_numeros,
        description="Esta herramienta permite sumar dos números."
    ),
    Tool(
        name="restar_numeros",
        func=restar_numeros,
        description="Esta herramienta permite restar dos números."
    )
]

prompt_t = """
Eres un gran asistente de IA que tiene acceso a herramientas adicionales para responder las siguientes preguntas lo mejor posible. Responde siempre en el mismo idioma que la pregunta del usuario. Tienes acceso a las siguientes herramientas:

{tools}

Para usar una herramienta, utiliza el siguiente formato:

'''
Pensamiento: ¿Necesito usar una herramienta? Sí
Acción: la acción a realizar debe ser una de [{tool_names}]
Entrada de acción: la entrada a la acción
Observación: el resultado de la acción
... (este Pensamiento/Acción/Entrada de acción/Observación puede repetirse 3 veces)
'''

Cuando tienes una respuesta que decirle al humano, o si no necesitas usar una herramienta, DEBES usar el formato:
'''
Pensamiento: ¿Necesito usar una herramienta? No
Respuesta final: [tu respuesta aquí]
'''

¡Comienza!

Pregunta: {input}
Pensamiento:{agent_scratchpad}
"""
# Asegúrate de que este prompt sea adecuado para tu caso de uso
# Crear el agente usando el prompt template
prompt = PromptTemplate.from_template(prompt_t)
agent = create_react_agent(llm, tools=tools, prompt=prompt)

# Crear el ejecutor del agente
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True  # Cambiado a True para manejar errores de análisis
)

# Ejecutar el agente usando `invoke`
response = agent_executor.invoke({"input": "¿Cuál es la suma de 5 y 10?"})

print(response["output"])
