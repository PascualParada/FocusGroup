from abc import ABC, abstractmethod

class ADKAgent(ABC):
    """
    Abstract base class for all agents in the ADK framework.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Initializes the ADKAgent.

        Args:
            model_name: The name of the model to be used by the agent.
            **kwargs: Additional keyword arguments for common parameters.
        """
        self.model_name = model_name
        # You can initialize other common parameters here
        # For example: self.temperature = kwargs.get('temperature', 0.7)

    @abstractmethod
    def get_instructions(self) -> str:
        """
        Returns the system prompt or instructions for the agent.
        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def process_task(self, task: str, context: dict = None) -> str:
        """
        Processes a given task, potentially using context.
        This method must be implemented by subclasses.

        Args:
            task: The task description string.
            context: An optional dictionary providing additional context for the task.

        Returns:
            A string representing the result or output of the task processing.
        """
        pass

    def get_capabilities(self) -> dict:
        """
        Returns a dictionary describing the capabilities of the agent.
        Subclasses can override this to provide more specific information.

        Returns:
            A dictionary with agent capabilities (e.g., {"version": "1.0"}).
        """
        return {"version": "1.0"}
