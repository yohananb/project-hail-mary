# 🛠 Project Hail Mary — AI Debugging Assistant

A web-based debugging assistant that uses Claude AI to diagnose code errors. Instead of sending your error to a generic AI prompt, it first classifies what type of problem you have, then routes it to a specialized AI expert for that specific error type.

**Live demo:** https://project-hail-mary-n749.onrender.com

---

## How It Works

Most AI debugging tools send your error to one generic prompt. This app uses a two-step AI pipeline:

**Step 1 — Classification:** Claude reads your input and classifies it into one of four categories:
- `TERMINAL_ERROR` — errors that appear in the terminal (ModuleNotFoundError, SyntaxError, etc.)
- `CODE_BUG` — code that runs but produces wrong results
- `CONFIG_ISSUE` — environment or configuration problems
- `GENERAL_QUESTION` — general coding questions

**Step 2 — Specialized Diagnosis:** Based on the classification, the app routes to a specialized prompt designed specifically for that error type. A terminal error gets a terminal expert. A code bug gets a debugging expert. The diagnosis is more accurate because the AI is primed for exactly that type of problem.

---

## Architecture

```
User submits error
        ↓
Flask receives the form submission
        ↓
Claude API Call #1 — Classifier
(returns one word: TERMINAL_ERROR, CODE_BUG, CONFIG_ISSUE, or GENERAL_QUESTION)
        ↓
App picks the matching specialized system prompt
        ↓
Claude API Call #2 — Specialist Diagnosis
(uses the specialized prompt for that error type)
        ↓
Flask sends diagnosis back to the browser
User sees the result + error type badge
```

---

## Technical Decisions

**Why two API calls instead of one?**
A single generic prompt produces generic answers. By classifying first, we can give Claude a specific role and context before diagnosing. A terminal error needs different expertise than a code bug. The classification step costs almost nothing (max_tokens=50, one word response) but significantly improves diagnosis quality.

**Why Flask?**
Flask is a lightweight Python web framework that acts as the bridge between the browser and the Claude API. It receives form submissions, passes them through the AI pipeline, and returns results to the HTML template.

**Why Tailwind CSS?**
Tailwind is the industry standard utility-first CSS framework. Instead of writing separate CSS files, styling is applied directly in HTML via utility classes. Faster to build, easier to maintain, and signals familiarity with modern frontend tooling.

**Why Render for deployment?**
Free tier, automatic deploys on every GitHub push, and straightforward environment variable management for keeping API keys secure.

---

## Tech Stack

- **Python** — core language
- **Flask** — web framework / server
- **Anthropic Claude API** — AI classification and diagnosis (claude-opus-4-8)
- **Tailwind CSS** — styling via CDN
- **Gunicorn** — production web server
- **Render** — deployment and hosting

---

## What I Learned Building This

- How to make API calls to a large language model and handle responses
- How to design a multi-step AI pipeline (classify → route → diagnose)
- How Flask connects Python backend logic to HTML frontend
- Environment variable management for keeping API keys secure
- Error handling — validating user input before touching the API
- Deploying a Python web app to production with Gunicorn and Render
- Using Git/GitHub to track progress and document the build process

---

## Running Locally

```bash
git clone https://github.com/yohananb/project-hail-mary
cd project-hail-mary
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

Run the app:
```bash
python3 app.py
```

Visit `http://127.0.0.1:5000`
