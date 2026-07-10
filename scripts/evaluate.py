"""
Run evaluation scenarios.

Usage:

    python scripts/evaluate.py --suite rag

    python scripts/evaluate.py --suite security

    python scripts/evaluate.py --suite adversarial
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.bootstrap import create_orchestrator
from src.evaluation.dataset import DatasetLoader
from src.evaluation.evaluator import Evaluator

SAMPLE_DIR = PROJECT_ROOT / "src" / "evaluation" / "samples"


DATASET_SUITES = {
    "rag": "rag_questions.json",
    "security": "security_questions.json",
    "adversarial": "adversarial_questions.json",
}


def get_dataset_path(
    suite: str,
) -> Path:
    """
    Resolve evaluation dataset path.
    """

    if suite not in DATASET_SUITES:
        available = ", ".join(DATASET_SUITES.keys())

        raise ValueError(f"Unknown suite '{suite}'. " f"Available: {available}")

    return SAMPLE_DIR / DATASET_SUITES[suite]


def main() -> None:

    parser = argparse.ArgumentParser(description="Run enterprise AI evaluation")

    parser.add_argument(
        "--suite",
        required=True,
        choices=DATASET_SUITES.keys(),
        help=("Evaluation suite to run " "(rag, security, adversarial)"),
    )

    args = parser.parse_args()

    dataset_path = get_dataset_path(args.suite)

    print("\n========== EVALUATION START ==========\n")

    print(f"Suite: {args.suite}")

    print(f"Dataset: {dataset_path.name}")

    loader = DatasetLoader()

    dataset = loader.load(str(dataset_path))

    orchestrator = create_orchestrator()

    evaluator = Evaluator(orchestrator=orchestrator)

    result = evaluator.evaluate(dataset)

    print("\n========== EVALUATION RESULT ==========\n")

    print(f"Total cases: {result['total_cases']}")

    if "accuracy" in result:
        print(f"Accuracy: {result['accuracy']:.2%}")

    for item in result["results"]:
        if item["retrieval_score"] == 0:

            print("\nFAILED:")
            print(item["question"])

            print("Expected:", item.get("expected_source"))

            print("Retrieved:", item.get("actual_sources"))


if __name__ == "__main__":
    main()
