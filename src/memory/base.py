"""
Memory storage interface.
"""

from abc import ABC, abstractmethod

from src.memory.conversation import Conversation


class MemoryStore(ABC):
    """
    Abstract conversation storage.
    """

    @abstractmethod
    def get(
        self,
        conversation_id: str,
    ) -> Conversation:
        pass

    @abstractmethod
    def save(
        self,
        conversation: Conversation,
    ) -> None:
        pass
