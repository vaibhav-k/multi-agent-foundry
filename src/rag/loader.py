"""
Document loader.

Loads enterprise knowledge documents
for the RAG pipeline.
"""

from pathlib import Path
from typing import List, Dict

from src.config import get_logger

logger = get_logger(__name__)


class DocumentLoader:
    """
    Loads documents from a directory.

    Supported formats:
    - Markdown (.md)
    - Text (.txt)
    """

    def __init__(
        self,
        document_path: str = "docs",
    ):
        self.document_path = Path(document_path)

    def load_documents(
        self,
    ) -> List[Dict[str, str]]:
        """
        Load all supported documents.

        Returns:
            List of documents containing:

            {
                "content": "...",
                "source": "filename.md"
            }
        """

        documents = []

        if not self.document_path.exists():

            logger.warning(
                "Document path does not exist: %s",
                self.document_path,
            )

            return documents

        for file in self.document_path.iterdir():

            if file.suffix.lower() not in [
                ".md",
                ".txt",
            ]:
                continue

            logger.info(
                "Loading document: %s",
                file.name,
            )

            content = file.read_text(encoding="utf-8")

            documents.append(
                {
                    "content": content,
                    "source": file.name,
                }
            )

        logger.info(
            "Loaded %s documents",
            len(documents),
        )

        return documents
