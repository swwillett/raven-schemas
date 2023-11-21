import json
import sys
from pathlib import Path
from typing import List

import click

from raven_schemas import types, validate


@click.group()
def raven_schemas():
    pass


@raven_schemas.command()
@click.option(
    "-s",
    "--schema-name",
    type=click.Choice([s.name for s in types.SchemaName]),
    required=True,
)
@click.option("-v", "--schema-version", multiple=True, required=True)
@click.option("-f", "--json-file", type=click.Path(exists=True), required=True)
def validate_file(schema_name: str, schema_version: List[str], json_file: Path):
    """Validate the given JSON file against the given schema"""
    with open(json_file) as f:
        json_data = json.load(f)

    try:
        versions = validate.find_first_valid_version(
            json_data, types.SchemaName[schema_name], schema_version
        )
    except validate.ValidationError as e:
        print(e)
        sys.exit(1)
    else:
        print(f"Successfully validated {schema_name} version(s): {versions}")
