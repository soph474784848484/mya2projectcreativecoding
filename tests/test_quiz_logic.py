import unittest

from quiz_logic import (
    QuizResponse,
    calibration_points,
    calibration_score,
    confidence_summary,
    knowledge_score,
    missed_question_ids,
)


class QuizLogicTests(unittest.TestCase):
    def test_knowledge_score(self):
        responses = [
            QuizResponse("1", "A", "A", "Know"),
            QuizResponse("2", "B", "C", "Guess"),
        ]
        self.assertEqual(knowledge_score(responses), 50.0)

    def test_calibration_rewards_confident_correct(self):
        response = QuizResponse("1", "A", "A", "Know")
        self.assertEqual(calibration_points(response), 2)

    def test_calibration_rewards_low_confidence_incorrect(self):
        response = QuizResponse("1", "B", "A", "Guess")
        self.assertEqual(calibration_points(response), 2)

    def test_calibration_penalises_confident_incorrect(self):
        response = QuizResponse("1", "B", "A", "Know")
        self.assertEqual(calibration_points(response), 0)

    def test_calibration_score(self):
        responses = [
            QuizResponse("1", "A", "A", "Know"),  # 2/2
            QuizResponse("2", "B", "A", "Think"), # 1/2
            QuizResponse("3", "C", "A", "Know"),  # 0/2
        ]
        self.assertEqual(calibration_score(responses), 50.0)

    def test_replay_returns_only_missed_questions(self):
        responses = [
            QuizResponse("q1", "A", "A", "Think"),
            QuizResponse("q2", "B", "C", "Know"),
            QuizResponse("q3", "D", "A", "Guess"),
        ]
        self.assertEqual(missed_question_ids(responses), ["q2", "q3"])

    def test_confidence_summary(self):
        responses = [
            QuizResponse("1", "A", "A", "Know"),
            QuizResponse("2", "B", "A", "Know"),
            QuizResponse("3", "A", "A", "Guess"),
        ]
        self.assertEqual(
            confidence_summary(responses),
            {
                "confident_correct": 1,
                "confident_incorrect": 1,
                "low_confidence_correct": 1,
            },
        )


if __name__ == "__main__":
    unittest.main()
