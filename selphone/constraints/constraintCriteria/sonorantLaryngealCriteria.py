from collections import Counter

""" Helper function for laryngealCriteria. Handles laryngeal criteria for sonorants"""

def sonorantLaryngeals(curr_num_laryngs: int, curr_manner: int, curr_place: int, mals: Counter) -> list[int]:
    match curr_num_laryngs:
        case 1: # Add voiceless sonorants
            if curr_manner == 256:
                match curr_place:

                    # Only add voiceless nasals if there is a voicing contrast in the plosives and at least 3 (voiced) nasals have already been selected
                    case 12 | 10 | 9 if mals[128] > 0 and mals[256 + 128] > 2:
                        return [0]

                    case _ if mals[256] > 2:
                        return [0]
                    
            else: # Only add voiceless non-nasal sonorants if at least 3 voiceless nasals have been selected 
                if mals[256] > 2:
                    return [0]

        case 2 | 3: # Add aspirated/breathy sonorants
            laryngeals = [0, 32, 160]
            old_laryng = laryngeals[curr_num_laryngs - 2]
            new_laryng = laryngeals[curr_num_laryngs - 1]
            if curr_manner == 256:
                match curr_place:
                    
                    # Only add aspirated/breathy nasals if there is an aspirated/breathy contrast in the plosives and at least 3 voiceless nasals have already been selected
                    case 12 | 10 | 9 if mals[new_laryng] > 0 and mals[256 + old_laryng] > 2:
                        return [0]

                    case _ if mals[256 + new_laryng] > 2:
                        return [0]
                    
            else: # Only add aspirated/breathy non-nasal sonorants if at least 3 aspirated/breathy nasals have been selected 
                if mals[256 + new_laryng] > 2:
                    return [0]
                
    return []