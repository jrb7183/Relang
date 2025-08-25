from collections import Counter

""" Helper function for laryngealCriteria. Handles laryngeal criteria for plosives"""

def plosiveLaryngeals(curr_laryngs: list[int], curr_num_laryngs: int, curr_place: int, mals: Counter, num_phonemes: int) -> list[int]:
    match curr_num_laryngs:
        case 1: # Add aspirated and voiced features
            if curr_place in [12, 10, 9]:
                return [32, 128]

            if curr_place != 0:
                if mals[128] > 2 and curr_place != 25:
                    if mals[32] > 2:
                        return [32, 128]

                    return [128]
                
                if mals[32] > 2:
                    return [32]
            
        case 2: # Add ejective features to pharyngeal plosives (curr_laryngs = [0, 32] or [0, 128])
            if curr_place == 25:
                if mals[64] > 8:
                    return [64]
            
            else:
                if 32 in curr_laryngs:
                    if mals[128] > 2:
                        return [128]
                    
                else:
                    if mals[32] > 2:
                        return [32]

        case 3: # Ignore pharyngeals; add breathy, ejective, and/or implosive features (curr_laryngs = [0, 32, 128])
            if curr_place != 25:
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
                            out_laryngs += [192]

                        return out_laryngs
                            
        case 4: # Add breathy and/or implosive features 
                if curr_place in [12, 10, 9]: # (curr_laryngs = [0, 32, 64, 128])
                    
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
                            
        case 5: # Add breathy, implosives, and/or clicks (curr_laryngs = [0, 32, 64, 128, 160] or [0, 32, 64, 128, 192])
            match curr_place:

                # Bilabial, alveolar, and velar places will only have curr_laryngs = [0, 32, 64, 128, 192]
                case 12 | 10:
                    if mals[192] > 3 and num_phonemes > 84:
                        if mals[32] > 3:
                            return [96, 160, 224]

                        return [96, 224]
                    
                case 9: # No velar clicks
                    if mals[32] > 3:
                        return [160]
                
                case 26 | 19:
                    if 160 in curr_laryngs: # curr_laryngs = [0, 32, 64, 128, 160]
                        if mals[192] > 3 and num_phonemes > 84:
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
            if curr_place in [12, 26, 10, 19]:
                if mals[192] > 3 and num_phonemes > 84:
                    return [96, 224]

        case 7: # Add breathy feature (curr_laryngs = [0, 32, 64, 96, 128, 192, 224])
            if (curr_place in [12, 10] and mals[32] > 3) or mals[160] > 3:
                return [160]

    return []