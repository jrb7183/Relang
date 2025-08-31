import random
import sys
from pandas import DataFrame

sys.path.append("..")
from probs.relangProbs import relang_probs
from utils.phonemeLoader import load_phonemes

from selphone.constraints.phonemeConstraints import update_constraints
from selphone.rhoticLimiter import is_rhotic, remove_rhotics
from selphone.constraints.constraintLimits import remove_selected
from selphone.featureSelector import select_feature
from selphone.guarantees import manage_guarantees


def select_consonants(consonants: DataFrame, probs, num_phonemes):
    sel_phonemes = []
    guarantees = []
    permit_phones = {10: {0: [0]}}
    loop_count = 0
    maxed_rhotics = False
    max_stops = num_phonemes * 3 // 4

    while len(sel_phonemes) < num_phonemes:
        curr_permit = remove_selected(permit_phones, sel_phonemes, num_phonemes, max_stops)
        phoneme_bin = 0

        # Checks for guarantees, and overrides the normal phoneme selector process if any valid ones are found
        if len(guarantees):
            i = 0
            
            while phoneme_bin == 0 and i < len(guarantees):
                place = guarantees[i] & 31
                manner = guarantees[i] & (7 << 8)
                laryng = guarantees[i] & (7 << 5)
                
                # Stop guarantees are ignored if the max has been met (meaning it's reduced to 0)
                if max_stops or manner & (3 << 9):
                    if place in permit_phones and manner in permit_phones[place] and laryng in permit_phones[place][manner]:
                        phoneme_bin = guarantees[i]
                        guarantees.pop(i)
                        
                        # Apply prob adjustments
                        pfs = ["Place", "Manner", "Laryngeals"]
                        for i in range(len(pfs)):
                            sel_feature = [place, manner, laryng][i]
                            prob_adjust = [0.001, 0.005, 0.05][i]

                            for feature in probs[pfs[i]]:
                                if feature[0] == sel_feature:
                                    feature[1] -= prob_adjust

                                # Ignore places in same major place
                                elif i or feature[0] % 8 != sel_feature % 8:
                                    feature[1] += prob_adjust

                i += 1

        if phoneme_bin == 0:

            # Place of Articulation
            sel_place = select_feature(0, probs, loop_count, curr_permit)
            phoneme_bin += sel_place
            curr_permit = curr_permit[sel_place]

            # Manner of Articulation
            sel_manner = select_feature(1, probs, loop_count, curr_permit)
            if sel_manner == -1:
                continue
            
            phoneme_bin += sel_manner
            curr_permit = curr_permit[sel_manner]

            # Laryngeal Features
            sel_laryng = select_feature(2, probs, loop_count, curr_permit)
            phoneme_bin += sel_laryng
            if sel_laryng == -1:
                continue

            # Laterality
            manner = (phoneme_bin >> 8)
            if manner > 3 and manner != 6: # No lateral plosives, nasals, affricates, trills, or sibilants
                if not (phoneme_bin % 4 == 0 or phoneme_bin % 32 == 25): # No Labial, Glottal or Pharyngeal laterals 

                    laterality = probs["Laterality"]
                    sel_num = random.random()

                    if sel_num >= laterality[0][1]:
                        phoneme_bin += laterality[1][0]
        
            # Filter out rhotics if max has been met
            if maxed_rhotics and is_rhotic(phoneme_bin):
                continue 

            # Temp fix to filter out non-lateral alveolar fricatives
            if sel_place == 10 and sel_manner == 1024 and phoneme_bin & (1 << 12) == 0:
                continue

            if consonants.at[phoneme_bin, "Selected"]: # Require phonemic equivalent without supresegmentals before adding ones with them
                # Nasality
                if manner != 1: # Not a nasal
                    nasality = probs["Nasality"]
                    sel_num = random.random()

                    if sel_num >= nasality[0][1]:
                        phoneme_bin += nasality[1][0]

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

                    while sel >= 0:
                        if sel_num < suprasegmentals[sel][1]:
                            phoneme_bin += suprasegmentals[sel][0]
                            sel = -1

                        else:
                            sel_num -= suprasegmentals[sel][1]
                            sel += 1

        # Find Phoneme
        if not consonants.at[phoneme_bin, "Selected"]:
            sel_phonemes += [(consonants.at[phoneme_bin, "Phoneme"], phoneme_bin)]
            consonants.at[phoneme_bin, "Selected"] = True

            loop_count = 0
            if sel_manner & (3 << 9) == 0 or (sel_place == 18 and sel_manner == 512):
                max_stops -= 1

            # Update Permitted Phonemes
            permit_phones = update_constraints(phoneme_bin, permit_phones, sel_phonemes, num_phonemes)
            if is_rhotic(phoneme_bin):
                [permit_phones, maxed_rhotics] = remove_rhotics(sel_phonemes, num_phonemes, permit_phones)

            guarantees += manage_guarantees(sel_phonemes)

        else:
            loop_count += 1
            if loop_count > 10**4:
                print(f"Error: only {len(sel_phonemes)} consonants could be generated.")
                break

    return sel_phonemes


if __name__ == "__main__":
    num = int(sys.argv[1])

    consonants = load_phonemes(True)
    probs = relang_probs([])
    sel_phones = select_consonants(consonants, probs, num)

    for i in range(len(sel_phones)):
        print(f"{i+1}. {sel_phones[i][0]}")