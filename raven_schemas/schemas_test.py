import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import jsonschema
import pytest

from raven_schemas import schemas as module

# See tests below for example paths that these regexes should match
SAMPLE_FILE_REGEX = r".*/(?P<schema_name>.*)_(?P<major>\d+)_(?P<minor>\d+)_(?P<patch>\d+)_sample_(?P<valid>(?:valid)|(?:invalid))_?(?P<suffix>.*)?.json"


def test_schema_file_regex():
    match = re.match(
        module.SCHEMA_FILE_REGEX, "schemas/modeling_input_1_2_3_schema.json"
    )
    assert match is not None
    assert match.groupdict() == {
        "schema_name": "modeling_input",
        "major": "1",
        "minor": "2",
        "patch": "3",
    }


@pytest.mark.parametrize(
    "filename, expected_groupdict",
    [
        (
            "schemas/modeling_input_1_0_0_sample_valid.json",
            {
                "schema_name": "modeling_input",
                "major": "1",
                "minor": "0",
                "patch": "0",
                "valid": "valid",
                "suffix": "",
            },
        ),
        (
            "schemas/modeling_input_1_2_3_sample_invalid_bad_roof_type.json",
            {
                "schema_name": "modeling_input",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "valid": "invalid",
                "suffix": "bad_roof_type",
            },
        ),
        ("schemas/modeling_input_abc_0_0_sample_invalid_bad_roof_type.json", None),
    ],
)
def test_sample_file_regex(filename, expected_groupdict):
    match = re.match(SAMPLE_FILE_REGEX, filename)
    if expected_groupdict is None:
        assert match is None
    else:
        assert match is not None
        assert match.groupdict() == expected_groupdict


@pytest.mark.parametrize(
    "filename",
    module.SCHEMA_DIR_FILES,
)
def test_all_filenames_in_schemas_directory_are_schemas_or_samples(filename):
    filename_str = str(filename)
    schema_match = re.match(module.SCHEMA_FILE_REGEX, filename_str)
    sample_match = re.match(SAMPLE_FILE_REGEX, filename_str)
    match = schema_match or sample_match
    assert match
    schema_name = match.groupdict()["schema_name"]
    version = ".".join(
        [
            match.groupdict()["major"],
            match.groupdict()["minor"],
            match.groupdict()["patch"],
        ]
    )
    assert schema_name in module.get_known_schemas_and_versions()
    assert version in module.get_known_schemas_and_versions()[schema_name]


def _get_schema_files_and_sample_files() -> Iterable[Tuple[Path, Path]]:
    """Return tuples of schema file paths and corresponding sample file paths
    raise ValueError if any sample files do not have matching schema files
    """
    schema_files = filter(
        lambda f: re.match(module.SCHEMA_FILE_REGEX, str(f)), module.SCHEMA_DIR_FILES
    )
    sample_files = filter(
        lambda f: re.match(SAMPLE_FILE_REGEX, str(f)), module.SCHEMA_DIR_FILES
    )

    sample_files_by_schema_and_version: Dict[Tuple, List[Path]] = {}
    for sample_file in sample_files:
        schema_and_version_info = module.get_file_schema_and_version(
            sample_file, SAMPLE_FILE_REGEX
        )
        sample_files_by_schema_and_version.setdefault(
            schema_and_version_info, []
        ).append(sample_file)

    for schema_file in schema_files:
        schema_and_version_info = module.get_file_schema_and_version(
            schema_file, module.SCHEMA_FILE_REGEX
        )
        matching_sample_files = sample_files_by_schema_and_version.pop(
            schema_and_version_info, []
        )
        if not matching_sample_files:
            raise ValueError(
                f"Schema file {schema_file} did not have any matching sample files"
            )
        for sample_file in matching_sample_files:
            yield schema_file, sample_file

    if sample_files_by_schema_and_version:
        raise ValueError(
            f"Some sample files did not have matching schema files: {sample_files_by_schema_and_version}"
        )


def pytest_generate_tests(metafunc):
    """Dynamically generate tests for every version of every schema in the schemas directory."""
    if "schema_file_and_sample_file" in metafunc.fixturenames:
        schema_files_and_sample_files = _get_schema_files_and_sample_files()
        metafunc.parametrize(
            "schema_file_and_sample_file", schema_files_and_sample_files
        )

    if "schema_file" in metafunc.fixturenames:
        schema_files = filter(
            lambda f: re.match(module.SCHEMA_FILE_REGEX, str(f)),
            module.SCHEMA_DIR_FILES,
        )
        metafunc.parametrize("schema_file", schema_files)


def test_schema_file_with_sample_data(schema_file_and_sample_file):
    """Test that the sample data for each schema version validates."""
    schema_file, sample_file = schema_file_and_sample_file
    schema = json.loads(schema_file.read_text())
    sample_data = json.loads(sample_file.read_text())

    sample_match = re.match(SAMPLE_FILE_REGEX, str(sample_file))
    assert sample_match is not None  # Should never happen - we pre-filter for this
    sample_info = sample_match.groupdict()
    if sample_info["valid"] == "valid":
        jsonschema.validate(schema=schema, instance=sample_data)
    else:
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(schema=schema, instance=sample_data)


def test_schema_file_is_valid(schema_file):
    """Test that each schema file is valid against a strict variant of the draft 2020-12 metaschema.
    Since the draft 2020-12 schema is not strict by default,
    we create a variant of it that disallows unevaluated properties.
    This allows us to catch typos in schema properties which would otherwise go unnoticed.

    It also aligns with the TypeScript library we use (Ajv), that validate schemas strictly by default.
    """
    schema = json.loads(schema_file.read_text())
    strict_validator = jsonschema.Draft202012Validator(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://json-schema.org/draft/2020-12/strict",
            "$ref": "https://json-schema.org/draft/2020-12/schema",
            "unevaluatedProperties": False,
        }
    )

    errors = list(strict_validator.iter_errors(schema))
    assert not errors


def test_schemas_contain_correct_version():
    """Test that, for each schema in the schemas directory, the version in the schema matches the version in the filename."""
    schema_files = filter(
        lambda f: re.match(module.SCHEMA_FILE_REGEX, str(f)),
        module.SCHEMA_DIR_FILES,
    )
    for schema_file in schema_files:
        schema = json.loads(schema_file.read_text())
        schema_name, major, minor, patch = module.get_file_schema_and_version(
            schema_file, module.SCHEMA_FILE_REGEX
        )
        input_schema_version = (
            schema.get("properties", {}).get("input_schema_version", {}).get("const")
        )

        if input_schema_version is not None:
            assert input_schema_version == f"{major}.{minor}.{patch}"
        else:
            pass
