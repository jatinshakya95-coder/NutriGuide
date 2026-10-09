# Agentic AI SDLC – NutriGuide Nutrition Agent

**Project:** NutriGuide – Personalised Nutrition Agentic AI Application  
**Model:** qwen/qwen3-8b via Groq API  
**Framework:** Python · Streamlit  
**Date:** 2025

---

## Phase 1 – Problem Definition

### Problem Statement
Millions of people lack access to personalised nutrition guidance due to the high cost of
professional dietitian services and the complexity of nutritional science. Generic diet
advice often ignores individual medical conditions, cultural food preferences, and local
ingredient availability.

### Goal
Build an AI-powered agent that collects a user's personal profile and generates a
personalised daily nutrition plan while answering follow-up diet questions in a conversational
chat interface.

### Success Criteria
| Criterion | Target |
|---|---|
| Plan relevance | Plan accounts for age, diet type, medical history, and location |
| Guardrail compliance | Zero instances of medical diagnosis or prescription |
| Usability | Beginner-friendly UI; no setup beyond API key |
| Ethics | Empathetic, non-judgmental tone; disclaimer on every recommendation |

---

## Phase 2 – Requirements Analysis

### Functional Requirements
- FR-01: Collect user profile (name, age, diet preference, medical history, location).
- FR-02: Generate a personalised daily nutrition plan on profile submission.
- FR-03: Provide a multi-turn chat interface for nutrition Q&A.
- FR-04: Allow plan regeneration on demand.
- FR-05: Display a medical disclaimer after every nutrition recommendation.

### Non-Functional Requirements
- NFR-01: API key must be accepted at runtime; never stored or logged.
- NFR-02: Max tokens per LLM call ≤ 900 (Groq free-tier OTPM compliance).
- NFR-03: Application must run with `streamlit run app.py` only.
- NFR-04: UI must be accessible to non-technical users.
- NFR-05: Response time < 15 seconds per LLM call on a typical free-tier quota.

### Constraints
- Must use Groq API (groq >= 0.9.0) and model `qwen/qwen3-8b`.
- Python and Streamlit only — no raw HTML, CSS, or JavaScript.
- Must run on Windows (run.bat) and any OS via CLI.

---

## Phase 3 – Agent Design

### Agent Architecture
NutriGuide uses a **single-agent, multi-turn conversational** architecture:

```
User Input
    │
    ▼
[Streamlit UI]  ←──── sidebar: API key + profile form
    │
    ▼
[nutrition_agent.py]
    ├── build_profile_context()   ← formats user profile as LLM context
    ├── generate_nutrition_plan() ← one-shot plan generation
    └── chat_with_agent()         ← stateful multi-turn conversation
    │
    ▼
[groq_client.py]
    └── call_llm()  ← sends messages to Groq API, returns reply
    │
    ▼
Groq API (qwen/qwen3-8b)
    │
    ▼
[Post-processing]
    └── append DISCLAIMER if recommendation keywords detected
    │
    ▼
Streamlit UI (plan tab / chat tab)
```

### Agent Components
| Component | Responsibility |
|---|---|
| `app.py` | UI rendering, session state, user interaction |
| `nutrition_agent.py` | System prompt, guardrails, plan generation, chat orchestration |
| `groq_client.py` | Stateless LLM call wrapper; API key handling |

### Memory Strategy
- **Short-term memory:** LLM conversation history stored in `st.session_state.llm_history`.
- **Window:** Last 20 messages (10 exchanges) kept to stay within token limits.
- **No long-term / persistent memory** by design (privacy-first).

---

## Phase 4 – LLM and Capability Selection

### LLM Selection Rationale
| Factor | Decision |
|---|---|
| Provider | Groq (ultra-low latency inference) |
| Model | `qwen/qwen3-8b` – strong reasoning, multilingual, free-tier available |
| Max tokens | 900 per call (free-tier OTPM limit is 1000; 100-token buffer) |
| Temperature | Default (Groq default ≈ 1.0) – suitable for creative meal planning |

### Capabilities Used
- **Instruction following:** Agent strictly follows system prompt scope and guardrails.
- **Reasoning:** Agent accounts for medical history when selecting foods.
- **Personalisation:** Profile context injected into every LLM call.
- **Multi-turn dialogue:** Conversation history maintains context across turns.

### Capabilities NOT Used (out of scope)
- Tool/function calling – not required for this use case.
- RAG / external knowledge retrieval – LLM knowledge is sufficient for general nutrition.
- Image understanding – text-only interface.

---

## Phase 5 – Prompt and Guardrail Design

### System Prompt Design Principles
1. **Role definition:** Agent is "NutriGuide", a friendly nutrition assistant.
2. **Scope restriction:** Explicit list of allowed topics (nutrition, diet, wellness).
3. **Guardrail rules (numbered):** Explicit prohibitions with fallback responses.
4. **Tone guidelines:** HAM (Helpful, Accountable, Mindful) — empathetic, plain language.
5. **Disclaimer instruction:** Agent is instructed to append the disclaimer verbatim.

