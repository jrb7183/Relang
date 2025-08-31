import json
import sys

sys.path.append("..")
from probs.calcAverage import averager, normalizer
from probs.modProbs import prob_modder

"""
This part of the Relang pipeline takes in all of the user-inputted phonologies and finds the
average percent occurrences of different types of features within them (i.e. different places,
manners, laryngeal features). These averages ideally shine light into the user's habits when
constructing proto-phonologies. Subsequently, the function uses these averages to modify the
base probs to steer away from those tendencies. 
"""
def relang_probs(phonologies: list[list[int]]) -> dict[str, list[list[int, float]]]:

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
        averages[i] = normalizer(averages[i], probs[features[i]])
        probs[features[i]] = prob_modder(probs[features[i]], averages[i], len(phonologies))

    return probs