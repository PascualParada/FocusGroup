import logging
from typing import Dict, Any
import asyncio

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    print("Warning: google.generativeai not found. Functionality requiring it will fail for SubAgentSombreroNegroADK.")

from ..base.adk_agent import ADKAgent
from ..prompts.sub_agent_prompts import SUB_AGENT_SOMBREROROJO_SYSTEM_PROMPT


class SubAgentSombreroRojoADK(ADKAgent):
    """
    SubAgentSombreroRojoADK - Agente especializado (función específica por definir)
    Adaptado para el framework ADK.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash", **kwargs):
        """
        Initializes the SubAgentSombreroRojoADK.

        Args:
            model_name: The name of the generative model to use.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(model_name=model_name, **kwargs)
        if genai:
            self.model = genai.GenerativeModel(model_name)
        else:
            self.model = None
            print("Error: SubAgentSombreroRojoADK GenerativeModel cannot be initialized because google.generativeai is not available.")

        self.logger = logging.getLogger(__name__)
        # Basic config for logging, if not already configured
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(level=logging.INFO)

    def get_instructions(self) -> str:
        """
        Returns the system prompt for SubAgentSombreroRojo.
        """
        return SUB_AGENT_SOMBREROROJO_SYSTEM_PROMPT

    async def process_task(self, task: str, context: Dict[str, Any] = None) -> str:
        """
        Procesa una tarea específica asignada por el orquestador.

        Args:
            task: The task description string.
            context: An optional dictionary providing additional context.

        Returns:
            A string representing the result or output of the task processing.
        """
        self.logger.info(f"SubAgentSombreroRojoADK received task: {task}")
        if not self.model:
            self.logger.error("SubAgentSombreroRojoADK model not initialized. Cannot process task.")
            return "Error: SubAgentSombreroRojoADK model not available."

        try:
            prompt = f"""
            {self.get_instructions()}

            Tarea asignada: {task}
            Contexto adicional: {context if context else 'No hay contexto adicional'}

            Desde tu perspectiva especializada, procesa esta tarea y proporciona una respuesta.
            """

            # Convertir generate_content en asíncrono usando asyncio.to_thread
            response = await asyncio.to_thread(self.model.generate_content, prompt)

            if response is None or not hasattr(response, 'text') or response.text is None:
                self.logger.error("SubAgentSombreroRojoADK LLM response was empty or malformed.")
                return "Error: LLM response was empty or malformed."

            self.logger.info(f"SubAgentSombreroRojoADK completed task: {task[:50]}...")
            return response.text

        except Exception as e:
            self.logger.error(f"Error in SubAgentSombreroRojoADK processing task '{task}': {str(e)}", exc_info=True)
            return f"Error procesando la tarea: {str(e)}"

    def get_capabilities(self) -> dict:
        """Retorna las capacidades de este subagente"""
        # This is copied from the old SubagentBeta,
        # assuming it fits the ADKAgent's expected format.
        return {
            "name": "SubAgentSombreroRojoADK", # Updated name
            "specialization": "Representas al sombrero rojo. Tu función es expresar tus emociones, intuiciones y sentimientos sin necesidad de justificarlos.", # Clarified specialization
            "status": "Activo",
            "model": self.model_name # Use model_name passed during init
        }
