"""
Enterprise document loader.

Loads markdown and text documents
from the knowledge repository.
"""

from pathlib import Path
from typing import Dict, List

from src.config import get_logger

logger = get_logger(__name__)


class DocumentLoader:
    """
    Loads enterprise documents.

    Supported:
    - Markdown (.md)
    - Text (.txt)
    """

    def __init__(
        self,
        directory: str = "src/rag/sample_docs",
    ):

        self.directory = Path(directory)

    def load_documents(self) -> List[Dict[str, str]]:
        """
        Load all supported documents.

        Returns:

        [
            {
                "source": "vpn.md",
                "content": "..."
            }
        ]
        """

        documents = []

        for file in self.directory.glob("*"):

            if file.suffix.lower() not in [
                ".md",
                ".txt",
            ]:
                continue

            content = file.read_text(encoding="utf-8")

            documents.append(
                {
                    "source": file.name,
                    "content": content,
                }
            )

            logger.info(f"Loaded document: {file.name}")

        logger.info(f"Loaded {len(documents)} documents")

        return documents
