"""SURE? - a confidence-based general knowledge quiz.

Run with:
    streamlit run app.py

The app deliberately keeps its feature set close to the A1 MVP: 12 questions,
random order, confidence rating before feedback, explanations, two result
scores, and replay of missed questions.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import streamlit as st

from quiz_logic import (
    CONFIDENCE_LEVELS,
    QuizResponse,
    calibration_score,
    confidence_summary,
    knowledge_score,
    missed_question_ids,
)


APP_DIR = Path(__file__).parent
QUESTION_FILE = APP_DIR / "questions.json"


@st.cache_data
def load_questions() -> list[dict]:
    """Load the local question bank once and return it as a list of dictionaries."""
    with QUESTION_FILE.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    required = {"id", "question", "options", "correct", "explanation"}
    for question in questions:
        missing = required.difference(question)
        if missing:
            raise ValueError(f"Question {question.get('id', '?')} is missing: {missing}")
        if question["correct"] not in question["options"]:
            raise ValueError(f"Correct answer is not in options for {question['id']}")
    return questions


def question_lookup(questions: list[dict]) -> dict[str, dict]:
    """Create an ID-to-question dictionary for fast lookup during replay."""
    return {question["id"]: question for question in questions}


def initialise_state(questions: list[dict]) -> None:
    """Create all Streamlit session-state values needed by the quiz."""
    if "started" not in st.session_state:
        st.session_state.started = False
    if "question_ids" not in st.session_state:
        st.session_state.question_ids = [q["id"] for q in questions]
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "feedback_shown" not in st.session_state:
        st.session_state.feedback_shown = False
    if "quiz_mode" not in st.session_state:
        st.session_state.quiz_mode = "Full quiz"


def start_quiz(question_ids: list[str], mode: str) -> None:
    """Reset the quiz using a shuffled copy of the supplied question IDs."""
    shuffled_ids = list(question_ids)
    random.shuffle(shuffled_ids)
    st.session_state.started = True
    st.session_state.question_ids = shuffled_ids
    st.session_state.current_index = 0
    st.session_state.responses = []
    st.session_state.feedback_shown = False
    st.session_state.quiz_mode = mode


def current_response() -> QuizResponse | None:
    """Return the response attached to the current question, if one exists."""
    index = st.session_state.current_index
    if index < len(st.session_state.responses):
        return st.session_state.responses[index]
    return None


def record_answer(question: dict, selected_answer: str, confidence: str) -> None:
    """Convert form input to a QuizResponse and save it in session state."""
    response = QuizResponse(
        question_id=question["id"],
        selected_answer=selected_answer,
        correct_answer=question["correct"],
        confidence=confidence,
    )

    # Each question can only be recorded once. The feedback screen appears
    # before the current index is advanced, so appending here keeps responses
    # aligned with question order.
    if len(st.session_state.responses) == st.session_state.current_index:
        st.session_state.responses.append(response)
    st.session_state.feedback_shown = True


def go_to_next_question() -> None:
    """Advance the index and hide the previous question's feedback."""
    st.session_state.current_index += 1
    st.session_state.feedback_shown = False


def response_from_dict(data: dict) -> QuizResponse:
    """Rebuild QuizResponse objects stored as dictionaries in session state."""
    return QuizResponse(**data)


def serialise_responses() -> list[dict]:
    """Convert dataclass responses to plain dictionaries for predictable state use."""
    serialised = []
    for response in st.session_state.responses:
        if isinstance(response, QuizResponse):
            serialised.append(
                {
                    "question_id": response.question_id,
                    "selected_answer": response.selected_answer,
                    "correct_answer": response.correct_answer,
                    "confidence": response.confidence,
                }
            )
        else:
            serialised.append(response)
    return serialised


def get_response_objects() -> list[QuizResponse]:
    """Return all stored responses as QuizResponse objects."""
    result = []
    for response in st.session_state.responses:
        if isinstance(response, QuizResponse):
            result.append(response)
        else:
            result.append(response_from_dict(response))
    return result


