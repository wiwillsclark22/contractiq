import textwrap

from contract_tools import extract_docx_text, split_into_clauses
from flag_rules import find_flags, load_registry

registry = load_registry()
paragraphs = extract_docx_text("sample_contract.docx")
clauses = split_into_clauses(paragraphs)

total_flags = 0
flags_with_authority = 0

for clause in clauses:
    for flag in find_flags(clause):
        rule = flag["rule"]
        total_flags += 1
        print(f"FLAG {total_flags}: {rule['name']}")
        print(f"  Where:    Section {clause['number']} ({clause['heading']})")
        print(f"  Found:    \"{flag['matched_text']}\"")
        print(f"  Why:      {rule['why']}")

        if rule["authority_ids"]:
            flags_with_authority += 1
            for source_id in rule["authority_ids"]:
                source = registry[source_id]
                print(f"  Authority: {source['title']} - {source['citation']}")
                print(f"             (verified {source['date_last_verified']})")
            note = textwrap.fill(rule["authority_note"], width=88,
                                 initial_indent="  Note:     ", subsequent_indent="            ")
            print(note)
        else:
            print("  Authority: none in the registry yet - needs research before relying on this")

        print(f"  Ask an attorney: {rule['question']}")
        print()

print(f"Total flags: {total_flags}")
print(f"Flags with verified authority: {flags_with_authority}")
print(f"Flags still needing research: {total_flags - flags_with_authority}")
