import pytest
import asyncio
from agents import OrchestratorAgent, SubagentAlpha, SubagentBeta

class TestMultiAgentIntegration:
    """Tests de integración para el sistema multiagente"""
    
    @pytest.fixture
    def setup_agents(self):
        """Configura los agentes para testing"""
        orchestrator = OrchestratorAgent()
        alpha = SubagentAlpha()
        beta = SubagentBeta()
        
        orchestrator.register_subagent("alpha", alpha)
        orchestrator.register_subagent("beta", beta)
        
        return orchestrator, alpha, beta
    
    def test_agent_initialization(self, setup_agents):
        """Prueba la inicialización de agentes"""
        orchestrator, alpha, beta = setup_agents
        
        assert orchestrator is not None
        assert alpha is not None
        assert beta is not None
        assert len(orchestrator.get_available_subagents()) == 2
    
    def test_subagent_capabilities(self, setup_agents):
        """Prueba las capacidades de los subagentes"""
        _, alpha, beta = setup_agents
        
        alpha_caps = alpha.get_capabilities()
        beta_caps = beta.get_capabilities()
        
        assert alpha_caps["name"] == "SubagentAlpha"
        assert beta_caps["name"] == "SubagentBeta"
        assert alpha_caps["status"] == "Activo"
        assert beta_caps["status"] == "Activo"