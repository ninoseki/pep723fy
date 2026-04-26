import argparse
from pathlib import Path

from .errors import DestinationHasMetadataError
from .main import inject


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pep723fy",
        description="Inject pyproject.toml or requirements.txt dependencies as PEP 723 inline script metadata.",
    )
    parser.add_argument(
        "destination",
        type=Path,
        help="Path to the destination Python script.",
    )
    parser.add_argument(
        "source",
        type=Path,
        nargs="?",
        help="Path to the source pyproject.toml or requirements.txt (default: ./pyproject.toml).",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite the destination's existing PEP 723 script block.",
    )
    parser.add_argument(
        "-g",
        "--group",
        action="append",
        default=[],
        metavar="NAME",
        help="Include a dependency group from [dependency-groups]. May be repeated.",
    )
    return parser


def app(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    if not args.source.is_file():
        raise SystemExit(f"source not found: {args.source}")

    try:
        inject(
            args.source,
            args.destination,
            force=args.force,
            groups=tuple(args.group),
        )
    except DestinationHasMetadataError as exc:
        raise SystemExit(str(exc)) from exc
    except KeyError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    app()
