# SURE?

SURE? is a confidence-based trivia quiz designed to encourage users to think before immediately searching for an answer.

For each question, the user:
1. Selects an answer.
2. Rates how confident they are using Guess, Think, or Know.

The quiz then gives feedback and, at the end, provides both a Knowledge Score and a Calibration Score.

The aim of SURE? is to make general knowledge more active by encouraging users to pause, retrieve information from memory, and reflect on how confident they are in what they know.

## What the quiz does

SURE? includes 12 trivia questions presented in a random order.

For each question, the user:
- selects an answer
- chooses a confidence level: Guess, Think, or Know
- locks in their response
- receives immediate feedback
- sees a short explanation of the correct answer

At the end of the quiz, the user can see:
- their Knowledge Score
- their Calibration Score
- confidence patterns
- all of their previous answers
- an option to replay missed questions
- an option to restart the full quiz## How to run SURE?

SURE? runs locally on a computer using Python.

### Step 1: Download the project

On this GitHub page, click Code and then Download ZIP.

Unzip the downloaded folder.

### Step 2: Open the project folder

On Mac, open Terminal.

On Windows, open Command Prompt or PowerShell.

Navigate to the downloaded SURE? project folder.

### Step 3: Install the required package

Mac:

python3 -m pip install -r requirements.txt

Windows:

py -m pip install -r requirements.txt

### Step 4: Start the quiz

Mac:

python3 -m streamlit run app.py

Windows:

py -m streamlit run app.py

The quiz should automatically open in the computer's web browser.

If it does not open automatically, enter:

http://localhost:8501

To stop the application, return to Terminal or Command Prompt and press Control + C.
## Project files

### app.py
This is the main application file. It controls the quiz interface, question flow, answer selection, confidence selection, feedback, results screen and replay options.

### quiz_logic.py
This file contains the quiz scoring and logic functions. It calculates the Knowledge Score, Calibration Score and confidence patterns shown at the end of the quiz.

### questions.json
This file contains the 12 trivia questions, answer options, correct answers and explanations.

### requirements.txt
This file contains the package required to run the quiz.

### tests/test_quiz_logic.py
This file contains tests used to check that the main scoring functions work correctly.

### results-screen.png
This is a screenshot of the completed SURE? prototype running successfully.

## Project scope

The final prototype focuses on:
- 12 trivia questions
- random question order
- Guess, Think and Know confidence ratings
- immediate feedback
- answer explanations
- Knowledge Score
- Calibration Score
- confidence pattern summary
- review of previous answers
- replaying missed questions
- restarting the full quiz

Possible extra features such as timed rounds, category packs and streaks were considered but were kept outside the final prototype so the core functionality could be developed and tested properly.

## Author

Sophie Purseglove  
Creative Coding A2  
SURE? Confidence-Based Trivia Quiz
