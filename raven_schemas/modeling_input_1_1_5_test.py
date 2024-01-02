import json

import jsonschema
import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_1_5_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_1_5_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


def test_valid_combination(
    valid_1_1_5_modeling_json,
):

    valid_1_1_5_modeling_json["survey"]["systems"]["primary_heating"] = {
        "fuel_type": "None",
        "ducted_heating": None,
        "functional": None,
        "over_age": None,
        "furnace_vent": None,
        "system": None,
        "insulated_ducts": None,
    }

    valid_1_1_5_modeling_json["survey"]["systems"]["cooling"]["type"] = "Central AC"

    validate.validate_json_single_version(
        valid_1_1_5_modeling_json, "modeling_input", "1.1.5"
    )


@pytest.mark.parametrize(
    "fuel_type",
    [
        "None",
    ],
)
def test_invalid_heating_combination(
    valid_1_1_5_modeling_json,
    fuel_type: str,
):

    valid_1_1_5_modeling_json["survey"]["systems"]["primary_heating"][
        "fuel_type"
    ] = fuel_type

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_5_modeling_json, "modeling_input", "1.1.5"
        )


@pytest.mark.parametrize(
    "cooling_type",
    [
        "Condenser",
    ],
)
def test_invalid_cooling_type_combination(
    valid_1_1_5_modeling_json,
    cooling_type: str,
):
    valid_1_1_5_modeling_json["survey"]["systems"]["cooling"]["type"] = cooling_type

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_5_modeling_json, "modeling_input", "1.1.5"
        )
