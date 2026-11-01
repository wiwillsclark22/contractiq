import csv
import re

from contract_tools import categorize_clause

# Each rule looks for one risky pattern inside clauses of one category.
# "authority_ids" points to rows in source_registry.csv. An empty list means
# we have NO verified legal source yet, and the report says so honestly.
# "authority_note" says what the sources do and do not tell us, so the
# report never overstates the law.
RULES = [
    {
        "name": "Shortened deadline to sue",
        "category": "Dispute Resolution",
        "pattern": r"brought within [\w-]+ \(\d+\) (?:months?|weeks?|days?)",
        "why": "The contract tries to cut the time to bring a claim far below the normal legal deadline.",
        "question": "Is this shortened deadline enforceable, and does it change if the dispute goes to arbitration?",
        "authority_ids": ["3", "2"],
        "authority_note": "A clause that shortens the time to sue does not bar an action brought within the statutory period (generally three years for contract claims). Whether arbitration changes this was not researched.",
    },
    {
        "name": "One party picks the arbitration rules",
        "category": "Dispute Resolution",
        "pattern": r"rules selected by [A-Z]\w+",
        "why": "One side controls the rules of the dispute process, which can tilt the outcome.",
        "question": "Can the other side be required to use rules that only one party chooses?",
        "authority_ids": ["10"],
        "authority_note": "South Carolina tests arbitration terms for unconscionability (no meaningful choice plus oppressive, one-sided terms) and strongly favors arbitration. The source is a consumer case; between businesses, showing no meaningful choice is usually harder. No case was found on a clause letting one party pick the rules.",
    },
    {
        "name": "Indemnity covers the other side's own negligence",
        "category": "Indemnification",
        "pattern": r"own negligence",
        "why": "You could be asked to pay for harm the other party caused through its own carelessness.",
        "question": "Is an indemnity for the other party's own negligence enforceable in South Carolina, and how clear must the wording be?",
        "authority_ids": ["9"],
        "authority_note": "South Carolina requires clear and unequivocal wording before an indemnity covers the indemnitee's own negligence. This clause names Provider's own negligence expressly, so it may meet that wording standard. Public-policy limits were not researched.",
    },
    {
        "name": "Very low liability cap",
        "category": "Limitation of Liability",
        "pattern": r"\((?:1|2|3)\) months? preceding",
        "why": "The most you could recover is limited to a tiny slice of recent fees, which may be far below a real loss.",
        "question": "Is a cap this low enforceable for a services contract, and are there exceptions such as gross negligence?",
        "authority_ids": ["13", "12"],
        "authority_note": "South Carolina courts generally enforce limitation-of-liability clauses (one case upheld a cap equal to the fee paid, by a 3-2 vote), but disfavor them, read them strictly against the drafter, and can strike them as unconscionable or against public policy. Do not assume this cap is void.",
    },
    {
        "name": "Automatic renewal",
        "category": "Term and Renewal",
        "pattern": r"automatically renews",
        "why": "The contract locks you in again unless you give notice long before the term ends.",
        "question": "What exactly must I do, and by what date, to avoid being renewed?",
        "authority_ids": ["18"],
        "authority_note": "South Carolina's 2024 automatic-renewal law requires advance notice of renewals, but for the Title 37 version the protection covers individuals buying for personal, family or household purposes. It appears not to cover a business customer like the one in this sample. No rule was found limiting the 180-day notice window here, so this is a point to negotiate.",
    },
    {
        "name": "One-sided termination right",
        "category": "Termination",
        "pattern": r"may terminate this Agreement at any time",
        "why": "One party can walk away at any time, while the other has a much harder path out.",
        "question": "Can I negotiate equal termination rights?",
        "authority_ids": ["17"],
        "authority_note": "South Carolina courts let a party end a contract on reasonable notice and find a termination wrongful only if it was arbitrary, malicious, or in bad faith. That case involved a contract with no set term. This contract has a fixed three-year term with a seven-day, no-cause exit for one side only, which the source does not decide.",
    },
    {
        "name": "High monthly late interest",
        "category": "Payment",
        "pattern": r"\d+(?:\.\d+)?% per month",
        "why": "A monthly rate adds up to a very high yearly rate on late payments.",
        "question": "Is this late-payment interest rate allowed in South Carolina?",
        "authority_ids": ["14", "15"],
        "authority_note": "South Carolina lets parties set any interest rate in a signed written contract, and one court enforced 18% per year on past-due accounts. This clause is 3% per month (36% per year). No case on a rate that high was found, and other limits (such as consumer-credit rules or unconscionability) were not researched.",
    },
    {
        "name": "Price can change at any time",
        "category": "Payment",
        "pattern": r"change its prices at any time",
        "why": "Prices can go up without your agreement during the contract.",
        "question": "Can I require advance notice or a cap on price increases?",
        "authority_ids": [],
        "authority_note": "",
    },
    {
        "name": "Long non-compete",
        "category": "Non-Compete",
        "pattern": r"for \w+ \(\d+\) years? afterward",
        "why": "The restriction keeps running for years after the contract ends.",
        "question": "Is a restriction of this length and scope enforceable in South Carolina?",
        "authority_ids": ["16"],
        "authority_note": "South Carolina courts disfavor restraints on competition and enforce them only if reasonable in time and place, necessary for a legitimate interest, not unduly harsh, and supported by consideration. The source is an employee case. This clause limits a customer's purchases, and whether the same test applies was not researched.",
    },
    {
        "name": "Other side owns work made from your materials",
        "category": "Intellectual Property",
        "pattern": r"owned exclusively by [A-Z]\w+",
        "why": "Work based on your logos or recipes could belong entirely to the other party.",
        "question": "Who owns designs created from my logo and materials, and can I get ownership or a broader license?",
        "authority_ids": ["11"],
        "authority_note": "Under federal law copyright starts with the author and moves to someone else only by transfer or work-made-for-hire rules. Those rules (17 U.S.C. sections 101 and 204) are not yet in the registry, so ownership of commissioned designs is unresolved.",
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
