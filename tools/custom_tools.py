from typing import Dict, Any, List

class CustomToolkit:
    """
    Herramientas personalizadas para el sistema multiagente
    """
    
    @staticmethod
    def format_response(agent_name: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Formatea las respuestas de los agentes"""
        return {
            "agent": agent_name,
            "content": content,
            "metadata": metadata or {},
            "timestamp": "timestamp_placeholder"
        }
    
    @staticmethod
    def validate_input(input_text: str) -> bool:
        """Valida las entradas del usuario"""
        return isinstance(input_text, str) and len(input_text.strip()) > 0
    
    @staticmethod
    def log_interaction(agent_name: str, query: str, response: str):
        """Registra las interacciones del sistema"""
        # Implementar logging personalizado aquí
        pass