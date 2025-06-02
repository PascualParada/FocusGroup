import sys
import os

# Add the parent directory of 'google_adk_agents' to the Python path
# This assumes the script is run from the repository root or 'test' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from google_adk_agents.base.adk_agent import ADKAgent
    from google_adk_agents.orchestrators.orchestrator_adk import OrchestratorADK
    from google_adk_agents.workers.sub_agent_alpha_adk import SubAgentAlphaADK
    from google_adk_agents.workers.sub_agent_beta_adk import SubAgentBetaADK
    print("Successfully imported ADKAgent, OrchestratorADK, SubAgentAlphaADK, SubAgentBetaADK")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred during import: {e}")
    sys.exit(1)

# Basic instantiation check (optional, but good for catching init errors)
# This requires google.generativeai to be configured, which might not be the case in a simple import test
# For now, we'll rely on the print statement for success if imports work.
# If GOOGLE_API_KEY is available, these could be uncommented, but that makes the test more complex.
# try:
#     # Mock or ensure API key is set if these are to be run
#     # For CI/CD, use mock objects or specific test keys
#     if os.getenv("GOOGLE_API_KEY"):
#         orchestrator = OrchestratorADK(model_name="gemini-1.5-flash") # Use a fast model for testing
#         alpha = SubAgentAlphaADK()
#         beta = SubAgentBetaADK()
#         print("Successfully instantiated ADK agents (if API key was available).")
#     else:
#         print("Skipping agent instantiation check as GOOGLE_API_KEY is not set.")
# except Exception as e:
#     print(f"Error during agent instantiation: {e}")
#     sys.exit(1)

print("ADK Agent import test completed successfully.")
