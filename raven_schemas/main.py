import json
import os
from enum import Enum
from pathlib import Path
from typing import List

import click
import jsonschema

PACKAGE_DIR = Path(os.path.dirname(__file__))


class SchemaName(Enum):
    modeling_input = "modeling_input"


def validate_json_single_version(data: dict, schema_name: SchemaName, version: str):
    """Validate the JSON schema for the given schema name at a specific version"""
    version_for_filename = version.replace(".", "_")
    schema_path = (
        PACKAGE_DIR
        / "schemas"
        / schema_name.name
        / f"{schema_name.value}_{version_for_filename}.json"
    )
    with open(schema_path) as f:
        schema = json.load(f)
    return jsonschema.validate(schema=schema, instance=data)


def find_valid_versions(
    json_data: dict, schema_name: SchemaName, versions: List[str]
) -> List[str]:
    """Find the first version in the list of versions that successfully validates
    @raises ValueError if none of the versions validate.
    """
    errors = []  # tuples of (version, message)
    valid_versions = []
    for version in versions:
        try:
            validate_json_single_version(json_data, schema_name, version)
        except jsonschema.exceptions.ValidationError as e:
            errors.append({"version": version, "message": e.message})
        except OSError:
            raise ValueError(f"Schema {schema_name} version {version} not found")
        else:
            # Successfully validated
            valid_versions.append(version)
    if valid_versions:
        return valid_versions
    if errors:
        raise ValueError(
            f"Errors validating {schema_name}:\n"
            + "\n".join([f"Version {e['version']}: {e['message']}" for e in errors])
        )
    raise ValueError(
        f"Errors validating {schema_name}: no versions validated but no errors raised"
    )


@click.group()
def raven_schemas():
    pass


@raven_schemas.command()
@click.option(
    "-s",
    "--schema-name",
    type=click.Choice([s.name for s in SchemaName]),
    required=True,
)
@click.option("-v", "--schema-version", multiple=True, required=True)
@click.option("-f", "--json-file", type=click.Path(exists=True), required=True)
def validate_file(schema_name: str, schema_version: List[str], json_file: Path):
    """Validate the given JSON file against the given schema"""
    with open(json_file) as f:
        json_data = json.load(f)

    versions = find_valid_versions(json_data, SchemaName[schema_name], schema_version)
    print(f"Successfully validated {schema_name} version(s): {versions}")
