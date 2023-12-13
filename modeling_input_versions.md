# Modeling Input Schema Versioning

This document tracks the version history of the [Schema Name] using [Semantic Versioning](https://semver.org/).

## Versioning Format

The version format follows the Semantic Versioning pattern: `MAJOR.MINOR.PATCH`

- **MAJOR** version changes when there are incompatible with previous versions (adding new sections or fields).
- **MINOR** version changes when functionality is added in a backward-compatible manner.
- **PATCH** version changes when backward-compatible bug fixes are made.

## Versions

### MINOR [1.1.0] - [12/5/2023]

#### Summary

- Added survey combination checks (already enforced in the energy model) to the schema logic using `allOf` and if/then conditional subschemas.

### PATCH [1.0.1] - [12/1/2023]

#### Summary

- Fixed bug caused by appliance boolean fields being set to `type: boolean` when they should've been `enum: [true, false, null]`. Null appliance fields are valid with application logic if, for example, the appliance is not present.

### MAJOR [1.0.0] - [Release Date]

#### Summary

- First iteration of schema for Modeling Input.
