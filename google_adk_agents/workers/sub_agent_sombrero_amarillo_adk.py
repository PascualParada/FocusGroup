import logging
from typing import Dict, Any
import asyncio

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    print("Warning: google.generativeai not found. Functionality requiring it will fail for SubAgentAlphaADK.")

from ..base.adk_agent import ADKAgent
from ..prompts.sub_agent_prompts import SUB_AGENT_SOMBREROAMARILLO_SYSTEM_PROMPT


class SubAgentSombreroAmarilloADK(ADKAgent):
    """
    SubAgentSombreroAmarilloADK - Agente especializado (función específica por definir)
    Adaptado para el framework ADK.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash", **kwargs):
        """
        Initializes the SubAgentAlphaADK.

        Args:
            model_name: The name of the generative model to use.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(model_name=model_name, **kwargs)
        if genai:
            self.model = genai.GenerativeModel(model_name)
        else:
            self.model = None
            print("Error: SubAgentSombreroAmarilloADK GenerativeModel cannot be initialized because google.generativeai is not available.")

        self.logger = logging.getLogger(__name__)
        # Basic config for logging, if not already configured by orchestrator or main app
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(level=logging.INFO)


    def get_instructions(self) -> str:
        """
        Returns the system prompt for SubAgentSombreroAmarillo.
        """
        return SUB_AGENT_SOMBREROAMARILLO_SYSTEM_PROMPT

    async def process_task(self, task: str, context: Dict[str, Any] = None) -> str:
        """
        Procesa una tarea específica asignada por el orquestador.

        Args:
            task: The task description string.
            context: An optional dictionary providing additional context.

        Returns:
            A string representing the result or output of the task processing.
        """
        self.logger.info(f"SubAgentSombreroAmarilloADK received task: {task}")
        if not self.model:
            self.logger.error("SubAgentSombreroAmarilloADK model not initialized. Cannot process task.")
            return "Error: SubAgentSombreroAmarilloADK model not available."

        try:
            print("SubAgentSombreroAmarilloADK: Iniciando procesamiento de tarea...")
            prompt = f"""
            {self.get_instructions()}

            Tarea asignada: {task}
            Contexto adicional: {context if context else 'No hay contexto adicional'}

            Procesa esta tarea según tu especialización y proporciona una respuesta detallada.
            """

            # Convertir generate_content en asíncrono usando asyncio.to_thread
            response = await asyncio.to_thread(self.model.generate_content, prompt)

            if response is None or not hasattr(response, 'text') or response.text is None:
                self.logger.error("SubAgentSombreroAmarilloADK LLM response was empty or malformed.")
                return "Error: LLM response was empty or malformed."

            self.logger.info(f"SubAgentSombreroAmarilloADK completed task: {task[:50]}...")
            return response.text

        except Exception as e:
            self.logger.error(f"Error in SubAgentSombreroAmarilloADK processing task '{task}': {str(e)}", exc_info=True)
            return f"Error procesando la tarea: {str(e)}"

    def get_capabilities(self) -> dict:
        """Retorna las capacidades de este subagente"""
        # This is copied from the old SubagentAlpha,
        # assuming it fits the ADKAgent's expected format.
        # The base ADKAgent.get_capabilities returns {"version": "1.0"},
        # so this provides more specific info.
        return {
            "name": "SubAgentSombreroAmarilloADK", # Updated name
            "specialization": "Actúas como el sombrero amarillo. Tu objetivo es identificar los beneficios, oportunidades, fortalezas y aspectos positivos de la propuesta o situación", # Clarified specialization
            "status": "Activo",
            "model": self.model_name # Use model_name passed during init
        }
