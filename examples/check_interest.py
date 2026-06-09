from bilingual_interest_detection import detect_interest


def main() -> None:
    examples = [
        ("es", "Me interesa la robótica y la psicología."),
        ("en", "I love robotics and artificial intelligence."),
    ]

    for language, text in examples:
        result = detect_interest(text, language=language)
        print(f"[{language}] {text}")
        print(f"score={result.score}")
        print(f"matches={[match.value for match in result.matches]}")


if __name__ == "__main__":
    main()
