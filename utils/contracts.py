import json
from functools import cache
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_ROOT = Path(__file__).resolve().parent.parent / "schemas" / "api"


@cache
def _schema(name: str) -> dict:
    with (SCHEMA_ROOT / f"{name}.schema.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def assert_schema(payload, name: str) -> None:
    errors = sorted(Draft202012Validator(_schema(name)).iter_errors(payload), key=lambda error: list(error.path))
    assert not errors, "; ".join(
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors
    )


def assert_envelope(response, expected_status: int = 200, schema: str | None = None) -> dict:
    assert response.status == expected_status, response.text()
    body = response.json()
    assert isinstance(body, dict)
    assert "data" in body
    data = body["data"]
    if schema:
        assert_schema(data, schema)
    return data


def assert_collection(response, schema: str | None = None) -> list:
    data = assert_envelope(response, schema=schema)
    assert isinstance(data, list)
    return data
