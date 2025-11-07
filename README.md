# anonjson
## anonjson.py — Anonymizes keys and/or values ​​in an arbitrary JSON.
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
### Example (--values-only):

#### Input:

```
{
    "id": 375,
    "url": "http://localhost:8080/api/dcim/interfaces/375/",
    "display_url": "http://localhost:8080/dcim/interfaces/375/",
    "display": "Et1/1",
    "device": {
        "id": 16,
        "url": "http://localhost:8080/api/dcim/devices/16/",
        "display": "rout-arista-03",
        "name": "rout-arista-03",
        "description": "Swicth Arista"
    },
    "vdcs": [],
    "module": null,
    "name": "Et1/1",
    "label": "",
    "type": {
        "value": "10gbase-t",
        "label": "10GBASE-T (10GE)"
    },
    "enabled": true,
    "description": "",
    "mode": {
        "value": "tagged",
        "label": "Tagueada"
    },
    "rf_role": null,
    "untagged_vlan": {
        "id": 2,
        "url": "http://localhost:8080/api/ipam/vlans/2/",
        "display": "lab-voice (30)",
        "vid": 30,
        "name": "lab-voice",
        "description": "voice-LAB"
    },
    "tagged_vlans": [
        {
            "id": 3,
            "url": "http://localhost:8080/api/ipam/vlans/3/",
            "display": "lab-guests (99)",
            "vid": 99,
            "name": "lab-guests",
            "description": "gesuts-LAB"
        },
        {
            "id": 13,
            "url": "http://localhost:8080/api/ipam/vlans/13/",
            "display": "loc-df5 (950)",
            "vid": 950,
            "name": "loc-df5",
            "description": "vlan-loc-df5"
        }
    ],
    "tags": [],
    "custom_fields": {},
    "created": "2025-11-02T19:08:26.693228Z",
    "last_updated": "2025-11-02T19:52:42.386508Z",
    "count_ipaddresses": 2,
    "count_fhrp_groups": 0,
    "_occupied": false
}
```

#### Output:

```
{
  "id": "val_num_0001",
  "url": "val_str_0001",
  "display_url": "val_str_0002",
  "display": "val_str_0003",
  "device": {
    "id": "val_num_0002",
    "url": "val_str_0004",
    "display": "val_str_0005",
    "name": "val_str_0005",
    "description": "val_str_0006"
  },
  "vdcs": [],
  "module": "val_null",
  "name": "val_str_0003",
  "label": "val_str_0007",
  "type": {
    "value": "val_str_0008",
    "label": "val_str_0009"
  },
  "enabled": "val_bool_0001",
  "description": "val_str_0007",
  "mode": {
    "value": "val_str_0010",
    "label": "val_str_0011"
  },
  "rf_role": "val_null",
  "untagged_vlan": {
    "id": "val_num_0003",
    "url": "val_str_0012",
    "display": "val_str_0013",
    "vid": "val_num_0004",
    "name": "val_str_0014",
    "description": "val_str_0015"
  },
  "tagged_vlans": [
    {
      "id": "val_num_0005",
      "url": "val_str_0016",
      "display": "val_str_0017",
      "vid": "val_num_0006",
      "name": "val_str_0018",
      "description": "val_str_0019"
    },
    {
      "id": "val_num_0007",
      "url": "val_str_0020",
      "display": "val_str_0021",
      "vid": "val_num_0008",
      "name": "val_str_0022",
      "description": "val_str_0023"
    }
  ],
  "tags": [],
  "custom_fields": {},
  "created": "val_str_0024",
  "last_updated": "val_str_0025",
  "count_ipaddresses": "val_num_0003",
  "count_fhrp_groups": "val_num_0009",
  "_occupied": "val_bool_0002"
}
```
