import random
import sys
from pandas import DataFrame
from collections import Counter

sys.path.append("..")
from probs.relangProbs import relangProbs
from utils.phonemeLoader import loadPhonemes

from selphone.constraints.phonemeConstraints import updateConstraints
from selphone.rhoticLimiter import isRhotic, removeRhotics
from selphone.constraints.constraintLimits import removeSelected
from selphone.featureSelector import selectFeature


def selectConsonants(consonants: DataFrame, probs, num_phonemes):
    sel_phonemes = []
    guarantees = {
        "places": Counter(),
        "manners": Counter(),
        "laryngeals": Counter(),
        "nasals": 0,
        "laterals": 0,
        "suprasegmentals": Counter(),
        "nasal manner": 0,
        "supr place": [0 for i in range(5)]
    }
    permit_phones = {26: {0: [0]}, 10: {0: [0]}}
    loop_count = 0
    maxed_rhotics = False

    while len(sel_phonemes) < num_phonemes:
        curr_permit = removeSelected(permit_phones, sel_phonemes, num_phonemes)
        phoneme_bin = 0

        # Place of Articulation
        sel_place = selectFeature(0, probs, guarantees, len(sel_phonemes), num_phonemes, loop_count, curr_permit)
        phoneme_bin += sel_place
        curr_permit = curr_permit[sel_place]

        # Manner of Articulation
        sel_manner = selectFeature(1, probs, guarantees, len(sel_phonemes), num_phonemes, loop_count, curr_permit)
        if sel_manner == -1:
            continue
        
        phoneme_bin += sel_manner
        curr_permit = curr_permit[sel_manner]

        # Laryngeal Features
        sel_laryng = selectFeature(2, probs, guarantees, len(sel_phonemes), num_phonemes, loop_count, curr_permit)
        phoneme_bin += sel_laryng
        if sel_laryng == -1:
            continue

        # Laterality
        manner = (phoneme_bin >> 8)
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
       
        # Filter out rhotics if max has been met
        if maxed_rhotics and isRhotic(phoneme_bin):
            continue 

        if consonants.at[phoneme_bin, "Selected"]: # Require phonemic equivalent without supresegmentals before adding ones with them
            # Nasality
            if manner != 1: # Not a nasal
                nasality = probs["Nasality"]
                sel_num = random.random()

                if sel_num >= nasality[0][1] or (sel_manner == guarantees["nasal manner"] and guarantees["nasals"] + len(sel_phonemes) == num_phonemes):
                    phoneme_bin += nasality[1][0]

                    # Set nasality guarantees
                    if guarantees["nasals"] > 0:
                        guarantees["nasals"] -= 1
                    else:
                        guarantees["nasals"] = min(num_phonemes // 10, num_phonemes - len(sel_phonemes) - guarantees["nasals"] - 1)
                        guarantees["nasal manner"] = sel_manner

            # Suprasegmentals
            if (phoneme_bin >> 11) == 0: # Can't be nasal
                suprasegmentals = probs["Suprasegmentals"] + []

                # No velarized velars, palatalized palatals, or pharyngealized pharyngeals
                if sel_place in [19, 9, 25]:
                    i = [19, 9, 25].index(sel_place) + 2
                    suprasegmentals[0][1] += suprasegmentals[i][1]
                    suprasegmentals.pop(i)

                sel_num = random.random()
                sel = 0

                if guarantees["suprasegmentals"].total() > 0:
                    for i in range(1, len(suprasegmentals)):

                        supr = suprasegmentals[i][0]
                        if sel_place == guarantees["supr place"][i] and guarantees["suprasegmentals"][supr] > 0:

                            sel_num = 0
                            while sel < len(suprasegmentals) and suprasegmentals[sel][0] != supr:
                                sel_num += suprasegmentals[sel][1]
                                sel += 1

                            if sel == len(suprasegmentals):
                                sel_num = 0

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
                                guarantees["supr place"][sel] = sel_place

                        sel = -1

                    else:
                        sel_num -= suprasegmentals[sel][1]
                        sel += 1

        # Find Phoneme
        if not consonants.at[phoneme_bin, "Selected"]:
            sel_phonemes += [(consonants.at[phoneme_bin, "Phoneme"], phoneme_bin)]
            consonants.at[phoneme_bin, "Selected"] = True

            loop_count = 0

            # Update Permitted Phonemes
            permit_phones = updateConstraints(phoneme_bin, permit_phones, sel_phonemes, num_phonemes)
            if isRhotic(phoneme_bin):
                [permit_phones, maxed_rhotics] = removeRhotics(sel_phonemes, num_phonemes, permit_phones)

        else:
            loop_count += 1
            if loop_count > 10**4:
                print(f"Error: only {len(sel_phonemes)} consonants could be generated.")
                break

    return sel_phonemes


if __name__ == "__main__":
    num = int(sys.argv[1])

    consonants = loadPhonemes(True)
    probs = relangProbs([])
    sel_phones = selectConsonants(consonants, probs["Consonants"], num)

    for i in range(len(sel_phones)):
        print(f"{i+1}. {sel_phones[i][0]}")