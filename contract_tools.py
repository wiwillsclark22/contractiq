import re
from docx import Document

# Rules for sorting clauses into categories.
# Python checks the clause heading first, then falls back to the clause text.
CATEGORY_KEYWORDS = {
    "Indemnification": ["indemnif", "hold harmless"],
    "Limitation of Liability": ["limitation of liability", "consequential"],
    "Termination": ["terminat"],
    "Term and Renewal": ["renewal", "renews"],
    "Payment": ["payment", "invoice"],
    "Confidentiality": ["confidential"],
    "Intellectual Property": ["intellectual property", "copyright", "owned exclusively"],
    "Non-Compete": ["non-compet", "shall not purchase"],
    "Dispute Resolution": ["dispute", "arbitration"],
}

# A heading looks like "5. Indemnification": digits, a dot, a space, then a short title.
HEADING_PATTERN = re.compile(r"^(\d+)\.\s+(.{1,60})$")


def extract_docx_text(path):
    """Read a Word file and return its non-empty paragraphs as a list of text."""
    document = Document(path)
    paragraphs = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def split_into_clauses(paragraphs):
    """Group paragraphs under the numbered heading that comes before them."""
    clauses = []
    current = {"number": "0", "heading": "Preamble", "paragraphs": []}

    for text in paragraphs:
        match = HEADING_PATTERN.match(text)
        if match:
            clauses.append(current)
            current = {"number": match.group(1), "heading": match.group(2), "paragraphs": []}
        else:
            current["paragraphs"].append(text)

    clauses.append(current)
    return clauses


def categorize_clause(clause):
    """Return a category name for a clause, or 'Other' if nothing matches."""
    heading = clause["heading"].lower()
    body = " ".join(clause["paragraphs"]).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in heading for word in keywords):
            return category

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in body for word in keywords):
            return category

    return "Other"
