"""Bilingual user-interest scoring for dialogue systems."""

from bilingual_interest_detection.schemas import InterestMatch, InterestResult, Language
from bilingual_interest_detection.scorer import InterestScorer, detect_interest, score_interest

__all__ = [
    "InterestMatch",
    "InterestResult",
    "InterestScorer",
    "Language",
    "detect_interest",
    "score_interest",
]

