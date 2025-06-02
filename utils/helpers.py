import logging
import asyncio
from typing import Any, Coroutine

def setup_logging(level: str = "INFO"):
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class AsyncRunner:
    """Utilidad para ejecutar funciones asíncronas en Streamlit"""
    
    @staticmethod
    def run(coro: Coroutine[Any, Any, Any]) -> Any:
        """Ejecuta una corrutina de forma síncrona"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(coro)