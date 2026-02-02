import json
from collections import defaultdict

# Load the data
with open("../data/accidents.json", "r") as f:
    data = json.load(f)

cleaned_data = []
seen_locations = defaultdict(list)

for entry in data:
    # Skip entries with null latitude/longitude
    if entry.get("latitude") is None or entry.get("longitude") is None:
        continue

    # Standardize severity
    severity = entry.get("severity", "").strip().capitalize()
    entry["severity"] = severity if severity else "Unknown"

    # Merge duplicates: same location within 1 min
    key = entry["location"]
    timestamp = entry["timestamp"]
    
    duplicates = seen_locations[key]
    merged = False
    for dup in duplicates:
        # simple timestamp difference check (can be improved)
        if abs(int(timestamp.split(":")[2]) - int(dup["timestamp"].split(":")[2])) < 60:
            # merge descriptions
            dup["description"] += " | " + entry.get("description", "")
            merged = True
            break

    if not merged:
        seen_locations[key].append(entry)
        cleaned_data.append(entry)

# Save cleaned data
with open("../data/cleaned_accidents.json", "w") as f:
    json.dump(cleaned_data, f, indent=4)

print(f"Original entries: {len(data)}")
print(f"Cleaned entries: {len(cleaned_data)}")
