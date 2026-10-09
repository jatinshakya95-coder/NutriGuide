"""
Groq API client wrapper.
The API key is accepted at call-time and is NEVER stored or logged.
"""

from groq import Groq

# llama-3.3-70b-versatile — reliable Groq free-tier model
MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 900                  # free-tier OTPM limit is 1000


def call_llm(
    api_key: str,
    messages: list[dict],
    max_tokens: int = MAX_TOKENS,
) -> str:
    """
    Send *messages* to the Groq LLM and return the assistant reply as a string.

    Parameters
    ----------
    api_key   : Groq API key supplied by the user at runtime (not stored).
    messages  : OpenAI-compatible list of {"role": ..., "content": ...} dicts.
    max_tokens: Upper bound for the response (default 900 for free-tier safety).

    Returns
    -------
    str : The assistant's reply text, or an error message string.
    """
    if not api_key or not api_key.strip():
        return "⚠️ No API key provided. Please enter your Groq API key in the sidebar."

    try:
        client = Groq(api_key=api_key.strip())
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    except Exception as exc:  # surface Groq errors gracefully
        return f"⚠️ Groq API error: {exc}"
