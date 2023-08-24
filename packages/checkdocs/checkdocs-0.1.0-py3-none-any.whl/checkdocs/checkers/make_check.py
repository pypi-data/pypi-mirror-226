import ast
import re
from typing import Any, Dict

from checkdocs.config.config import docstrings_regex


def checkdocs(function: ast.FunctionDef) -> Dict:
    """
    Check if the docstrings of the function are the same as the parameters.

    Parameters
    ----------
    function : ast.FunctionDef
        Function to check.

    Returns
    -------
    dict
        A dictionary with the following keys:
        - name: the name of the function
        - ok: the number of docstrings that match with the parameters
        - error: the number of docstrings that don't match with the parameters
        - error_log: a list with the names of the variables that don't match

    Examples
    --------

    """
    parameters = get_parameters(function)
    docstring = get_docstrings(function)

    output = {
        "name": function.__dict__["name"],
        "ok": 0,
        "error": 0,
        "error_log": [],
    }

    if docstring:
        for parameter in parameters:
            for regex in docstrings_regex:
                pattern = re.compile(regex["regex"].format(param_name=parameter))
                result: list[Any] = pattern.findall(docstring)

                if not result:
                    continue

                name = result[0].split(regex["sep"])[0].strip()
                docstring_type_hint = (
                    result[0]
                    .split(regex["sep"])[1][
                        regex["string_limits"][0] : regex["string_limits"][1]
                    ]
                    .strip()
                )
                correct_type_hint = parameters[name]

                if docstring_type_hint == correct_type_hint:
                    output["ok"] += 1

                else:
                    output["error_log"].append(  # type: ignore
                        f"[bold red]Variable: {name}[/bold red] | [bold purple]Docstring: {docstring_type_hint} -> Function definition: {correct_type_hint}[/bold purple]"
                    )
                    output["error"] += 1
    return output


def get_parameters(obj) -> dict:
    parameters = {}
    arg_list = list(map(ast.unparse, obj.args.args))
    for arg in arg_list:
        splited_arg = arg.split(":")
        if len(splited_arg) == 2:
            parameters[splited_arg[0].strip()] = splited_arg[1].strip()

    return parameters


def get_docstrings(funcion):
    return ast.get_docstring(funcion)
