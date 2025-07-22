import sys

sys.path.append("..")
from selphone.constraintCriteria import placeCriteria, mannerCriteria

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
    laryngeal = (phoneme_bin & (7 << 5)) % 256
    curr_laryngeals = curr_manners[manner]

    is_sonorant = phoneme_bin & 256 == 256
    match len(curr_laryngeals):
        case 1: # If obstruent, add voiced and aspirated features; if sonorant add tenuis and breathy features
            if is_sonorant:
                curr_laryngeals += [0, 160]
            else:
                curr_laryngeals += [32, 128]
        
        case 3: # If obstruent, add breathy, ejective, and/or implosive features; if sonorant add aspirated features
            if is_sonorant:
                if laryngeal == 0:
                    curr_laryngeals += [32]

            elif laryngeal in [32, 128]:
                curr_laryngeals += [64]
                
                if laryngeal == 32:
                    curr_laryngeals += [160]

                if manner == 0:
                    curr_laryngeals += [192]

        case 4: # Ignore sonorants; add breathy feature for obstruents
            if not is_sonorant:
                if laryngeal == 32:
                    curr_laryngeals += [160]

        case 5: # Ignore everything but plosives; add breathy or click features
            if manner == 0:
                if laryngeal == 32:
                    curr_laryngeals += [160]
                
                if laryngeal in [64, 192]:
                    curr_laryngeals += [96, 224]

        case 6: # Add click features
            if laryngeal in [64, 192]:
                    curr_laryngeals += [96, 224]

        case 7: # Add breathy feature
            if laryngeal == 32:
                    curr_laryngeals += [160]
    
    return curr_permit