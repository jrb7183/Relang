import random
import sys
from pandas import DataFrame
from collections import Counter

sys.path.append("..")
from probs.relangProbs import relangProbs
from utils.phonemeLoader import loadPhonemes
from selphone.phonemeConstraints import updateConstraints
from selphone.rhoticLimiter import isRhotic, removeRhotics
from selphone.constraintLimits import removeSelected


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
        "supr place": 0
    }
    permit_phones = {26: {0: [0]}, 10: {0: [0]}}
    loop_count = 0
    maxed_rhotics = False

    while len(sel_phonemes) < num_phonemes:
        curr_permit = removeSelected(permit_phones, sel_phonemes, num_phonemes)
        phoneme_bin = 0

        # Debug loop
        # print(len(sel_phonemes))
        # for key in guarantees:
        #     if key not in ["nasals", "laterals"]:
        #         print(key, guarantees[key].total(), guarantees[key])
        #     else:
        #         print(key, guarantees[key])

        # print("")

        # Place of Articulation
        places = probs["Place"] + []

        places = list(filter(lambda place: place[0] in curr_permit, places))
        # if guarantees["places"].total() + len(sel_phonemes) == num_phonemes:
        #     temp = list(filter(lambda place: guarantees["places"][place[0]] > 0, places))
        #     if len(temp) > 0:
        #         places = temp

        places.sort(reverse=True, key=lambda place: place[1])

        sel_place = places[0][0]
        if len(places) > 1:
            sel_place = random.choice(places[:2])[0]

        phoneme_bin += sel_place
        curr_permit = curr_permit[sel_place]

        # Select prob_adjust to lower max prob and increase others
        # if len(places) > 1:
        #     prob_adjust = max(places[-1][1], 0.01)
        #     if places[0][1] - (prob_adjust * (len(places) - 1)) < 0:
        #         prob_adjust = places[0][1] / (len(places) - 1)

        #     # print(sel_place, prob_adjust)

        #     for place in probs["Place"]:
        #         if place in places:
        #             if place[0] == sel_place:
        #                 place[1] -= prob_adjust * (len(places) - 1)

        #             else:
        #                 place[1] += prob_adjust

        prob_adjust = 0.005
        sel_major_place = sel_place % 8
        for place in probs["Place"]:
            if place[0] == sel_place:
                place[1] -= prob_adjust

            elif place[0] % 8 != sel_major_place:
                place[1] += prob_adjust

            # If loop count is too high, the top two features might be in a positive feedback loop
            if loop_count > 100 and place in places[:2]:
                place[1] = 0

        # Set place guarantees
        if guarantees["places"][sel_place] > 0:
            guarantees["places"][sel_place] -= 1

        else:
            if sel_place != 0: # Not glottal
                guarantees["places"][sel_place] = min(2, num_phonemes - len(sel_phonemes) - guarantees["places"].total() - 1)


        # Manner of Articulation
        manners = probs["Manner"] + []

        manners = list(filter(lambda manner: manner[0] in curr_permit, manners))
        if len(manners) == 0:
            continue

        if guarantees["manners"].total() + len(sel_phonemes) == num_phonemes:
            temp = list(filter(lambda manner: guarantees["manners"][manner[0]] > 0, manners))
            if len(temp) > 0:
                manners = temp

        manners.sort(reverse=True, key= lambda manner : manner[1])

        sel_manner = manners[0][0]
        if len(manners) > 1:
            sel_manner = random.choice(manners[:2])[0]

        phoneme_bin += sel_manner
        curr_permit = curr_permit[sel_manner]

        # Select prob_adjust to lower max prob and increase others
        # if len(manners) > 1:
        #     prob_adjust = max((guarantees["manners"][sel_manner] + 1) / len(sel_phonemes), 0.05)
        #     if manners[0][1] - (prob_adjust * (len(manners) - 1)) < 0:
        #         prob_adjust = manners[0][1] / (len(manners) - 1)

        #     print(manners, guarantees["manners"][sel_manner])
        #     print(sel_manner, prob_adjust, "\n")

        #     for manner in probs["Manner"]:
        #         if manner in manners:
        #             if manner[0] == sel_manner:
        #                 manner[1] -= prob_adjust * (len(manners) - 1)

        #             else:
        #                 manner[1] += prob_adjust

        prob_adjust = 0.005
        for manner in probs["Manner"]:
            if manner[0] == sel_manner:
                manner[1] -= prob_adjust

            else:
                manner[1] += prob_adjust

            # If loop count is too high, the top two features might be in a positive feedback loop
            if loop_count > 100 and manner in manners[:2]:
                manner[1] = 0

        # Set manner guarantees
        if guarantees["manners"][sel_manner] > 0:
            guarantees["manners"][sel_manner] -= 1

        else:
            guarantees["manners"][sel_manner] = min(2, num_phonemes - len(sel_phonemes) - guarantees["manners"].total() - 1)
        

        # Laryngeal Features
        manner = (phoneme_bin >> 8)
        laryngeals = probs["Laryngeals"] + []

        

        laryngeals = list(filter(lambda laryngeal: laryngeal[0] in curr_permit, laryngeals))
        if len(laryngeals) == 0:
            continue

        if guarantees["laryngeals"].total() > 0:
            temp = list(filter(lambda laryngeal: guarantees["laryngeals"][laryngeal[0]] > 0, laryngeals))
            if len(temp) != 0:
                laryngeals = temp

        laryngeals.sort(reverse=True, key= lambda laryngeal : laryngeal[1])

        sel_laryngeal = laryngeals[0][0]
        if len(laryngeals) > 1:
            sel_laryngeal = random.choice(laryngeals[:2])[0]

        phoneme_bin += sel_laryngeal

        # Select prob_adjust to lower max prob and increase others
        # if len(laryngeals) > 1:
        #     prob_adjust = max(laryngeals[-1][1], 0.01)
        #     if laryngeals[0][1] - (prob_adjust * (len(laryngeals) - 1)) < 0:
        #         prob_adjust = laryngeals[0][1] / (len(laryngeals) - 1)

        #     # print(laryngeals)
        #     # print(sel_laryngeal, prob_adjust, "\n")

        #     for laryngeal in probs["Laryngeals"]:
        #         if laryngeal in laryngeals:
        #             if laryngeal[0] == sel_laryngeal:
        #                 laryngeal[1] -= prob_adjust * (len(laryngeals) - 1)

        #             else:
        #                 laryngeal[1] += prob_adjust

        prob_adjust = 0.05
        for laryng in probs["Laryngeals"]:
            if laryng[0] == sel_laryngeal:
                laryng[1] -= prob_adjust

            else:
                laryng[1] += prob_adjust

            # If loop count is too high, the top two features might be in a positive feedback loop
            if loop_count > 100 and laryng in laryngeals[:2]:
                laryng[1] = 0

        # # Set laryngeal guarantees
        if guarantees["laryngeals"][sel_laryngeal] > 0:
            guarantees["laryngeals"][sel_laryngeal] -= 1

        else:
            guarantees["laryngeals"][sel_laryngeal] = min(2, num_phonemes - len(sel_phonemes) - guarantees["laryngeals"].total() - 1)


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
                    suprasegmentals[0][1] += suprasegmentals[i][1] + 0.0001
                    suprasegmentals.pop(i)

                sel_num = random.random()
                sel = 0

                if guarantees["suprasegmentals"].total() > 0:
                    sel_num = 0
                    key = guarantees["suprasegmentals"].most_common(1)[0][0]

                    while sel < len(suprasegmentals) and suprasegmentals[sel][0] != key:
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
    # temp = float(sys.argv[2])

    consonants = loadPhonemes(True)
    # print(consonants[(consonants.index % 8 == 0) & (consonants.index < 1300)])
    probs = relangProbs()
    sel_phones = selectConsonants(consonants, probs["Consonants"], num)

    for i in range(len(sel_phones)):
        print(f"{i+1}. {sel_phones[i][0]}")