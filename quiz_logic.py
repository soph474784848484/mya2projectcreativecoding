"""Core quiz logic for SURE?.

This module deliberately contains no Streamlit code so the scoring and replay
logic can be tested independently from the interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


CONFIDENCE_LEVELS = ("Guess", "Think", "Know")
CONFIDENCE_WEIGHT = {"Guess": 1, "Think": 2, "Know": 3}


@dataclass(frozen=True)
class QuizResponse:
    """One completed answer from the player."""

    question_id: str
    selected_answer: str
    correct_answer: str
    confidence: str

    @property
    def is_correct(self) -> bool:
        """Return True when the player's selected answer is correct."""
        return self.selected_answer == self.correct_answer


def knowledge_score(responses: Sequence[QuizResponse]) -> float:
    """Return the percentage of questions answered correctly."""
    if not responses:
        return 0.0
    correct = sum(response.is_correct for response in responses)
    return round((correct / len(responses)) * 100, 1)


def calibration_points(response: QuizResponse) -> int:
    """Score how well confidence matches correctness on a 0-2 scale.

    Correct + Know = 2 points; correct + Think = 1; correct + Guess = 0.
    Incorrect + Guess = 2 points; incorrect + Think = 1; incorrect + Know = 0.

    The metric is intentionally simple and transparent. It is a prototype
    learning signal, not a validated psychological measurement.
    """
    if response.confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"Unknown confidence level: {response.confidence}")

    if response.confidence == "Think":
        return 1
    if response.is_correct and response.confidence == "Know":
        return 2
    if (not response.is_correct) and response.confidence == "Guess":
        return 2
    return 0


def calibration_score(responses: Sequence[QuizResponse]) -> float:
    """Return calibration as a percentage from 0 to 100."""
    if not responses:
        return 0.0
    earned = sum(calibration_points(response) for response in responses)
    possible = len(responses) * 2
    return round((earned / possible) * 100, 1)


def missed_question_ids(responses: Iterable[QuizResponse]) -> list[str]:
    """Return IDs for questions the player answered incorrectly."""
    return [response.question_id for response in responses if not response.is_correct]


def confidence_summary(responses: Sequence[QuizResponse]) -> dict[str, int]:
    """Count useful confidence patterns for the result screen."""
    summary = {
        "confident_correct": 0,
        "confident_incorrect": 0,
        "low_confidence_correct": 0,
    }
    for response in responses:
        if response.is_correct and response.confidence == "Know":
            summary["confident_correct"] += 1
        elif (not response.is_correct) and response.confidence == "Know":
            summary["confident_incorrect"] += 1
        elif response.is_correct and response.confidence == "Guess":
            summary["low_confidence_correct"] += 1
    return summary
