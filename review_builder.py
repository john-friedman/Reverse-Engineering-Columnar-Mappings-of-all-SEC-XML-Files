import argparse
import csv
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
import hashlib

from mappings.all import SEC_DOCUMENTS_MAPPING


def _split_camel(token: str):
    return re.findall(r"[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+", token)


def normalize_segment(segment: str) -> str:
    segment = segment.strip()
    if segment.startswith("@"):
        segment = segment[1:]
    segment = segment.replace(":", "_")
    words = []
    for raw in re.split(r"[^A-Za-z0-9]+", segment):
        if not raw:
            continue
        parts = _split_camel(raw) or [raw]
        words.extend([p.lower() for p in parts])
    return " ".join(words)


def normalize_path(path: str):
    return [normalize_segment(seg) for seg in path.strip("/").split("/") if seg]


def jaccard(a_tokens, b_tokens):
    a = set(a_tokens)
    b = set(b_tokens)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def seg_sim(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio()


def path_similarity(raw_path: str, canonical_path: str):
    raw_segs = normalize_path(raw_path)
    can_segs = normalize_path(canonical_path)

    if not raw_segs or not can_segs:
        return 0.0, {}

    raw_leaf = raw_segs[-1]
    can_leaf = can_segs[-1]
    leaf_score = seg_sim(raw_leaf, can_leaf)

    max_len = max(len(raw_segs), len(can_segs))
    depth_score = 1.0 - (abs(len(raw_segs) - len(can_segs)) / max_len)

    tail_n = min(3, len(raw_segs), len(can_segs))
    tail_scores = []
    for i in range(1, tail_n + 1):
        tail_scores.append(seg_sim(raw_segs[-i], can_segs[-i]))
    suffix_score = sum(tail_scores) / len(tail_scores)

    token_score = jaccard(raw_segs, can_segs)

    raw_attr = raw_path.split("/")[-1].startswith("@")
    can_attr = canonical_path.split("/")[-1].startswith("@")
    attr_score = 1.0 if raw_attr == can_attr else 0.0

    score = (
        0.40 * suffix_score
        + 0.25 * leaf_score
        + 0.15 * token_score
        + 0.10 * depth_score
        + 0.10 * attr_score
    )

    metrics = {
        "leaf_score": round(leaf_score, 4),
        "suffix_score": round(suffix_score, 4),
        "token_score": round(token_score, 4),
        "depth_score": round(depth_score, 4),
        "attr_match": bool(raw_attr == can_attr),
    }
    return score, metrics


def choose_action(score: float):
    if score >= 0.97:
        return "auto_add"
    if score >= 0.75:
        return "review"
    return "skip"


def table_lookup(mapping_obj):
    path_to_info = {}
    for table_name, table_map in mapping_obj.items():
        for xpath, out_key in table_map.items():
            path_to_info[xpath] = {"table": table_name, "output_key": out_key}
    return path_to_info


def infer_family(form_type: str):
    if form_type.startswith("ATS-N"):
        return "ATS-N"
    if form_type.startswith("SBSE"):
        return "SBSE"
    if form_type.startswith("CFPORTAL"):
        return "CFPORTAL"
    if form_type.startswith("C"):
        return "C"
    if form_type.startswith("N-MFP"):
        return "N-MFP"
    return form_type


def build_review_rows(xpaths_data):
    rows = []

    for form_type, xpath_counts in xpaths_data.items():
        mapping_obj = SEC_DOCUMENTS_MAPPING.get(form_type)
        if not mapping_obj:
            continue

        canonical = table_lookup(mapping_obj)
        canonical_paths = list(canonical.keys())
        canonical_set = set(canonical_paths)

        for raw_xpath, count in xpath_counts.items():
            if raw_xpath.endswith("@schemaLocation"):
                continue
            if raw_xpath in canonical_set:
                continue
            if not canonical_paths:
                continue

            best_path = None
            best_score = -1.0
            best_metrics = {}

            for can_path in canonical_paths:
                score, metrics = path_similarity(raw_xpath, can_path)
                if score > best_score:
                    best_score = score
                    best_path = can_path
                    best_metrics = metrics

            out_info = canonical[best_path]
            action = choose_action(best_score)

            match_reasons = []
            if best_metrics["leaf_score"] >= 0.90:
                match_reasons.append("leaf_match")
            if best_metrics["suffix_score"] >= 0.90:
                match_reasons.append("suffix_match")
            if best_metrics["token_score"] >= 0.70:
                match_reasons.append("token_overlap")
            if best_metrics["attr_match"]:
                match_reasons.append("attribute_alignment")
            if best_metrics["depth_score"] >= 0.80:
                match_reasons.append("depth_alignment")

            rows.append(
                {
                    "record_id": hashlib.sha1(f"{form_type}|{raw_xpath}".encode("utf-8")).hexdigest()[:16],
                    "form": form_type,
                    "family": infer_family(form_type),
                    "count": count,
                    "raw_xpath": raw_xpath,
                    "normalized_xpath": "/" + "/".join(normalize_path(raw_xpath)),
                    "suggested_canonical_xpath": best_path,
                    "suggested_table": out_info["table"],
                    "suggested_output_key": out_info["output_key"],
                    "confidence": round(best_score, 4),
                    "match_reasons": match_reasons,
                    "action": action,
                    "review_status": "pending",
                    "reviewer_choice": None,
                    "review_notes": None,
                }
            )

    rows.sort(key=lambda r: (r["form"], -r["count"], -r["confidence"], r["raw_xpath"]))
    return rows


def main():
    parser = argparse.ArgumentParser(description="Build review.jsonl for malformed/new XPath alias review.")
    parser.add_argument(
        "--input",
        default=r"xpaths\xpath_03102026.json",
        help="Path to XPath frequency JSON.",
    )
    parser.add_argument(
        "--pairs-csv",
        default="review_pairs.csv",
        help="CSV with raw_xpath and suggested_canonical_xpath.",
    )
    parser.add_argument(
        "--xref-csv",
        default="review_xref.csv",
        help="CSV with raw_xpath, suggested table, and form.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    pairs_csv_path = Path(args.pairs_csv)
    xref_csv_path = Path(args.xref_csv)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    rows = build_review_rows(data)

    # File 1: rawxpath,suggestedxpath
    with pairs_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["raw_xpath", "suggested_xpath"])
        for row in rows:
            writer.writerow([row["raw_xpath"], row["suggested_canonical_xpath"]])

    # File 2: xpath,table,form
    with xref_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["xpath", "table", "form"])
        for row in rows:
            writer.writerow([row["raw_xpath"], row["suggested_table"], row["form"]])

    auto_add = sum(1 for r in rows if r["action"] == "auto_add")
    review = sum(1 for r in rows if r["action"] == "review")
    skip = sum(1 for r in rows if r["action"] == "skip")

    print(f"Input: {input_path}")
    print(f"Output (pairs csv): {pairs_csv_path}")
    print(f"Output (xref csv): {xref_csv_path}")
    print(f"Rows: {len(rows)}")
    print(f"Actions -> auto_add: {auto_add}, review: {review}, skip: {skip}")


if __name__ == "__main__":
    main()
