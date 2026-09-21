import re
from dataclasses import dataclass
from uuid import uuid4


def unique_name(prefix: str, run_id: str = "local") -> str:
    safe = re.sub(r"[^a-zA-Z0-9-]+", "-", run_id).strip("-")[:16] or "local"
    return f"E2E-{prefix}-{safe}-{uuid4().hex[:8]}"


@dataclass(frozen=True)
class BoardData:
    name: str
    description: str

    @classmethod
    def build(cls, run_id: str) -> "BoardData":
        return cls(unique_name("Board", run_id), "Created by Playwright automation; safe to remove.")
