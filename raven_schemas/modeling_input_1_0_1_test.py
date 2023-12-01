import json
from typing import Optional

import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_0_0_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_0_1_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


def test_valid_dishwasher_not_present(
    valid_1_0_0_modeling_json,
):
    survey_dishwasher_data = {
        "functional": None,
        "over_age": None,
    }
    valid_1_0_0_modeling_json["survey"]["appliances"][
        "dishwasher"
    ] = survey_dishwasher_data
    validate.validate_json_single_version(
        valid_1_0_0_modeling_json, "modeling_input", "1.0.1"
    )


@pytest.mark.parametrize(
    "fuel_type, type, functional, over_age, gas_hookup_present",
    [[None, None, None, None, True], [None, None, None, None, False]],
)
def test_valid_cooking_not_present(
    valid_1_0_0_modeling_json,
    fuel_type: Optional[bool],
    type: Optional[str],
    functional: Optional[bool],
    over_age: Optional[bool],
    gas_hookup_present: Optional[bool],
):
    survey_cooking_data = {
        "fuel_type": fuel_type,
        "type": type,
        "functional": functional,
        "over_age": over_age,
        "gas_hookup_present": gas_hookup_present,
    }
    valid_1_0_0_modeling_json["survey"]["appliances"]["cooking"] = survey_cooking_data
    validate.validate_json_single_version(
        valid_1_0_0_modeling_json, "modeling_input", "1.0.1"
    )


@pytest.mark.parametrize(
    "fuel_type, over_age, gas_hookup_present", [[None, None, True], [None, None, False]]
)
def test_valid_dryer_not_present(
    valid_1_0_0_modeling_json,
    fuel_type: Optional[str],
    over_age: Optional[bool],
    gas_hookup_present: Optional[bool],
):
    survey_dryer_data = {
        "fuel_type": fuel_type,
        "over_age": over_age,
        "gas_hookup_present": gas_hookup_present,
    }
    valid_1_0_0_modeling_json["survey"]["appliances"]["dryer"] = survey_dryer_data
    validate.validate_json_single_version(
        valid_1_0_0_modeling_json, "modeling_input", "1.0.1"
    )
