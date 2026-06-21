# Kegel Health Assessment

Anonymous Flask web app for clinical ED screening, pathway triage, and customized Kegel (PFMT) plan generation.

## Setup (manual)

```powershell
cd e:\zhome\kegelapp
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Open http://localhost:5000

## Architecture

MCP-style **provider registry** dispatches modular services:

| Provider | Role |
|----------|------|
| `questionnaire` | Loads and validates 32-question battery |
| `scoring` | IIEF-EF score, severity, etiology mapping |
| `triage` | Pathway routing (PFMT, CBT, urology, cardiology, emergency) |
| `plan` | Customized Kegel plan via local LLM or template fallback |

**OOP UI components** (`SiteHeader`, `SiteFooter`, `PageLayout`) render shared chrome once — pages include `components/header.html` and `components/footer.html` via the layout composer.

## LLM configuration

### Local (default) — Ollama

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Ensure Ollama is running with a pulled model. If unavailable, the app falls back to a structured template plan.

### Hosted — Gemini API

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.0-flash
```

### Template only (no LLM)

```env
LLM_PROVIDER=template
```

## Privacy

Responses are stored in the Flask session only (browser cookie). No database, no accounts, no PII collection.

## Disclaimer

For informational purposes only. Not medical advice. See `ResearchDoc.md` and `Questionnaire.md` for clinical logic reference.
