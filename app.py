import streamlit as st
import pandas as pd

st.set_page_config(page_title="Career Decision Engine", layout="wide")
st.title("🎯 Regret-Minimization Career Decision Engine")

try:
    from career_data import CAREERS
    from input_handler import get_student_profile
    from simulator import simulate_career
    from regret_calculator import calculate_regret
    from recommender import recommend

    st.success("✅ Modules loaded successfully")

    # Layout sliders in two columns
    col1, col2 = st.columns(2)

    with col1:
        interest = st.slider("📘 Interest in technical work", 0, 10, 5)
        skill = st.slider("🛠️ Skill readiness", 0, 10, 5)
        risk = st.selectbox("⚖️ Risk tolerance", ["Low", "Medium", "High"])

    with col2:
        finance = st.selectbox("💰 Financial pressure", ["Low", "Medium", "High"])
        grind = st.selectbox("🔥 Willingness to grind", ["Low", "Medium", "High"])
        stability = st.selectbox("🏡 Need for long-term stability", ["Low", "Medium", "High"])

    if st.button("🚀 Simulate Career Futures"):
        student = get_student_profile(interest, skill, risk, finance, grind, stability)

        results = []
        for career, params in CAREERS.items():
            outcomes = simulate_career(params, student)
            regret_data = calculate_regret(outcomes)
            results.append({"career": career, **regret_data})

        # Convert to DataFrame for better visuals
        df = pd.DataFrame(results).sort_values("worst_regret")

        best = df.iloc[0]

        st.subheader("📊 Career Comparison")
        st.dataframe(df, use_container_width=True)

        # Add a bar chart for regret scores
        st.bar_chart(df.set_index("career")["worst_regret"])

        # Highlight recommendation
        st.success(
            f"🏆 Recommended Career: **{best['career']}** "
            f"(Minimum Worst-Case Regret: {best['worst_regret']})"
        )

except Exception as e:
    st.error("❌ App crashed")
    st.exception(e)
