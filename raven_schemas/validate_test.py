import json
import re
from pathlib import Path
from typing import Iterable

import pytest

from raven_schemas import types
from raven_schemas import validate as module


@pytest.fixture
def valid_modeling_json():
    with open(
        module.PACKAGE_DIR / "schemas/modeling_input_1_0_0_sample.json"
    ) as modeling_input:
        return json.load(modeling_input)


def validate_json_single_version__happy_path(valid_modeling_json):
    module.find_valid_versions(
        valid_modeling_json,
        types.SchemaName.modeling_input,
        ["1.0.0"],
    )


def test_validate_json_single_version__bad_version():
    with pytest.raises(ValueError):
        module.validate_json_single_version(
            {"test": "data"}, types.SchemaName.modeling_input, "not a real version"
        )


def test_validate_json_single_version__bad_version_sneaky_underscores():
    # Since we're doing 'version.replace(".", "_")', we need to explicitly check for underscores first
    # or else version "1_0_0" will be interchangeable with "1.0.0"
    with pytest.raises(ValueError):
        module.validate_json_single_version(
            {"test": "data"}, types.SchemaName.modeling_input, "1_0_0"
        )


def test_find_valid_versions__happy_path(valid_modeling_json):
    assert module.find_valid_versions(
        valid_modeling_json,
        types.SchemaName.modeling_input,
        ["1.0.0"],
    ) == ["1.0.0"]


def test_find_valid_versions__no_versions_provided():
    with pytest.raises(ValueError):
        module.find_valid_versions(
            {"test": "data"}, types.SchemaName.modeling_input, []
        )


def test_find_valid_versions__no_versions_validated():
    with pytest.raises(module.ValidationError):
        module.find_valid_versions(
            {"invalid": "data"}, types.SchemaName.modeling_input, ["1.0.0"]
        )


def get_schema_files() -> Iterable[Path]:
    """Get a list of all schema versions in the schemas directory."""
    return module.PACKAGE_DIR.glob("schemas/*_schema.json")


def pytest_generate_tests(metafunc):
    """Dynamically generate tests for every version of every schema in the schemas directory."""
    if "schema_file" in metafunc.fixturenames:
        schema_file = get_schema_files()
        metafunc.parametrize("schema_file", schema_file)


def test_schema_file_with_sample_data(schema_file):
    """Test that the sample data for each schema version validates."""
    match = re.match(r"(.*/(.*)_(\d+_\d+_\d+))_schema.json", str(schema_file))
    assert (
        match is not None
    ), 'Schema file name should be in the form "schema_name_1_0_0_schema.json"'
    prefix, schema_name, version_raw = match.groups()
    version = version_raw.replace("_", ".")

    try:
        schema_name_enum = types.SchemaName[schema_name]
    except KeyError:
        raise ValueError(f"Schema name {schema_name} is not valid")

    with open(f"{prefix}_sample.json") as sample_file:
        sample_data = json.load(sample_file)

    module.validate_json_single_version(sample_data, schema_name_enum, version)
