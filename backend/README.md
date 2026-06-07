# OmniMind Backend — Phase 1 Foundation

> A production-quality FastAPI backend foundation for the OmniMind AI platform.

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app creation, CORS, lifecycle, error handlers
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # All endpoint definitions (/, /health, /chat)
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Pydantic Settings — env-based configuration
│   ├── models/
│   │   └── __init__.py      # (Future) SQLAlchemy / ORM models
│   ├── schemas/
│   │   ├── __init__.py      # Re-exports for convenience
│   │   ├── chat.py          # ChatRequest / ChatResponse
│   │   └── common.py        # HealthResponse, RootResponse, ErrorResponse
│   ├── services/
│   │   └── __init__.py      # (Future) Business logic — AI calls, memory, RAG
│   └── utils/
│       ├── __init__.py
│       └── logging_config.py # Structured logging setup
├── requirements.txt
├── .env                      # Local dev environment variables
├── .gitignore
└── README.md                 # ← You are here
```

### Why each folder exists

| Folder | Purpose |
|--------|---------|
| `api/` | HTTP layer — defines routes and request/response contracts |
| `config/` | Centralised settings so nothing is hard-coded |
| `models/` | Database/ORM models (added in future phases) |
| `schemas/` | Pydantic models for request validation & response serialisation |
| `services/` | Business logic, external API calls, AI integrations |
| `utils/` | Cross-cutting helpers (logging, date formatting, etc.) |

---

## Quick Setup

### 1. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will be accessible at **http://localhost:8000**.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root — confirms the server is running |
| GET | `/health` | Health check for monitoring/orchestration |
| POST | `/chat` | Temporary echo endpoint (frontend ↔ backend verification) |

### GET /

```json
{ "message": "OmniMind Backend Running" }
```

### GET /health

```json
{ "status": "healthy", "service": "OmniMind Backend" }
```

### POST /chat

**Request body:**
```json
{ "message": "Hello OmniMind" }
```

**Response:**
```json
{ "reply": "Received: Hello OmniMind" }
```

**Validation error (empty message):**
```json
{ "success": false, "error": "String should have at least 1 character" }
```

---

## API Documentation (auto-generated)

FastAPI provides interactive docs out of the box:

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI — try endpoints live |
| http://localhost:8000/redoc | ReDoc — clean readable API reference |

These are generated automatically from the Pydantic schemas and route decorators. No manual OpenAPI authoring needed.

---

## Configuration

All settings are managed via environment variables (loaded from `.env`).

| Variable | Default | Purpose |
|----------|---------|---------|
| `PROJECT_NAME` | OmniMind Backend | Shown in docs title |
| `VERSION` | 0.1.0 | API version |
| `API_PREFIX` | /api/v1 | (Reserved for future versioned routes) |
| `FRONTEND_URL` | http://localhost:5173 | Added to CORS allowed origins |
| `DEBUG` | false | Enables verbose logging |

---

## CORS — What & Why

**Cross-Origin Resource Sharing (CORS)** is a browser security mechanism.

Your React frontend (running on `localhost:5173`) and the backend (on `localhost:8000`) are different **origins**. Without CORS headers, the browser blocks the frontend from calling the backend.

This backend allows:
- Origins: `http://localhost:5173`, `http://localhost:3000`
- Methods: `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`
- Credentials: enabled

---

## Error Handling

All errors follow the same envelope:

```json
{ "success": false, "error": "<human-readable message>" }
```

| Scenario | HTTP Status | Example error |
|----------|-------------|---------------|
| Validation failure | 422 | "String should have at least 1 character" |
| Server error | 500 | "Internal server error" |

---

## Logging

Structured logs are written to stdout in the format:

```
2026-06-07 19:30:00 | INFO     | app.main | Starting OmniMind Backend v0.1.0
2026-06-07 19:30:01 | INFO     | app.api.routes | Chat message received: Hello OmniMind
```

Logs capture: startup, shutdown, every chat request, and any unhandled exceptions.

---

## Testing the Backend

### Using curl

```bash
# Root
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Chat (valid)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello OmniMind"}'

# Chat (empty — triggers validation error)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```

### Using the browser

Open http://localhost:8000/docs and use the Swagger UI "Try it out" buttons.

---

## Frontend Integration (React)

### Complete fetch example

```jsx
import { useState } from "react";

function Chat() {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendMessage = async () => {
    setLoading(true);
    setError("");
    setReply("");

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Request failed");
      }

      const data = await res.json();
      setReply(data.reply);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? "Sending..." : "Send"}
      </button>

      {reply && <p><strong>Reply:</strong> {reply}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Chat;
```

### Request flow

```
React UI  →  HTTP POST /chat  →  FastAPI  →  Pydantic validates  →  JSON response  →  React state update
```

---

## What's NOT in Phase 1

This foundation deliberately excludes:

- AI model integrations (OpenAI, Claude, Gemini, Ollama)
- Authentication / JWT
- Database / ORM
- Memory systems / Vector DBs / RAG
- File uploads
- Agents

These will be layered on top of this clean foundation in future phases.
