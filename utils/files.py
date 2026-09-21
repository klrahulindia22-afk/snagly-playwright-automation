"""Utilities for deterministic disposable upload data."""

from pathlib import Path


def create_sized_file(directory: Path, name: str, size_bytes: int, content: bytes = b"E2E") -> Path:
    """Create an exact-size test file efficiently and return its path."""
    if size_bytes < 0:
        raise ValueError("size_bytes must be non-negative")
    if not content and size_bytes:
        raise ValueError("content must not be empty when size_bytes is positive")
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    if size_bytes == 0:
        path.touch()
        return path
    repeats, remainder = divmod(size_bytes, len(content))
    path.write_bytes(content * repeats + content[:remainder])
    return path
