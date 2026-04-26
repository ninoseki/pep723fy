class DestinationHasMetadataError(RuntimeError):
    """Destination already contains a PEP 723 script block; refuse to overwrite without --force."""
