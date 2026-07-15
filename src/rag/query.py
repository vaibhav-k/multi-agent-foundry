"""
Query transformation utilities.

Improves user questions before sending them
to Azure AI Search.
"""

import re


class QueryRewriter:
    """
    Converts natural language questions into
    search-optimized queries.

    Responsibilities:

    - Normalize whitespace
    - Remove conversational filler
    - Expand enterprise abbreviations
    - Normalize casing
    - Preserve search intent
    """

    ABBREVIATIONS = {
        "VPN": "VPN virtual private network",
        "MFA": "MFA multi factor authentication",
        "SSO": "SSO single sign on",
        "IT": "IT information technology",
    }

    FILLER_PHRASES = [
        "can you please tell me",
        "can you tell me",
        "please tell me",
        "could you please tell me",
        "could you tell me",
        "please explain",
        "i want to know",
        "tell me",
    ]

    def rewrite(
        self,
        question: str,
    ) -> str:
        """
        Rewrite user query for retrieval.

        Converts conversational language into
        a concise search query.
        """

        if not question:
            return ""

        query = question.strip()

        query = self._normalize_whitespace(query)

        query = self._remove_filler(query)

        query = self._expand_abbreviations(query)

        query = self._normalize_case(query)

        query = self._normalize_spacing(query)

        return query

    def _normalize_whitespace(
        self,
        text: str,
    ) -> str:
        """
        Collapse repeated whitespace.
        """

        return re.sub(
            r"\s+",
            " ",
            text,
        )

    def _remove_filler(
        self,
        text: str,
    ) -> str:
        """
        Remove conversational phrases.
        """

        lowered = text.lower()

        for phrase in self.FILLER_PHRASES:
            if lowered.startswith(phrase):
                text = text[len(phrase) :].strip()
                break

        return text

    def _expand_abbreviations(
        self,
        text: str,
    ) -> str:
        """
        Expand enterprise terms.
        """

        for short, expanded in self.ABBREVIATIONS.items():

            text = re.sub(
                rf"\b{short}\b",
                expanded,
                text,
                flags=re.IGNORECASE,
            )

        return text

    def _normalize_case(
        self,
        text: str,
    ) -> str:
        """
        Normalize casing while preserving
        enterprise acronyms.
        """

        words = []

        for word in text.split():

            # Preserve enterprise acronyms
            if word.isupper() and len(word) > 1:
                words.append(word)

            # Normalize standalone pronoun
            elif word == "I":
                words.append("i")

            else:
                words.append(word.lower())

        normalized = " ".join(words)

        # Preserve sentence casing
        if normalized:
            normalized = normalized[0].upper() + normalized[1:]

        return normalized

    def _normalize_spacing(
        self,
        text: str,
    ) -> str:
        """
        Preserve punctuation formatting.
        """

        return re.sub(
            r"\s+([?.!,])",
            r"\1",
            text,
        )
