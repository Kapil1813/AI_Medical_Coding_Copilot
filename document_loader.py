"""
document_loader.py

Purpose:
---------
This module is responsible for reading uploaded medical documents
and converting them into plain text that can later be processed
by our AI Medical Coding Agents.

Supported Formats:
- PDF
- DOCX
- TXT
- CSV
"""

import fitz  # PyMuPDF
import pandas as pd
from docx import Document


class DocumentLoader:

    @staticmethod
    def load(uploaded_file):
        """
        Detect file type and extract text.

        Parameters
        ----------
        uploaded_file : Streamlit UploadedFile

        Returns
        -------
        str
            Extracted document text
        """

        if uploaded_file is None:
            return ""

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".pdf"):
            return DocumentLoader.read_pdf(uploaded_file)

        elif file_name.endswith(".docx"):
            return DocumentLoader.read_docx(uploaded_file)

        elif file_name.endswith(".txt"):
            return DocumentLoader.read_txt(uploaded_file)

        elif file_name.endswith(".csv"):
            return DocumentLoader.read_csv(uploaded_file)

        else:
            raise ValueError(f"Unsupported file type: {file_name}")

    @staticmethod
    def read_pdf(uploaded_file):

        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    @staticmethod
    def read_docx(uploaded_file):

        document = Document(uploaded_file)

        paragraphs = []

        for paragraph in document.paragraphs:
            paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    @staticmethod
    def read_txt(uploaded_file):

        return uploaded_file.read().decode("utf-8")

    @staticmethod
    def read_csv(uploaded_file):

        df = pd.read_csv(uploaded_file)

        return df.to_string(index=False)