def apply_theme() -> None:
    """Add a small amount of CSS so the app visually matches the SURE? pitch deck."""
    st.markdown(
        """
        <style>
        .stApp { background: #0B1732; color: #F5F7FF; }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }
        h1, h2, h3 { color: #F5F7FF; }
        .sure-kicker { color: #43D9FF; font-weight: 800; letter-spacing: .08em; }
        .sure-card {
            border: 1px solid #273858;
            background: #101D39;
            border-radius: 18px;
            padding: 1.1rem 1.2rem;
            margin: .5rem 0 1rem 0;
        }
        .sure-muted { color: #C8D1E3; }
        .stProgress > div > div > div > div { background-color: #C9F45B; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_intro(all_question_ids: list[str]) -> None:
    """Show the landing screen before the quiz starts."""
    st.markdown('<div class="sure-kicker">MEMORY BEFORE SEARCH</div>', unsafe_allow_html=True)
    st.title("SURE?")
    st.subheader("A quiz that scores what you know - and how well you know it.")
    st.markdown(
        """
        <div class="sure-card">
        Answer each question, then commit to <b>Guess</b>, <b>Think</b> or <b>Know</b>
        before feedback appears. At the end you will see a knowledge score and a
        confidence-calibration score.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("The calibration score is a simple prototype metric, not a psychological assessment.")
    if st.button("Start the 12-question quiz", type="primary", use_container_width=True):
        start_quiz(all_question_ids, "Full quiz")
        st.rerun()


def render_question(question: dict, number: int, total: int) -> None:
    """Render one question, collect answer + confidence, then show feedback."""
    progress = number / total
    st.progress(progress, text=f"{st.session_state.quiz_mode} • Question {number} of {total}")
    st.caption(question.get("category", "General knowledge"))
    st.header(question["question"])

    if not st.session_state.feedback_shown:
        with st.form(key=f"question_form_{question['id']}_{number}"):
            selected = st.radio(
                "Choose your answer",
                question["options"],
                index=None,
            )
            confidence = st.radio(
                "Before you see the answer, how sure are you?",
                CONFIDENCE_LEVELS,
                index=None,
                horizontal=True,
                help="Guess = low confidence, Think = medium confidence, Know = high confidence.",
            )
            submitted = st.form_submit_button("Lock in answer", type="primary", use_container_width=True)

        if submitted:
            if selected is None or confidence is None:
                st.warning("Choose both an answer and a confidence level before locking it in.")
            else:
                record_answer(question, selected, confidence)
                # Store plain dictionaries before rerun so the state remains simple.
                st.session_state.responses = serialise_responses()
                st.rerun()
        return

    response = current_response()
    if isinstance(response, dict):
        response = response_from_dict(response)

    if response is None:
        st.error("The response could not be loaded. Restart the quiz to continue.")
        return

    if response.is_correct:
        st.success(f"Correct. You chose {response.selected_answer} and rated it {response.confidence}.")
    else:
        st.error(
            f"Not quite. You chose {response.selected_answer}; the correct answer is {response.correct_answer}."
        )

    st.info(question["explanation"])
    if question.get("source_url"):
        st.markdown(f"Source: [{question.get('source_name', 'Reference')}]({question['source_url']})")

    label = "See results" if number == total else "Next question"
    if st.button(label, type="primary", use_container_width=True):
        go_to_next_question()
        st.rerun()


def result_message(knowledge: float, calibration: float) -> str:
    """Create a neutral interpretation using both result scores."""
    if knowledge >= 75 and calibration >= 75:
        return "You knew a lot and your confidence usually matched the outcome."
    if knowledge >= 75 and calibration < 75:
        return "Your knowledge score was strong, but your confidence did not always match the result."
    if knowledge < 75 and calibration >= 75:
        return "Your confidence was fairly well calibrated, even when you did not know every answer."
    return "There is room to build both knowledge and confidence calibration. Replay missed questions to try again."


def render_results(question_map: dict[str, dict], all_question_ids: list[str]) -> None:
    """Show final scores, confidence patterns, and replay controls."""
    responses = get_response_objects()
    k_score = knowledge_score(responses)
    c_score = calibration_score(responses)
    patterns = confidence_summary(responses)
    missed_ids = missed_question_ids(responses)

    st.markdown('<div class="sure-kicker">RESULTS</div>', unsafe_allow_html=True)
    st.title("How sure were you?")
    left, right = st.columns(2)
    left.metric("Knowledge score", f"{k_score:.0f}%")
    right.metric("Calibration score", f"{c_score:.0f}%")
    st.markdown(f"**{result_message(k_score, c_score)}**")

    st.markdown("### Confidence patterns")
    st.write(f"Confident and correct: **{patterns['confident_correct']}**")
    st.write(f"Confident but incorrect: **{patterns['confident_incorrect']}**")
    st.write(f"Low confidence but correct: **{patterns['low_confidence_correct']}**")

    with st.expander("Review every answer"):
        for index, response in enumerate(responses, start=1):
            question = question_map[response.question_id]
            icon = "✓" if response.is_correct else "✗"
            st.markdown(
                f"**{icon} {index}. {question['question']}**  \n"
                f"Your answer: {response.selected_answer}  \n"
                f"Confidence: {response.confidence}  \n"
                f"Correct answer: {response.correct_answer}"
            )
            st.caption(question["explanation"])

    st.divider()
    col1, col2 = st.columns(2)
    if missed_ids:
        if col1.button("Replay missed questions", use_container_width=True):
            start_quiz(missed_ids, "Replay missed")
            st.rerun()
    else:
        col1.success("No missed questions to replay.")

    if col2.button("Restart full quiz", use_container_width=True):
        start_quiz(all_question_ids, "Full quiz")
        st.rerun()


def main() -> None:
    """Coordinate the full Streamlit application."""
    st.set_page_config(page_title="SURE?", page_icon="?", layout="centered")
    apply_theme()

    questions = load_questions()
    q_map = question_lookup(questions)
    all_question_ids = [question["id"] for question in questions]
    initialise_state(questions)

    if not st.session_state.started:
        render_intro(all_question_ids)
        return

    total = len(st.session_state.question_ids)
    index = st.session_state.current_index

    if index >= total:
        render_results(q_map, all_question_ids)
        return

    question_id = st.session_state.question_ids[index]
    render_question(q_map[question_id], index + 1, total)


if __name__ == "__main__":
    main()
