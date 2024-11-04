from apeagent import Agent
from typing import Dict, Any

# Configuración de la API OpenAI
Agent.openai_client("your-api-key")


@Agent.tool
def sumar_tool(x: float, y: float) -> Dict[str, Any]:
    """Realiza la suma de dos números.
    Args:
        x (float): Primer número.
        y (float): Segundo número.
    """
    resultado = x + y
    return {
        "operacion": "suma",
        "x": x,
        "y": y,
        "resultado": resultado
    }

@Agent.tool
def restar_tool(x: float, y: float) -> Dict[str, Any]:
    """Realiza la resta de dos números.
    Args:
        x (float): Primer número.
        y (float): Segundo número.
    """
    resultado = x - y
    return {
        "operacion": "resta",
        "x": x,
        "y": y,
        "resultado": resultado
    }

@Agent.tool
def consulta_listin_telefonico(nombre: str) -> Dict[str, Any]:
    """Consulta el listín telefónico de Macaque Consulting.
    Args:
        nombre (str): Nombre de la persona a buscar.
    """
    listin_telefonico = {
        "Juan": "123456789",
        "Maria": "987654321",
        "Pedro": "456789123"
    }
    if nombre in listin_telefonico:
        telefono = listin_telefonico[nombre]
        return {
            "nombre": nombre,
            "telefono": telefono
        }
    else:
        return {
            "nombre": nombre,
            "telefono": "No encontrado"
        }



# Configuración de Agentes
def configurar_agentes():

    # Agente principal con capacidades multifuncionales
    agente_listin = Agent(
        name="Agente_Listin_Telefonico",
        instructions="""
        Eres un agente de inteligencia artificial con capacidades de consultar el listin telefónico de Macaque Consulting.
        """,
        functions=[consulta_listin_telefonico],
        model="gpt-4o-mini",
        temperature=0.0,
        parallel_tool_calls=True,
        memory_enabled=False,
        debug=False
    )
    
    
    # Agente principal con capacidades multifuncionales
    agente_principal = Agent(
        name="Agente_Principal",
        instructions="""
        Eres un agente de inteligencia artificial con capacidades de chatear.
        Puedes sumar, restar y consultar el listin telefónico de Macaque Consulting.
        """,
        functions=[sumar_tool, restar_tool, agente_listin],
        model="gpt-4o",
        temperature=0.5,
        parallel_tool_calls=True,
        memory_enabled=True,
        memory_max_conversations=40,
        debug=False
    )
    
    return agente_principal


if __name__ == "__main__":
    agente_principal = configurar_agentes()
    while True:
        user_id = "user_1"
        query = input("Usuario: ")
        response = agente_principal.call(query, user_id)
        print(f"Agente: {response}")
        if query == "exit":
            break
