#!/usr/bin/env python
import typer
from fhircraft.mapping import convert_response_from_api_to_fhir
from fhircraft.openapi.parser import load_openapi
from fhircraft.utils import load_file
from pydantic import ValidationError
from rich import print, print_json
from rich.table import Table
from rich.console import Console
app = typer.Typer()
from rich.progress import Progress, SpinnerColumn, TextColumn

@app.command()
def convert_api_to_fhir(api_response: str, openapi_spec: str, enpoint: str, method: str, status_code: str, profile_url: str = None):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        api_response = load_file(api_response)
        progress.add_task(description="Processing...", total=None)
        fhir_response = convert_response_from_api_to_fhir(api_response, openapi_spec, enpoint, method, status_code)
        print_json(fhir_response.json(indent=2))


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