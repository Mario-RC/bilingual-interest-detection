import unittest

from bilingual_interest_detection import InterestScorer, detect_interest, score_interest


class InterestScorerTest(unittest.TestCase):
    def test_scores_spanish_maximum_keywords(self) -> None:
        self.assertEqual(
            score_interest("Me interesa la robótica y la psicología.", language="es"),
            100,
        )

    def test_scores_english_maximum_keywords(self) -> None:
        self.assertEqual(
            score_interest("I love robotics and artificial intelligence.", language="en"),
            100,
        )

    def test_scores_english_medium_keywords(self) -> None:
        self.assertEqual(score_interest("I like history and video games.", language="en"), 50)

    def test_scores_spanish_low_keywords(self) -> None:
        self.assertEqual(
            score_interest("Me aburren la política y los impuestos.", language="es"),
            25,
        )

    def test_scores_english_low_keywords(self) -> None:
        self.assertEqual(
            score_interest("Politics and taxes are boring.", language="en"),
            25,
        )

    def test_scores_spanish_high_keywords(self) -> None:
        self.assertEqual(score_interest("Me entusiasman el cine y la música.", language="es"), 75)

    def test_scores_unknown_text_zero(self) -> None:
        self.assertEqual(score_interest("Hoy he leído un libro.", language="es"), 0)

    def test_auto_language_returns_best_match(self) -> None:
        result = detect_interest("Me gusta el cine and social interaction.")

        self.assertEqual(result.score, 100)
        self.assertTrue(result.matches)

    def test_accent_normalization(self) -> None:
        self.assertEqual(score_interest("Me gusta la musica y la electronica.", language="es"), 75)

    def test_custom_ranges_are_supported(self) -> None:
        scorer = InterestScorer(term_ranges={80: {"en": {"robotics"}}}, regex_ranges={})

        result = scorer.analyze("I want to learn robotics.", language="en")

        self.assertEqual(result.score, 80)
        self.assertEqual(result.matches[0].value, "robotics")

    def test_custom_regex_ranges_are_supported(self) -> None:
        scorer = InterestScorer(
            term_ranges={},
            regex_ranges={90: {"en": (r"\bmachine learning\b",)}},
        )

        result = scorer.analyze("I want to study machine learning.", language="en")

        self.assertEqual(result.score, 90)
        self.assertEqual(result.matches[0].kind, "regex")


if __name__ == "__main__":
    unittest.main()
