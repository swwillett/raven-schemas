import json
from typing import Optional

import jsonschema
import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_1_4_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_1_4_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


@pytest.mark.parametrize(
    "distType",
    [
        ["Radiator"],
        ["Radiant Floor"],
        ["Radiant Baseboard"],
    ],
)
def test_valid_dist_type_combination(
    valid_1_1_4_modeling_json,
    distType: Optional[str],
):
    dist_type = distType

    valid_1_1_4_modeling_json["survey"]["systems"]["primary_heating"][
        "dist_type"
    ] = dist_type

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_1_4_modeling_json, "modeling_input", "1.1.4"
        )
