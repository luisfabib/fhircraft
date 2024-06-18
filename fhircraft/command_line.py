#!/usr/bin/env python
import typer
from fhircraft.mapping import convert_response_from_api_to_fhir, convert_response_from_fhir_to_api
from fhircraft.openapi.parser import load_openapi, validate_specs
from fhircraft.fhir.path import fhirpath
from fhir.resources.R4B import get_fhir_model_class
from fhircraft.utils import load_file, ensure_list
from pydantic import ValidationError
from rich import print, print_json
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated
import jsonpath_ng as jsonpath
import json 
import yaml

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
    "Convert an API response into a FHIR resource based on the its OpenAPI specification"
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
def convert_fhir_to_api(
        fhir_response: Annotated[str, typer.Argument(help="Path to the FHIR file")],
        openapi_spec: Annotated[str, typer.Argument(help="Path to the OpenAPI specification file")],
        endpoint: Annotated[str, typer.Argument(help="API Enpoint used to obtain the JSON file")],
        method: Annotated[str, typer.Argument(help="API HTTP method used to obtain the JSON file")] = 'get',
        status_code: Annotated[int, typer.Argument(help="API status code obtained along the JSON file")] = 200,
        format: Annotated[str, typer.Option(help="Format of the converted FHIR resource")] = 'json'
    ):
    "Convert FHIR resource into an API response based on the its OpenAPI specification"
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        fhir_response = load_file(fhir_response)
        progress.add_task(description="Processing...", total=None)
        api_response = convert_response_from_fhir_to_api(fhir_response, openapi_spec, endpoint, method, str(status_code))
        if format=='json':
            print_json(json.dumps(api_response, indent=2))
        elif format=='yaml':
            print(yaml.dump(api_response, indent=2))


@app.command()
def validate_openapi_spec(
        openapi_spec: str
    ):
    "Validate OpenAPI specification"
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:    
        progress.add_task(description="Validating...", total=None)
        validation_errors = validate_specs(openapi_spec)
    if validation_errors:
        console = Console()
        table = Table("OpenAPI specification path", "Error","Error message", leading=2, highlight=True)
        for error in validation_errors:
            location = '.'.join([loc.split('[')[0] if isinstance(loc, str) else f'[{loc}]' for loc in error['loc'] if isinstance(loc, (str, int)) and loc not in ['Schema', 'properties']])
            location = location.replace('function-after','').replace('..','.').replace('.[','[')
            location = f'{location[:30]}(...){location[-70:]}'
            if location.endswith('Reference.$ref'):
                continue
            table.add_row(Text(location, overflow='ellipsis'), error['type'], error['msg'])
        console.print(f'\n :x: VALIDATION FAILED \n\n The OpenAPI specification is not valid and contains the following errors:\n', style='bright_red')
        console.print(table)
        console.print()
        raise typer.Exit(code=1)
    else:
        print('[green]:heavy_check_mark: Successfully validated the OpenAPI specification. No errors found.')



@app.command()
def get_fhir_path(
        fhir_response: Annotated[str, typer.Argument(help="Path to the FHIR file")],
        fhir_path: Annotated[str, typer.Argument(help="FHIRpath to access")],   
    ):
    "Get the value in FHIR resource based on FHIRpath"
    fhir_response = load_file(fhir_response)
    model = get_fhir_model_class(fhir_response.get('resourceType'))
    value = fhirpath.parse(fhir_path).get_value(model.parse_obj(fhir_response))
    value = json.dumps([json.loads(val.json()) if hasattr(val,'json') else val for val in ensure_list(value)], indent=3)
    print(value)    
    
@app.command()
def get_json_path(
        api_response: Annotated[str, typer.Argument(help="Path to the API response file")],
        json_path: Annotated[str, typer.Argument(help="JSONpath to access")],   
    ):
    "Get the value in API response based on JSONpath"
    api_response = load_file(api_response)
    matches = jsonpath.parse(json_path).find(api_response)
    value = json.dumps([match.value for match in ensure_list(matches)], indent=3)
    print(value)    
    
if __name__ == "__main__":
    app()