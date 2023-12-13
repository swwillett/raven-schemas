import json
from typing import Optional

import jsonschema
import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_1_0_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_1_0_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


@pytest.mark.parametrize(
    "fuel_type, ducted_heating, functional, over_age, furnace_vent, system, insulated_ducts, dist_type",
    [
        ["Gas", True, True, True, "Metal", "Baseboard", "Adequate", None],
        ["Gas", True, True, True, "Metal", "Boiler", "Adequate", None],
        ["Gas", True, True, True, "Metal", "Mini Split", "Adequate", None],
        ["Electricity", True, True, True, None, "Furnace", "Adequate", "Radiator"],
        ["Gas", True, True, True, None, "Mini Split", "Adequate", None],
    ],
)
def test_invalid_heating_combination(
    valid_1_1_0_modeling_json,
    fuel_type: Optional[str],
    ducted_heating: Optional[bool],
    functional: Optional[bool],
    over_age: Optional[bool],
    furnace_vent: Optional[str],
    system: Optional[str],
    insulated_ducts: Optional[str],
    dist_type: Optional[str],
):
    invalid_primary_heating = {
        "fuel_type": fuel_type,
        "ducted_heating": over_age,
        "functional": functional,
        "over_age": over_age,
        "furnace_vent": furnace_vent,
        "system": system,
        "insulated_ducts": insulated_ducts,
        "dist_type": dist_type,
    }

    valid_1_1_0_modeling_json["survey"]["systems"][
        "primary_heating"
    ] = invalid_primary_heating

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_0_modeling_json, "modeling_input", "1.1.0"
        )


@pytest.mark.parametrize(
    "type, over_age",
    [
        ["Condenser", None],
        ["Ducted Heat Pump", None],
        ["Mini Split", None],
        ["Window Units", None],
    ],
)
def test_invalid_cooling(
    valid_1_1_0_modeling_json,
    type: Optional[str],
    over_age: Optional[bool],
):
    invalid_cooling = {
        "type": type,
        "over_age": over_age,
    }

    valid_1_1_0_modeling_json["survey"]["systems"]["cooling"] = invalid_cooling

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_0_modeling_json, "modeling_input", "1.1.0"
        )


@pytest.mark.parametrize(
    "fuel_type, type, functional, over_age, gas_hookup_present",
    [
        ["Electricity", "Range", True, True, True],
        [None, "Range", True, True, None],
    ],
)
def test_invalid_cooking_combination(
    valid_1_1_0_modeling_json,
    fuel_type: Optional[str],
    type: Optional[str],
    functional: Optional[bool],
    over_age: Optional[bool],
    gas_hookup_present: Optional[bool],
):
    invalid_cooking = {
        "fuel_type": fuel_type,
        "type": type,
        "functional": functional,
        "over_age": over_age,
        "gas_hookup_present": gas_hookup_present,
    }

    valid_1_1_0_modeling_json["survey"]["appliances"]["cooking"] = invalid_cooking

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_0_modeling_json, "modeling_input", "1.1.0"
        )


@pytest.mark.parametrize(
    "fuel_type, over_age, gas_hookup_present",
    [
        ["Electricity", True, True],
    ],
)
def test_invalid_dryer_combination(
    valid_1_1_0_modeling_json,
    fuel_type: Optional[str],
    over_age: Optional[bool],
    gas_hookup_present: Optional[bool],
):
    invalid_dryer = {
        "fuel_type": fuel_type,
        "over_age": over_age,
        "gas_hookup_present": gas_hookup_present,
    }

    valid_1_1_0_modeling_json["survey"]["appliances"]["dryer"] = invalid_dryer

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_0_modeling_json, "modeling_input", "1.1.0"
        )
