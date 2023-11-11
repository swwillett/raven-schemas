import json

import pytest

from raven_schemas import types
from raven_schemas import validate as module


@pytest.fixture
def valid_modeling_json():
    with open(
        module.PACKAGE_DIR / "schemas/modeling_input/test_data/1_0_0.json"
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
