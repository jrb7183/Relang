import random
import sys
import numpy as np
import pandas as pd
import time
from collections import Counter

sys.path.append(".")
from probs.relangProbs import relangProbs
from utils.phonemeLoader import loadPhonemes

# def adjustProb(phonemes: pd.DataFrame, sel_bin, laryngs, num_types):
    
#     for phoneme in phonemes.index:
#         if phonemes.at[phoneme, "Selected"]:
#             continue

#         curr_bin = phonemes.at[phoneme, "Binary"]
#         curr_prob = phonemes.at[phoneme, "Probability"]

#         # Place (make consonants in current place more likely, and makes consonants in nearby places less likely)
#         sel_place = sel_bin % 32
#         curr_place = curr_bin % 32

#         sel_major_place = sel_bin % 8
#         curr_major_place = curr_bin % 8

#         if sel_place != curr_place:
#             curr_prob -= 0.001

#             if sel_major_place == curr_major_place:
#                 curr_prob -= 0.003

#         # Laryngeal features
#         sel_son = (sel_bin >> 8) % 2
#         curr_son = (curr_bin >> 8) % 2

#         curr_laryng = (curr_bin >> 5) % 8
#         if len(laryngs) >= 2 and not (curr_son == 1 or curr_laryng == 8):

#             if curr_laryng not in laryngs:
#                 curr_prob -= 0.06 * len(laryngs)
        
#         # Manner
#         sel_manner = (sel_bin >> 8) % 8
#         curr_manner = (curr_bin >> 8) % 8

#         if sel_manner != curr_manner:
#             curr_prob -= 0.0007

#             if sel_place == curr_place and sel_manner & 5 == 4 and curr_manner & 5 == 4: # Prevent occurrence of fricatives and sibilants of the same place
#                 curr_prob -= 2
                
#         if sel_manner == 1 and curr_manner == 1: # Nasal
#             curr_prob -= 0.1 * (num_types["nasals"] - 1)

#         # Suprs/Coarts
#         sel_suprs = (sel_bin >> 11) % 32
#         curr_suprs = (curr_bin >> 11) % 32

#         if sel_suprs != curr_suprs:
#             curr_prob -= 0.1

#         # Sonorance (If previous consonant was an obstruent, favor sonorants and vice versa)

#         if sel_son == curr_son:
#             if sel_son == 0: # Last consonant picked was an obstruent
#                 curr_prob -= 0.001

#             else: # Last consonant picked was an sonorant
#                 curr_prob -= 0.01

#         phonemes.at[phoneme, "Probability"] = curr_prob
        
#     phonemes.sort_values(by="Probability", ascending=False)
#     return


# """ 
# Takes in the probabilities for every phoneme and returns a list of length
# num_phones. When selecting each phoneme, the most probable one is considered,
# and then, based on temp, phonemes up to a certain lower probability are also
# considered. Next, one of these phonemes are randomly selected, and every 
# other phoneme's probability is adjusted based on the selection.
# """
# def selectPhonemes(phonemes: pd.DataFrame, num_phones, temp):
#     selected_phones = []
#     laryngs = set()
#     num_types = Counter()

#     for _ in range(num_phones):

#         # Choose phonemes to select from
#         unsel_phonemes = phonemes[phonemes["Selected"] == False]
#         min_prob = unsel_phonemes.head(1).at[unsel_phonemes.index[0], "Probability"] - (12 * temp)

#         sel_phone_frame = phonemes[(phonemes["Probability"] > min_prob) & (phonemes["Selected"] == False)]

#         # print(min_prob)
#         # print(phonemes)
#         # print(sel_phone_frame)
#         # print()

#         # Randomly select phoneme from sel_phone_list
#         pick = sel_phone_frame.sample()
#         picked_phoneme = pick.index[0]
        
#         selected_phones += [picked_phoneme]
#         phonemes.at[picked_phoneme, "Selected"] = True

#         # Adjust probabilities based on selected phoneme
#         sel_bin = pick.at[picked_phoneme, "Binary"]

#         if (sel_bin >> 8) % 2 == 0:
#             laryngs.add((sel_bin >> 5) % 8)

#         if (sel_bin >> 8) % 8 == 1:
#             num_types["nasals"] += 1

#         adjustProb(phonemes, sel_bin, laryngs, num_types)
        
#     return selected_phones


