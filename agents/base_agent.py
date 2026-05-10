from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    name: str = "base-agent"

    @abstractmethod
    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
