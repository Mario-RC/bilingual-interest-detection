from bilingual_interest_detection import detect_interest


def main() -> None:
    examples = [
        ("es", "Siento pinchazos en el brazo y un poco de mareo."),
        ("en", "I feel dizzy and my glucose is low."),
    ]

    for language, text in examples:
        result = detect_interest(text, language=language)
        print(f"[{language}] {text}")
        print(f"score={result.score}")
        print(f"matches={[match.value for match in result.matches]}")


if __name__ == "__main__":
    main()

