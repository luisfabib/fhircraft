#!/usr/bin/env python
import typer
from fhircraft.mapping import convert_response_from_api_to_fhir
from fhircraft.openapi.parser import load_openapi
from fhircraft.utils import load_file
from pydantic import ValidationError
from rich import print, print_json
from rich.table import Table
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def convert_api_to_fhir(
        api_response: Annotated[str, typer.Argument(help="Path to the JSON file")],
        openapi_spec: Annotated[str, typer.Argument(help="Path to the OpenAPI specification file")],
        endpoint: Annotated[str, typer.Argument(help="API Enpoint used to obtain the JSON file")],
        method: Annotated[str, typer.Argument(help="API HTTP method used to obtain the JSON file")] = 'get',
        status_code: Annotated[int, typer.Argument(help="API status code obtained along the JSON file")] = 200,
        format: Annotated[str, typer.Option(help="Format of the converted FHIR resource")] = 'json'
    ):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        api_response = load_file(api_response)
        progress.add_task(description="Processing...", total=None)
        fhir_response = convert_response_from_api_to_fhir(api_response, openapi_spec, endpoint, method, str(status_code))
        if format=='json':
            print_json(fhir_response.json(indent=2))
        elif format=='yaml':
            print(fhir_response.yaml(indent=2))
        elif format=='xml':
            print(fhir_response.xml(pretty_print=True))


@app.command()
def convert_fhir_to_api():
    pass


@app.command()
def validate_openapi_specs(openapi_spec: str):
    try:
        load_openapi(openapi_spec)
    except ValidationError as exc: 
        console = Console()
        table = Table("Field", "Error","Message")
        for error in exc.errors():
            table.add_row('.'.join(error['loc']), error['type'], error['msg'])
        console.print(f'[red]:x: The OpenAPI specification is not valid and contains the following errors:', table, style='red')
        raise typer.Exit(code=1)
    print('[green]:heavy_check_mark: Successfully validated the OpenAPI specification. No errors found.')


if __name__ == "__main__":
    app()