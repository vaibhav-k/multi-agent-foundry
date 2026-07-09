from src.memory.store import InMemoryStore


def test_memory_store():

    store = InMemoryStore()

    conversation = store.get("test")

    conversation.add_message(
        "user",
        "Hello",
    )

    store.save(conversation)

    result = store.get("test")

    assert len(result.messages) == 1
