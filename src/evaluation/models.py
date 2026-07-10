"""
Evaluation domain models.
"""

from pydantic import BaseModel


class EvaluationDataset(BaseModel):
    """
    Collection of evaluation cases.
    """

    cases: list[EvaluationCase]


class EvaluationCase(BaseModel):
    """
    Single evaluation test case.
    """

    question: str

    expected_source: str | None = None

    expected_behavior: str | None = None

    category: str


class EvaluationResult(BaseModel):
    """
    Result of one evaluation execution.
    """

    question: str

    category: str

    retrieval_score: float = 0.0

    answer_score: float = 0.0

    safety_score: float = 0.0

    latency_seconds: float = 0.0

    success: bool = True

    error: str | None = None


class EvaluationReport(BaseModel):
    """
    Complete evaluation report.
    """

    total_cases: int

    retrieval_accuracy: float

    safety_accuracy: float

    average_latency: float

    results: list[EvaluationResult]
