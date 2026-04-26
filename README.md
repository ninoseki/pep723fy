# pep723fy

Inject PEP 723 inline script metadata based on pyproject.toml (PEP 621/735) or requirements.txt (PEP 440).

## Installation

```bash
pip install pep723fy
# or
uv tool pep723fy # or just do "uvx pep723fy"
```

## Usage

```bash
# inject inline script metadata based on pyproject.toml
pep723fy script.py pyproject.toml
# inject inline script metadata based on requirements.txt
pep723fy script.py requirements.txt
```

```bash
$ pep723fy --help
usage: p723fy [-h] [-s SOURCE] -d DESTINATION [-f] [-g NAME]

Project pyproject.toml dependencies into PEP 723 inline script metadata.

options:
  -h, --help            show this help message and exit
  -s, --source SOURCE   Path to the source pyproject.toml (default: ./pyproject.toml).
  -d, --destination DESTINATION
                        Path to the destination Python script.
  -f, --force           Overwrite the destination's existing PEP 723 script block.
  -g, --group NAME      Include a dependency group from [dependency-groups]. May be repeated.
```
