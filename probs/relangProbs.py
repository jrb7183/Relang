import json
from collections import Counter

"""Placeholder for now, just loading in the base probs"""
def relangProbs(phonologies: list[list[int]]) -> dict[str, dict[str, list[list[int, float]]]]:

    # Calculate average percentages that places, manners, laryngeal features, etc. occur.
    counters = {
        "places": Counter(),
        "manners": Counter(),
        "laryngs": Counter(),
        "lats": Counter(),
        "nasals": Counter(),
        "suprs": Counter()
    }

    averages = {}

    for phonology in phonologies:
        for phoneme in phonology:
            counters["places"][phoneme & 31] += 1
            counters["manners"][phoneme & (7 << 8)] += 1
            counters["laryngs"][phoneme & (7 << 5)] += 1
            counters["lats"][phoneme & (1 << 12)] += 1
            counters["nasals"][phoneme & (1 << 11)] += 1
            counters["suprs"][phoneme & (7 << 13)] += 1

        for counter in counters:
            for cat in counters[counter]:
                
                if cat in averages:
                    averages[f"{counter} {cat}"] += counters[counter][cat] / counters[counter].total()
                else:
                    averages[f"{counter} {cat}"] = counters[counter][cat] / counters[counter].total()

    for cat in averages:
        averages[cat] = averages[cat] / len(phonologies)

    print(averages)

        


    # with open("../data/baseProbs.json", "r", encoding="utf-8") as f:
    #     prob_dict = json.load(f)

    # return prob_dict