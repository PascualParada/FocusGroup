import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class SubagentBeta:
    """
    SubagentBeta - Agente especializado (función específica por definir)
    """
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)
        
    def _get_system_message(self) -> str:
        return """
        Eres SubagentBeta, un agente especializado en el sistema multiagente.
        
        Características:
        - Tienes un enfoque diferente al de SubagentAlpha
        - Proporcionas perspectivas complementarias
        - Te especializas en tu área asignada (por definir)
        - Trabajas en colaboración con el sistema multiagente
        
        Tu función específica será definida según los requerimientos del sistema.
        Por ahora, actúas como un asistente general con un enfoque alternativo.
        """
    
    async def process_task(self, task: str, context: dict = None) -> str:
        """
        Procesa una tarea específica asignada por el orquestador
        """
        try:
            prompt = f"""
            {self._get_system_message()}
            
            Tarea asignada: {task}
            Contexto adicional: {context if context else 'No hay contexto adicional'}
            
            Desde tu perspectiva especializada, procesa esta tarea y proporciona una respuesta.
            """
            
            response = self.model.generate_content(prompt)
            logger.info(f"SubagentBeta completó la tarea: {task[:50]}...")
            return response.text
            
        except Exception as e:
            logger.error(f"Error en SubagentBeta: {str(e)}")
            return f"Error procesando la tarea: {str(e)}"
    
    def get_capabilities(self) -> dict:
        """Retorna las capacidades de este subagente"""
        return {
            "name": "SubagentBeta",
            "specialization": "Función por definir",
            "status": "Activo",
            "model": "gemini-1.5-flash"
        }