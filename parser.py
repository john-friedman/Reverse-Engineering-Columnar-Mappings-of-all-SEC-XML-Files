import warnings
from mappings.mappings import SCHEDULE_13D
import xml.etree.ElementTree as ET


def _strip_ns(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def _find(node, rel_path):
    current = [node]
    for step in rel_path.split("/"):
        next_level = []
        for el in current:
            for child in el:
                if _strip_ns(child.tag) == step:
                    next_level.append(child)
        if not next_level:
            return None
        current = next_level
    return current[0]


def _resolve(node, path_or_paths):
    candidates = [path_or_paths] if isinstance(path_or_paths, str) else path_or_paths
    for path in candidates:
        el = _find(node, path)
        if el is not None and el.text and el.text.strip():
            return el.text.strip()
    return None


def _find_all(root, rel_path):
    current = [root]
    for step in rel_path.split("/"):
        next_level = []
        for el in current:
            for child in el:
                if _strip_ns(child.tag) == step:
                    next_level.append(child)
        if not next_level:
            return []
        current = next_level
    return current


def _leaf_paths(node, prefix=""):
    leaves = []
    for child in node:
        tag = _strip_ns(child.tag)
        path = f"{prefix}/{tag}" if prefix else tag
        text = child.text.strip() if child.text and child.text.strip() else None
        if text and not list(child):
            leaves.append((path, text))
        else:
            leaves.extend(_leaf_paths(child, path))
    return leaves


def parse(xml_path, mapping):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = {}

    for table_name, table_def in mapping.items():
        anchor_path      = table_def["anchor"]
        columns          = table_def["columns"]
        anchor_path_list = [anchor_path] if isinstance(anchor_path, str) else anchor_path

        anchor_nodes = []
        for ap in anchor_path_list:
            nodes = _find_all(root, ap)
            if nodes:
                anchor_nodes = nodes
                break

        if not anchor_nodes:
            results[table_name] = []
            continue

        rows = []
        for anchor_node in anchor_nodes:
            row = {}
            for col_name, col_path in columns.items():
                row[col_name] = _resolve(anchor_node, col_path)
            rows.append(row)

        results[table_name] = rows

    return results


def audit(xml_path, mapping):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for table_name, table_def in mapping.items():
        anchor_path      = table_def["anchor"]
        columns          = table_def["columns"]
        anchor_path_list = [anchor_path] if isinstance(anchor_path, str) else anchor_path

        anchor_nodes = []
        for ap in anchor_path_list:
            nodes = _find_all(root, ap)
            if nodes:
                anchor_nodes = nodes
                break

        if not anchor_nodes:
            continue

        covered = set()
        for path_or_paths in columns.values():
            if isinstance(path_or_paths, str):
                covered.add(path_or_paths)
            else:
                covered.update(path_or_paths)

        for i, anchor_node in enumerate(anchor_nodes):
            for leaf_path, leaf_val in _leaf_paths(anchor_node):
                if leaf_path not in covered:
                    warnings.warn(
                        f"UNMAPPED  table={table_name!r}  row={i+1}"
                        f"  path={leaf_path!r}  value={leaf_val!r}"
                    )


def print_tables(tables):
    for table_name, rows in tables.items():
        print(f"\n{'='*60}")
        print(f"  {table_name}  ({len(rows)} row{'s' if len(rows) != 1 else ''})")
        print(f"{'='*60}")
        if not rows:
            print("  (no data)")
            continue
        for i, row in enumerate(rows):
            if len(rows) > 1:
                print(f"  -- row {i+1} --")
            for col, val in row.items():
                print(f"  {col:<30} {val}")


if __name__ == "__main__":
    xml_file = "data/schedule13d.xml"
    tables = parse(xml_file, SCHEDULE_13D)
    audit(xml_file, SCHEDULE_13D)