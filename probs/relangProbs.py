import json

"""Placeholder for now, just loading in the base probs"""
def relangProbs():
    with open("../data/baseProbs.json", "r", encoding="utf-8") as f:
        prob_dict = json.load(f)

    return prob_dict