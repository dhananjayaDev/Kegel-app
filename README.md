# Kegel Health Assessment

Anonymous Flask web app for clinical ED screening, pathway triage, and customized Kegel (PFMT) plan generation.

## Setup (local dev)

```powershell
cd e:\zhome\kegelapp
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Open http://localhost:5000

## Three deployment targets

| Target | `APP_DEPLOYMENT` | LLM priority (`LLM_PROVIDER=auto`) |
|--------|------------------|-------------------------------------|
| **Web (hosted)** | `web` | Gemini (`.env`) → optional local Ollama → template |
| **Windows desktop** | `desktop` | Local Ollama → optional Gemini → template |
| **Android APK** | `android` | Local Ollama → optional Gemini → template |

The app **probes Ollama automatically** (`/api/tags`) across configured URLs and picks an installed model. Desktop and mobile builds include **Settings → Local LLM** to point at a PC on your Wi‑Fi (`http://192.168.x.x:11434`).

---

## 1. Web app (Gemini from `.env`)

Set in `.env` or your host’s environment:

```env
APP_DEPLOYMENT=web
LLM_PROVIDER=auto
GEMINI_API_KEY=your-key-here
FLASK_SECRET_KEY=random-secret
FLASK_DEBUG=0
```

### Render (included `render.yaml`)

1. Connect the repo to [Render](https://render.com)
2. Add `GEMINI_API_KEY` in the dashboard
3. Deploy — start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

After building desktop/APK, set download URLs:

```env
DESKTOP_APP_URL=https://your-cdn/KegelHealth-Setup.exe
MOBILE_APP_URL=https://your-cdn/kegel-health.apk
```

---

## 2. Windows desktop + installer

The desktop app embeds Flask in a native window (pywebview). The installer wizard explains **Ollama** setup.

### Build

```powershell
.\desktop\build.ps1
```

Outputs:

- `desktop\dist\KegelHealth.exe` — portable
- `dist\installer\KegelHealth-Setup.exe` — Inno Setup wizard (if Inno Setup 6 is installed)

### End-user Ollama setup

1. Install [Ollama](https://ollama.com/download)
2. Run `ollama pull llama3.2`
3. Launch **Kegel Health** — plans use the local model when Ollama is running

---

## 3. Android APK

The APK embeds Python (Chaquo) + Flask and loads the same UI in a WebView. Local LLM works when Ollama is reachable (same device via Termux on supported setups, or a PC on the same network).

### Build

1. Install [Android Studio](https://developer.android.com/studio) and JDK 17
2. Open the `android/` folder in Android Studio (Gradle sync)
3. Sync Python sources and build:

```powershell
.\android\build.ps1
```

4. Sign the release APK in Android Studio (**Build → Generate Signed Bundle / APK**)

APK path: `android/app/build/outputs/apk/release/`

---

## LLM configuration reference

```env
LLM_PROVIDER=auto    # auto | ollama | gemini | template
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
GEMINI_API_KEY=
```

Check runtime status: `GET /api/llm/status`

---

## Architecture

MCP-style **provider registry** dispatches modular services:

| Provider | Role |
|----------|------|
| `questionnaire` | Loads and validates 32-question battery |
| `scoring` | IIEF-EF score, severity, etiology mapping |
| `triage` | Pathway routing (PFMT, CBT, urology, cardiology, emergency) |
| `plan` | Customized Kegel plan via LLM chain or template fallback |

## Privacy

Responses are stored in the Flask session only (browser cookie). No database, no accounts, no PII collection.

## Disclaimer

For informational purposes only. Not medical advice. See `ResearchDoc.md` and `Questionnaire.md` for clinical logic reference.
