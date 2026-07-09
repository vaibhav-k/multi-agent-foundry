from src.orchestrator.state import StateManager


def test_state_creation():

    manager = StateManager()

    state = manager.create("abc", "How do I setup VPN?")

    assert state.conversation_id == "abc"
    assert state.user_message.startswith("How")