def selectConsonants(consonants: pd.DataFrame, probs, num_phonemes):
    sel_phonemes = []
    
    while len(sel_phonemes) < num_phonemes:
        phoneme_bin = 0

        # Place of Articulation
        places = probs["Place"]
        sel_num = random.random()
        sel = False

        while sel >= 0:
            if sel_num < places[sel][1]:
                phoneme_bin += places[sel][0]
                sel = -1

            else:
                sel_num -= places[sel][1]
                sel += 1

        # Manner of Articulation
        manners = probs["Manner"] + []

        # If the POA is palatal or velar, remove chance for taps and trills
        if phoneme_bin == 19 or phoneme_bin == 9:
            manners.pop(5)
            manners.pop(5)

            for manner in manners:
                manner[1] += 0.04

        # If the POA has no coronal component, remove chance for sibilants
        if phoneme_bin & 2 == 0:
            manners[2][1] += manners[3][1]
            manners.pop(3)

        # If POA is glottal, only allow obstruents and approximants
        if phoneme_bin == 0:
            manners = [[0, 0.58], [512, 0.04], [1024, 0.38]]

        sel_num = random.random()
        sel = False

        while sel >= 0:
            if sel_num < manners[sel][1]:
                phoneme_bin += manners[sel][0]
                sel = -1

            else:
                sel_num -= manners[sel][1]
                sel += 1

        # Laryngeal Features
        manner = (phoneme_bin >> 8)
        if phoneme_bin != 0 and phoneme_bin != 512: # If not a glottal stop or affricate
            laryngeals = probs["Laryngeals"] + []
            sel_num = random.random()
            sel = False

            
            if manner > 0: # If not a plosive, remove chance for clicks and implosives
                laryngeals[0][1] += laryngeals[3][1]
                laryngeals[4][1] += laryngeals[7][1]
                laryngeals[4][1] += laryngeals[6][1]

                laryngeals.pop(3)
                laryngeals.pop()
                laryngeals.pop()

            if manner % 2 == 1: # If a sonorant, remove chance for ejectives
                laryngeals[0][1] += laryngeals[2][1]
                laryngeals.pop(2)

            if phoneme_bin % 8 == 0: # Glottal fricative
                laryngeals = [[0, 0.8], [128, 0.2]]

            if phoneme_bin == 537: # Pharyngeal Affricate
                laryngeals = [[0, 0.7], [32, 0.24], [64, 0.06]]

            while sel >= 0:
                if sel_num < laryngeals[sel][1]:
                    phoneme_bin += laryngeals[sel][0]
                    sel = -1

                else:
                    sel_num -= laryngeals[sel][1]
                    sel += 1

        # Nasality
        if manner != 1: # Not a nasal
            nasality = probs["Nasality"]
            sel_num = random.random()
            sel = False

            while sel >= 0:
                if sel_num < nasality[sel][1]:
                    phoneme_bin += nasality[sel][0]
                    sel = -1

                else:
                    sel_num -= nasality[sel][1]
                    sel += 1

        # Laterality
        if manner > 2: # No lateral plosives or nasals
            if not (phoneme_bin % 4 == 0 or phoneme_bin % 32 == 25): # No Labial, Glottal or Pharyngeal laterals 

                laterality = probs["Laterality"]
                sel_num = random.random()
                sel = False

                while sel >= 0:
                    if sel_num < laterality[sel][1]:
                        phoneme_bin += laterality[sel][0]
                        sel = -1

                    else:
                        sel_num -= laterality[sel][1]
                        sel += 1

        # Suprasegmentals
        if (phoneme_bin >> 11) == 0: # Can't be nasal
            suprasegmentals = probs["Suprasegmentals"]
            sel_num = random.random()
            sel = False

            while sel >= 0:
                if sel_num < suprasegmentals[sel][1]:
                    phoneme_bin += suprasegmentals[sel][0]
                    sel = -1

                else:
                    sel_num -= suprasegmentals[sel][1]
                    sel += 1

        # Find Phoneme
        sel_phonemes += [consonants.at[phoneme_bin, "Phoneme"]]
        consonants.at[phoneme_bin, "Selected"] = True

    return sel_phonemes


if __name__ == "__main__":
    num = int(sys.argv[1])
    # temp = float(sys.argv[2])

    consonants = loadPhonemes(True)
    # print(consonants[(consonants.index % 8 == 0) & (consonants.index < 1300)])
    probs = relangProbs()
    sel_phones = selectConsonants(consonants, probs["Consonants"], num)

    for i in range(len(sel_phones)):
        print(f"{i+1}. {sel_phones[i]}")