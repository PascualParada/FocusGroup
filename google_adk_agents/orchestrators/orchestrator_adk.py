import logging
from typing import Dict, Any, List

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

    def __init__(self, model_name: str, **kwargs):
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

    def process_task(self, task: str, context: Dict[str, Any] = None) -> str:
        """
        Procesa una consulta del usuario y coordina con los subagentes
        """
        self.logger.info(f"Received task for processing: {task}")
        if not self.model:
            self.logger.error("Orchestrator model not initialized. Cannot process task.")
            return "Error: Orchestrator model not available."

        try:
            # Analizar la consulta
            analysis_prompt = f"""
            {self.get_instructions()}

            Consulta del usuario: {task}

            Analiza esta consulta y determina:
            1. ¿Qué subagente(s) deberían manejar esta consulta?
            2. ¿Qué información específica necesitas de cada subagente?
            3. ¿Cómo coordinarás las respuestas?

            Considera los siguientes subagentes disponibles: {self.get_available_subagents()}

            Responde con tu plan de acción.
            """

            self.logger.info("Generating analysis for task...")
            # Assuming generate_content returns an object with a 'text' attribute
            response = self.model.generate_content(analysis_prompt)

            # Check if response or response.text is None
            if response is None or not hasattr(response, 'text') or response.text is None:
                self.logger.error("LLM response was empty or malformed.")
                return "Error: LLM response was empty or malformed."

            analysis_result = response.text
            self.logger.info(f"Orchestrator analysis: {analysis_result}")

            # TODO: Implement actual delegation logic based on analysis_result
            # For now, returning the analysis as was in the old method.
            # Example:
            # chosen_agent_name = self._parse_chosen_agent(analysis_result)
            # if chosen_agent_name and chosen_agent_name in self.subagents:
            #     sub_task = self._extract_sub_task(analysis_result)
            #     return self.subagents[chosen_agent_name].process_task(sub_task, context)
            # else:
            #     return "Could not determine an appropriate subagent or subagent not found."

            return analysis_result

        except Exception as e:
            self.logger.error(f"Error in orchestrator processing task '{task}': {str(e)}", exc_info=True)
            return f"Error procesando la consulta: {str(e)}"
