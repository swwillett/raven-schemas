import json
from typing import Optional

import jsonschema
import pytest

from raven_schemas import validate
from raven_schemas.constants import PACKAGE_DIR


@pytest.fixture
def valid_1_0_0_modeling_json():
    with open(
        PACKAGE_DIR / "schemas/modeling_input_1_0_0_sample_valid.json"
    ) as modeling_input:
        return json.load(modeling_input)


@pytest.mark.parametrize(
    "attic_type, insulation, insulation_material, estimated_insulation_depth",
    [
        # fmt: off
        pytest.param("Finished", None, None, None, id="Finished-insulation-required"),
        pytest.param("Finished", "Adequate", "fiberglass (batts)", None, id="Finished-insulation_material-unwanted"),
        pytest.param("Finished", "Adequate", "fiberglass (batts)", "0-4 inches", id="Finished-estimated_insulation_depth-unwanted"),
        pytest.param("Cathedral Ceiling", "Adequate", None, None, id="Cathedral-insulation-unwanted"),
        pytest.param("Cathedral Ceiling", None, "fiberglass (batts)", None, id="Cathedral-insulation_material-unwanted"),
        pytest.param("Cathedral Ceiling", "Adequate", None, "0-4 inches", id="Cathedral-estimated_insulation_depth-unwanted"),
        pytest.param("Vented", "Adequate", "fiberglass (batts)", "0-4 inches", id="Vented-insulation-unwanted"),
        pytest.param("Vented", None, "fiberglass (batts)", None, id="Vented-insulation_material-required"),
        pytest.param("Vented", None, None, "0-4 inches", id="Vented-estimated_insulation_depth-required"),
        pytest.param("Unvented", "Adequate", "fiberglass (batts)", "0-4 inches", id="Unvented-insulation-unwanted"),
        pytest.param("Unvented", None, "fiberglass (batts)", None, id="Unvented-insulation_material-required"),
        pytest.param("Unvented", None, None, "0-4 inches", id="Unvented-estimated_insulation_depth-required"),
        # fmt: on
    ],
)
def test_invalid_attic_type_combinations(
    valid_1_0_0_modeling_json,
    attic_type: str,
    insulation: Optional[str],
    insulation_material: Optional[str],
    estimated_insulation_depth: Optional[str],
):
    survey_attic_data = {
        "type": attic_type,
        "insulation": insulation,
        "insulation_material": insulation_material,
        "estimated_insulation_depth": estimated_insulation_depth,
    }
    valid_1_0_0_modeling_json["survey"]["structure"]["attic_type"] = survey_attic_data
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate.validate_json_single_version(
            valid_1_0_0_modeling_json, "modeling_input", "1.0.0"
        )


