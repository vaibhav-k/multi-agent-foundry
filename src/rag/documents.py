"""
Enterprise document loader.

Loads and enriches enterprise knowledge documents.

Supported formats:

- Markdown (.md)
- Text (.txt)

Pipeline:

File
 |
 v
Document Loader
 |
 v
Metadata Extraction
 |
 v
Chunking
 |
 v
Azure AI Search
"""

from pathlib import Path
from typing import Dict, List

import re

from src.config import get_logger

logger = get_logger(__name__)


class DocumentLoader:
    """
    Loads enterprise documents.

    Adds metadata required for:

    - Retrieval
    - Reranking
    - Citations
    - Evaluation
    """

    SUPPORTED_EXTENSIONS = {
        ".md",
        ".txt",
    }

    def __init__(
        self,
        directory: str = "src/rag/sample_docs",
    ):

        self.directory = Path(directory)

    def load_documents(
        self,
    ) -> List[Dict[str, str]]:
        """
        Load all enterprise documents.

        Returns:

        [
            {
                "document_id": "...",
                "source": "...",
                "title": "...",
                "category": "...",
                "content": "..."
            }
        ]
        """

        documents = []

        for file in self.directory.glob("*"):

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            content = file.read_text(
                encoding="utf-8",
            )

            metadata = self.extract_metadata(
                file,
                content,
            )

            document = {
                "document_id": metadata["document_id"],
                "source": file.name,
                "title": metadata["title"],
                "category": metadata["category"],
                "content": content,
            }

            documents.append(document)

            logger.info(
                "Loaded document: %s",
                file.name,
            )

        logger.info(
            "Loaded %s enterprise documents",
            len(documents),
        )

        return documents

    def extract_metadata(
        self,
        file: Path,
        content: str,
    ) -> Dict[str, str]:
        """
        Extract document metadata.

        Currently uses:

        - filename
        - markdown title
        - keyword classification
        """

        document_id = self._create_document_id(
            file.name,
        )

        title = self.extract_title(
            content,
            file.stem,
        )

        category = self.detect_category(
            content,
            file.name,
        )

        return {
            "document_id": document_id,
            "title": title,
            "category": category,
        }

    def extract_title(
        self,
        content: str,
        fallback: str,
    ) -> str:
        """
        Extract first markdown heading.
        """

        match = re.search(
            r"^#\s+(.*)",
            content,
            re.MULTILINE,
        )

        if match:

            return match.group(1).strip()

        return fallback.replace(
            "_",
            " ",
        ).title()

    def detect_category(
        self,
        content: str,
        filename: str,
    ) -> str:
        """
        Infer document category.

        Used for ranking/filtering.
        """

        text = (filename + " " + content).lower()

        categories = {
            "network": [
                "vpn",
                "network",
                "wifi",
                "firewall",
            ],
            "security": [
                "security",
                "password",
                "mfa",
                "authentication",
            ],
            "software": [
                "install",
                "application",
                "software",
            ],
            "onboarding": [
                "employee",
                "joining",
                "onboarding",
            ],
        }

        for category, keywords in categories.items():

            for keyword in keywords:

                if keyword in text:

                    return category

        return "general"

    def _create_document_id(
        self,
        filename: str,
    ) -> str:
        """
        Create Azure Search compatible ID.
        """

        return re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            filename.replace(
                ".md",
                "",
            ),
        )
