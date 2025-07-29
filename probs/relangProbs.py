import json
from collections import Counter

# Calculates average occurrences of types of a given feature in a sound inventory
def averager(phonology: list[int], feature: int, averages: dict[int, int]) -> dict[int, float]:
    feature_cats = Counter()
    for phoneme in phonology:
        feature_cats[phoneme & feature] += 1

    for cat in feature_cats:
        if cat in averages:
            averages[cat] += feature_cats[cat] / feature_cats.total()
        
        else:
            averages[cat] = feature_cats[cat] / feature_cats.total()

    return averages


# Takes in the base probability and average found for a given category
# of a feature and outputs a modded prob. 
def probModder(baseProb: int, avg: int) -> int:
    return (2 * baseProb) - avg

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
        for cat in probs[features[i]]:
            if cat[0] in averages[i]:
                avg = averages[i][cat[0]] / len(phonologies)
                if cat[0] == 10:
                    print(avg, cat[1])
                cat[1] = probModder(cat[1], avg)

        print(probs[features[i]])

    return probs