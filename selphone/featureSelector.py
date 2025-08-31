import random

# Selects the place, manner, or laryngeal features for a phoneme.
def select_feature(feat: int, probs: dict[str, list[list]], loop_count: int, curr_permit) -> int:
    pfs = ["Place", "Manner", "Laryngeals"]

    features = probs[pfs[feat]] + []

    features = list(filter(lambda cat: cat[0] in curr_permit, features))
    if len(features) == 0:
        return -1

    features.sort(reverse=True, key=lambda cat: cat[1])

    sel_feature = features[0][0]
    if len(features) > 1:
        sel_feature = random.choice(features[:3])[0]

    # Lower selected prob and increase others
    prob_adjust = [0.001, 0.005, 0.05][feat]

    for feature in probs[pfs[feat]]:
        if feature[0] == sel_feature:
            feature[1] -= prob_adjust

        # Ignore places in same major place
        elif feat or feature[0] % 8 != sel_feature % 8:
            feature[1] += prob_adjust

        # If loop count is too high, the top two features might be in a positive feedback loop
        if loop_count > 100 and feature in features[:2]:
            feature[1] = 0

    return sel_feature