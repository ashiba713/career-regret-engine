import random

def simulate_career(career_params, student, runs=200):
    outcomes = []

    for _ in range(runs):
        success = random.uniform(0.4, 0.9)

        interest_match = student["interest"] / 10
        skill_match = student["skill"] / 10

        stress = random.uniform(0, career_params["burnout"])
        risk_penalty = career_params["risk"] / 10

        outcome_score = (
            success * 10 +
            interest_match * 5 +
            skill_match * 5 -
            stress -
            risk_penalty * 5
        )

        outcomes.append(outcome_score)

    return outcomes
