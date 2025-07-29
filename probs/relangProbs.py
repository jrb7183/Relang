import json
from collections import Counter

# Calculates average occurrences of types of a given feature in a sound inventory
def averager(phonology: list[int], feature: int):
    feature_cats = Counter()
    for phoneme in phonology:
        feature_cats[phoneme & feature] += 1

    averages = {}
    for cat in feature_cats:
        averages[cat] = feature_cats[cat] / feature_cats.total()

    return averages

"""
This part of the Relang pipeline takes in all of the user-inputted phonologies and finds the
average percent occurrences of different types of features within them (i.e. different places,
manners, laryngeal features). These averages ideally shine light into the user's habits when
constructing proto-phonologies. Subsequently, the function uses these averages to modify the
base probs to steer away from those tendencies. 
"""
def relangProbs(phonologies: list[list[int]]) -> dict[str, dict[str, list[list[int, float]]]]:

    # Calculate average percentages that places, manners, laryngeal features, etc. occur.
    # [place, laryngeals, manners, nasalization, lateralization, suprasegmentals]
    averages = [{}, {}, {}, {}, {}, {}]
    bins = [31, (7 << 5), (7 << 8), (1 << 11), (1 << 12), (7 << 13)]

    for phonology in phonologies:
        for i in range(len(averages)):
            averages[i] = averager(phonology, bins[i])

    for feature in averages:
        feature = {bin: avg / len(phonologies) for (bin, avg) in feature.items()}

        print(feature)

        


    # with open("../data/baseProbs.json", "r", encoding="utf-8") as f:
    #     prob_dict = json.load(f)

    # return prob_dict