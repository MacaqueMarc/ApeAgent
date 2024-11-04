
# ApeAgent

**ApeAgent** es un framework creado por Macaque Consulting para crear agentes inteligentes que pueden ejecutar funciones específicas (herramientas) de forma secuencial o en paralelo, manteniendo el contexto de conversación. Este enfoque multiagente es ideal para sistemas complejos que necesitan eficiencia en el consumo de tokens y control detallado de procesos.

## Instalación

```bash
pip install apeagent
```

## Ventajas del Sistema Multiagente

La arquitectura de orquestación multiagente en **ApeAgent** optimiza el uso de tokens y mejora la precisión del modelo en entornos complejos. Las principales ventajas incluyen:

- **Reducción del consumo de tokens**: Cada agente utiliza solo el contexto necesario para cada consulta, optimizando costos y mejorando la rapidez.
- **Control detallado de procesos**: Los agentes especializados permiten un control granular y facilidad de depuración, ideal para sistemas en los que cada tarea debe gestionarse con precisión.
- **Minimización de alucinaciones del modelo**: Al dividir tareas en agentes especializados, el sistema reduce la probabilidad de respuestas incoherentes o inexactas.
- **Capacidad para crear sistemas autosupervisados o de verificación ("juez")**: Puedes incluir un agente que verifique las respuestas de otros agentes antes de presentarlas al usuario.
- **Eficiencia y paralelismo**: Los agentes pueden ejecutar tareas en paralelo y mantener el contexto en conversaciones prolongadas.

## Parámetros de Configuración del Agente

Al configurar un agente en **ApeAgent**, puedes ajustar su comportamiento a través de varios parámetros:

- **`name`**: Nombre del agente, sin espacios.
- **`instructions`**: Mensaje de rol del sistema que guía al agente (define su propósito).
- **`functions`**: Herramientas o agentes a los que el agente tiene acceso, listados en forma de lista.
- **`model`**: Modelo a usar (actualmente integración con modelos de OpenAI).
- **`temperature`**: Controla la creatividad de las respuestas del agente.
- **`parallel_tool_calls`**: Permite que el agente ejecute herramientas en paralelo.
- **`memory_enabled`**: Permite que el agente mantenga el contexto de la conversación.
- **`memory_max_conversations`**: Número máximo de interacciones que el agente almacena en memoria.
- **`debug`**: Activa la salida en consola para depuración.

## Cómo Definir Herramientas (`Tools`)

Las herramientas son funciones que el agente puede usar para realizar tareas específicas. Deben definirse con el decorador `@Agent.tool` y deben estar **tipadas** y con **comentarios descriptivos** para que el modelo entienda su propósito y uso.

### Ejemplo de una Herramienta Simple

```python
from apeagent import Agent
from typing import Dict

@Agent.tool
def sumar(x: float, y: float) -> Dict[str, float]:
    """Realiza la suma de dos números y devuelve el resultado."""
    return {"resultado": x + y}
```

### Configuración Básica del Agente

```python
agente_calculadora = Agent(
    name="Calculadora",
    instructions="Eres un agente que puede realizar operaciones matemáticas simples.",
    functions=[sumar],
    model="gpt-4o",
    temperature=0.0
)
```

## Ejemplo Avanzado: Sistema Multiagente con Jerarquía

### Herramienta para Consultar el Clima

```python
@Agent.tool
def consultar_clima(ciudad: str) -> Dict[str, str]:
    """Proporciona el clima actual para una ciudad específica usando la API de OpenWeather."""
    # Implementación de la consulta de clima...
    ...
```

### Configuración de Agentes Especializados y Agente Principal

```python
agente_clima = Agent(
    name="Agente_Clima",
    instructions="Eres un agente especializado en proporcionar información sobre el clima.",
    functions=[consultar_clima],
    model="gpt-4o",
    temperature=0.0
)

agente_principal = Agent(
    name="Agente_Principal",
    instructions="Eres un asistente versátil que puede: 1. Proporcionar información sobre el clima. 2. Realizar operaciones matemáticas.",
    functions=[agente_clima, agente_calculadora],
    model="gpt-4o",
    temperature=0.5,
    parallel_tool_calls=True,
    memory_enabled=True,
    memory_max_conversations=40,
    debug=True
)
```

## Uso del Agente Principal

```python
consulta_clima = "¿Cuál es el clima en Barcelona?"
respuesta_clima = agente_principal.call(consulta_clima)
print("Agente (clima):", respuesta_clima)

consulta_suma = "Suma 7 y 5"
respuesta_suma = agente_principal.call(consulta_suma)
print("Agente (suma):", respuesta_suma)
```

## Ejemplo de Salida

```
Agente (clima): La temperatura en Barcelona es 20°C con cielo despejado.
Agente (suma): El resultado es 12.
```
