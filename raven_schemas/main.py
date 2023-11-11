import json
import os
from enum import Enum
from pathlib import Path

import jsonschema

import click

PACKAGE_DIR = Path(os.path.dirname(__file__))

class SchemaName(Enum):
    modeling_input = 'modeling_input'


def validate_json_single_version(data: dict, schema_name: SchemaName, version: str):
    """Validate the JSON schema for the given schema name at a specific version"""
    version_for_filename = version.replace(".", "_")
    schema_path = PACKAGE_DIR / "schemas" / schema_name.value / f"{schema_name.value}_{version_for_filename}.json"
    with open(schema_path) as f:
        schema = json.load(f)
    return jsonschema.validate(schema=schema, instance=data)

def validate_json(data: dict, schema_name: SchemaName, versions: List[str]):
    """Validate the JSON schema for the given schema name at a specific version"""
    errors = [] # tuples of (version, message)
    for version in versions:
        try:
            validate_json_single_version(json_data, SchemaName[schema_name], version)
            except jsonschema.exceptions.ValidationError as e:
                e.append({'version': version, 'message': e.message})
            except OSError as e:


@click.group()
def raven_schemas():
    pass

@raven_schemas.command()
@click.option("-s", "--schema-name", type=click.Choice([s.name for s in SchemaName]), required=True)
@click.option("-v", "--schema-version", multiple=True, required=True)
@click.option("-f", "--json-file", type=click.Path(exists=True), required=True)
def validate_file(schema_name: str, schema_version: List[str], json_file: Path):
    """Validate the given JSON file against the given schema"""
    with open(json_file) as f:
        json_data = json.load(f)

    errors = []
    for version in schema_version:
        try:
            validate_json(json_data, SchemaName[schema_name], version)
            except jsonschema.exceptions.ValidationError as e:
                e.append({'version': version, 'message': e.message})
