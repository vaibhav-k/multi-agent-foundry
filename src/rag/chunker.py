"""
Document chunking module.
"""

import re
from typing import List, Dict


class DocumentChunker:
    """
    Splits documents into searchable chunks.
    """

    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def chunk_documents(
        self,
        documents: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:

        chunks = []

        for document in documents:

            source = document["source"]

            # Azure Search compatible key
            safe_source = re.sub(
                r"[^a-zA-Z0-9_-]",
                "_",
                source,
            )

            content = document["content"]

            words = content.split()

            for index in range(
                0,
                len(words),
                self.chunk_size,
            ):

                chunk_words = words[index : index + self.chunk_size]

                chunks.append(
                    {
                        "chunk_id": f"{safe_source}-{index//self.chunk_size+1}",
                        "source": source,
                        "content": " ".join(chunk_words),
                    }
                )

        return chunks
