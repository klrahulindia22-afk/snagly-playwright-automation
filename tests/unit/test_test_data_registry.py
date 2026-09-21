from pathlib import Path

import pytest

from test_data.registry import TestDataRegistry as DataRegistry


def test_registry_covers_every_manual_case(test_data_registry: DataRegistry):
    assert len(test_data_registry.ids()) == 172
    assert test_data_registry.ids()[0] == "SNAG-TC-001"
    assert test_data_registry.ids()[-1] == "SNAG-TC-172"


@pytest.mark.case_id("SNAG-TC-001")
def test_case_data_is_loaded_from_marker(case_data):
    assert case_data.case_id == "SNAG-TC-001"
    assert case_data.scenario
    assert case_data.values["unique"]["board"].startswith("E2E-")


def test_file_factory_creates_exact_size(test_file_factory):
    attachment = test_file_factory("sample.txt", 101)
    assert isinstance(attachment, Path)
    assert attachment.stat().st_size == 101


def test_file_factory_rejects_empty_pattern_for_nonempty_file(test_file_factory):
    with pytest.raises(ValueError, match="content must not be empty"):
        test_file_factory("invalid.bin", 1, b"")
