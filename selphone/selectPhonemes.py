import random
import sys
import numpy as np
import pandas as pd
import time
from collections import Counter

sys.path.append(".")
from probs.phoneProb import calcBaseProb

def adjustProb(phonemes: pd.DataFrame, sel_bin, laryngs, num_types):
    
    for phoneme in phonemes.index:
        if phonemes.at[phoneme, "Selected"]:
            continue

        curr_bin = phonemes.at[phoneme, "Binary"]
        curr_prob = phonemes.at[phoneme, "Probability"]

        # Place (make consonants in current place more likely, and makes consonants in nearby places less likely)
        sel_place = sel_bin % 32
        curr_place = curr_bin % 32

        sel_major_place = sel_bin % 8
        curr_major_place = curr_bin % 8

        if sel_place != curr_place:
            curr_prob -= 0.001

            if sel_major_place == curr_major_place:
                curr_prob -= 0.003

        # Laryngeal features
        sel_son = (sel_bin >> 8) % 2
        curr_son = (curr_bin >> 8) % 2

        curr_laryng = (curr_bin >> 5) % 8
        if len(laryngs) >= 2 and not (curr_son == 1 or curr_laryng == 8):

            if curr_laryng not in laryngs:
                curr_prob -= 0.06 * len(laryngs)
        
        # Manner
        sel_manner = (sel_bin >> 8) % 8
        curr_manner = (curr_bin >> 8) % 8

        if sel_manner != curr_manner:
            curr_prob -= 0.0007

            if sel_place == curr_place and sel_manner & 5 == 4 and curr_manner & 5 == 4: # Prevent occurrence of fricatives and sibilants of the same place
                curr_prob -= 2
                
        if sel_manner == 1 and curr_manner == 1: # Nasal
            curr_prob -= 0.1 * (num_types["nasals"] - 1)

        # Suprs/Coarts
        sel_suprs = (sel_bin >> 11) % 32
        curr_suprs = (curr_bin >> 11) % 32

        if sel_suprs != curr_suprs:
            curr_prob -= 0.1

        # Sonorance (If previous consonant was an obstruent, favor sonorants and vice versa)

        if sel_son == curr_son:
            if sel_son == 0: # Last consonant picked was an obstruent
                curr_prob -= 0.001

            else: # Last consonant picked was an sonorant
                curr_prob -= 0.01

        phonemes.at[phoneme, "Probability"] = curr_prob
        
    phonemes.sort_values(by="Probability", ascending=False)
    return


""" 
Takes in the probabilities for every phoneme and returns a list of length
num_phones. When selecting each phoneme, the most probable one is considered,
and then, based on temp, phonemes up to a certain lower probability are also
considered. Next, one of these phonemes are randomly selected, and every 
other phoneme's probability is adjusted based on the selection.
"""
def selectPhonemes(phonemes: pd.DataFrame, num_phones, temp):
    selected_phones = []
    laryngs = set()
    num_types = Counter()

    for _ in range(num_phones):

        # Choose phonemes to select from
        unsel_phonemes = phonemes[phonemes["Selected"] == False]
        min_prob = unsel_phonemes.head(1).at[unsel_phonemes.index[0], "Probability"] - (12 * temp)

        sel_phone_frame = phonemes[(phonemes["Probability"] > min_prob) & (phonemes["Selected"] == False)]

        # print(min_prob)
        # print(phonemes)
        # print(sel_phone_frame)
        # print()

        # Randomly select phoneme from sel_phone_list
        pick = sel_phone_frame.sample()
        picked_phoneme = pick.index[0]
        
        selected_phones += [picked_phoneme]
        phonemes.at[picked_phoneme, "Selected"] = True

        # Adjust probabilities based on selected phoneme
        sel_bin = pick.at[picked_phoneme, "Binary"]

        if (sel_bin >> 8) % 2 == 0:
            laryngs.add((sel_bin >> 5) % 8)

        if (sel_bin >> 8) % 8 == 1:
            num_types["nasals"] += 1

        adjustProb(phonemes, sel_bin, laryngs, num_types)
        
    return selected_phones


if __name__ == "__main__":
    num = int(sys.argv[1])
    temp = float(sys.argv[2])

    probs = calcBaseProb(True)
    sel_phones = selectPhonemes(probs, num, temp)
    for i in range(len(sel_phones)):
        print(f"{i+1}. {sel_phones[i]}")