"""
NutriGuide – Personalised Nutrition Agentic AI
Streamlit UI entry point
"""

import streamlit as st
import sys
import os

# Make sibling packages importable when running `streamlit run app.py`
# from inside nutrition_agent/
sys.path.insert(0, os.path.dirname(__file__))

from agent.nutrition_agent import generate_nutrition_plan, chat_with_agent

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="NutriGuide – AI Nutrition Assistant",
    page_icon="🥗",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session-state initialisation
# ---------------------------------------------------------------------------
if "profile_saved" not in st.session_state:
    st.session_state.profile_saved = False
if "chat_history" not in st.session_state:       # list[dict] for display
    st.session_state.chat_history = []
if "llm_history" not in st.session_state:        # list[dict] for LLM
    st.session_state.llm_history = []
if "nutrition_plan" not in st.session_state:
    st.session_state.nutrition_plan = None
if "profile" not in st.session_state:
    st.session_state.profile = {}

# ---------------------------------------------------------------------------
# Sidebar – API key + user profile form
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings & Profile")
    st.markdown("---")

    # --- API key (never stored beyond this session variable) ---
    st.subheader("🔑 Groq API Key")
    api_key = st.text_input(
        "Enter your Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Your key is used only for this session and is never stored or logged.",
    )
    st.caption("🔒 Your API key is not saved or logged.")

    st.markdown("---")

    # --- User profile ---
    st.subheader("👤 Your Profile")

    name = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
    age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
    diet = st.selectbox(
        "Diet Preference",
        options=["Vegetarian", "Non-Vegetarian", "Vegan"],
    )
    medical_history = st.multiselect(
        "Medical History (select all that apply)",
        options=[
            "None",
            "Type 2 Diabetes",
            "High Blood Pressure",
            "High Cholesterol",
            "Thyroid Disorder",
            "Obesity",
            "Heart Disease",
            "Kidney Disease",
            "Gluten Intolerance / Celiac",
            "Lactose Intolerance",
        ],
        default=["None"],
    )
    city = st.text_input("City", placeholder="e.g. Mumbai")
    country = st.text_input("Country", placeholder="e.g. India")

    st.markdown("---")
    save_btn = st.button("💾 Save Profile & Generate Plan", use_container_width=True)

    if save_btn:
        if not api_key.strip():
            st.error("Please enter your Groq API key first.")
        elif not name.strip():
            st.error("Please enter your name.")
        elif not city.strip() or not country.strip():
            st.error("Please enter your city and country.")
        else:
            profile = {
                "name": name.strip(),
                "age": int(age),
                "diet": diet,
                "medical_history": ", ".join(medical_history),
                "location": f"{city.strip()}, {country.strip()}",
            }
            st.session_state.profile = profile
            st.session_state.chat_history = []
            st.session_state.llm_history = []

            with st.spinner("🤖 Generating your personalised nutrition plan…"):
                plan = generate_nutrition_plan(api_key, profile)

            st.session_state.nutrition_plan = plan
            st.session_state.profile_saved = True
            st.success("✅ Profile saved and plan generated!")

    # --- Reset ---
    if st.session_state.profile_saved:
        st.markdown("---")
        if st.button("🔄 Reset Everything", use_container_width=True):
            for key in ["profile_saved", "chat_history", "llm_history",
                        "nutrition_plan", "profile"]:
                del st.session_state[key]
            st.rerun()

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.title("🥗 NutriGuide – Personalised Nutrition AI Agent")
st.caption(
    "Powered by Groq · Model: qwen/qwen3.8-27b · "
    "Agentic AI for personalised daily nutrition planning"
)
st.markdown("---")

