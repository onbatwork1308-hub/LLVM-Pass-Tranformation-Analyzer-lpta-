import re
from pathlib import Path

import yaml

DATA_FILE = Path(__file__).parent.parent / "data" / "pass_descriptions.yaml"

_cache = None
_normalized_cache = None

def _normalize(name: str) -> str:
    """
    name: any pass name spelling.
    returns: lowercase, no symbols, no traling 'pass'.  
    """

    name = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    if name.endswith("pass"):
        name = name[:-len("pass")]

    return name

def load_pass_descriptions() -> dict:
    """
    returns: all pass descriptions from the yaml file, loaded once and cached.
    """

    global _cache
    if _cache is None:
        with open(DATA_FILE) as file:
            _cache = yaml.safe_load(file)

    return _cache

def _normalized_descriptions() -> dict:
    """
    returns: yaml descriptions re-keyed by their  normalized name, cached.
    """

    global _normalized_cache

    if _normalized_cache is None:
        raw = load_pass_descriptions()
        _normalized_cache = {_normalize(key): value for key, value in raw.items()}

    return _normalized_cache

def describe_pass(pass_name: str) ->str:
    """
    pass_name: name of the pass, in any casing/style. 
    returns: description, or a fallback message if unknown.
    """

    entry = _normalized_descriptions().get(_normalize(pass_name))

    if entry: 
        return entry.get("description", "No description available.")
    return "Unrecognized pass - description not added yet."
