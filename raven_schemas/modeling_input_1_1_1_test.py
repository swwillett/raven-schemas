import json
from typing import Optional

import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_1_1_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_1_1_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


@pytest.mark.parametrize(
    "roofMaterial",
    [
        "NotFound",
        "Shake",
    ],
)
def test_valid_roof_material_combination(
    valid_1_1_1_modeling_json,
    roofMaterial: Optional[str],
):
    valid_roofMaterial = roofMaterial

    valid_1_1_1_modeling_json["roofMaterial"] = valid_roofMaterial

    print(valid_roofMaterial)

    validate.validate_json_single_version(
        valid_1_1_1_modeling_json, "modeling_input", "1.1.1"
    )
