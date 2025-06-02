import google.generativeai as genai
from typing import Dict, Any, List
import logging
from ..base.adk_agent import ADKAgent
from ..workers.sub_agent_sombrero_amarillo_adk import SubAgentSombreroAmarilloADK
from ..workers.sub_agent_sombrero_negro_adk import SubAgentSombreroNegroADK
import asyncio

# Attempting to import genai, assuming it will be available in the environment
try:
    import google.generativeai as genai
except ImportError:
    # Fallback or error handling if google.generativeai is not found
    # For now, we'll let it raise an error if not found during execution,
    # or define a mock/stub if needed for testing in isolation.
    genai = None
    print("Warning: google.generativeai not found. Functionality requiring it will fail.")


from ..base.adk_agent import ADKAgent
from ..prompts.orchestrator_prompts import ORCHESTRATOR_SYSTEM_PROMPT


class OrchestratorADK(ADKAgent):
    """
    Orchestrator agent for the ADK framework.
    Manages subagents and delegates tasks accordingly.
    """

    def __init__(self, model_name: str = "gemini-1.5-pro", **kwargs):
        """
        Initializes the OrchestratorADK.

        Args:
            model_name: The name of the generative model to use.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(model_name=model_name, **kwargs)
        if genai:
            self.model = genai.GenerativeModel(model_name)
        else:
            # Handle the case where genai is not available
            self.model = None
            # Consider logging a more severe warning or raising an error
            # depending on how critical genai is at this stage.
            print("Error: GenerativeModel cannot be initialized because google.generativeai is not available.")

        self.subagents: Dict[str, ADKAgent] = {}
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO) # Basic config for logging

        # Inicializar y registrar los subagentes
        self.subagent_sombrero_amarillo = SubAgentSombreroAmarilloADK("gemini-1.5-flash")
        self.subagent_sombrero_negro = SubAgentSombreroNegroADK("gemini-1.5-flash")
        
        self.register_subagent("sombrero_amarillo", self.subagent_sombrero_amarillo)
        self.register_subagent("sombrero_negro", self.subagent_sombrero_negro)

    def get_instructions(self) -> str:
        """
        Returns the system prompt for the orchestrator agent.
        """
        return ORCHESTRATOR_SYSTEM_PROMPT

    def register_subagent(self, agent_name: str, agent_instance: ADKAgent):
        """Registra un subagente en el orquestador"""
        self.subagents[agent_name] = agent_instance
        self.logger.info(f"Subagente {agent_name} registrado exitosamente")

    def get_available_subagents(self) -> List[str]:
        """Retorna la lista de subagentes disponibles"""
        return list(self.subagents.keys())

    async def process_task(self, task: str, context: Dict[str, Any] = None) -> str:
        """
        Procesa una consulta del usuario y coordina con los subagentes
        """
        self.logger.info(f"Received task for processing: {task}")
        if not self.model:
            self.logger.error("Orchestrator model not initialized. Cannot process task.")
            return "Error: Orchestrator model not available."

        try:
            # Verificar que los subagentes estén disponibles
            if "sombrero_amarillo" not in self.subagents:
                self.logger.error("Sombrero Amarillo no está registrado")
                return "Error: Sombrero Amarillo no está disponible"
            
            if "sombrero_negro" not in self.subagents:
                self.logger.error("Sombrero Negro no está registrado")
                return "Error: Sombrero Negro no está disponible"

            # Verificar que los modelos de los subagentes estén inicializados
            if not self.subagents["sombrero_amarillo"].model:
                self.logger.error("Modelo del Sombrero Amarillo no está inicializado")
                return "Error: Modelo del Sombrero Amarillo no está disponible"
            
            if not self.subagents["sombrero_negro"].model:
                self.logger.error("Modelo del Sombrero Negro no está inicializado")
                return "Error: Modelo del Sombrero Negro no está disponible"

            # Analizar la consulta
            analysis_prompt = f"""
            {self.get_instructions()}

            Consulta del usuario: {task}

            Analiza esta consulta y determina:
            1. ¿Qué subagente(s) deberían manejar esta consulta?
            2. ¿Qué información específica necesitas de cada subagente?
            3. ¿Cómo coordinarás las respuestas?

            Pasa la consulta a los subagentes disponibles: {self.get_available_subagents()}

            Responde con tu plan de acción.
            """

            self.logger.info("Generating analysis for task...")
            response = await asyncio.to_thread(self.model.generate_content, analysis_prompt)

            if response is None or not hasattr(response, 'text') or response.text is None:
                self.logger.error("LLM response was empty or malformed.")
                return "Error: LLM response was empty or malformed."

            analysis_result = response.text
            self.logger.info(f"Orchestrator analysis: {analysis_result}")

            # Llamar a los subagentes de forma asíncrona
            try:
                self.logger.info("Llamando a los subagentes de forma asíncrona...")
                sombrero_amarillo_task = await self.subagents["sombrero_amarillo"].process_task(task, context)
                sombrero_negro_task = await self.subagents["sombrero_negro"].process_task(task, context)
                
                # Ya no necesitamos asyncio.gather porque estamos esperando las respuestas directamente
                self.logger.info(f"Sombrero Amarillo response: {sombrero_amarillo_task}")
                self.logger.info(f"Sombrero Negro response: {sombrero_negro_task}")
                
                # Asignar las respuestas a las variables correctas
                sombrero_amarillo_response = sombrero_amarillo_task
                sombrero_negro_response = sombrero_negro_task
            except Exception as e:
                self.logger.error(f"Error en la llamada a los subagentes: {str(e)}", exc_info=True)
                return f"Error en la llamada a los subagentes: {str(e)}"

            # Generar resumen comparativo
            summary_prompt = f"""
            {self.get_instructions()}

            Basado en las respuestas de los subagentes, genera un resumen comparativo:

            Respuesta del Sombrero Amarillo:
            {sombrero_amarillo_response}

            Respuesta del Sombrero Negro:
            {sombrero_negro_response}

            Genera un informe que incluya:
            1. Principales fortalezas identificadas (Sombrero Amarillo)
            2. Principales riesgos o debilidades detectadas (Sombrero Negro)
            3. Contrastes clave entre ambas perspectivas
            """

            self.logger.info("Generando resumen comparativo...")
            summary_response = await asyncio.to_thread(self.model.generate_content, summary_prompt)
            if summary_response is None or not hasattr(summary_response, 'text') or summary_response.text is None:
                self.logger.error("Error generando resumen comparativo")
                return "Error: No se pudo generar el resumen comparativo"
            
            return summary_response.text

        except Exception as e:
            self.logger.error(f"Error in orchestrator processing task '{task}': {str(e)}", exc_info=True)
            return f"Error procesando la consulta: {str(e)}"
