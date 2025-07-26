from collections import Counter

"""
This criteria function helps determine how to update the current constraints for the
phoneme selector. Based on the phonemes in the selected phoneme list, and the current
number of places and manners features, they check which criteria are met. If any are, 
then they return the corresponding manners.
"""

# Determines which manners to add to the constraints
def mannerCriteria(curr_manners: list[int], sel_phonemes: list[list]) -> list[int]:
    curr_num_manners = len(curr_manners)
    phoneme_bin = sel_phonemes[-1][1]

    curr_place = phoneme_bin % 32
    curr_manner = phoneme_bin & (7 << 8)
    
    places = Counter(map(lambda sel_phoneme: sel_phoneme[1] % 32, sel_phonemes))
    manners = Counter(map(lambda sel_phoneme: (sel_phoneme[1] & (7 << 8)) % 2048, sel_phonemes))
    
    match curr_num_manners:
        case 1: # Add nasals
            if 0 in curr_manners:
                match curr_place:
                    case 25 | 0: # If glottal or pharyngeal, nasals are physically impossible. Skip to fricatives
                        return [1024]
                
                    case 12 | 10 | 9:
                        return [256]
                
                    case 18 | 19 if manners[256] >= 3:
                        return [256]

                    case _ if manners[256] >= 4:
                        return [256]

        case 2: # Add fricatives/sibilants, taps, trills, and approximants
            if 0 in curr_manners:
                new_manners =  [1792]
                if curr_place & 2 == 2: # Ignore sibilants for non coronals
                    new_manners += [1536]
                
                if curr_place % 8 != 2 and curr_place != 25: # Ignore fricatives for coronals and pharyngeals (since the latter already has them)
                    new_manners += [1024]

                if curr_place % 10 != 9: # Ignore taps and trills for palatals and velars
                    new_manners += [768, 1280]
                
                match curr_place:
                    case 0 if curr_manner == 1024 and manners[512] > 5: # If glottal, skip to affricates 
                        return [512]
                    
                    case 12 | 4 | 10 | 9 if places[curr_place] >= 2:
                        return new_manners

                    case 18 | 19 if manners[1024] + manners[1536] + manners[768] + manners[1280] + manners[1792] > 4:
                        return new_manners

                    case 25 if places[25] >= 3 and manners[768] + manners[1280] + manners[1792] > 6: 
                        return new_manners
                    
                    case 26 | 2 | 17 if manners[1024] + manners[1536] + manners[768] + manners[1280] + manners[1792] > 7:
                        return new_manners
                
        case 4: # Add affricates to velars
            if curr_manner == 1024 and curr_place == 9:
                return [512]

        case 5: # Add affricates to palatals and pharyngeals
            if curr_place == 19 and curr_manner == 1024 and manners[512] > 2:
                return [512]
            
            elif curr_place == 25 and manners[512] > 8:
                return [512]
            
        case 6: # Add affricates
            if curr_manner in [1024, 1536]:
                match curr_place:
                    case 18 | 19 | 25: # Ignore post-alveolars, palatals, and pharyngeals
                        return []
                    
                    case 12 | 10 | 9:
                        return [512]
                    
                    case 2 if manners[512] > 2:
                        return [512]
                    
                    case _ if manners[512] > 6:
                        return [512]

    return []