import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Career Decision Engine", layout="wide", page_icon="🎯")
st.title("🎯 Regret-Minimization Career Decision Engine")

try:
    from career_data import CAREERS
    from input_handler import get_student_profile
    from simulator import simulate_career
    from regret_calculator import calculate_regret
    from recommender import recommend

    st.success("✅ Modules loaded successfully")

    # Animated intro
    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        .fade-in {
            animation: fadeIn 2s ease-in;
        }
        </style>
        <h3 class="fade-in">Answer honestly — your future self will thank you!</h3>
        """,
        unsafe_allow_html=True,
    )

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

        df = pd.DataFrame(results).sort_values("worst_regret")
        best = df.iloc[0]

        st.subheader("📊 Career Comparison")

        # Interactive animated bar chart
        fig = px.bar(
            df,
            x="worst_regret",
            y="career",
            orientation="h",
            color="worst_regret",
            color_continuous_scale="turbo",
            animation_frame=None,
            title="Worst-Case Regret by Career",
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Highlight recommendation with animation
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; background:linear-gradient(90deg,#00c6ff,#0072ff); color:white; animation: fadeIn 2s ease-in;">
                🏆 <b>Recommended Career:</b> {best['career']}<br>
                ✨ Minimum Worst-Case Regret: {best['worst_regret']}
            </div>
            """,
            unsafe_allow_html=True,
        )

except Exception as e:
    st.error("❌ App crashed")
    st.exception(e)
