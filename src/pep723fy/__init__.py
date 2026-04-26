from .main import (  # noqa: F401
    PEP723_BLOCK,
    Metadata,
    build_metadata_block,
    inject,
    read_pyproject,
    read_requirements,
    read_source,
)

try:
    from ._version import version

    __version__ = version
except ImportError:
    __version__ = "0.0.0"
