import os
from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def extract_from_pdf(file_path):
    """Extract text from a PDF resume."""

    text = []

    reader = PdfReader(file_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_from_docx(file_path):
    """Extract text from a DOCX resume."""

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text
            )

    return "\n".join(paragraphs)


def extract_from_txt(file_path):
    """Extract text from a TXT resume."""

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


def extract_resume_text(file_path):
    """Automatically select the correct parser."""

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = Path(
        file_path
    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            "Unsupported resume format.\n"
            "Supported formats: PDF, DOCX, TXT"
        )

    if extension == ".pdf":

        return extract_from_pdf(
            file_path
        )

    elif extension == ".docx":

        return extract_from_docx(
            file_path
        )

    elif extension == ".txt":

        return extract_from_txt(
            file_path
        )

    return ""


if __name__ == "__main__":

    print("=" * 60)
    print("RESUME PARSER TEST")
    print("=" * 60)

    print(
        "Supported formats:",
        ", ".join(SUPPORTED_EXTENSIONS)
    )

    print(
        "\nResume parser is ready."
    )