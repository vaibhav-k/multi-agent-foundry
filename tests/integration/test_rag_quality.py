"""
RAG quality integration test.
"""

from src.evaluation.dataset import DatasetLoader


def test_evaluation_dataset():

    dataset = DatasetLoader().load("src/evaluation/samples/rag_questions.json")

    assert len(dataset.cases) > 0
