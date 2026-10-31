from contract_tools import extract_docx_text, split_into_clauses, categorize_clause

paragraphs = extract_docx_text("sample_contract.docx")
clauses = split_into_clauses(paragraphs)

print(f"Found {len(clauses)} sections\n")

counts = {}
for clause in clauses:
    category = categorize_clause(clause)
    counts[category] = counts.get(category, 0) + 1
    words = len(" ".join(clause["paragraphs"]).split())
    print(f"{clause['number']:>2}. {clause['heading']:<26} -> {category:<24} ({words} words)")

print("\nCategory totals:")
for category, count in counts.items():
    print(f"  {category}: {count}")
