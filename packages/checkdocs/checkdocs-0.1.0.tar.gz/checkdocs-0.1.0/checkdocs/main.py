from rich import print
from typer import Argument, Typer
from typing_extensions import Annotated

from checkdocs.checkers.check_file import check_file
from checkdocs.checkers.check_folder import check_folder
from checkdocs.config.config import base_path
from checkdocs.printers import output_formatter, printer

app = Typer()


@app.command()
def file(
    name: Annotated[str, Argument(help="Filename to check. Only [.py] files.")],
):
    file_path = base_path / name
    result = check_file(file_path)
    result = [{"name": name, "result": result}]
    printer(result)


@app.command()
def folder(
    name: Annotated[
        str, Argument(help="Folder name to check. Only [.py] files will be checked.")
    ],
):
    path = base_path / name
    result = check_folder(path)
    printer(result)
