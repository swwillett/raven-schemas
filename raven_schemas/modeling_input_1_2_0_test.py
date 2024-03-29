import json

import jsonschema
import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_2_0_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_2_0_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


def test_invalid_survey_without_solar_panels(valid_1_2_0_modeling_json):

    valid_1_2_0_modeling_json["survey"]["structure"]["solar_panels"] = None

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_2_0_modeling_json, "modeling_input", "1.2.0"
        )
