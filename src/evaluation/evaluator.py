"""
Evaluation execution framework.
"""

from src.evaluation.metrics import (
    retrieval_accuracy,
)


class Evaluator:
    """
    Executes evaluation scenarios.
    """

    def __init__(
        self,
        orchestrator,
    ):
        self.orchestrator = orchestrator

    def evaluate(
        self,
        dataset,
    ) -> dict:
        """
        Execute evaluation cases.
        """

        results = []

        for case in dataset.cases:

            workflow = self.orchestrator.run(case.question)

            print("\nQUESTION:")
            print(case.question)

            print("EXPECTED:")
            print(case.expected_source)

            print("ACTUAL SOURCES:")
            print(sources)

            sources = [c.name for c in (workflow.knowledge_output.citations)]

            score = retrieval_accuracy(
                expected=case.expected_source,
                actual=sources,
            )

            results.append(
                {
                    "question": case.question,
                    "retrieval_score": score,
                }
            )

        return {
            "total_cases": len(results),
            "results": results,
            "accuracy": (sum(r["retrieval_score"] for r in results) / len(results)),
        }
