from pathlib import Path

import pytest

from pep723fy.main import (
    PEP723_BLOCK,
    Metadata,
    build_metadata_block,
    inject,
    read_pyproject,
    read_requirements,
    read_source,
)


def test_read_pyproject(source: Path) -> None:
    metadata = read_pyproject(source)
    assert metadata.requires_python == ">=3.12"
    assert metadata.dependencies == ["httpx>=0.27", "rich"]


def test_build_metadata_block_with_deps() -> None:
    block = build_metadata_block(
        Metadata(requires_python=">=3.12", dependencies=["httpx>=0.27", "rich"])
    )
    assert block == (
        "# /// script\n"
        '# requires-python = ">=3.12"\n'
        "# dependencies = [\n"
        '#   "httpx>=0.27",\n'
        '#   "rich",\n'
        "# ]\n"
        "# ///\n"
    )


def test_build_metadata_block_no_deps() -> None:
    block = build_metadata_block(Metadata(requires_python=">=3.10"))
    assert "# dependencies = []" in block


def test_block_matches_pep723_regex() -> None:
    block = build_metadata_block(
        Metadata(requires_python=">=3.12", dependencies=["rich"])
    )
    match = PEP723_BLOCK.search(block)
    assert match is not None
    assert match.group("type") == "script"


def test_inject_creates_new_file(source: Path, tmp_path: Path) -> None:
    destination = tmp_path / "out.py"
    inject(source, destination)

    content = destination.read_text(encoding="utf-8")
    assert content.startswith("# /// script")
    assert "# ///" in content
    assert '#   "httpx>=0.27",' in content


def test_inject_refuses_existing_block_without_force(
    source: Path, destination_with_block: Path
) -> None:
    original = destination_with_block.read_text(encoding="utf-8")

    with pytest.raises(Exception):
        inject(source, destination_with_block)

    assert destination_with_block.read_text(encoding="utf-8") == original


def test_inject_replaces_existing_block(
    source: Path, destination_with_block: Path
) -> None:
    inject(source, destination_with_block, force=True)

    content = destination_with_block.read_text(encoding="utf-8")
    assert content.count("# /// script") == 1
    assert '# requires-python = ">=3.12"' in content
    assert "print('hi')" in content


def test_inject_prepends_when_no_block(
    source: Path, destination_no_block: Path
) -> None:
    inject(source, destination_no_block)

    content = destination_no_block.read_text(encoding="utf-8")
    assert content.startswith("# /// script")
    assert content.rstrip().endswith("print('hello')")


def test_read_requirements(requirements_source: Path) -> None:
    metadata = read_requirements(requirements_source)
    assert metadata.requires_python is None
    assert metadata.dependencies == ["httpx>=0.27", "rich", "uv==0.11.7"]


def test_read_source_dispatches_by_extension(
    source: Path, requirements_source: Path
) -> None:
    assert read_source(source) == Metadata(
        requires_python=">=3.12", dependencies=["httpx>=0.27", "rich"]
    )
    assert read_source(requirements_source) == Metadata(
        dependencies=["httpx>=0.27", "rich", "uv==0.11.7"]
    )


def test_inject_from_requirements(
    requirements_source: Path, tmp_path: Path
) -> None:
    destination = tmp_path / "out.py"
    inject(requirements_source, destination)

    content = destination.read_text(encoding="utf-8")
    assert "# /// script" in content
    assert '#   "httpx>=0.27",' in content
    assert '#   "rich",' in content
    assert "requires-python" not in content


def test_inject_preserves_shebang(
    source: Path, destination_with_shebang: Path
) -> None:
    inject(source, destination_with_shebang)

    content = destination_with_shebang.read_text(encoding="utf-8")
    assert content.startswith("#!/usr/bin/env python3\n# /// script")
