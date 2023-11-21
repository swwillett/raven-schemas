import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import jsonschema
import pytest

from raven_schemas import types
from raven_schemas.constants import SCHEMA_DIR

# See tests below for example paths that these regexes should match
SCHEMA_FILE_REGEX = (
    r".*/(?P<schema_name>.*)_(?P<major>\d+)_(?P<minor>\d+)_(?P<patch>\d+)_schema.json"
)
SAMPLE_FILE_REGEX = r".*/(?P<schema_name>.*)_(?P<major>\d+)_(?P<minor>\d+)_(?P<patch>\d+)_sample_(?P<valid>(?:valid)|(?:invalid))_?(?P<suffix>.*)?.json"
SCHEMA_DIR_FILES = list(SCHEMA_DIR.glob("*"))


def test_schema_file_regex():
    match = re.match(SCHEMA_FILE_REGEX, "schemas/modeling_input_1_2_3_schema.json")
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
    SCHEMA_DIR_FILES,
)
def test_all_files_in_schemas_directory_are_schemas_or_samples(filename):
    filename_str = str(filename)
    schema_match = re.match(SCHEMA_FILE_REGEX, filename_str)
    sample_match = re.match(SAMPLE_FILE_REGEX, filename_str)
    match = schema_match or sample_match
    assert match
    assert match.groupdict()["schema_name"] in types.SchemaName.__members__


def _get_file_schema_and_version(file_path, regex):
    match = re.match(regex, str(file_path))
    assert (
        match is not None
    )  # This should never happen because we're only calling this function on files that match the regex
    file_info = match.groupdict()
    return (
        file_info["schema_name"],
        file_info["major"],
        file_info["minor"],
        file_info["patch"],
    )


def _get_schema_files_and_sample_files() -> Iterable[Tuple[Path, Path]]:
    """Return tuples of schema file paths and corresponding sample file paths
    raise ValueError if any sample files do not have matching schema files
    """
    schema_files = filter(
        lambda f: re.match(SCHEMA_FILE_REGEX, str(f)), SCHEMA_DIR_FILES
    )
    sample_files = filter(
        lambda f: re.match(SAMPLE_FILE_REGEX, str(f)), SCHEMA_DIR_FILES
    )

    sample_files_by_schema_and_version: Dict[Tuple, List[Path]] = {}
    for sample_file in sample_files:
        schema_and_version_info = _get_file_schema_and_version(
            sample_file, SAMPLE_FILE_REGEX
        )
        sample_files_by_schema_and_version.setdefault(
            schema_and_version_info, []
        ).append(sample_file)

    for schema_file in schema_files:
        schema_and_version_info = _get_file_schema_and_version(
            schema_file, SCHEMA_FILE_REGEX
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
        schema_file = _get_schema_files_and_sample_files()
        metafunc.parametrize("schema_file_and_sample_file", schema_file)


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