if not st.session_state.profile_saved:
    # Welcome / onboarding screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            ### 👋 Welcome to NutriGuide!

            NutriGuide is an **Agentic AI nutrition assistant** that:

            - 🥦 Builds a **personalised daily nutrition plan** tailored to you
            - 💬 Answers your **nutrition and diet questions** in a live chat
            - 🏥 Respects your **medical history** and dietary preferences
            - 🌍 Considers **local food availability** based on your location

            #### How to get started
            1. Enter your **Groq API key** in the sidebar *(free at console.groq.com)*
            2. Fill in your **profile details**
            3. Click **Save Profile & Generate Plan**
            4. Chat with NutriGuide using the chat box below your plan!

            ---
            > ⚠️ **Medical Disclaimer:** NutriGuide provides general nutrition
            > guidance only. It is **not a substitute** for professional medical
            > or dietary advice. Always consult a qualified nutritionist or doctor
            > before making significant changes to your diet, especially if you
            > have a medical condition.
            """
        )
else:
    profile = st.session_state.profile

    # --- Profile summary badge ---
    with st.expander("📋 Your Profile Summary", expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.metric("Name", profile.get("name", "—"))
        c1.metric("Age", profile.get("age", "—"))
        c2.metric("Diet", profile.get("diet", "—"))
        c2.metric("Location", profile.get("location", "—"))
        c3.metric("Medical History", profile.get("medical_history", "None"))

    st.markdown("---")

    # --- Tabs: Nutrition Plan | Chat ---
    tab_plan, tab_chat = st.tabs(["📊 My Nutrition Plan", "💬 Ask NutriGuide"])

    # ── Tab 1: Nutrition Plan ──────────────────────────────────────────────
    with tab_plan:
        st.subheader(f"🌟 Personalised Daily Nutrition Plan for {profile['name']}")
        if st.session_state.nutrition_plan:
            st.markdown(st.session_state.nutrition_plan)
        else:
            st.info("No plan generated yet. Save your profile in the sidebar.")

        st.markdown("---")
        if st.button("🔁 Regenerate Nutrition Plan", key="regen_btn"):
            with st.spinner("🤖 Regenerating your plan…"):
                plan = generate_nutrition_plan(api_key, profile)
            st.session_state.nutrition_plan = plan
            st.rerun()

    # ── Tab 2: Chat ────────────────────────────────────────────────────────
    with tab_chat:
        st.subheader("💬 Chat with NutriGuide")
        st.caption(
            "Ask any nutrition or diet question. "
            "NutriGuide will not provide medical diagnoses or prescriptions."
        )

        # Display chat history
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.info(
                    "👋 Hi! I'm NutriGuide. Ask me anything about nutrition, "
                    "healthy eating, or your meal plan!"
                )
            else:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        with st.chat_message("user"):
                            st.markdown(msg["content"])
                    else:
                        with st.chat_message("assistant", avatar="🥗"):
                            st.markdown(msg["content"])

        # Chat input
        user_input = st.chat_input("Type your nutrition question here…")
        if user_input:
            if not api_key.strip():
                st.error("Please enter your Groq API key in the sidebar to chat.")
            else:
                # Add user message to display history
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input}
                )

                # Get agent response
                with st.spinner("NutriGuide is thinking…"):
                    reply = chat_with_agent(
                        api_key=api_key,
                        profile=profile,
                        conversation_history=st.session_state.llm_history,
                        user_message=user_input,
                    )

                # Update LLM history (trimmed to last 10 exchanges to save tokens)
                st.session_state.llm_history.append(
                    {"role": "user", "content": user_input}
                )
                st.session_state.llm_history.append(
                    {"role": "assistant", "content": reply}
                )
                if len(st.session_state.llm_history) > 20:
                    st.session_state.llm_history = st.session_state.llm_history[-20:]

                # Add assistant reply to display history
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": reply}
                )

                st.rerun()

        # Clear chat button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.session_state.llm_history = []
                st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "🔒 Privacy: Your API key is used only in-session and never stored or logged.  "
    "⚠️ NutriGuide is for informational purposes only — not a substitute for "
    "professional medical or dietary advice."
)
