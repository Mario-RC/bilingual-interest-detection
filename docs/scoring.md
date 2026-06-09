# Scoring Model

The detector is a deterministic scoring layer for dialogue systems. It assigns a
score to the current user utterance by matching normalized tokens and regex
patterns against predefined bilingual rule ranges.

## Default Ranges

```text
20    travel and place-related terms
50    animal-related terms
70    insect, cockroach, or swarm-related terms
100   health, glucose, pain, dizziness, or diabetes-related terms
```

The final score is the highest score triggered by any matching rule.

## Matching Steps

1. Normalize text to lowercase and remove accents.
2. Tokenize with a lightweight regex.
3. Remove common Spanish or English stopwords.
4. Apply a small suffix-based stemmer.
5. Match terms and regex patterns for the selected language.
6. Return the highest score plus the matched rules.

`language="auto"` does not run statistical language detection. It simply tries
Spanish and English rules and returns the highest-scoring match.

