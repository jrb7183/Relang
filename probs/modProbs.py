# Takes in the base probability and average found for a given category
# of a feature and outputs a modded prob. 
def prob_modder(base_probs: list[list[int, float]], avgs: dict[int, float], len_phono: int) -> list[list[int, float]]:
    unmodded = []
    total_diff = 0

    # Modify probabilities of feature categories found in the given phonologies
    for base_prob in base_probs:
        if base_prob[0] in avgs:
            
            avg = avgs[base_prob[0]] / len_phono
            mod = base_prob[1] - avg

            base_prob[1] += mod
            total_diff += mod

        else:
            unmodded += [base_prob[0]]

    # If modding the averages caused them to not add up to 1, distribute the discrepancy
    # across unmodded probs if possible, but all the probs otherwise.
    if abs(total_diff) > 0.0001:
        if unmodded:
            
            mod = total_diff * -1 / len(unmodded)
            for base_prob in base_probs:

                if base_prob[0] in unmodded:
                    base_prob[1] += mod

        else:
            mod = total_diff * -1 / len(base_probs)
            for base_prob in base_probs:
                base_prob[1] += mod


    return base_probs