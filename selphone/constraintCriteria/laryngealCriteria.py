import sys
from collections import Counter

sys.path.append("../..")
from selphone.constraintCriteria.sonorantLaryngealCriteria import sonorantLaryngeals

"""
This criteria function helps determine how to update the current constraints for the
phoneme selector. Based on the phonemes in the selected phoneme list, and the current
number of places, manners, and laryngeal features, they check which criteria are met.
If any are, then they return the corresponding laryngeal features.
"""

# Determines which laryngeals to add to the constraints
def laryngealCriteria(curr_laryngs: list[int], sel_phonemes: list[list]) -> list[int]:
    curr_num_laryngs = len(curr_laryngs)
    phoneme_bin = sel_phonemes[-1][1]
    is_sonorant = (phoneme_bin >> 8) % 2

    curr_place = phoneme_bin % 32
    curr_manner = phoneme_bin & (7 << 8)
    
    manners = Counter(map(lambda sel_phoneme: sel_phoneme[1] & (7 << 8), sel_phonemes))
    pals = Counter(map(lambda sel_phoneme: sel_phoneme[1] & 255, sel_phonemes)) # places + laryngeals
    mals = Counter(map(lambda sel_phoneme: sel_phoneme[1] & (63 << 5), sel_phonemes)) # manners + laryngeals
    

    if is_sonorant: # Sonorants
        return sonorantLaryngeals(curr_num_laryngs, curr_manner, curr_place, manners, mals)
                    
    else: # Obstruents
        match curr_num_laryngs:
            case 1: # Add aspirated and voiced features
                if curr_manner == 0:
                    if curr_place in [12, 10, 9]:
                        return [32, 128]

                    if curr_place != 0:
                        if mals[128] > 2 and curr_place != 25:
                            if mals[32] > 2:
                                return [32, 128]

                            return [128]
                        
                        if mals[32] > 2:
                            return [32]
                
                else:
                    if curr_place == 25 and curr_manner != 1024:
                        if mals[32] > 2:
                            return [32]
                
                    elif curr_place != 0:
                        if mals[128] > 2 and pals[128 + curr_place] > 1:
                            if mals[32] > 2 and pals[32 + curr_place] > 1:
                                return [32, 128]
                            
                            return [128]
                        
                        if mals[32] > 2 and pals[32 + curr_place] > 1:
                            return [32]
                    
                    elif curr_place == 0 and curr_manner == 1024 and mals[128] > 2:
                        return [128]
                
            case 2: # Add ejective features to pharyngeal plosives and affricates (curr_laryngs = [0, 32] or [0, 128])
                if curr_place == 25 and mals[64] > 8:
                    return [64]
                
                elif curr_manner == 0:
                    if 32 in curr_laryngs:
                        if mals[128] > 2:
                            return [128]
                        
                    else:
                        if mals[32] > 2:
                            return [32]
                        
                elif curr_place != 0:
                    if 32 in curr_laryngs:
                        if mals[128] > 2 and pals[128 + curr_place] > 1:
                            return [128]
                        
                    else:
                        if mals[32] > 2 and pals[32 + curr_place] > 1:
                            return [32]

            case 3: # Add breathy, ejective, and/or implosive features
                if curr_place != 25 or curr_manner == 1024:
                    match curr_manner:
                        case 0:

                            if curr_place in [12, 10, 9]:
                                if mals[32] > 2:
                                    if mals[32] > 2 and mals[128] > 2:
                                        return [64, 160, 192]
                                    
                                    return [64]

                                if mals[128] > 2:
                                    return [64, 192]
                                
                            else:
                                if mals[64] > 2:
                                    out_laryngs = [64]

                                    if mals[160] > 2:
                                        out_laryngs += [160]

                                    if mals[192] > 2:
                                        out_laryngs == [192]

                                    return out_laryngs
                                
                        case 1024 | 1536: # Continuant
                            if curr_place in [12, 10, 9]:
                                if mals[64] > 2:
                                    if mals[160] > 2:
                                        return [64, 160]
                                    
                                    return [64]
                                
                                if mals[160] > 2:
                                    return [160]
                                
                            else: 
                                if mals[64 + 1024] + mals[64 + 1536] > 1 and pals[64 + curr_place] > 0:
                                    if mals[160 + 1024] + mals[160 + 1536] > 1 and pals[160 + curr_place] > 0:
                                        return [64, 160]
                                    
                                    return [64]
                                
                                if mals[160 + 1024] + mals[160 + 1536] > 1 and pals[160 + curr_place] > 0:
                                    return [160]
                            
                        case 512: # Affricate
                            if curr_place in [12, 10, 9]:
                                if mals[64 + 1024] + mals[64 + 1536] > 1:
                                    if mals[160 + 1024] + mals[160 + 1536] > 1:
                                        return [64, 160]
                                    
                                    return [64]
                                
                                if mals[160 + 1024] + mals[160 + 1536] > 1 and pals[160 + curr_place] > 1:
                                    return [160]
                                
                            else: 
                                if mals[64 + 512] > 1 and pals[64 + curr_place] > 1:
                                    if mals[160 + 512] > 1 and pals[160 + curr_place] > 1:
                                        return [64, 160]
                                    
                                    return [64]
                                
                                if mals[160 + 512] > 1 and pals[160 + curr_place] > 1:
                                    return [160]

                            
            case 4: # Add breathy and/or implosive features 
                match curr_manner: 
                    case 0: # (curr_laryngs = [0, 32, 64, 128])
                        if curr_place in [12, 10, 9]:
                            
                            if mals[128] > 3:
                                if mals[32] > 3:
                                    return [160, 192]

                                return [192]
                            
                        else:
                            out_laryngs = []

                            if mals[160] > 3:
                                out_laryngs += [160]

                            if mals[192] > 3:
                                out_laryngs += [192]

                            return out_laryngs
                    
                    case 1024 | 1536: # Continuant (curr_laryngs = [0, 32, 64, 128] or [0, 32, 128, 160])
                        out_laryng = 64
                        if 64 in curr_laryngs:
                            out_laryng = 160

                        if curr_place in [12, 10, 9]:

                            if mals[out_laryng] > 2:
                                return [out_laryng]
                            
                        else:                             
                            if mals[out_laryng + 1024] + mals[out_laryng + 1536] > 1 and pals[out_laryng + curr_place] > 0:
                                return [out_laryng]
                            
                    case 512: # Affricate (curr_laryngs = [0, 32, 64, 128] or [0, 32, 128, 160])
                        out_laryng = 64
                        if 64 in curr_laryngs:
                            out_laryng = 160

                        if curr_place in [12, 10, 9]:

                            if mals[out_laryng + 1024] + mals[out_laryng + 1536] > 1:
                                return [out_laryng]
                            
                        else:                             
                            if mals[out_laryng + 512] > 1 and pals[out_laryng + curr_place] > 1:
                                return [out_laryng]
                            
            case 5: # Ignore non-plosives, add breathy, implosives, and/or clicks (curr_laryngs = [0, 32, 64, 128, 160] or [0, 32, 64, 128, 192])
                if curr_manner == 0:
                    match curr_place:

                        # Bilabial, alveolar, and velar places will only have curr_laryngs = [0, 32, 64, 128, 192]
                        case 12 | 10:
                            if mals[192] > 3:
                                if mals[32] > 3:
                                    return [96, 160, 224]

                                return [96, 224]
                            
                        case 9: # No velar clicks
                            if mals[32] > 3:
                                return [160]
                        
                        case 26 | 19:
                            if 160 in curr_laryngs: # curr_laryngs = [0, 32, 64, 128, 160]
                                if mals[192] > 3:
                                    return [192]

                            else:
                                out_laryngs = []
                                if mals[160] > 3:
                                    out_laryngs += [160]

                                if mals[96] + mals[224] > 3:
                                    out_laryngs += [96, 224]

                                return out_laryngs

                        case _: # No labio-dental, retroflex, post-alveolar, or uvular clicks
                            if 160 in curr_laryngs: # curr_laryngs = [0, 32, 64, 128, 160]
                                if mals[192] > 3:
                                    return [192]

                            else:
                                out_laryngs = []
                                if mals[160] > 3:
                                    return [160]
                                
            case 6: # Add clicks in permitted places (curr_laryngs = [0, 32, 64, 128, 160, 192])
                if curr_place in [12, 10]:
                    if mals[192] > 3:
                        return [96, 224]
                    
                elif curr_place in [26, 19]:
                    if mals[96] + mals[224] > 3:
                        return [96, 224]

            case 7: # Add breathy feature (curr_laryngs = [0, 32, 64, 96, 128, 192, 224])
                if curr_place in [12, 10]:
                    if mals[32] > 3:
                        return [160]
                    
                else:
                    if mals[160] > 3:
                        return [160]

    return []