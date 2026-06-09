import unittest

from bilingual_interest_detection import InterestScorer, detect_interest, score_interest


class InterestScorerTest(unittest.TestCase):
    def test_scores_spanish_medical_keywords_high(self) -> None:
        self.assertEqual(score_interest("Siento dolor y mareo.", language="es"), 100)

    def test_scores_english_medical_keywords_high(self) -> None:
        self.assertEqual(
            score_interest("I feel dizzy and my glucose is low.", language="en"),
            100,
        )

    def test_scores_english_blood_sugar_regex_high(self) -> None:
        result = detect_interest("My blood sugar is low.", language="en")

        self.assertEqual(result.score, 100)
        self.assertTrue(any(match.kind == "regex" for match in result.matches))

    def test_scores_spanish_travel_keywords_low(self) -> None:
        self.assertEqual(score_interest("Me gusta viajar a nuevos lugares.", language="es"), 20)

    def test_scores_english_travel_keywords_low(self) -> None:
        self.assertEqual(score_interest("I enjoy traveling to new places.", language="en"), 20)

    def test_scores_unknown_text_zero(self) -> None:
        self.assertEqual(score_interest("Hoy he leído un libro.", language="es"), 0)

    def test_auto_language_returns_best_match(self) -> None:
        result = detect_interest("Siento pinchazos y dizziness.")

        self.assertEqual(result.score, 100)
        self.assertTrue(result.matches)

    def test_accent_normalization(self) -> None:
        self.assertEqual(score_interest("Quiero viajar en avión.", language="es"), 20)

    def test_custom_ranges_are_supported(self) -> None:
        scorer = InterestScorer(term_ranges={80: {"en": {"robotics"}}}, regex_ranges={})

        result = scorer.analyze("I want to learn robotics.", language="en")

        self.assertEqual(result.score, 80)
        self.assertEqual(result.matches[0].value, "robotics")


if __name__ == "__main__":
    unittest.main()

