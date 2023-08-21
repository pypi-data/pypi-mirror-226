import json
import sys

data = [
    {
        "a": "Abc",
        "b": 1,
        "c": ["a", "b", "c"],
        "d": {
            "p": "pqr"
        },
        "e": 2.5,
        "f": True
    },
    {
        "a1": "Abc",
        "b1": 1,
        "c1": ["a", "b", "c"],
        "d1": {
            "p": "pqr"
        },
        "e1": 2.5,
        "f1": True
    },
    {
        "a2": "Abc",
        "b2": 1,
        "c2": ["a", "b", "c"],
        "d2": {
            "p": "pqr"
        },
        "e2": 2.5,
        "f2": True
    },
    {
        "a3": "Abc",
        "b3": 1,
        "c3": ["a", "b", "c"],
        "d3": {
            "p": "pqr"
        },
        "e3": 2.5,
        "f3": True
    },
    {
        "a4": "Abc",
        "b4": 1,
        "c4": ["a", "b", "c"],
        "d4": {
            "p": "pqr"
        },
        "e4": 2.5,
        "f4": True
    },
    {
        "a5": "Abc",
        "b5": 1,
        "c5": ["a", "b", "c"],
        "d5": {
            "p": "pqr"
        },
        "e5": 2.5,
        "f5": True
    },
]
print(data)
print(f'Memory Size of data: {sys.getsizeof(data)}')  # 44
json_str = json.dumps(data)
print(json_str)
print(type(json_str))
print(f'Length of json string: {len(json_str)}')  # 174 char
print(f'Memory Size of json string: {sys.getsizeof(json_str)}')  # 199
print(f'Size of json string: {len(json_str.encode("utf-8"))}')  # 174 bytes

MAX_JSON_SIZE = 128 # 128 * 1024 * 1024 (134217728)bytes

if len(json_str) > MAX_JSON_SIZE:
    print(f'Sending in batches')
else:
   print(f'Sending in one chunk')