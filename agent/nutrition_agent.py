"""
Nutrition agent – system prompt, guardrails, and conversation helpers.
"""

from __future__ import annotations

from utils.groq_client import call_llm

# ---------------------------------------------------------------------------
# Medical disclaimer – appended after every nutrition recommendation.
# ---------------------------------------------------------------------------
DISCLAIMER = (
    "\n\n⚠️ **Disclaimer:** This is AI-generated guidance only and does not "
    "replace professional medical or dietary advice. Please consult a qualified "
    "nutritionist or doctor before making major dietary changes."
)

# ---------------------------------------------------------------------------
# System prompt – kept SHORT to minimise input tokens and maximise speed.
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are NutriGuide, a concise, empathetic AI nutrition assistant. "
    "Only answer nutrition and diet questions. "
    "Never diagnose diseases or prescribe medication. "
    "If asked non-nutrition questions say: 'I only assist with nutrition topics.' "
    "For serious conditions always recommend consulting a Registered Dietitian or doctor. "
    "After every nutrition plan or recommendation add: "
    "'⚠️ Disclaimer: This is AI-generated guidance only and does not replace "
    "professional medical or dietary advice. Please consult a qualified "
    "nutritionist or doctor before making major dietary changes.'"
)


def build_profile_context(profile: dict) -> str:
    """Return a compact one-liner profile string for the LLM prompt."""
    return (
        f"Name:{profile.get('name','?')} | Age:{profile.get('age','?')} | "
        f"Diet:{profile.get('diet','?')} | Medical:{profile.get('medical_history','None')} | "
        f"Location:{profile.get('location','?')}"
    )


def generate_nutrition_plan(api_key: str, profile: dict) -> str:
    """Generate a personalised daily nutrition plan for the user profile."""
    profile_ctx = build_profile_context(profile)
    user_message = (
        f"Profile: {profile_ctx}\n\n"
        "Give me a personalised DAILY NUTRITION PLAN. Include:\n"
        "1. Daily calorie range\n"
        "2. Macro split (carbs/protein/fats)\n"
        "3. Sample meals (Breakfast, Snack, Lunch, Snack, Dinner)\n"
        "4. Key nutrients for my medical history\n"
        "5. Foods to prefer and avoid\n"
        "6. Hydration tip\n"
        "Use locally available foods for my location. Be concise."
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    reply = call_llm(api_key, messages)
    if "disclaimer" not in reply.lower():
        reply += DISCLAIMER
    return reply


def chat_with_agent(
    api_key: str,
    profile: dict,
    conversation_history: list[dict],
    user_message: str,
) -> str:
    """Continue a multi-turn nutrition chat, injecting the user profile."""
    profile_ctx = build_profile_context(profile)
    system_with_profile = SYSTEM_PROMPT + f"\nUser profile: {profile_ctx}"

    messages = [{"role": "system", "content": system_with_profile}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    reply = call_llm(api_key, messages)

    recommendation_keywords = (
        "meal", "diet", "eat", "food", "calorie", "nutrient",
        "breakfast", "lunch", "dinner", "snack", "protein", "carb",
        "fat", "vitamin", "mineral", "hydrat", "plan", "recommend",
    )
    lower_reply = reply.lower()
    if any(kw in lower_reply for kw in recommendation_keywords):
        if "disclaimer" not in lower_reply:
            reply += DISCLAIMER
    return reply
