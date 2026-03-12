import json
from mappings.all import SEC_DOCUMENTS_MAPPING

IGNORED_KEYS = {"EX-2.01.INS", "EX-100.CAL","EX-100.LAB","EX-100.PRE","EX-100.REF","EX-100.DEF","EX-101.LAB","EX-101.PRE","EX-101.DEF","EX-101.CAL"}

THRESHOLD = 50  # XPaths with count below this will be filtered out

def split_json_by_at_symbol(input_file, threshold=THRESHOLD):
    """
    Split a JSON file into two outputs:
    - One with keys containing '@' (attributes)
    - One without '@' (no attributes)
    
    Logic: For each form type (e.g., 'N-MFP/A', 'QUALIF'), check if ANY of its
    xpath keys contain '@' (excluding @schemaLocation). If at least one does, 
    the entire form type goes to the 'attributes' file. Otherwise, 'no_attributes'.
    
    Skips form types already present in SEC_DOCUMENTS_MAPPING.
    Skips form types in IGNORED_KEYS.
    Filters out individual XPaths with count below threshold.
    """
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    xml_paths_attributes = {}
    xml_paths_no_attributes = {}
    
    already_mapped = set(SEC_DOCUMENTS_MAPPING.keys())
    skipped = []
    ignored = []
    total_xpaths_removed = 0

    for form_type, xpath_dict in data.items():
        # Skip form types already handled in SEC_DOCUMENTS_MAPPING
        if form_type in already_mapped:
            skipped.append(form_type)
            continue

        # Skip ignored keys
        if form_type in IGNORED_KEYS:
            ignored.append(form_type)
            continue

        # Remove @schemaLocation keys and apply threshold filter
        cleaned_xpath_dict = {
            k: v for k, v in xpath_dict.items()
            if not k.endswith('@schemaLocation') and v >= threshold
        }

        # Track how many were removed by threshold
        original_count = len([k for k in xpath_dict if not k.endswith('@schemaLocation')])
        total_xpaths_removed += original_count - len(cleaned_xpath_dict)

        # Skip form types that have no xpaths left after filtering
        if not cleaned_xpath_dict:
            continue

        # Check if ANY remaining xpath key contains '@'
        has_at_symbol = any('@' in xpath for xpath in cleaned_xpath_dict.keys())
        
        if has_at_symbol:
            xml_paths_attributes[form_type] = cleaned_xpath_dict
        else:
            xml_paths_no_attributes[form_type] = cleaned_xpath_dict
    
    # Write outputs
    output_attributes = input_file.replace('.json', '_with_attributes.json')
    output_no_attributes = input_file.replace('.json', '_no_attributes.json')
    
    with open(output_attributes, 'w') as f:
        json.dump(xml_paths_attributes, f, indent=2)
    
    with open(output_no_attributes, 'w') as f:
        json.dump(xml_paths_no_attributes, f, indent=2)
    
    # Summary
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

    print(f"\n✅ WITH '@' (attributes)    → {output_attributes}")
    print(f"   Form types: {len(xml_paths_attributes)}")
    for k in list(xml_paths_attributes.keys())[:5]:
        print(f"   - {k}")
    if len(xml_paths_attributes) > 5:
        print(f"   ... and {len(xml_paths_attributes) - 5} more")
    
    print(f"\n✅ WITHOUT '@' (no attributes) → {output_no_attributes}")
    print(f"   Form types: {len(xml_paths_no_attributes)}")
    for k in list(xml_paths_no_attributes.keys())[:5]:
        print(f"   - {k}")
    if len(xml_paths_no_attributes) > 5:
        print(f"   ... and {len(xml_paths_no_attributes) - 5} more")
    
    return xml_paths_attributes, xml_paths_no_attributes


if __name__ == "__main__":
    input_file = r"xpaths\xpath_03102026.json"
    split_json_by_at_symbol(input_file, threshold=THRESHOLD)