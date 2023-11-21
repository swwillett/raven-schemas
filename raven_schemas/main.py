import json
import sys
from pathlib import Path
from pprint import pprint
from typing import List

import click

from raven_schemas import schemas, validate


@click.group()
def raven_schemas():
    pass


@raven_schemas.command()
@click.option(
    "-s",
    "--schema-name",
    type=click.Choice(schemas.get_known_schemas_and_versions().keys()),
    required=True,
)
@click.option("-v", "--schema-version", multiple=True)
@click.option("-f", "--json-file", type=click.Path(exists=True), required=True)
def validate_file(schema_name: str, schema_version: List[str], json_file: Path):
    """
    Validate a JSON file against the given schema.
    If versions are provided, the file will be validated against those versions.
    If no versions are provided, the file will be validated against all known versions of the schema.
    """
    if not schema_version:
        schema_version = schemas.get_known_schemas_and_versions()[schema_name]
        print(f"Checking known versions of {schema_name} schema: {schema_version}.")

    with open(json_file) as f:
        json_data = json.load(f)

    try:
        versions = validate.find_valid_versions(json_data, schema_name, schema_version)
    except validate.ValidationError as e:
        print(e)
        sys.exit(1)
    else:
        print(f"✅ File is valid for {schema_name} version(s): {versions}")


@raven_schemas.command()
def list_schemas():
    """Return a list of schema names and versions"""
    print("Known schemas and versions:")
    pprint(schemas.get_known_schemas_and_versions())
