import json

import pytest

from raven_schemas import types
from raven_schemas import validate as module


@pytest.fixture
def valid_1_0_0_modeling_json():
    with open(
        module.PACKAGE_DIR / "schemas/modeling_input_1_0_0_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


def validate_json_single_version__happy_path(valid_modeling_json):
    module.find_first_valid_version(
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


def test_find_valid_versions__happy_path(valid_1_0_0_modeling_json):
    assert module.find_first_valid_version(
        valid_1_0_0_modeling_json,
        types.SchemaName.modeling_input,
        ["1.0.0"],
    ) == ["1.0.0"]


def test_find_valid_versions__no_versions_provided():
    with pytest.raises(ValueError):
        module.find_first_valid_version(
            {"test": "data"}, types.SchemaName.modeling_input, []
        )


def test_find_valid_versions__no_versions_validated():
    with pytest.raises(module.ValidationError):
        module.find_first_valid_version(
            {"invalid": "data"}, types.SchemaName.modeling_input, ["1.0.0"]
        )
