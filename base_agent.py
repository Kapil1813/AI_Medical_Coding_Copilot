"""
base_agent.py

Base class for all AI Agents.
"""

from abc import ABC, abstractmethod
from models.workflow_state import WorkflowState


class BaseAgent(ABC):

    @abstractmethod
    def run(self, state: WorkflowState) -> WorkflowState:
        """
        Executes the AI Agent.
        """
        pass