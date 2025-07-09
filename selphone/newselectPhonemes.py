import random
import sys
import numpy as np
import pandas as pd
import time
from collections import Counter

sys.path.append(".")
from probs.relangProbs import relangProbs
from utils.phonemeLoader import loadPhonemes


def selectConsonants(consonants: pd.DataFrame, probs, num_phonemes):
    sel_phonemes = []
    guarantees = {
        "places": Counter(),
        "manners": Counter(),
        "laryngeals": Counter(),
        "nasals": 0,
        "laterals": 0,
        "suprasegmentals": Counter()
    }
    
    while len(sel_phonemes) < num_phonemes:
        phoneme_bin = 0

        # Debug loop
        print(len(sel_phonemes))
        for key in guarantees:
            if key not in ["nasals", "laterals"]:
                print(key, guarantees[key].total(), guarantees[key])
            else:
                print(key, guarantees[key])

        print("")

        # Place of Articulation
        places = probs["Place"] + []
        if guarantees["places"].total() + len(sel_phonemes) == num_phonemes:
            places = list(filter(lambda place: guarantees["places"][place[0]] > 0, places))

        places.sort(reverse=True, key= lambda place : place[1])

        sel_place = places[0][0]
        phoneme_bin += sel_place

        # Select prob_adjust to lower max prob and increase others
        prob_adjust = max(places[-1][1], 0.01)
        if places[0][1] - (prob_adjust * (len(places) - 1)) < 0:
            prob_adjust = places[0][1] / (len(places) - 1)

        # print(sel_place, prob_adjust)

        for place in probs["Place"]:
            if place[0] == sel_place:
                place[1] -= prob_adjust * (len(places) - 1)

            else:
                place[1] += prob_adjust

        # Set place guarantees
        if guarantees["places"][sel_place] > 0:
            guarantees["places"][sel_place] -= 1

        else:
            if sel_place != 0: # Not glottal
                guarantees["places"][sel_place] = min(num_phonemes // 5, num_phonemes - len(sel_phonemes) - guarantees["places"].total() - 1)



        # Manner of Articulation
        manners = probs["Manner"] + []

        # If the POA is palatal or velar, remove chance for taps and trills
        if phoneme_bin == 19 or phoneme_bin == 9:
            manners.pop(5)
            manners.pop(5)

            for manner in manners:
                manner[1] += 0.04

        # If POA is pharyngeal, remove nasals
        if phoneme_bin == 25:
            manners.pop(4)

        # If the POA has no coronal component, remove chance for sibilants
        if phoneme_bin & 2 == 0:
            manners.pop(3)

        # If POA is glottal, only allow obstruents and approximants
        if phoneme_bin == 0:
            manners = [[0, 0.58], [512, 0.04], [1024, 0.38]]

        if guarantees["manners"].total() + len(sel_phonemes) == num_phonemes:
            manners = list(filter(lambda manner: guarantees["manners"][manner[0]] > 0, manners))
            
            if len(manners) == 0:
                continue

        manners.sort(reverse=True, key= lambda manner : manner[1])

        sel_manner = manners[0][0]
        phoneme_bin += sel_manner

        # Select prob_adjust to lower max prob and increase others
        prob_adjust = max(manners[-1][1], 0.01)
        if manners[0][1] - (prob_adjust * (len(manners) - 1)) < 0:
            prob_adjust = manners[0][1] / (len(manners) - 1)

        # print(manners)
        # print(sel_manner, prob_adjust, "\n")

        for manner in probs["Manner"]:
            if manner[0] == sel_manner:
                manner[1] -= prob_adjust * (len(manners) - 1)

            else:
                manner[1] += prob_adjust

        # Set manner guarantees
        if guarantees["manners"][sel_manner] > 0:
            guarantees["manners"][sel_manner] -= 1

        else:
            guarantees["manners"][sel_manner] = min(num_phonemes // 4, num_phonemes - len(sel_phonemes) - guarantees["manners"].total() - 1)
        

        # Laryngeal Features
        manner = (phoneme_bin >> 8)
        if phoneme_bin != 0 and phoneme_bin != 512: # If not a glottal stop or affricate
            laryngeals = probs["Laryngeals"] + []
            
            if manner > 0 or sel_place == 25: # If not a plosive or is pharyngeal, remove chance for clicks and implosives
                laryngeals.pop(3)
                laryngeals.pop()
                laryngeals.pop()

            elif manner == 0 and (sel_place == 2 or sel_place == 18 or sel_place == 4 or sel_place % 8 == 1): # If a plosive in a place with no clicks, remove clicks
                laryngeals.pop(3)
                laryngeals.pop()

            if manner % 2 == 1: # If a sonorant, remove chance for ejectives
                laryngeals.pop(2)

            if phoneme_bin % 8 == 0: # Glottal fricative, only tenuis and voiced
                laryngeals.pop(2)
                laryngeals.pop(2)
                laryngeals.pop()
                print(laryngeals)

            if sel_place == 25 and manner % 2 == 0 and manner < 3: # Pharyngeal Plosive or Affricate
                laryngeals.pop()
                laryngeals.pop()
                print(laryngeals)

            if guarantees["laryngeals"].total() + len(sel_phonemes) == num_phonemes:
                laryngeals = list(filter(lambda laryngeal: guarantees["laryngeals"][laryngeal[0]] > 0, laryngeals))

                if len(laryngeals) == 0:
                    continue

            laryngeals.sort(reverse=True, key= lambda laryngeal : laryngeal[1])

            sel_laryngeal = laryngeals[0][0]
            phoneme_bin += sel_laryngeal

            # Select prob_adjust to lower max prob and increase others
            prob_adjust = max(laryngeals[-1][1], 0.01)
            if laryngeals[0][1] - (prob_adjust * (len(laryngeals) - 1)) < 0:
                prob_adjust = laryngeals[0][1] / (len(laryngeals) - 1)

            # print(laryngeals)
            # print(sel_laryngeal, prob_adjust, "\n")

            for laryngeal in probs["Laryngeals"]:
                if laryngeal[0] == sel_laryngeal:
                    laryngeal[1] -= prob_adjust * (len(laryngeals) - 1)

                else:
                    laryngeal[1] += prob_adjust

        # Set laryngeal guarantees
        if guarantees["laryngeals"][sel_laryngeal] > 0:
            guarantees["laryngeals"][sel_laryngeal] -= 1

        else:
            guarantees["laryngeals"][sel_laryngeal] = min(num_phonemes // 3, num_phonemes - len(sel_phonemes) - guarantees["laryngeals"].total() - 1)


        # Nasality
        if manner != 1: # Not a nasal
            nasality = probs["Nasality"]
            sel_num = random.random()

            if sel_num >= nasality[0][1] or guarantees["nasals"] + len(sel_phonemes) == num_phonemes:
                phoneme_bin += nasality[1][0]

                # Set nasality guarantees
                if guarantees["nasals"] > 0:
                    guarantees["nasals"] -= 1
                else:
                    guarantees["nasals"] = min(num_phonemes // 10, num_phonemes - len(sel_phonemes) - guarantees["nasals"] - 1)


        # Laterality
        if manner > 3 and manner != 6: # No lateral plosives, nasals, affricates, trills, or sibilants
            if not (phoneme_bin % 4 == 0 or phoneme_bin % 32 == 25): # No Labial, Glottal or Pharyngeal laterals 

                laterality = probs["Laterality"]
                sel_num = random.random()

                if sel_num >= laterality[0][1] or guarantees["laterals"] + len(sel_phonemes) == num_phonemes:
                    phoneme_bin += laterality[1][0]

                    # Set laterality guarantees
                    if guarantees["laterals"] > 0:
                        guarantees["laterals"] -= 1
                    else:
                        guarantees["laterals"] = min(num_phonemes // 10, num_phonemes - len(sel_phonemes) - guarantees["laterals"] - 1)


        # Suprasegmentals
        if (phoneme_bin >> 11) == 0: # Can't be nasal
            suprasegmentals = probs["Suprasegmentals"]
            sel_num = random.random()
            sel = 0

            if guarantees["suprasegmentals"].total() > 0:
                sel_num = 0
                key = guarantees["suprasegmentals"].most_common(1)[0][0]

                while suprasegmentals[sel][0] != key:
                    sel_num += suprasegmentals[sel][1]
                    sel += 1

                sel = 0

            while sel >= 0:
                if sel_num < suprasegmentals[sel][1]:
                    phoneme_bin += suprasegmentals[sel][0]
                    
                    # Set suprasegmental guarantees
                    if sel != 0:
                        sel_supr = suprasegmentals[sel][0]
                        if guarantees["suprasegmentals"][sel_supr] > 0:
                            guarantees["suprasegmentals"][sel_supr] -= 1
                            
                        else:
                            guarantees["suprasegmentals"][sel_supr] = min(num_phonemes // 10, num_phonemes - len(sel_phonemes) - guarantees["suprasegmentals"].total() - 1)

                    sel = -1

                else:
                    sel_num -= suprasegmentals[sel][1]
                    sel += 1

        # Find Phoneme
        if not consonants.at[phoneme_bin, "Selected"]:
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