import json
from typing import Optional

import jsonschema
import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_1_2_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_1_2_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


@pytest.mark.parametrize(
    "estimated_insulation_depth, cooking_type",
    [["<4 inches", "Cooktop Only"], ["0-4 inches", "Cooktop and Oven"]],
)
def test_valid_roof_material_combination(
    valid_1_1_2_modeling_json,
    estimated_insulation_depth: Optional[str],
    cooking_type: Optional[str],
):
    valid_1_1_2_modeling_json["survey"]["structure"]["attic_type"][
        "estimated_insulation_depth"
    ] = estimated_insulation_depth
    valid_1_1_2_modeling_json["survey"]["appliances"]["cooking"]["type"] = type

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_2_modeling_json, "modeling_input", "1.1.2"
        )
