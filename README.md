# Bilingual Interest Detection

Standalone bilingual interest scoring for dialogue systems. The package extracts
the lightweight interest-scoring idea from the affective dialogue system and
turns it into a reusable Python library with a CLI, structured results, tests,
and Spanish/English rules.

The detector is intentionally model-free: it does not download LLMs or machine
learning models. It uses deterministic keyword and regex rules to assign a score
from `0` to `100` to the current user message.

## Features

- Spanish and English interest scoring.
- Integer scores compatible with simple dialogue-routing logic.
- Keyword matching, phrase matching, and optional regex patterns.
- Accent normalization and lightweight stemming.
- Structured results with matched terms and patterns.
- CLI with plain-text and JSON output.
- No runtime dependencies outside the Python standard library.

## Scoring Overview

The default ranges mirror the original scoring behavior and extend it with
English equivalents:

```text
0      no configured interest signal detected
20     travel or place-related terms
50     animal-related terms
70     insect, cockroach, or swarm-related terms
100    health, glucose, pain, dizziness, or diabetes-related terms
```

When several rules match, the detector returns the highest score. `language="auto"`
tries both Spanish and English rule sets and returns the strongest match.

## Installation

```bash
python -m pip install -e ".[dev]"
```

## CLI

Spanish:

```bash
interest-detect "Siento dolor y mareo." --language es
```

English:

```bash
interest-detect "I feel dizzy and my glucose is low." --language en
```

JSON output:

```bash
interest-detect "My blood sugar is low." --language en --json --pretty
```

Score-only output:

```bash
interest-detect "Me gusta viajar a nuevos lugares." --language es --score-only
```

## Python API

```python
from bilingual_interest_detection import detect_interest, score_interest

spanish_score = score_interest("Siento dolor y mareo.", language="es")
english_result = detect_interest(
    "I feel dizzy and my glucose is low.",
    language="en",
)

print(spanish_score)
print(english_result.score)
print([match.value for match in english_result.matches])
```

## Custom Rules

You can pass your own ranges when creating a scorer:

```python
from bilingual_interest_detection import InterestScorer

scorer = InterestScorer(
    term_ranges={
        80: {"en": {"robotics"}, "es": {"robótica"}},
    },
    regex_ranges={
        90: {"en": (r"\bmachine learning\b",)},
    },
)

result = scorer.analyze("I want to study machine learning.", language="en")
print(result.score)
```

## Repository Layout

```text
src/bilingual_interest_detection/   importable Python package
tests/                              unit tests
examples/                           minimal usage examples
docs/                               scoring notes
```

