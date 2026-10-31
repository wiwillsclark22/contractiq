import csv
import re

from contract_tools import categorize_clause

# Each rule looks for one risky pattern inside clauses of one category.
# "authority_ids" points to rows in source_registry.csv. An empty list means
# we have NO verified legal source yet, and the report says so honestly.
RULES = [
    {
        "name": "Shortened deadline to sue",
        "category": "Dispute Resolution",
        "pattern": r"brought within [\w-]+ \(\d+\) (?:months?|weeks?|days?)",
        "why": "The contract tries to cut the time to bring a claim far below the normal legal deadline.",
        "question": "Is this shortened deadline enforceable, and does it change if the dispute goes to arbitration?",
        "authority_ids": ["3", "2"],
    },
    {
        "name": "One party picks the arbitration rules",
        "category": "Dispute Resolution",
        "pattern": r"rules selected by [A-Z]\w+",
        "why": "One side controls the rules of the dispute process, which can tilt the outcome.",
        "question": "Can the other side be required to use rules that only one party chooses?",
        "authority_ids": [],
    },
    {
        "name": "Indemnity covers the other side's own negligence",
        "category": "Indemnification",
        "pattern": r"own negligence",
        "why": "You could be asked to pay for harm the other party caused through its own carelessness.",
        "question": "Is an indemnity for the other party's own negligence enforceable in South Carolina, and how clear must the wording be?",
        "authority_ids": [],
    },
    {
        "name": "Very low liability cap",
        "category": "Limitation of Liability",
        "pattern": r"\((?:1|2|3)\) months? preceding",
        "why": "The most you could recover is limited to a tiny slice of recent fees, which may be far below a real loss.",
        "question": "Is a cap this low enforceable for a services contract, and are there exceptions such as gross negligence?",
        "authority_ids": [],
    },
    {
        "name": "Automatic renewal",
        "category": "Term and Renewal",
        "pattern": r"automatically renews",
        "why": "The contract locks you in again unless you give notice long before the term ends.",
        "question": "What exactly must I do, and by what date, to avoid being renewed?",
        "authority_ids": [],
    },
    {
        "name": "One-sided termination right",
        "category": "Termination",
        "pattern": r"may terminate this Agreement at any time",
        "why": "One party can walk away at any time, while the other has a much harder path out.",
        "question": "Can I negotiate equal termination rights?",
        "authority_ids": [],
    },
    {
        "name": "High monthly late interest",
        "category": "Payment",
        "pattern": r"\d+(?:\.\d+)?% per month",
        "why": "A monthly rate adds up to a very high yearly rate on late payments.",
        "question": "Is this late-payment interest rate allowed in South Carolina?",
        "authority_ids": [],
    },
    {
        "name": "Price can change at any time",
        "category": "Payment",
        "pattern": r"change its prices at any time",
        "why": "Prices can go up without your agreement during the contract.",
        "question": "Can I require advance notice or a cap on price increases?",
        "authority_ids": [],
    },
    {
        "name": "Long non-compete",
        "category": "Non-Compete",
        "pattern": r"for \w+ \(\d+\) years? afterward",
        "why": "The restriction keeps running for years after the contract ends.",
        "question": "Is a restriction of this length and scope enforceable in South Carolina?",
        "authority_ids": [],
    },
    {
        "name": "Other side owns work made from your materials",
        "category": "Intellectual Property",
        "pattern": r"owned exclusively by [A-Z]\w+",
        "why": "Work based on your logos or recipes could belong entirely to the other party.",
        "question": "Who owns designs created from my logo and materials, and can I get ownership or a broader license?",
        "authority_ids": [],
    },
]


def load_registry(path="source_registry.csv"):
    """Read the source registry into a dictionary keyed by source id."""
    with open(path, newline="", encoding="utf-8") as file:
        return {row["id"]: row for row in csv.DictReader(file)}


def find_flags(clause):
    """Return a list of flags found in one clause."""
    category = categorize_clause(clause)
    text = " ".join(clause["paragraphs"])
    flags = []

    for rule in RULES:
        if rule["category"] != category:
            continue
        match = re.search(rule["pattern"], text)
        if match:
            flags.append({"rule": rule, "matched_text": match.group(0)})

    return flags
