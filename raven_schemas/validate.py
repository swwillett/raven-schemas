import json
from typing import List

import jsonschema

from raven_schemas.constants import PACKAGE_DIR


class ValidationError(ValueError):
    pass


def validate_json_single_version(data: dict, schema_name: str, version: str):
    """Validate the JSON schema for the given schema name at a specific version"""
    if "_" in version:
        raise ValueError(
            f"Version {version} should be in the form '1.0.0', not '1_0_0'"
        )
    version_for_filename = version.replace(".", "_")
    schema_path = (
        PACKAGE_DIR / "schemas" / f"{schema_name}_{version_for_filename}_schema.json"
    )
    try:
        with open(schema_path) as f:
            schema = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Schema {schema_name} version {version} not found")
    return jsonschema.validate(schema=schema, instance=data)


def find_valid_versions(
    json_data: dict, schema_name: str, versions: List[str]
) -> List[str]:
    """Find the first version in the list of versions that successfully validates
    @raises ValidationError if none of the versions validate.
    """
    errors = []  # dicts with versions and error messages
    valid_versions = []
    for version in versions:
        try:
            validate_json_single_version(json_data, schema_name, version)
        except jsonschema.exceptions.ValidationError as e:
            errors.append({"version": version, "message": e.message})
        else:
            # Successfully validated
            valid_versions.append(version)
    if valid_versions:
        return valid_versions
    if errors:
        raise ValidationError(
            f"Errors validating {schema_name}:\n"
            + "\n  ".join([f"Version {e['version']}: {e['message']}" for e in errors])
        )

    raise ValueError(
        f"Errors validating {schema_name}: we should have encountered a valid version or an error"
    )
