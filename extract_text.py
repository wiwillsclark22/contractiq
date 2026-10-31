from docx import Document


def extract_docx_text(path):
    """Read a Word file and return its non-empty paragraphs as a list of text."""
    document = Document(path)
    paragraphs = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)
    return paragraphs


paragraphs = extract_docx_text("sample_contract.docx")
print(f"Extracted {len(paragraphs)} paragraphs\n")

for number, text in enumerate(paragraphs, start=1):
    print(number, text[:70])
