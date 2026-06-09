"""Public schemas for interest detection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Language = Literal["auto", "en", "es"]


@dataclass(frozen=True)
class InterestMatch:
    """Single rule match contributing to an interest score."""

    score: int
    language: str
    value: str
    kind: Literal["term", "regex"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "language": self.language,
            "value": self.value,
            "kind": self.kind,
        }


@dataclass(frozen=True)
class InterestResult:
    """Structured output for a user-interest scoring pass."""

    score: int
    language: str
    matches: tuple[InterestMatch, ...] = field(default_factory=tuple)
    tokens: tuple[str, ...] = field(default_factory=tuple)

    @property
    def matched(self) -> bool:
        return self.score > 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "language": self.language,
            "matched": self.matched,
            "matches": [match.to_dict() for match in self.matches],
            "tokens": list(self.tokens),
        }

