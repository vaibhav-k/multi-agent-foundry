"""
In-memory conversation store.

Development implementation.

Production replacement:
- Azure Cosmos DB
- Azure Cache for Redis
"""

from src.memory.base import MemoryStore
from src.memory.conversation import Conversation


class InMemoryStore(MemoryStore):
    """
    Simple memory implementation.
    """

    def __init__(self):
        self._store: dict[str, Conversation] = {}

    def get(
        self,
        conversation_id: str,
    ) -> Conversation:

        if conversation_id not in self._store:
            self._store[conversation_id] = Conversation(conversation_id=conversation_id)

        return self._store[conversation_id]

    def save(
        self,
        conversation: Conversation,
    ) -> None:

        self._store[conversation.conversation_id] = conversation
