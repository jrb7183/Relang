import random
from collections import Counter

# Selects the place, manner, or laryngeal features for a phoneme.
def selectFeature(feat: int, probs: dict[str, list[list]], guarantees: dict[str, Counter], sp_len: int, num_phonemes: int, loop_count: int, curr_permit) -> int:
    pfs = ["Place", "Manner", "Laryngeals"]
    gfs = ["places", "manners", "laryngeals"]

    features = probs[pfs[feat]] + []

    features = list(filter(lambda cat: cat[0] in curr_permit, features))
    if len(features) == 0:
        return -1
    
    if guarantees[gfs[feat]].total() + sp_len == num_phonemes:
        temp = list(filter(lambda cat: guarantees[gfs[feat]][cat[0]] > 0, features))
        if len(temp) > 0:
            features = temp

    features.sort(reverse=True, key=lambda cat: cat[1])

    sel_feature = features[0][0]
    if len(features) > 1:
        sel_feature = random.choice(features[:2])[0]

    # Lower selected prob and increase others
    prob_adjust = 0.005
    if feat == 2:
        prob_adjust = 0.05

    for feature in probs[pfs[feat]]:
        if feature[0] == sel_feature:
            feature[1] -= prob_adjust

        # Ignore places in same major place
        elif feat or feature[0] % 8 != sel_feature % 8:
            feature[1] += prob_adjust

        # If loop count is too high, the top two features might be in a positive feedback loop
        if loop_count > 100 and feature in features[:2]:
            feature[1] = 0

    # Set place guarantees
    if guarantees[gfs[feat]][sel_feature] > 0:
        guarantees[gfs[feat]][sel_feature] -= 1

    else:
        if feat or sel_feature != 0: # Not glottal
            guarantees[gfs[feat]][sel_feature] = min(2, num_phonemes - sp_len - guarantees[gfs[feat]].total() - 1)

    return sel_feature