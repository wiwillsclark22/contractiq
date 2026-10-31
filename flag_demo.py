from contract_tools import extract_docx_text, split_into_clauses, categorize_clause
from flag_rules import find_flags, load_registry

registry = load_registry()
paragraphs = extract_docx_text("sample_contract.docx")
clauses = split_into_clauses(paragraphs)

total_flags = 0

for clause in clauses:
    for flag in find_flags(clause):
        rule = flag["rule"]
        total_flags += 1
        print(f"FLAG {total_flags}: {rule['name']}")
        print(f"  Where:    Section {clause['number']} ({clause['heading']})")
        print(f"  Found:    \"{flag['matched_text']}\"")
        print(f"  Why:      {rule['why']}")

        if rule["authority_ids"]:
            for source_id in rule["authority_ids"]:
                source = registry[source_id]
                print(f"  Authority: {source['citation']} (verified {source['date_last_verified']})")
        else:
            print("  Authority: none in the registry yet - needs research before relying on this")

        print(f"  Ask an attorney: {rule['question']}")
        print()

print(f"Total flags: {total_flags}")
