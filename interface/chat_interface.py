import streamlit as st
import asyncio
from typing import Dict, Any
from agents import OrchestratorAgent, SubagentAlpha, SubagentBeta
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class ChatInterface:
    """
    Interfaz de chat usando Streamlit para el sistema multiagente
    """
    
    def __init__(self):
        self.orchestrator = None
        self.subagent_alpha = None
        self.subagent_beta = None
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Inicializa todos los agentes del sistema"""
        try:
            # Crear agentes
            self.orchestrator = OrchestratorAgent(settings.ORCHESTRATOR_MODEL)
            self.subagent_alpha = SubagentAlpha(settings.SUBAGENT_MODEL)
            self.subagent_beta = SubagentBeta(settings.SUBAGENT_MODEL)
            
            # Registrar subagentes en el orquestador
            self.orchestrator.register_subagent("alpha", self.subagent_alpha)
            self.orchestrator.register_subagent("beta", self.subagent_beta)
            
            logger.info("Todos los agentes inicializados correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando agentes: {str(e)}")
            st.error(f"Error inicializando el sistema: {str(e)}")
    
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
                st.success("✅ SubagentAlpha: Activo") 
                st.success("✅ SubagentBeta: Activo")
            else:
                st.error("❌ Sistema no inicializado")
            
            st.header("Información de Agentes")
            if self.subagent_alpha:
                alpha_info = self.subagent_alpha.get_capabilities()
                st.json(alpha_info)
            
            if self.subagent_beta:
                beta_info = self.subagent_beta.get_capabilities()
                st.json(beta_info)
        
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
                        # Aquí se ejecutaría el procesamiento asíncrono
                        # Por ahora simulamos una respuesta
                        response = f"[Orquestador] Procesando: '{prompt}'\n\n"
                        response += "El orquestador analizará tu consulta y determinará qué subagentes pueden ayudar mejor."
                        
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