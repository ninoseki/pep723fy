# pep723fy

Inject [PEP 723](https://peps.python.org/pep-0723/) inline script metadata into a Python file from a `pyproject.toml` ([PEP 621](https://peps.python.org/pep-0621/) / [PEP 735](https://peps.python.org/pep-0735/)) or `requirements.txt`.

## Installation

```bash
pip install pep723fy
# or
uv tool install pep723fy   # or just `uvx pep723fy ...`
```

## Usage

From `pyproject.toml`:

```bash
pep723fy script.py pyproject.toml
```

From `requirements.txt`:

```bash
pep723fy script.py requirements.txt
```

Use `--help` for more details:

```bash
$ pep723fy --help
usage: pep723fy [-h] [-f] [-g NAME] destination [source]

Inject pyproject.toml or requirements.txt dependencies as PEP 723 inline
script metadata.

positional arguments:
  destination       Path to the destination Python script.
  source            Path to the source pyproject.toml or requirements.txt
                    (default: ./pyproject.toml).

options:
  -h, --help        show this help message and exit
  -f, --force       Overwrite the destination's existing PEP 723 script block.
  -g, --group NAME  Include a dependency group from [dependency-groups]. May
                    be repeated.
```
