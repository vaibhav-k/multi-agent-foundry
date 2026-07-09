"""
RAG quality integration test.
"""

from src.evaluation.dataset import EvaluationDataset


def test_evaluation_dataset():

    dataset = EvaluationDataset().load("src/evaluation/samples/rag_questions.json")

    assert len(dataset) > 0
