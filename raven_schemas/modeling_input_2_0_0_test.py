import json

import jsonschema
import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_2_0_0_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_2_0_0_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


def test_invalid_survey_with_most_windows(valid_2_0_0_modeling_json):

    valid_2_0_0_modeling_json["survey"]["structure"][
        "most_windows"
    ] = "Double Pane, Metal"

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_2_0_0_modeling_json, "modeling_input", "2.0.0"
        )


def test_invalid_survey_with_primary_siding_material(valid_2_0_0_modeling_json):

    valid_2_0_0_modeling_json["survey"]["structure"]["primary_siding_material"] = {
        "type": "Stucco"
    }

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_2_0_0_modeling_json, "modeling_input", "2.0.0"
        )


def test_invalid_survey_with_foundation_under_main_floor_space_type(
    valid_2_0_0_modeling_json,
):

    valid_2_0_0_modeling_json["survey"]["structure"][
        "foundation_under_main_floor_space"
    ]["type"] = "Vented Crawlspace"

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_2_0_0_modeling_json, "modeling_input", "2.0.0"
        )
