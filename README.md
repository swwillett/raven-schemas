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
1. Check
    ```bash
    poetry shell

    ```
1. Use built-in help to see invocation details:
    ```bash
    nrgx-models --help # See all commands provided by this package
    nrgx-models model-home --help # See command options for the modeling command
    ```
1. Follow developer setup instructions below if you expect to check in code.


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
