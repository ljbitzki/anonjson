# anonjson
### anonjson.py — Anonymizes keys and/or values ​​in an arbitrary JSON.
### (Useful for interacting with LLMs without exposing real data.)

Quick anonymization
```
python anonjson.py input.json
```

Input JSON from stdin
```
cat input.json | python anonjson.py -
```

Anonymize only the values, preserving the original keys
```
python anonjson.py input.json --values-only
```

Compact output (without indentation)
```
python anonjson.py input.json --compact
```

Saves the replacement key/value map in a separate JSON file
```
python anonjson.py input.json --emit-map
```
