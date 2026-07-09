"""
Evaluation dataset loading utilities.
"""

import json
from pathlib import Path


class EvaluationDataset:
    """
    Loads RAG evaluation questions.
    """

    def load(
        self,
        path: str,
    ) -> list[dict]:

        return json.loads(Path(path).read_text(encoding="utf-8"))
