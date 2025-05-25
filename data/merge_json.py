import json
import sys
from pathlib import Path


def load_json_file(path: Path) -> list[dict]:
    """
    Loads a JSON file from disk, expecting a top-level array of objects.
    Returns that array as a Python list of dicts.
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} does not contain a top-level JSON array.")
    return data


def merge_json_lists(file_paths: list[Path], output_path: Path) -> None:
    """
    Given a list of file paths (each pointing to a JSON file containing an array of objects),
    merges them into a single list of objects, filling missing fields with [] or None
    (depending on whether the key is list-typed). Writes the result to output_path.
    """
    # 1) Load all records from each input file
    all_records: list[dict] = []
    for p in file_paths:
        all_records.extend(load_json_file(p))

    # 2) Determine the union of all keys
    all_keys: set[str] = set()
    for rec in all_records:
        all_keys.update(rec.keys())

    # 3) Detect which keys are list-typed (i.e. at least one record has a list under that key)
    list_typed_keys: set[str] = set()
    for rec in all_records:
        for k, v in rec.items():
            if isinstance(v, list):
                list_typed_keys.add(k)

    # 4) Build a new merged list, filling missing keys
    merged_records: list[dict] = []
    for rec in all_records:
        new_rec: dict = {}
        for key in all_keys:
            if key in rec:
                value = rec[key]
                # Convert literal string "None" → actual None
                if value == "None":
                    new_rec[key] = None
                else:
                    new_rec[key] = value
            else:
                # If this key was list-typed somewhere, use []
                if key in list_typed_keys:
                    new_rec[key] = []
                else:
                    new_rec[key] = None
        merged_records.append(new_rec)

        # 4.5) Re-assign numeric IDs to any record where id is None
    existing_ids = [
        rec["id"] for rec in merged_records if isinstance(rec.get("id"), int)
    ]
    max_id = max(existing_ids, default=0)

    for rec in merged_records:
        if rec.get("id") is None:
            max_id += 1
            rec["id"] = max_id

    # 5) Write merged_records back out as a JSON array
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(merged_records, f, ensure_ascii=False, indent=2)

    print(f"Merged {len(all_records)} records into '{output_path}'.")


if __name__ == "__main__":
    """
    Basic usage:
        python merge_jsons.py input1.json input2.json [...] -o merged.json

    You can pass as many input files as you like. The script writes to merged.json (or the path you specify).
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Merge multiple JSON files (arrays of objects) into one, "
        "filling missing fields with [] or null."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Paths to input JSON files (each must contain a top-level array of objects).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="merged.json",
        help="Path for the merged JSON output (default: merged.json).",
    )

    args = parser.parse_args()
    input_paths = [Path(p) for p in args.inputs]
    output_path = Path(args.output)

    # Verify inputs exist
    for p in input_paths:
        if not p.is_file():
            print(f"Error: '{p}' is not a file.")
            sys.exit(1)

    merge_json_lists(input_paths, output_path)
