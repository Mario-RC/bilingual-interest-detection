"""Command-line interface for bilingual interest detection."""

from __future__ import annotations

import argparse
import json
from typing import Any

from bilingual_interest_detection import InterestScorer


def main() -> None:
    parser = argparse.ArgumentParser(prog="interest-detect")
    parser.add_argument("text", help="Text to score.")
    parser.add_argument("--language", choices=["auto", "en", "es"], default="auto")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable result.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    parser.add_argument("--score-only", action="store_true", help="Print only the numeric score.")
    args = parser.parse_args()

    result = InterestScorer().analyze(args.text, language=args.language)

    if args.score_only:
        print(result.score)
        return

    if args.json:
        print(
            json.dumps(
                _json_payload(result),
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return

    matches = ", ".join(match.value for match in result.matches) if result.matches else "-"
    print(f"{result.score}\t{result.language}\t{matches}")


def _json_payload(result: Any) -> dict[str, Any]:
    return result.to_dict()


if __name__ == "__main__":
    main()