@pytest.mark.parametrize(
    "attic_type, insulation, insulation_material, estimated_insulation_depth",
    [
        ["Finished", "Adequate", None, None],
        ["Finished", "Damaged/Inadequate", None, None],
        ["Cathedral Ceiling", None, None, None],
        ["Vented", None, None, None],
        ["Vented", None, "fiberglass (batts)", "0-4 inches"],
        ["Vented", None, "fiberglass (batts)", "4-6 inches"],
        ["Vented", None, "fiberglass (batts)", "6-8 inches"],
        ["Vented", None, "fiberglass (batts)", "8-10 inches"],
        ["Vented", None, "fiberglass (batts)", "10+ inches"],
        ["Vented", None, "fiberglass (loose)", "0-4 inches"],
        ["Vented", None, "fiberglass (loose)", "4-6 inches"],
        ["Vented", None, "fiberglass (loose)", "6-8 inches"],
        ["Vented", None, "fiberglass (loose)", "8-10 inches"],
        ["Vented", None, "fiberglass (loose)", "10+ inches"],
        ["Vented", None, "mineral wool (batts)", "0-4 inches"],
        ["Vented", None, "mineral wool (batts)", "4-6 inches"],
        ["Vented", None, "mineral wool (batts)", "6-8 inches"],
        ["Vented", None, "mineral wool (batts)", "8-10 inches"],
        ["Vented", None, "mineral wool (batts)", "10+ inches"],
        ["Vented", None, "mineral wool (loose)", "0-4 inches"],
        ["Vented", None, "mineral wool (loose)", "4-6 inches"],
        ["Vented", None, "mineral wool (loose)", "6-8 inches"],
        ["Vented", None, "mineral wool (loose)", "8-10 inches"],
        ["Vented", None, "mineral wool (loose)", "10+ inches"],
        ["Vented", None, "cellulose", "0-4 inches"],
        ["Vented", None, "cellulose", "4-6 inches"],
        ["Vented", None, "cellulose", "6-8 inches"],
        ["Vented", None, "cellulose", "8-10 inches"],
        ["Vented", None, "cellulose", "10+ inches"],
        ["Vented", None, "spray foam", "0-4 inches"],
        ["Vented", None, "spray foam", "4-6 inches"],
        ["Vented", None, "spray foam", "6-8 inches"],
        ["Vented", None, "spray foam", "8-10 inches"],
        ["Vented", None, "spray foam", "10+ inches"],
        ["Unvented", None, None, None],
        ["Unvented", None, "fiberglass (batts)", "0-4 inches"],
        ["Unvented", None, "fiberglass (batts)", "4-6 inches"],
        ["Unvented", None, "fiberglass (batts)", "6-8 inches"],
        ["Unvented", None, "fiberglass (batts)", "8-10 inches"],
        ["Unvented", None, "fiberglass (batts)", "10+ inches"],
        ["Unvented", None, "fiberglass (loose)", "0-4 inches"],
        ["Unvented", None, "fiberglass (loose)", "4-6 inches"],
        ["Unvented", None, "fiberglass (loose)", "6-8 inches"],
        ["Unvented", None, "fiberglass (loose)", "8-10 inches"],
        ["Unvented", None, "fiberglass (loose)", "10+ inches"],
        ["Unvented", None, "mineral wool (batts)", "0-4 inches"],
        ["Unvented", None, "mineral wool (batts)", "4-6 inches"],
        ["Unvented", None, "mineral wool (batts)", "6-8 inches"],
        ["Unvented", None, "mineral wool (batts)", "8-10 inches"],
        ["Unvented", None, "mineral wool (batts)", "10+ inches"],
        ["Unvented", None, "mineral wool (loose)", "0-4 inches"],
        ["Unvented", None, "mineral wool (loose)", "4-6 inches"],
        ["Unvented", None, "mineral wool (loose)", "6-8 inches"],
        ["Unvented", None, "mineral wool (loose)", "8-10 inches"],
        ["Unvented", None, "mineral wool (loose)", "10+ inches"],
        ["Unvented", None, "cellulose", "0-4 inches"],
        ["Unvented", None, "cellulose", "4-6 inches"],
        ["Unvented", None, "cellulose", "6-8 inches"],
        ["Unvented", None, "cellulose", "8-10 inches"],
        ["Unvented", None, "cellulose", "10+ inches"],
        ["Unvented", None, "spray foam", "0-4 inches"],
        ["Unvented", None, "spray foam", "4-6 inches"],
        ["Unvented", None, "spray foam", "6-8 inches"],
        ["Unvented", None, "spray foam", "8-10 inches"],
        ["Unvented", None, "spray foam", "10+ inches"],
    ],
)
def test_valid_attic_type_combinations(
    valid_1_0_0_modeling_json,
    attic_type: str,
    insulation: Optional[str],
    insulation_material: Optional[str],
    estimated_insulation_depth: Optional[str],
):
    survey_attic_data = {
        "type": attic_type,
        "insulation": insulation,
        "insulation_material": insulation_material,
        "estimated_insulation_depth": estimated_insulation_depth,
    }
    valid_1_0_0_modeling_json["survey"]["structure"]["attic_type"] = survey_attic_data
    validate.validate_json_single_version(
        valid_1_0_0_modeling_json, "modeling_input", "1.0.0"
    )