### Guardrail Layers
| Layer | Mechanism |
|---|---|
| System prompt | LLM instructed to refuse out-of-scope and medical queries |
| Post-processing | Python code appends disclaimer if LLM omits it |
| UI | Captions and info boxes reinforce the agent's limitations |
| Profile validation | UI prevents submission without required fields |

### Disclaimer (enforced after every recommendation)
```
⚠️ Disclaimer: This is AI-generated guidance only and does not replace
professional medical or dietary advice. Please consult a qualified
nutritionist or doctor before making major dietary changes.
```

### Prompt Injection Mitigation
- System prompt is always prepended as the first message with `role: system`.
- Profile context is supplied by the application, not by user free-text.
- User free-text is limited to the chat input field.

---

## Phase 6 – Application Development

### Technology Stack
| Layer | Technology |
|---|---|
| UI | Streamlit ≥ 1.35 |
| LLM API | Groq Python SDK ≥ 0.9.0 |
| Language | Python 3.10+ |
| Dependency management | pip + requirements.txt |

### File Breakdown
| File | Lines (approx.) | Purpose |
|---|---|---|
| `app.py` | ~240 | Full Streamlit UI, session state, tabs, chat rendering |
| `agent/nutrition_agent.py` | ~130 | System prompt, plan generation, chat orchestration |
| `utils/groq_client.py` | ~42 | Groq SDK wrapper, error handling |
| `requirements.txt` | 3 | Runtime dependencies |
| `run.bat` | 21 | Windows one-click launcher |

### Key Implementation Decisions
- **`sys.path.insert`** in `app.py` enables `from agent.x import y` without a package install.
- **Session state** (`st.session_state`) persists profile, chat history, and plan across reruns.
- **`st.chat_message` + `st.chat_input`** provide a native Streamlit chat UI.
- **Tabs** separate the plan view from the chat to avoid UI clutter.
- **Token window trimming** (`llm_history[-20:]`) prevents exceeding free-tier OTPM limits.

---

## Phase 7 – Testing and Evaluation

### Test Scenarios
| Test ID | Scenario | Expected Result |
|---|---|---|
| T-01 | Missing API key | Error message; no LLM call made |
| T-02 | Missing profile fields | Sidebar validation error; form not submitted |
| T-03 | Valid vegetarian profile | Generates plant-based meal plan with disclaimer |
| T-04 | Valid diabetic profile | Plan avoids high-GI foods; mentions blood sugar |
| T-05 | Out-of-scope question ("What is 2+2?") | Polite refusal; redirects to nutrition topics |
| T-06 | Medical diagnosis request ("Do I have diabetes?") | Refuses; recommends doctor |
| T-07 | Plan regeneration | New plan generated; disclaimer present |
| T-08 | Chat multi-turn | Subsequent messages build on prior context |
| T-09 | Invalid API key | Groq error message displayed gracefully |
| T-10 | Disclaimer presence | Every plan/recommendation contains disclaimer text |

### Evaluation Metrics
- **Guardrail pass rate:** 100% of medical queries refused.
- **Disclaimer presence:** 100% of nutrition recommendations include disclaimer.
- **Relevance:** Plan addresses diet preference and medical conditions.
- **Tone:** Responses are empathetic and non-judgmental.

---

## Phase 8 – Deployment

### Local Deployment (Current)
```bash
pip install -r requirements.txt
streamlit run app.py
```
Access at: `http://localhost:8501`

### Windows One-Click
```
double-click run.bat
```

### Cloud Deployment Options
| Platform | Steps |
|---|---|
| Streamlit Community Cloud | Push to GitHub → connect repo → set no secrets (API key is user-provided) |
| Render / Railway | `Dockerfile` or `Procfile` with `streamlit run app.py --server.port $PORT` |
| Docker | `FROM python:3.11-slim` → `COPY . .` → `RUN pip install -r requirements.txt` → `CMD streamlit run app.py` |

### Security Notes
- API key is **not** stored in `.env`, environment variables, or any file.
- API key lives only in `st.session_state` for the duration of the browser session.
- No database, no logging of user data.

---

## Phase 9 – Documentation

### User Documentation
See **README.md** for:
- Feature overview
- Quick-start instructions (Windows + CLI)
- Usage walkthrough
- Guardrails and ethics summary

### Developer Documentation
- All functions and modules have **docstrings** explaining parameters and return values.
- Code follows **PEP 8** style conventions.
- Architecture diagram provided in Phase 3 of this document.

### Maintenance Guidelines
- **Model update:** Change `MODEL` constant in `utils/groq_client.py`.
- **Token limit change:** Change `MAX_TOKENS` constant in `utils/groq_client.py`.
- **New guardrail:** Add rule to `SYSTEM_PROMPT` in `agent/nutrition_agent.py`.
- **New profile field:** Add widget in `app.py` sidebar; add key to `build_profile_context()`.
- **Dependency updates:** Run `pip install --upgrade -r requirements.txt` periodically.

### Known Limitations
- LLM responses may occasionally contain inaccuracies; disclaimer mitigates risk.
- Free-tier Groq quota limits response length (max 900 tokens per call).
- No persistent user accounts; profile must be re-entered each session.
- English-primary; multilingual support depends on the underlying model.

---

*Document generated as part of the NutriGuide Agentic AI SDLC.*
