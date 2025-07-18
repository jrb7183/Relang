
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

def updatePermitted(phoneme_bin: int, curr_permit: dict):
    
    # Update Place Permissions
    places = []
    place = phoneme_bin % 32

    match len(list(curr_permit.keys())):
        case 2: # Add both labial, velar and glottal places
            places = [12, 4, 9, 0]
        
        case 6: # Add post-alveolar and palatal places
            if place in [12, 4, 9, 0]:
                places = [18, 19]

        case 8: # Add retroflex, uvular, and pharyngeal places
            if place in [18, 19]:
                places = [2, 17, 25]

    if len(places) > 0:
        for new_place in places:
                if new_place != 18:
                    curr_permit[new_place] = {0: [0]}
                else:
                    curr_permit[new_place] = {512: [0]}

    # Update Manner Permissions
    manners = []
    manner = (phoneme_bin & (7 << 8)) % 2048
    curr_manners = curr_permit[place]

    match len(list(curr_manners.keys())):
        case 1: # Add nasals
            manners = [256]
        
        case 2: # Add fricatives and/or sibilants, taps, trills, and approximants
            manners = [768, 1280, 1792]
            if place & 2 == 2:
                manners += [1536]

            if place % 8 != 2:
                manners += [1024]

        case 4: # Add affricates
            if place != 18 and manner in [1024, 1536]:
                manners = [512]

        case 5: # Add affricates for palatals
            if place == 19 and manner in [1024, 1536]:
                manners = [512]

    if len(manners) > 0:
        for new_manner in manners:
                if (new_manner >> 8) % 2 == 0:
                    curr_manners[new_manner] = [0]
                else:
                    curr_manners[new_manner] = [128]
        
    return curr_permit