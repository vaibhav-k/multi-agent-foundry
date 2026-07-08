"""
Tests for agent prompt templates.
"""

from pathlib import Path

PROMPT_DIR = Path("src/prompts")


def test_prompt_directory_exists():

    assert PROMPT_DIR.exists()


def test_system_prompt_exists():

    prompt = PROMPT_DIR / "system.txt"

    assert prompt.exists()


def test_planner_prompt_exists():

    prompt = PROMPT_DIR / "planner.txt"

    assert prompt.exists()


def test_knowledge_prompt_exists():

    prompt = PROMPT_DIR / "knowledge.txt"

    assert prompt.exists()


def test_safety_prompt_exists():

    prompt = PROMPT_DIR / "safety.txt"

    assert prompt.exists()
