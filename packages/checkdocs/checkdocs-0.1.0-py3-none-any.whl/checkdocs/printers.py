from typing import Dict, List

from rich.console import Console
from rich.table import Table


def printer(results: List[Dict]) -> None:
    console = Console()
    formatted_result = output_formatter(results)
    if len(formatted_result["errors_log_table"]) > 0:
        print_error_log_table(formatted_result["errors_log_table"])
    else:
        console.print("[bold green]No errors found![/bold green]")

    print_summary(formatted_result)


def output_formatter(results: List[Dict]) -> Dict:
    ok_quantity = 0
    error_quantity = 0
    files_quantity = len(results)
    for result in results:
        for row in result["result"]:
            if row["ok"]:
                ok_quantity += row["ok"]
            if row["error"]:
                error_quantity += row["error"]

    errors_log_table = []
    for result in results:
        for row in result["result"]:
            for log in row["error_log"]:
                errors_log_table.append(
                    {
                        "filename": result["name"],
                        "function_name": row["name"],
                        "error_log": log,
                    }
                )

    summary_result = {
        "oks_quantity": ok_quantity,
        "errors_quantity": error_quantity,
        "files_quantity": files_quantity,
        "errors_log_table": errors_log_table,
    }

    return summary_result


def print_error_log_table(error_log_table: List[Dict]) -> None:
    table = Table(title="Errors", show_header=True, header_style="bold magenta")

    table.add_column("File", justify="right", style="cyan", no_wrap=True)
    table.add_column("Function", justify="right", style="cyan", no_wrap=True)
    table.add_column("Error", justify="center", style="red", no_wrap=True)

    for row in error_log_table:
        table.add_row(row["filename"], row["function_name"], row["error_log"])

    console = Console()
    console.print(table)


def print_summary(result):
    table = Table(title="Summary", show_header=True, header_style="bold magenta")

    table.add_column("Correct Macthes", justify="center", style="cyan", no_wrap=True)
    table.add_column("Errors", justify="center", style="cyan", no_wrap=True)
    table.add_column("Analyzed files", justify="center", style="cyan", no_wrap=True)

    table.add_row(
        str(result["oks_quantity"]),
        str(result["errors_quantity"]),
        str(result["files_quantity"]),
    )

    console = Console()
    console.print(table)
