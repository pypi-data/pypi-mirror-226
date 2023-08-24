from pathlib import Path
from typing import Any, Dict, List

functions_exclusion_list: List[str] = ["__init__", "__main__"]

docstrings_regex: List[Dict[str, Any]] = [
    {
        "regex": r"{param_name} \([^)]+\)",
        "sep": " ",
        "string_limits": [1, -1],
    },  # var_a (int): ...
    {
        "regex": r"{param_name} \: \S+",
        "sep": ":",
        "string_limits": [None, None],
    },  # var_a : int ...
]

base_path = Path.cwd()
