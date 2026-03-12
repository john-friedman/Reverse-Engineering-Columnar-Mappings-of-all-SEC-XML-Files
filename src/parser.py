import xml.etree.ElementTree as ET
from io import BytesIO
from os.path import commonprefix

def parser(xml_bytes, mapping):
    rows = []

    for table_name, table_mapping in mapping.items():
        paths = list(table_mapping.keys())
        prefix = commonprefix(paths)
        row_boundary = prefix.rsplit("/", 1)[0] if "/" in prefix else prefix

        empty_row = {col: None for col in table_mapping.values()}
        current_path = []
        current_row = empty_row.copy()

        for event, elem in ET.iterparse(BytesIO(xml_bytes), events=("start", "end")):
            tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag.split(":")[-1]

            if event == "start":
                current_path.append(tag)
            else:
                path = "/" + "/".join(current_path)

                if path in table_mapping:
                    current_row[table_mapping[path]] = elem.text

                if path == row_boundary:
                    current_row["_table"] = table_name
                    rows.append(current_row)
                    current_row = empty_row.copy()

                current_path.pop()

    return rows