import json
from mappings.all import SEC_DOCUMENTS_MAPPING

IGNORED_KEYS = {"EX-2.01.INS", "EX-100.CAL","EX-100.LAB","EX-100.PRE","EX-100.REF","EX-100.DEF","EX-101.LAB","EX-101.PRE","EX-101.DEF","EX-101.CAL"}

THRESHOLD = 50  # XPaths with count below this will be filtered out

def process_xpaths(input_file, threshold=THRESHOLD):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    result = {}
    already_mapped = set(SEC_DOCUMENTS_MAPPING.keys())
    skipped = []
    ignored = []
    total_xpaths_removed = 0

    for form_type, xpath_dict in data.items():
        if form_type in already_mapped:
            skipped.append(form_type)
            continue

        if form_type in IGNORED_KEYS:
            ignored.append(form_type)
            continue

        cleaned_xpath_dict = {
            k: v for k, v in xpath_dict.items()
            if not k.endswith('@schemaLocation') and v >= threshold
        }

        original_count = len([k for k in xpath_dict if not k.endswith('@schemaLocation')])
        total_xpaths_removed += original_count - len(cleaned_xpath_dict)

        if not cleaned_xpath_dict:
            continue

        result[form_type] = cleaned_xpath_dict

    output_file = input_file.replace('.json', '_processed.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Input: {input_file}")
    print(f"Total form types: {len(data)}")
    print(f"Threshold: {threshold} (XPaths with count < {threshold} removed)")
    print(f"Total XPaths removed by threshold: {total_xpaths_removed}")
    print(f"\n⏭️  Skipped (already in SEC_DOCUMENTS_MAPPING): {len(skipped)}")
    for k in skipped:
        print(f"   - {k}")
    print(f"\n🚫 Ignored (in IGNORED_KEYS): {len(ignored)}")
    for k in ignored:
        print(f"   - {k}")
    print(f"\n✅ Output → {output_file}")
    print(f"   Form types: {len(result)}")

    return result


if __name__ == "__main__":
    input_file = r"xpaths\xpath_03102026.json"
    process_xpaths(input_file, threshold=THRESHOLD)