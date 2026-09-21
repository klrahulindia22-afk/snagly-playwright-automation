import json
import re
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from config.settings import Settings
from utils.data_factory import unique_name

ROOT = Path(__file__).resolve().parent
CASE_ID_PATTERN = re.compile(r"^SNAG-TC-\d{3}$")


@dataclass(frozen=True)
class CaseData:
    case_id: str
    module: str
    submodule: str
    test_type: str
    priority: str
    scenario: str
    source_test_data: str
    role: str
    values: dict[str, Any]


class TestDataRegistry:
    """Loads case metadata and resolves runtime-safe values on demand."""

    def __init__(self, cases_path: Path | None = None, common_path: Path | None = None):
        self.cases_path = cases_path or ROOT / "cases.json"
        self.common_path = common_path or ROOT / "common.json"
        self.common = self._read(self.common_path)
        payload = self._read(self.cases_path)
        self.expected_count = payload["expected_count"]
        self._case_items = payload["cases"]
        self._cases = {item["case_id"]: item for item in self._case_items}
        self.validate()

    @staticmethod
    def _read(path: Path) -> Any:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)

    def validate(self) -> None:
        ids = [item["case_id"] for item in self._case_items]
        if len(ids) != self.expected_count:
            raise ValueError(f"Expected {self.expected_count} cases but found {len(ids)}")
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate test case IDs found")
        invalid = [case_id for case_id in ids if not CASE_ID_PATTERN.fullmatch(case_id)]
        if invalid:
            raise ValueError(f"Invalid case IDs: {invalid}")
        expected = {f"SNAG-TC-{number:03d}" for number in range(1, self.expected_count + 1)}
        missing = sorted(expected - set(ids))
        if missing:
            raise ValueError(f"Missing test data for: {missing}")
        unknown_refs = {
            ref
            for item in self._case_items
            for ref in item.get("data_refs", [])
            if ref not in self.common
        }
        if unknown_refs:
            raise ValueError(f"Unknown common data references: {sorted(unknown_refs)}")

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._cases))

    def raw(self, case_id: str) -> dict[str, Any]:
        try:
            return deepcopy(self._cases[case_id])
        except KeyError as exc:
            raise KeyError(f"No test data registered for {case_id}") from exc

    def for_case(self, case_id: str, settings: Settings, temp_dir: Path) -> CaseData:
        item = self.raw(case_id)
        role = item.get("role", "owner")
        values = self._runtime_values(case_id, settings, temp_dir)
        for ref in item.get("data_refs", []):
            values[ref] = deepcopy(self.common[ref])
        values.update(deepcopy(item.get("values", {})))
        return CaseData(
            case_id=case_id,
            module=item["module"],
            submodule=item["submodule"],
            test_type=item["type"],
            priority=item["priority"],
            scenario=item["scenario"],
            source_test_data=item.get("source_test_data", ""),
            role=role,
            values=values,
        )

    def _runtime_values(self, case_id: str, settings: Settings, temp_dir: Path) -> dict[str, Any]:
        now = datetime.now(UTC)
        users = {
            "owner": {"email": settings.test_user_email, "password": settings.test_user_password},
            "team": {"email": settings.team_user_email, "password": settings.team_user_password},
            "client": {"email": settings.client_user_email, "password": settings.client_user_password},
            "other_owner": {"email": settings.other_owner_email, "password": settings.other_owner_password},
            "admin": {"email": settings.admin_email, "password": settings.admin_password},
        }
        return {
            "case_id": case_id,
            "run_id": settings.test_run_id,
            "users": users,
            "unique": {
                "board": unique_name("Board", settings.test_run_id),
                "list": unique_name("List", settings.test_run_id),
                "card": unique_name("Card", settings.test_run_id),
                "label": unique_name("Label", settings.test_run_id),
                "email": f"{unique_name('user', settings.test_run_id).lower()}@example.test",
            },
            "dates": {
                "past": (now - timedelta(days=1)).isoformat(),
                "today": now.isoformat(),
                "future": (now + timedelta(days=7)).isoformat(),
                "far_future": (now + timedelta(days=90)).isoformat(),
            },
            "temp_dir": str(temp_dir),
        }
