from pathlib import Path

from pypdf import PdfReader


class RAGLoader:

    def load_pdf(
        self,
        pdf_path: str
    ):

        reader = PdfReader(pdf_path)

        text = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text.append(page_text)

        return "\n".join(text)

    def load_directory(
        self,
        folder: str
    ):

        documents = []

        folder_path = Path(folder)

        for pdf_file in folder_path.glob("*.pdf"):

            documents.append(
                {
                    "name": pdf_file.name,
                    "text": self.load_pdf(
                        str(pdf_file)
                    )
                }
            )

        return documents