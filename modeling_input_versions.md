# Modeling Input Schema Versioning

This document tracks the version history of the [Schema Name] using [Semantic Versioning](https://semver.org/).

## Versioning Format

The version format follows the Semantic Versioning pattern: `MAJOR.MINOR.PATCH`

- **MAJOR** version changes when there are incompatible with previous versions (adding new sections or fields).
- **MINOR** version changes when functionality is added in a backward-compatible manner.
- **PATCH** version changes when backward-compatible bug fixes are made.

## Versions

### PATCH [1.1.3] - [12/19/2023]

#### Summary

- Added support for 'Barrel' roof material type

### PATCH [1.1.2] - [12/16/2023]

#### Summary

- Changed '0-4 inches' estimated insulation depth to '<4 inches' and updated cooking type to 'Cooktop and Oven' or 'Range'

### PATCH [1.1.1] - [12/14/2023]

#### Summary

- Added support for 'Shake' roof material type

### MINOR [1.1.0] - [12/5/2023]

#### Summary

- Added survey combination checks (already enforced in the energy model) to the schema logic using `allOf` and if/then conditional subschemas.

### PATCH [1.0.1] - [12/1/2023]

#### Summary

- Fixed bug caused by appliance boolean fields being set to `type: boolean` when they should've been `enum: [true, false, null]`. Null appliance fields are valid with application logic if, for example, the appliance is not present.

### MAJOR [1.0.0] - [Release Date]

#### Summary

- First iteration of schema for Modeling Input.
