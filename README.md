# Bilingual Interest Detection

Standalone bilingual interest scoring for dialogue systems. The package turns
rule-based user-interest detection into a reusable Python library with a CLI,
structured results, tests, and Spanish/English rules.

The detector is intentionally model-free: it does not download LLMs or machine
learning models. It uses deterministic keyword rules, plus optional custom regex
rules, to assign a score from `0` to `100` to the current user message.

## Features

- Spanish and English interest scoring.
- Integer scores compatible with simple dialogue-routing logic.
- Keyword matching, phrase matching, and optional regex patterns.
- Accent normalization and lightweight stemming.
- Structured results with matched terms and patterns.
- CLI with plain-text and JSON output.
- No runtime dependencies outside the Python standard library.

## Scoring Overview

Each message is assigned the highest score associated with any matching keyword.
The resulting interest signal can be used by dialogue systems to modulate
conversation strategy, internal engagement variables, speech expressiveness, or
proactive topic elaboration.

The default ranges are organized into four scoring tiers:

```text
0      no configured interest signal detected
25     low-interest topics such as politics, religion, football, wars, or taxes
50     medium-interest topics such as mathematics, cars, history, or languages
75     high-interest topics such as cinema, music, space, electronics, or travel
100    maximum-interest topics such as robotics, animals, AI, emotions, or psychology
```

When several rules match, the detector returns the highest score. `language="auto"`
tries both Spanish and English rule sets and returns the strongest match.

## Default Keywords

```text
Score   English                                      Spanish
25      politics, religion, football, wars,          política, religión, fútbol, guerras,
        economy, gossip, bureaucracy, taxes,         economía, cotilleos, burocracia,
        finance, strategy                            impuestos, finanzas, estrategia
50      mathematics, learning, cars, cartoons,       matemáticas, aprender, coches,
        history, literature, video games,            dibujos animados, historia, literatura,
        languages, physics, geography                videojuegos, idiomas, física, geografía
75      cinema, theater, music, space, mechanics,    cine, teatro, música, espacio, mecánica,
        the avengers, science fiction, electronics,  los vengadores, ciencia ficción, electrónica,
        engines, travel, fashion                     motor, viajes, moda
100     robotics, animals, research, technology,     robótica, animales, investigación, tecnología,
        pilates, artificial intelligence, emotions,  pilates, inteligencia artificial, emociones,
        social interaction, programming, psychology  interacción social, programación, psicología
```

## Installation

```bash
python -m pip install -e ".[dev]"
```

## CLI

Spanish:

```bash
interest-detect "Me interesa la robótica y la psicología." --language es
```

English:

```bash
interest-detect "I love robotics and artificial intelligence." --language en
```

JSON output:

```bash
interest-detect "I love robotics and artificial intelligence." --language en --json --pretty
```

Score-only output:

```bash
interest-detect "Me aburren la política y los impuestos." --language es --score-only
```

## Python API

```python
from bilingual_interest_detection import detect_interest, score_interest

spanish_score = score_interest("Me interesa la robótica y la psicología.", language="es")
english_result = detect_interest(
    "I love robotics and artificial intelligence.",
    language="en",
)

print(spanish_score)
print(english_result.score)
print([match.value for match in english_result.matches])
```

## Custom Rules

The built-in word lists and stopwords live in
`src/bilingual_interest_detection/defaults.py`, keeping the scoring logic focused
on matching and ranking. For small adaptations, you can either edit that file or
pass custom ranges at runtime.

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
