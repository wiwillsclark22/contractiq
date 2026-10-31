import csv

with open("source_registry.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    sources = list(reader)

print(f"Loaded {len(sources)} sources\n")

for source in sources:
    print(source["id"], "-", source["citation"])
    print("   Type:", source["authority_type"])
    print("   Verified on:", source["date_last_verified"])
    print()
