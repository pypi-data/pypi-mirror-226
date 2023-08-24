from pathlib import Path
from typing import List

from rich import print

from checkdocs.checkers.check_file import check_file


def check_folder(folder_path: Path) -> List[dict]:
    py_files = list(folder_path.rglob("*.py"))

    print(f":boom: Found {len(py_files)} Python files!")
    results = []

    for file in py_files:
        result = check_file(file)
        results.append({"name": file.name, "result": result})
    return results
