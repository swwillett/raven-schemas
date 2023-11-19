# raven-schemas
Cross-repo relevant JSON schemas and language specific bindings for using them.


## Setup instructions

1. Ensure python 3.10 is installed
    * Generally you can just do this by running `python3.10` in a terminal.
1. Check out this repo
    ```bash
    git clone git@github.com:T110-nrgx/raven-schemas.git
    ```
    *After this, run the commands below from the repository root, ie. the `raven-schemas` directory.*
1. Install poetry and our package:
    ```bash
    pip install poetry
    poetry install
    ```
1. Check a test file against a schema!
    ```bash
    poetry shell
    raven-schemas validate-file -s modeling_input -f raven_schemas/schemas/modeling_input_1_0_0_sample.json -v 1.0.0
    ```
1. Follow [developer setup instructions](#developer-setup-instructions) and [Modifying a schema: checklist](#modifying-a-schema-checklist) below if you expect to check in code.


## Developer setup instructions

These instructions assume that you've already followed the setup instructions above.
```bash
# Install our precommit hooks
poetry shell
pre-commit install

# Get info about the virtualenv Poetry created
# To set up VS Code, ctrl+shift+P->"Python: select interpreter"->"+ Enter interpreter path..." and paste the Virtualenv executable path this command produces.
poetry env info

# Run unit tests
poetry shell
pytest .
```


## Using JSON Schema

Schemas in `raven-schemas` are written using the [JSON Schema standard](https://json-schema.org/understanding-json-schema).

A few properties that you should be familiar with:
* `if-then-else` with `"allOf"` ([Docs](https://json-schema.org/understanding-json-schema/reference/comments#comments)): used for conditional validation.
* `"$comment"` ([Docs](https://json-schema.org/understanding-json-schema/reference/comments#comments)): used for comments.
* `"additionalProperties": false` ([Docs](https://json-schema.org/understanding-json-schema/reference/object#additional-properties)): used to disallow extra properties. We generally use this in every object.
* `"required": [...]` ([Docs](https://json-schema.org/understanding-json-schema/reference/object#required)): Use to require properties. We generally use this in every object and list every property.


## Modifying a schema: checklist

Let's say you want to add a new required field to the current schema
1. choose a version number for your new schema.
    * Schemas are versioned with [semver](https://semver.org/), in the format `major.minor.patch`, so you will increment one of those three numbers.
    * *note* schemas are currently consumed strictly based on version number, so bumping any sub-number will require updates to all consumers & producers.
1. create a branch for your version, `vmajor_minor_patch`.
1. add a new version of the schema (eg. `raven_schemas/schemas/modeilng_input_3_0_0_schema.json`)
1. add a new sample file as well   (eg. `raven_schemas/schemas/modeilng_input_3_0_0_sample.json`)
1. modify the sample file and schema as appropriate. See [Using JSON Schema](#using-json-schema) above for details.
1. create your pull request, ensure all checks pass, and get the PR reviewed
1. As you land your PR, follow the [releasing](#releasing) steps below
1. Identify code that handles this schema type - we'll call them **consumer(s)** if they receive the data described in this schema and **producer(s)** if they produce it - and update them appropriately.
   a. **Consumer(s)** should be updated to be compatible with both the previous version *and* the new version.
   a. **Producer(s)** should be update to produce only the new schema type if possible.
   a. See [Using `raven-schemas`](#using-raven-schemas) below.
   a. Producer and consumer code can be developed and reviewed in parallel, but the backwards-compatible **consumer** code must be deployed first to avoid sequencing issues.


## Releasing

To release a new version of `raven-schemas`, do the following in your branch just before landing to `main`:

```
# in most cases when adding a schema you'll want to bump the minor version of the package
# but bump2version can do a "major" or "patch" bump as well.
$ poetry run bump2version minor
$ git push
$ git push --tags
```

Then, go to GitHub and [create a new release](https://github.com/T110-nrgx/raven-schemas/releases/new) based off of the version bump tag you just created.

## Using `raven-schemas`

### Usage In Python

To add or upgrade `raven-schemas` as a dependency for your Python package (eg. [`energy-modeling`](https://github.com/T110-nrgx/energy-modeling)), run `poetry add git+ssh://git@github.com:t110-nrgx/raven-schemas.git#VERSION` where `VERSION` is the version tag you want to depend on (eg. `v0.3.0`).

Then, import and use it - see [example code](https://github.com/T110-nrgx/energy-modeling/blob/3db22e8cdb43b0adc4ad0e1d0669c2a38bdfdd97/nrgx_building_model/data_types.py#L150).


### Usage In Typescript

To use a schema in typescript, copy the relevant schema version files into your repository and use them directly with the schema validation library [`@exodus/schemasafe`](https://github.com/ExodusMovement/schemasafe#installation).
