# SURE? - Sophie Purseglove A2 Creative Coding

SURE? is a confidence-based trivia quiz designed to encourage users to think before immediately searching for an answer.

For every question, the user does two things:

1. Selects an answer.
2. Rates how confident they are using **Guess, Think, or Know**.

The quiz then provides feedback and, at the end, gives the user both a **Knowledge Score** and a **Calibration Score**.

The aim of SURE? is to make general knowledge more active by encouraging users to pause, retrieve information from memory, and reflect on how confident they are in what they know.

## What the quiz does

SURE? includes 12 trivia questions presented in a random order.

For each question, the user:

- selects an answer
- chooses a confidence level: Guess, Think, or Know
- locks in their response
- receives immediate feedback
- sees a short explanation of the correct answer

At the end of the quiz, the user can:

- view their Knowledge Score
- view their Calibration Score
- see their confidence patterns
- review every answer
- replay only the questions they answered incorrectly
- restart the full quiz

## How to run SURE?

SURE? runs locally in a web browser using Python.

### Step 1: Download the project

Make sure you are on the main page of this GitHub repository.

If you are viewing an individual file such as `README.md`, click the repository name at the top of the page to return to the main repository page.

Click the **Code** button and select **Download ZIP**.

Once the ZIP file has downloaded, double-click it to unzip it.

You should now have a normal project folder on your computer.

---

### Step 2: Open the project folder in Terminal

#### Mac

Open **Terminal**.

Type:

```bash
cd 
```

Make sure there is a space after `cd`.

Then drag the downloaded project folder directly into the Terminal window.

Terminal will automatically add the folder location.

Press **Enter**.

Terminal should now show that it is working inside the project folder.

#### Windows

Open the downloaded project folder.

Click in the folder address bar, type:

```text
powershell
```

and press **Enter**.

This opens PowerShell directly inside the project folder.

---

### Step 3: Install the required package

This project uses Streamlit to display the quiz in a web browser.

#### Mac

Copy and paste:

```bash
python3 -m pip install -r requirements.txt
```

Then press **Enter**.

#### Windows

Copy and paste:

```bash
py -m pip install -r requirements.txt
```

Then press **Enter**.

Wait until the installation has finished before continuing.

If Streamlit is already installed, the Terminal may display messages saying **Requirement already satisfied**. This is normal.

---

### Step 4: Start the quiz

#### Mac

Copy and paste:

```bash
python3 -m streamlit run app.py
```

Then press **Enter**.

#### Windows

Copy and paste:

```bash
py -m streamlit run app.py
```

Then press **Enter**.

### First-time Streamlit users

The first time Streamlit runs, it may display:

```text
Welcome to Streamlit!
Email:
```

Entering an email address is optional.

Simply leave the field blank and press **Enter** to continue.

---

### Step 5: Open SURE?

The quiz should automatically open in the default web browser.

If it does not open automatically, look in Terminal for:

```text
Local URL: http://localhost:8501
```

Then open a browser and enter:

```text
http://localhost:8501
```

Keep the Terminal or PowerShell window open while using the quiz.

---

### Step 6: Use the quiz

Once SURE? opens:

1. Start the quiz.
2. Select an answer.
3. Choose **Guess, Think, or Know**.
4. Lock in the response.
5. Read the feedback and explanation.
6. Continue through all 12 questions.
7. View the Knowledge Score and Calibration Score.
8. Review answers, replay missed questions, or restart the full quiz.

When finished, return to Terminal or PowerShell and press:

```text
Control + C
```

This stops the application.

## Project files

### `app.py`

The main application file.

It controls the interface, question flow, answer selection, confidence selection, feedback, results screen and replay functionality.

### `quiz_logic.py`

Contains the main scoring and quiz logic functions.

It calculates the Knowledge Score, Calibration Score and confidence patterns shown on the results screen.

### `questions.json`

Contains the 12 trivia questions, answer options, correct answers and explanations.

### `requirements.txt`

Contains the package required to run SURE?.

### `tests/test_quiz_logic.py`

Contains tests used to check that the quiz scoring and logic work correctly.

### `config.toml`

Contains the Streamlit display settings used by the project.

### `results-screen.png`

A screenshot showing the completed SURE? prototype running successfully.

## Project scope

The final prototype focuses on the core SURE? experience:

- 12 trivia questions
- random question order
- Guess, Think and Know confidence ratings
- immediate feedback
- answer explanations
- Knowledge Score
- Calibration Score
- confidence pattern summary
- answer review
- replaying missed questions
- restarting the full quiz

Additional ideas including timed rounds, category packs and streaks were considered during development but were intentionally kept outside the final prototype so the core functionality could be completed and tested properly.
