import sys
from collections import Counter

sys.path.append("..")
from selphone.constraints.constraintCriteria.laryngealCriteria.sonorantLaryngealCriteria import sonorant_laryngeals
from selphone.constraints.constraintCriteria.laryngealCriteria.plosiveLaryngealCriteria import plosive_laryngeals
from selphone.constraints.constraintCriteria.laryngealCriteria.obstruentLaryngealCriteria import np_obstruent_laryngeals

"""
This criteria function helps determine how to update the current constraints for the
phoneme selector. Based on the phonemes in the selected phoneme list, and the current
number of places, manners, and laryngeal features, they check which criteria are met.
If any are, then they return the corresponding laryngeal features.
"""

# Determines which laryngeals to add to the constraints
def laryngeal_criteria(curr_laryngs: list[int], sel_phonemes: list[list], num_phonemes: int) -> list[int]:

    # Find information relevant to laryngeal feature criteria
    curr_num_laryngs = len(curr_laryngs)
    phoneme_bin = sel_phonemes[-1][1]
    is_sonorant = (phoneme_bin >> 8) % 2

    curr_place = phoneme_bin % 32
    curr_manner = phoneme_bin & (7 << 8)
    
    pals = Counter(map(lambda sel_phoneme: sel_phoneme[1] & 255, sel_phonemes)) # places + laryngeals
    mals = Counter(map(lambda sel_phoneme: sel_phoneme[1] & (63 << 5), sel_phonemes)) # manners + laryngeals

    # Determine new laryngeal constraints based on information found
    if is_sonorant:
        return sonorant_laryngeals(curr_num_laryngs, curr_manner, curr_place, mals)             
    
    if curr_manner == 0:
        return plosive_laryngeals(curr_laryngs, curr_num_laryngs, curr_place, mals, num_phonemes)
    
    return np_obstruent_laryngeals(curr_laryngs, curr_num_laryngs, curr_manner, curr_place, mals, pals)