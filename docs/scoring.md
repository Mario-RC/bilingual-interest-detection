# Scoring Model

The detector is a deterministic scoring layer for dialogue systems. It assigns a
score to the current user utterance by matching normalized tokens against
predefined bilingual keyword ranges. Custom regex ranges can also be supplied
for deployment-specific phrases.

The score is intended as a compact signal for dialogue systems. It can inform
short-term conversational decisions, topic elaboration, engagement tracking, and
expressive behavior such as speech prosody or embodied feedback.

## Default Ranges

```text
25    low-interest topics such as politics, religion, football, wars, or taxes
50    medium-interest topics such as mathematics, cars, history, or languages
75    high-interest topics such as cinema, music, space, electronics, or travel
100   maximum-interest topics such as robotics, animals, AI, emotions, or psychology
```

The final score is the highest score triggered by any matching rule.

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

## Matching Steps

1. Normalize text to lowercase and remove accents.
2. Tokenize with a lightweight regex.
3. Remove common Spanish or English stopwords.
4. Apply a small suffix-based stemmer.
5. Match terms and optional regex patterns for the selected language.
6. Return the highest score plus the matched rules.

`language="auto"` does not run statistical language detection. It simply tries
Spanish and English rules and returns the highest-scoring match.
