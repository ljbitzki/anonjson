#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
anonjson.py — Anonymizes keys and/or values in an arbitrary JSON. Useful for interacting with LLMs without exposing real data.

Usage:
  python anonjson.py input.json                # Write input_anon.json
  cat input.json | python anonjson.py -        # Write 20251101_010203_anon.json
  python anonjson.py input.json --values-only  # Preserves keys, anonymizes only values.

Details:
- If the --output option is not passed, the script will always write automatically.:
  * file:  <name>_anon.json  (ex.: input.json -> input_anon.json)
  * stdin:    YYYYMMDD_HHMMSS_anon.json
"""

import argparse
import json
import sys
from typing import Any, Dict, Tuple, Optional
from pathlib import Path
from datetime import datetime

def _next(counter: Dict[str, int], name: str) -> int:
    counter[name] = counter.get(name, 0) + 1
    return counter[name]

def anonymize_json(obj: Any,
                   key_map: Dict[str, str],
                   val_maps: Dict[str, Dict[Any, str]],
                   counters: Dict[str, int],
                   values_only: bool = False) -> Any:
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            new_key = k
            if not values_only:
                if k not in key_map:
                    idx = _next(counters, "key")
                    key_map[k] = f"key_{idx:04d}"
                new_key = key_map[k]
            new_obj[new_key] = anonymize_json(v, key_map, val_maps, counters, values_only=values_only)
        return new_obj

    if isinstance(obj, list):
        return [anonymize_json(x, key_map, val_maps, counters, values_only=values_only) for x in obj]

    if obj is None:
        return "val_null"
    if isinstance(obj, bool):
        t = "bool"
    elif isinstance(obj, (int, float)):
        t = "num"
    elif isinstance(obj, str):
        t = "str"
    else:
        t = "str"
        obj = str(obj)

    if obj not in val_maps[t]:
        idx = _next(counters, f"val_{t}")
        val_maps[t][obj] = f"val_{t}_{idx:04d}"
    return val_maps[t][obj]

def derive_output_path(input_fp: Optional[str], given_output: Optional[str]) -> Path:
    """Determines the exit path based on parameters"""
    if given_output: # Users can still force a name
        return Path(given_output)

    if not input_fp or input_fp == "-":
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return Path(f"{ts}_anon.json")

    in_path = Path(input_fp)
    if in_path.suffix:
        # Insert _anon before the extension
        return in_path.with_name(f"{in_path.stem}_anon{in_path.suffix}")
    else:
        return in_path.with_name(f"{in_path.name}_anon.json")

def run(input_fp: str,
        output_fp: Optional[str],
        emit_map_fp: Optional[str],
        compact: bool,
        values_only: bool) -> Tuple[Any, Dict[str, Any], Path]:
    # Load the JSON
    if input_fp == "-" or input_fp is None:
        data = json.load(sys.stdin)
    else:
        with open(input_fp, "r", encoding="utf-8") as f:
            data = json.load(f)

    key_map: Dict[str, str] = {}
    val_maps: Dict[str, Dict[Any, str]] = {"str": {}, "num": {}, "bool": {}}
    counters: Dict[str, int] = {}

    anon = anonymize_json(data, key_map, val_maps, counters, values_only=values_only)

    # Sets automatic name if no name is provided -o / --output
    out_path = derive_output_path(input_fp, output_fp)

    # Write output
    with open(out_path, "w", encoding="utf-8") as f:
        if compact:
            json.dump(anon, f, ensure_ascii=False, separators=(",", ":"))
        else:
            json.dump(anon, f, ensure_ascii=False, indent=2)

    # Optional map of original values
    if emit_map_fp:
        full_map = {
            "keys": key_map if not values_only else {},
            "values": {
                "string": val_maps["str"],
                "number": val_maps["num"],
                "bool":   val_maps["bool"],
                "null":   {"null": "val_null"}
            }
        }
        with open(emit_map_fp, "w", encoding="utf-8") as f:
            json.dump(full_map, f, ensure_ascii=False, indent=2)

    return anon, {"keys": key_map, "values": val_maps}, out_path

def main():
    parser = argparse.ArgumentParser(description="Anonymizes keys and/or values of an arbitrary JSON.")
    parser.add_argument("input", help="Input JSON file or '-' for stdin")
    parser.add_argument("-o", "--output", help="(Optional) Forces the output file name.")
    parser.add_argument("--emit-map", help="(Optional) Saves the replacement map in a separate JSON file.")
    parser.add_argument("--compact", action="store_true", help="Compact output (without indentation).")
    parser.add_argument("--values-only", action="store_true", help="Anonymize only the values, preserving the original keys.")
    args = parser.parse_args()

    try:
        _, _, out_path = run(args.input, args.output, args.emit_map, args.compact, args.values_only)
        print(f"Anonymized JSON written in: {out_path}")
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Invalid JSON: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)

if __name__ == "__main__":
    main()
