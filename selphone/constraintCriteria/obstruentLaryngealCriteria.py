from collections import Counter

""" Helper function for laryngealCriteria. Handles laryngeal criteria for non-plosive obstruents"""

def npObstruentLaryngeals(curr_laryngs: list[int], curr_num_laryngs: int, curr_manner: int, curr_place: int, mals: Counter, pals: Counter) -> list[int]:
    match curr_num_laryngs:
        case 1: # Add aspirated and voiced features
            if curr_place == 25 and curr_manner == 512:
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
            
        case 2: # Add ejective features to pharyngeal affricates (curr_laryngs = [0, 32] or [0, 128])
            if curr_place == 25 and curr_manner == 512:
                if mals[64] > 8:
                    return [64]
                    
            elif curr_place != 0:
                if 32 in curr_laryngs:
                    if mals[128] > 2 and pals[128 + curr_place] > 1:
                        return [128]
                    
                else:
                    if mals[32] > 2 and pals[32 + curr_place] > 1:
                        return [32]

        case 3: # Add breathy, ejective, and/or implosive features (curr_laryngs = [0, 32, 128])
            if curr_place != 25 or curr_manner == 1024:      
                if curr_manner != 512: # Continuant
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
                    
                else: # Affricate
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
                        
        case 4: # Add breathy and/or ejective features (curr_laryngs = [0, 32, 64, 128] or [0, 32, 128, 160])
            if curr_manner != 512: # Continuant 
                out_laryng = 64
                if 64 in curr_laryngs:
                    out_laryng = 160

                if curr_place in [12, 10, 9]:

                    if mals[out_laryng] > 2:
                        return [out_laryng]
                    
                else:                             
                    if mals[out_laryng + 1024] + mals[out_laryng + 1536] > 1 and pals[out_laryng + curr_place] > 0:
                        return [out_laryng]
                    
            else: # Affricate
                out_laryng = 64
                if 64 in curr_laryngs:
                    out_laryng = 160

                if curr_place in [12, 10, 9]:

                    if mals[out_laryng + 1024] + mals[out_laryng + 1536] > 1:
                        return [out_laryng]
                    
                else:                             
                    if mals[out_laryng + 512] > 1 and pals[out_laryng + curr_place] > 1:
                        return [out_laryng]
                    
    return []