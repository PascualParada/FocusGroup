import streamlit as st
import asyncio
from typing import Dict, Any
from google_adk_agents.orchestrators.orchestrator_adk import OrchestratorADK
from google_adk_agents.workers.sub_agent_sombrero_amarillo_adk import SubAgentSombreroAmarilloADK
from google_adk_agents.workers.sub_agent_sombrero_negro_adk import SubAgentSombreroNegroADK
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class ChatInterface:
    """
    Interfaz de chat usando Streamlit para el sistema multiagente
    """
    
    def __init__(self):
        self.orchestrator = None
        self.subagent_sombrero_amarillo = None
        self.subagent_sombrero_negro = None
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Inicializa todos los agentes del sistema"""
        try:
            # Crear agentes
            self.orchestrator = OrchestratorADK(settings.ORCHESTRATOR_MODEL)
            self.subagent_sombrero_amarillo = SubAgentSombreroAmarilloADK(settings.SUBAGENT_MODEL)
            self.subagent_sombrero_negro = SubAgentSombreroNegroADK(settings.SUBAGENT_MODEL)
            
            # Registrar subagentes en el orquestador
            self.orchestrator.register_subagent("sombrero_amarillo", self.subagent_sombrero_amarillo)
            self.orchestrator.register_subagent("sombrero_negro", self.subagent_sombrero_negro)
            
            logger.info("Todos los agentes inicializados correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando agentes: {str(e)}")
            st.error(f"Error inicializando el sistema: {str(e)}")

    async def process_message(self, message: str) -> str:
        """Procesa un mensaje de forma asíncrona usando el orquestador"""
        try:
            response = await self.orchestrator.process_task(message)
            return response
        except Exception as e:
            logger.error(f"Error procesando mensaje: {str(e)}")
            return f"Error procesando la consulta: {str(e)}"
    
    def run(self):
        """Ejecuta la interfaz de chat"""
        st.set_page_config(
            page_title=settings.CHAT_TITLE,
            page_icon="🤖",
            layout="wide"
        )
        
        st.title(settings.CHAT_TITLE)
        st.markdown(settings.CHAT_DESCRIPTION)
        
        # Sidebar con información del sistema
        with st.sidebar:
            st.header("Estado del Sistema")
            if self.orchestrator:
                st.success("✅ Orquestador: Activo")
                st.success("✅ SubagentSombreroAmarillo: Activo") 
                st.success("✅ SubagentSombreroNegro: Activo")
            else:
                st.error("❌ Sistema no inicializado")
            
            st.header("Información de Agentes")
            if self.subagent_sombrero_amarillo:
                sombrero_amarillo_info = self.subagent_sombrero_amarillo.get_capabilities()
                st.json(sombrero_amarillo_info)
            
            if self.subagent_sombrero_negro:
                sombrero_negro_info = self.subagent_sombrero_negro.get_capabilities()
                st.json(sombrero_negro_info)
        
        # Chat principal
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Mostrar historial de chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input del usuario
        if prompt := st.chat_input("Escribe tu mensaje aquí..."):
            # Añadir mensaje del usuario
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Procesar con el orquestador
            with st.chat_message("assistant"):
                with st.spinner("Procesando con el sistema multiagente..."):
                    try:
                        # Crear un nuevo event loop para el procesamiento asíncrono
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        # Ejecutar el procesamiento asíncrono
                        response = loop.run_until_complete(self.process_message(prompt))
                        
                        # Cerrar el loop
                        loop.close()
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"Error procesando la consulta: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

def main():
    """Función principal para ejecutar la interfaz"""
    chat = ChatInterface()
    chat.run()

if __name__ == "__main__":
    main()