import shutil
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def _copy(name: str, target: Path) -> Path:
    shutil.copyfile(FIXTURES / name, target)
    return target


@pytest.fixture
def source(tmp_path: Path) -> Path:
    return _copy("basic_pyproject.toml", tmp_path / "pyproject.toml")


@pytest.fixture
def grouped_source(tmp_path: Path) -> Path:
    return _copy("grouped_pyproject.toml", tmp_path / "pyproject.toml")


@pytest.fixture
def requirements_source(tmp_path: Path) -> Path:
    return _copy("requirements.txt", tmp_path / "requirements.txt")


@pytest.fixture
def destination_with_block(tmp_path: Path) -> Path:
    return _copy("existing_with_block.py", tmp_path / "out.py")


@pytest.fixture
def destination_no_block(tmp_path: Path) -> Path:
    return _copy("existing_no_block.py", tmp_path / "out.py")


@pytest.fixture
def destination_with_shebang(tmp_path: Path) -> Path:
    return _copy("existing_with_shebang.py", tmp_path / "out.py")
