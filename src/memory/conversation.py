"""
Conversation memory models.

Stores short-term conversation history.
"""

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Single conversation message.
    """

    role: str

    content: str


class Conversation(BaseModel):
    """
    Conversation history.

    This represents short-term memory.
    """

    conversation_id: str

    messages: list[Message] = Field(default_factory=list)

    def add_message(
        self,
        role: str,
        content: str,
    ):
        """
        Add a message to conversation history.
        """

        self.messages.append(
            Message(
                role=role,
                content=content,
            )
        )
