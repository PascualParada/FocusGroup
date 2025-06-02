import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class SubagentAlpha:
    """
    SubagentAlpha - Agente especializado (función específica por definir)
    """
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)
        
    def _get_system_message(self) -> str:
        return """
        Eres SubagentAlpha, un agente especializado en el sistema multiagente.
        
        Características:
        - Respondes de manera concisa y específica
        - Te enfocas en tu área de especialización (por definir)
        - Colaboras efectivamente con el orquestador y otros subagentes
        - Proporcionas información clara y estructurada
        
        Tu función específica será definida según los requerimientos del sistema.
        Por ahora, actúas como un asistente general que puede procesar cualquier tipo de consulta.
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
            
            Procesa esta tarea según tu especialización y proporciona una respuesta detallada.
            """
            
            response = self.model.generate_content(prompt)
            logger.info(f"SubagentAlpha completó la tarea: {task[:50]}...")
            return response.text
            
        except Exception as e:
            logger.error(f"Error en SubagentAlpha: {str(e)}")
            return f"Error procesando la tarea: {str(e)}"
    
    def get_capabilities(self) -> dict:
        """Retorna las capacidades de este subagente"""
        return {
            "name": "SubagentAlpha",
            "specialization": "Función por definir",
            "status": "Activo",
            "model": "gemini-1.5-flash"
        }