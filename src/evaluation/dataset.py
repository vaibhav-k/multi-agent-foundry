"""
Evaluation dataset loading utilities.
"""

import json
from pathlib import Path

from src.evaluation.models import (
    EvaluationCase,
    EvaluationDataset,
)


class DatasetLoader:
    """
    Loads evaluation datasets.
    """

    def load(
        self,
        path: str,
    ) -> EvaluationDataset:
        """
        Load evaluation cases from JSON.
        """

        data = json.loads(Path(path).read_text(encoding="utf-8"))

        return EvaluationDataset(cases=[EvaluationCase(**item) for item in data])
