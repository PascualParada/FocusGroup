import google.generativeai as genai
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """
    Agente Orquestador principal que coordina y delega tareas a los subagentes.
    """
    
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.model = genai.GenerativeModel(model_name)
        self.subagents = {}
        
    def _get_system_message(self) -> str:
        return """
        Eres el Agente Orquestador principal de un sistema multiagente.
        
        Tu responsabilidad es:
        1. Analizar las consultas del usuario
        2. Determinar qué subagente(s) pueden ayudar mejor
        3. Delegar tareas a los subagentes apropiados
        4. Coordinar las respuestas y proporcionar una respuesta final coherente
        
        Tienes acceso a dos subagentes:
        - SubagentAlpha: Subagente especializado (función por definir)
        - SubagentBeta: Subagente especializado (función por definir)
        
        Siempre explica tu razonamiento sobre por qué eliges un subagente específico.
        """
    
    def register_subagent(self, name: str, subagent):
        """Registra un subagente en el orquestador"""
        self.subagents[name] = subagent
        logger.info(f"Subagente {name} registrado exitosamente")
    
    async def process_query(self, query: str, context: Dict[str, Any] = None) -> str:
        """
        Procesa una consulta del usuario y coordina con los subagentes
        """
        try:
            # Analizar la consulta
            analysis_prompt = f"""
            {self._get_system_message()}
            
            Consulta del usuario: {query}
            
            Analiza esta consulta y determina:
            1. ¿Qué subagente(s) deberían manejar esta consulta?
            2. ¿Qué información específica necesitas de cada subagente?
            3. ¿Cómo coordinarás las respuestas?
            
            Responde con tu plan de acción.
            """
            
            response = self.model.generate_content(analysis_prompt)
            logger.info(f"Plan del orquestador: {response.text}")
            
            # Aquí implementarías la lógica de delegación
            # Por ahora, retornamos el análisis del orquestador
            return response.text
            
        except Exception as e:
            logger.error(f"Error en el orquestador: {str(e)}")
            return f"Error procesando la consulta: {str(e)}"
    
    def get_available_subagents(self) -> List[str]:
        """Retorna la lista de subagentes disponibles"""
        return list(self.subagents.keys())