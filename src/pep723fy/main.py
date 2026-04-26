import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .errors import DestinationHasMetadataError

# PEP 723 reference regex for locating an existing script metadata block.
PEP723_BLOCK = re.compile(
    r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$"
)


@dataclass
class Metadata:
    requires_python: str | None = None
    dependencies: list[str] = field(default_factory=list)


def _expand_group(
    groups_table: dict, name: str, seen: set[str] | None = None
) -> list[str]:
    seen = seen or set()

    if name in seen:
        return []

    seen.add(name)

    if name not in groups_table:
        raise KeyError(f"dependency group {name!r} not found in [dependency-groups]")

    out: list[str] = []
    for item in groups_table[name]:
        if isinstance(item, dict) and "include-group" in item:
            out.extend(_expand_group(groups_table, item["include-group"], seen))
        else:
            out.append(item)  # type: ignore

    return out


def read_pyproject(path: Path, groups: tuple[str, ...] = ()) -> Metadata:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project", {})
    deps: list[str] = list(project.get("dependencies", []))

    if groups:
        groups_table = data.get("dependency-groups", {})
        for group in groups:
            deps.extend(_expand_group(groups_table, group))

    return Metadata(requires_python=project.get("requires-python"), dependencies=deps)


def read_requirements(path: Path) -> Metadata:
    deps: list[str] = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        # Strip inline comments: a `#` preceded by whitespace.
        line = re.split(r"\s+#", line, maxsplit=1)[0].rstrip()
        if line:
            deps.append(line)

    return Metadata(dependencies=deps)


def read_source(path: Path, groups: tuple[str, ...] = ()) -> Metadata:
    if path.name == "pyproject.toml":
        return read_pyproject(path, groups=groups)

    return read_requirements(path)


def build_metadata_block(metadata: Metadata) -> str:
    lines = ["# /// script"]

    if metadata.requires_python:
        lines.append(f'# requires-python = "{metadata.requires_python}"')

    if metadata.dependencies:
        lines.append("# dependencies = [")
        for dep in metadata.dependencies:
            lines.append(f'#   "{dep}",')
        lines.append("# ]")
    else:
        lines.append("# dependencies = []")

    lines.append("# ///")
    return "\n".join(lines) + "\n"


def _splice(existing: str, block: str) -> str:
    for match in PEP723_BLOCK.finditer(existing):
        if match.group("type") == "script":
            return (
                existing[: match.start()] + block.rstrip("\n") + existing[match.end() :]
            )

    if existing.startswith("#!"):
        shebang, _, rest = existing.partition("\n")
        return f"{shebang}\n{block}{rest}"

    if existing and not existing.startswith("\n"):
        return f"{block}\n{existing}"

    return f"{block}{existing}"


def has_script_block(content: str) -> bool:
    return any(m.group("type") == "script" for m in PEP723_BLOCK.finditer(content))


def inject(
    source: Path,
    destination: Path,
    *,
    force: bool = False,
    groups: tuple[str, ...] = (),
) -> str:
    block = build_metadata_block(read_source(source, groups=groups))

    existing = destination.read_text(encoding="utf-8") if destination.exists() else ""
    if existing and has_script_block(existing) and not force:
        raise DestinationHasMetadataError(
            f"{destination} already contains a PEP 723 script block; pass --force to overwrite."
        )

    new_content = _splice(existing, block) if existing else block
    destination.write_text(new_content, encoding="utf-8")
    return new_content
