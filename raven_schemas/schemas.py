import functools
import re
from typing import Dict, List

from raven_schemas.constants import SCHEMA_DIR

SCHEMA_DIR_FILES = list(SCHEMA_DIR.glob("*"))
# Example: "schemas/modeling_input_1_2_3_schema.json"
SCHEMA_FILE_REGEX = (
    r".*/(?P<schema_name>.*)_(?P<major>\d+)_(?P<minor>\d+)_(?P<patch>\d+)_schema.json"
)


def get_file_schema_and_version(file_path, regex):
    match = re.match(regex, str(file_path))
    if match is None:
        raise ValueError(f"File path {file_path} does not match regex {regex}")
    file_info = match.groupdict()
    return (
        file_info["schema_name"],
        file_info["major"],
        file_info["minor"],
        file_info["patch"],
    )


@functools.cache
def get_known_schemas_and_versions() -> Dict[str, List[str]]:
    """All known schemas and versions supported in this library.
    eg. {'modeling_input': ['1.0.0', '1.2.3'], ...}
    """
    schema_versions: Dict[str, List[str]] = {}
    for file_path in SCHEMA_DIR_FILES:
        try:
            schema_name, major, minor, patch = get_file_schema_and_version(
                file_path, SCHEMA_FILE_REGEX
            )
        except ValueError:
            continue
        else:
            schema_versions.setdefault(schema_name, []).append(
                f"{major}.{minor}.{patch}"
            )
    return schema_versions
