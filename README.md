# NutriGuide – Personalised Nutrition Agentic AI

## Overview

NutriGuide is a **Python + Streamlit** application that demonstrates **Agentic AI** behaviour using the **Groq API** with model `qwen/qwen3-32b`. The AI agent understands your personal profile, reasons about your dietary needs and medical history, and generates a tailored daily nutrition plan. You can also chat with it to ask any diet or nutrition question.

---

## Features

| Feature | Details |
|---|---|
| 🤖 Agentic AI | Agent reasons over user profile, applies guardrails, generates plans |
| 🥗 Personalised Plans | Daily calorie targets, macros, sample meals, foods to prefer/avoid |
| 💬 Chat Interface | Multi-turn conversation with full chat history |
| 🔒 Privacy-first | API key is session-only; never stored or logged |
| 🏥 Medical Guardrails | No diagnosis, no prescriptions; always recommends a doctor |
| ⚠️ Disclaimer | Appended automatically to every nutrition recommendation |

---

## Project Structure

```
nutrition_agent/
├── app.py                    ← Streamlit UI (sidebar: API key + user profile)
├── agent/
│   └── nutrition_agent.py   ← Agent logic, system prompt, guardrails
├── utils/
│   └── groq_client.py       ← Groq client wrapper, call_llm()
├── SDLC.md                  ← Full Agentic AI SDLC plan (all 9 phases)
├── requirements.txt          ← Python dependencies
├── run.bat                  ← Windows: install deps + run app
└── README.md                ← This file
```

---

## Quick Start

### Prerequisites
- Python 3.10 or later
- A **free Groq API key** → [console.groq.com](https://console.groq.com)

### Option A – Windows (one-click)
```
double-click run.bat
```

### Option B – Manual
```bash
cd nutrition_agent
pip install -r requirements.txt
streamlit run app.py
```

Open your browser at **http://localhost:8501**.

---

## Usage

1. **Enter your Groq API key** in the sidebar (never stored or logged).
2. **Fill in your profile**: name, age, diet preference, medical history, location.
3. Click **Save Profile & Generate Plan** – the agent generates your nutrition plan.
4. Switch to the **💬 Ask NutriGuide** tab to chat about any nutrition topic.
5. Use **Regenerate** to refresh your plan anytime.

---

## Guardrails & Ethics

- The system prompt strictly limits the agent to **nutrition and diet topics only**.
- The agent will **refuse** to diagnose diseases or prescribe medication.
- Every nutrition plan includes a mandatory **medical disclaimer**.
- Users are always recommended to **consult a Registered Dietitian or doctor** for serious conditions.
- The agent follows **HAM (Helpful, Accountable, Mindful) AI ethics principles**.

---

## Technical Details

| Item | Value |
|---|---|
| LLM Provider | Groq |
| Model | `qwen/qwen3-32b` |
| Max tokens per call | 900 (free-tier OTPM safe) |
| UI Framework | Streamlit |
| Language | Python 3.10+ |

---

## Disclaimer

> ⚠️ NutriGuide provides **general nutrition information only**. It is **not a substitute** for professional medical or dietary advice. Always consult a qualified nutritionist or licensed physician before making significant changes to your diet.
