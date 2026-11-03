# CivicNex · Bengaluru CivicPilot

**Tagline:** Detect. Connect. Act. Transform.  
**Team identity:** Building practical AI solutions that make everyday city life better.  
**Theme:** Smarter Streets, Better Living.

Bengaluru CivicPilot is an agentic-AI smart-city prototype that turns resident reports into structured incidents, connects duplicate and potentially related reports, prioritizes neighbourhood impact, and supports human-reviewed simulated workflows.

## What's improved in this build

- Reworked responsive CivicNex interface with a consistent navy/teal visual system, mobile navigation, clear status and priority treatments.
- Dashboard totals, category distribution, priority watchlist and neighbourhood insights are derived from the backend incident list rather than hardcoded totals.
- Reporting supports all six civic challenge areas, validates required fields, accepts optional coordinates, and attempts AI triage after the report is safely created. If triage is unavailable, the saved report remains available.
- Command Centre now supports text search, priority/status filters, refresh, investigation links and database-backed status updates.
- Investigation view shows the original complaint, score, AI assessment and stored ripple relationships.
- Resolution Tracking and Neighbourhood Insights use database incidents, and simulated map elements are clearly labelled.
- Backend now permits the local Vite origin through CORS, and mock AI mode no longer requires the Anthropic SDK to be importable.
- Backend tests were repaired and expanded for validation, triage, seeded relationships and deterministic impact scoring.

## Run locally

### Backend (Windows PowerShell)

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Backend (macOS/Linux)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend (Windows/macOS/Linux)

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

Optional frontend API URL: create `frontend/.env` with `VITE_API_URL=http://localhost:8000`.

## AI mode

Mock mode is the default and works without API credentials. For Claude integration, install backend requirements and set these environment variables in the backend process:

```env
AI_MODE=llm
CLAUDE_API_KEY=your_key_here
```

Never commit a real API key. If Claude is unavailable, set `AI_MODE=mock` and restart the backend.

## Demo data

The project includes seeded Bengaluru demonstration scenarios. The existing reset endpoint is `POST http://localhost:8000/demo/reset`. It clears and reloads the demo incidents.

