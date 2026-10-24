# ASHA Sahayak

Voice-first, multilingual (Marathi/Hindi/English) triage assistant for frontline
health workers. A rule-based red-flag layer decides urgency; an optional LLM
only writes the referral note.

> **Important:** This is decision support, not a diagnosis. It is intended for
> trained health workers and should be reviewed by a clinician before real use.

## Features

- Voice or typed symptom entry using the browser Web Speech API
- Marathi, Hindi, and English interface and advice
- Safety-first red-flag triage rules
- Optional Anthropic-generated referral note with a fixed triage level
- SQLite case history, referral notes, and simple statistics

## Setup

Create a virtual environment (recommended), install the dependencies, and start
the Flask development server:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> in Chrome. Voice input requires a browser with
Web Speech API support.

The app works without an API key. To enable optional referral-note generation,
set `ANTHROPIC_API_KEY` before starting the server:

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your_key"
# macOS/Linux
export ANTHROPIC_API_KEY=your_key
```

Case data is stored locally in `cases.db`, which is intentionally excluded from
Git.

## Tools and credits

Flask, SQLite, Web Speech API, Anthropic Claude API (referral note text), and
Claude (AI assistance in building this project).
