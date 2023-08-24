import ast
from pathlib import Path
from typing import Dict, List

from checkdocs.checkers.make_check import checkdocs
from checkdocs.config.config import functions_exclusion_list


def check_file(file_path: Path) -> List[Dict]:
    tree = parse_file(file_path)
    functions = get_functions(tree)
    results = []

    if is_list_not_empty(functions):
        for function in functions:
            if function.name in functions_exclusion_list:
                continue

            result = checkdocs(function)
            results.append(result)

    return results


def parse_file(file: Path) -> ast.Module:
    with open(file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    return tree


def get_functions(tree: ast.Module) -> list[ast.FunctionDef]:
    result = [
        tree_function
        for tree_function in ast.walk(tree)
        if isinstance(tree_function, ast.FunctionDef)
    ]

    return result


def is_list_not_empty(list_to_check: List) -> bool:
    return len(list_to_check) > 0
