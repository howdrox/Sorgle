import json

# Load the JSON data
with open('data/all_professors.json', 'r', encoding='utf-8') as f:
    professors = json.load(f)

# Sort by 'name'
professors_sorted = sorted(professors, key=lambda x: x['name'])

# Add sequential IDs starting from 1
for idx, prof in enumerate(professors_sorted, start=1):
    prof['id'] = idx

# Save to a new JSON file
with open('data/all_professors_sorted.json', 'w', encoding='utf-8') as f:
    json.dump(professors_sorted, f, ensure_ascii=False, indent=2)

print("Professors sorted and IDs added. Output saved to all_professors_sorted.json")