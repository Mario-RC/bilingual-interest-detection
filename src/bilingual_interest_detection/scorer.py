"""Lightweight bilingual interest scoring with keyword and regex rules."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from bilingual_interest_detection.defaults import (
    DEFAULT_IGNORE_WORDS,
    DEFAULT_REGEX_RANGES,
    DEFAULT_TERM_RANGES,
    ENGLISH_SUFFIXES,
    SPANISH_SUFFIXES,
)
from bilingual_interest_detection.schemas import InterestMatch, InterestResult, Language


@dataclass
class InterestScorer:
    """Score how relevant a text is for predefined user-interest ranges."""

    term_ranges: dict[int, dict[str, set[str]]] = field(
        default_factory=lambda: {
            score: {language: set(terms) for language, terms in per_language.items()}
            for score, per_language in DEFAULT_TERM_RANGES.items()
        }
    )
    regex_ranges: dict[int, dict[str, tuple[str, ...]]] = field(
        default_factory=lambda: {
            score: dict(per_language) for score, per_language in DEFAULT_REGEX_RANGES.items()
        }
    )
    ignore_words: dict[str, set[str]] = field(
        default_factory=lambda: {
            language: set(words) for language, words in DEFAULT_IGNORE_WORDS.items()
        }
    )

    def score(self, sentence: str, *, language: Language = "auto") -> int:
        """Return only the highest interest score."""

        return self.analyze(sentence, language=language).score

    def analyze(self, sentence: str, *, language: Language = "auto") -> InterestResult:
        """Return the score plus matched terms, regexes, and normalized tokens."""

        languages = ("es", "en") if language == "auto" else (language,)
        matches: list[InterestMatch] = []
        tokens_by_language: dict[str, tuple[str, ...]] = {}

        for candidate_language in languages:
            tokens = tuple(self._tokenize(sentence, candidate_language))
            tokens_by_language[candidate_language] = tokens
            token_stems = {self._stem(token, candidate_language) for token in tokens}
            normalized_text = _normalize(sentence)

            for score, per_language_terms in self.term_ranges.items():
                terms = per_language_terms.get(candidate_language, set())
                for term in sorted(terms):
                    if self._term_matches(term, normalized_text, token_stems, candidate_language):
                        matches.append(
                            InterestMatch(
                                score=score,
                                language=candidate_language,
                                value=term,
                                kind="term",
                            )
                        )

            for score, per_language_patterns in self.regex_ranges.items():
                patterns = per_language_patterns.get(candidate_language, ())
                for pattern in patterns:
                    if re.search(pattern, normalized_text, flags=re.IGNORECASE):
                        matches.append(
                            InterestMatch(
                                score=score,
                                language=candidate_language,
                                value=pattern,
                                kind="regex",
                            )
                        )

        if not matches:
            selected_language = "auto" if language == "auto" else language
            selected_tokens = tokens_by_language.get(selected_language, ())
            return InterestResult(score=0, language=selected_language, tokens=selected_tokens)

        best_score = max(match.score for match in matches)
        selected_language = next(match.language for match in matches if match.score == best_score)
        selected_matches = tuple(match for match in matches if match.score == best_score)
        selected_tokens = tokens_by_language.get(selected_language, ())
        return InterestResult(
            score=best_score,
            language=selected_language,
            matches=selected_matches,
            tokens=selected_tokens,
        )

    def _tokenize(self, sentence: str, language: str) -> list[str]:
        normalized = _normalize(sentence)
        ignore = set(self.ignore_words.get(language, set()))
        ignore.update(word for word in normalized.split() if len(word) == 2)
        words = re.findall(r"[a-z0-9]+", normalized)
        return sorted({word for word in words if word not in ignore})

    def _term_matches(
        self,
        term: str,
        normalized_text: str,
        token_stems: set[str],
        language: str,
    ) -> bool:
        normalized_term = _normalize(term)
        phrase_pattern = rf"\b{re.escape(normalized_term)}\b"
        if " " in normalized_term and re.search(phrase_pattern, normalized_text):
            return True
        term_tokens = re.findall(r"[a-z0-9]+", normalized_term)
        term_stems = {self._stem(token, language) for token in term_tokens}
        return bool(term_stems) and term_stems.issubset(token_stems)

    @staticmethod
    def _stem(word: str, language: str) -> str:
        suffixes = SPANISH_SUFFIXES if language == "es" else ENGLISH_SUFFIXES
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 1:
                if language == "en" and suffix == "ies":
                    return f"{word[: -len(suffix)]}y"
                return word[: -len(suffix)]
        return word


def score_interest(sentence: str, *, language: Language = "auto") -> int:
    """Compatibility helper returning only the integer score."""

    return InterestScorer().score(sentence, language=language)


def detect_interest(sentence: str, *, language: Language = "auto") -> InterestResult:
    """Return a structured interest detection result."""

    return InterestScorer().analyze(sentence, language=language)


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    without_marks = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", without_marks).strip()
