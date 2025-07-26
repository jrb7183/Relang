import sys

sys.path.append("..")
from selphone.constraintCriteria.placeCriteria import placeCriteria
from selphone.constraintCriteria.mannerCriteria import mannerCriteria
from selphone. constraintCriteria.laryngealCriteria import laryngealCriteria
"""
Updates the phonemes permitted to be selected by the Phoneme Selector.
These constraints allow the selector to produce more naturalistic sound
inventories by upholding certain phonological patterns observed in languages
around the world. 

For example, a language has a voiced alveolar plosive /d/, it (logically) 
implies that the language also has a tenuis alveolar plosive /t/.

Of course, there are always exceptions with natural languages (i.e. Arabic
has a voiced labial plosive /b/ but no tenuis labial plosive /p/).
Nevertheless, Relang is aiming to make sketches for sound inventories of 
proto-languages, which should be more regular.
"""

def updateConstraints(phoneme_bin: int, curr_permit: dict[int, dict[int, list]], sel_phonemes: list[list]):
    
    # Update Place Permissions
    place = phoneme_bin % 32
    curr_num_places = len(list(curr_permit.keys()))
    places = placeCriteria(curr_num_places, sel_phonemes)

    if len(places) > 0:
        for new_place in places:
            if new_place != 18:
                curr_permit[new_place] = {0: [0]}
            else:
                curr_permit[new_place] = {512: [0]}

    # Update Manner Permissions
    manner = (phoneme_bin & (7 << 8)) % 2048
    curr_manners = curr_permit[place]

    curr_num_manners = len(list(curr_manners.keys()))
    manners = mannerCriteria(curr_num_manners, sel_phonemes)

    if len(manners) > 0:
        for new_manner in manners:
            if (new_manner >> 8) % 2 == 0:
                curr_manners[new_manner] = [0]
            else:
                curr_manners[new_manner] = [128]
        
    # Update Laryngeal Permissions
    curr_laryngeals = curr_manners[manner]
    laryngeals = laryngealCriteria(curr_laryngeals, sel_phonemes)
    curr_laryngeals += laryngeals
    
    return curr_permit