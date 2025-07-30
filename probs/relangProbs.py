import json
from collections import Counter

# Calculates average occurrences of types of a given feature in a sound inventory
def averager(phonology: list[int], feature: int, averages: dict[int, int]) -> dict[int, float]:
    feature_cats = Counter()
    
    for phoneme in phonology:
        if feature != (7 << 13) or phoneme & (1 << 13) != 0:
            feature_cats[phoneme & feature] += 1
        
        else:
            feature_cats[0] += 1
            

    for cat in feature_cats:
        if cat in averages:
            averages[cat] += feature_cats[cat] / feature_cats.total()
        
        else:
            averages[cat] = feature_cats[cat] / feature_cats.total()

    return averages


# Takes in the base probability and average found for a given category
# of a feature and outputs a modded prob. 
def probModder(base_probs: list[list[int, float]], avgs: dict[int, float], len_phono: int) -> list[list[int, float]]:
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

"""
This part of the Relang pipeline takes in all of the user-inputted phonologies and finds the
average percent occurrences of different types of features within them (i.e. different places,
manners, laryngeal features). These averages ideally shine light into the user's habits when
constructing proto-phonologies. Subsequently, the function uses these averages to modify the
base probs to steer away from those tendencies. 
"""
def relangProbs(phonologies: list[list[int]]) -> dict[str, dict[str, list[list[int, float]]]]:

    # Calculate average percentages that places, manners, laryngeal features, etc. occur.
    # [place, laryngeals, manners, nasality, laterality, suprasegmentals]
    averages = [{}, {}, {}, {}, {}, {}]
    bins = [31, (7 << 5), (7 << 8), (1 << 11), (1 << 12), (7 << 13)]

    for phonology in phonologies:
        for i in range(len(averages)):
            averages[i] = averager(phonology, bins[i], averages[i])

    # Calculate modified probs for Phoneme Selector
    with open("../data/baseProbs.json", "r", encoding="utf-8") as f:
        probs = json.load(f)
    probs = probs["Consonants"]

    features = ["Place", "Laryngeals", "Manner", "Nasality", "Laterality", "Suprasegmentals"]
    for i in range(len(features)):
        probModder(probs[features[i]], averages[i], len(phonologies))

    return probs