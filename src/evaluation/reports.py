"""
Evaluation report generation.
"""


def print_report(report):

    print("""
========== EVALUATION REPORT ==========
""")

    print(f"Cases: {report.total_cases}")

    print(f"Retrieval Accuracy: " f"{report.retrieval_accuracy:.2%}")

    print(f"Safety Accuracy: " f"{report.safety_accuracy:.2%}")

    print(f"Average Latency: " f"{report.average_latency:.2f}s")
