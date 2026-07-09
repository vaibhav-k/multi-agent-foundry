"""
Agent state lifecycle management.
"""

from src.state.models import AgentState


class StateManager:
    """
    Creates and manages workflow state.
    """

    def create(
        self,
        conversation_id: str,
        message: str,
    ) -> AgentState:
        """
        Create initial workflow state.
        """

        return AgentState(
            conversation_id=conversation_id,
            user_message=message,
        )
