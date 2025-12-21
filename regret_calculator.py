def calculate_regret(outcomes):
    best_outcome = max(outcomes)

    regrets = [best_outcome - o for o in outcomes]

    return {
        "worst_regret": max(regrets),
        "average_regret": sum(regrets) / len(regrets),
        "expected_outcome": sum(outcomes) / len(outcomes)
    }
