import re


class RAGCleaner:

    def clean(
        self,
        documents
    ):

        cleaned_documents = []

        for document in documents:

            text = document["text"]

            # -----------------------------
            # Remove repeated whitespace
            # -----------------------------

            text = re.sub(
                r"\s+",
                " ",
                text
            )

            # -----------------------------
            # Remove page numbers
            # Example:
            # "Page 12"
            # "12"
            # -----------------------------

            text = re.sub(
                r"\bPage\s+\d+\b",
                "",
                text,
                flags=re.IGNORECASE
            )

            # -----------------------------
            # Remove long copyright lines
            # -----------------------------

            text = re.sub(
                r"Copyright ©.*?reserved\.",
                "",
                text,
                flags=re.IGNORECASE
            )

            # -----------------------------
            # Remove multiple spaces
            # -----------------------------

            text = re.sub(
                r"\s{2,}",
                " ",
                text
            )

            cleaned_documents.append(

                {
                    "name": document["name"],
                    "text": text.strip()
                }

            )

        return cleaned_documents