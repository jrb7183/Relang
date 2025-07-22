from collections import Counter


def placeCriteria(curr_permit_len: int, sel_phonemes: list[list]) -> bool:
    places = Counter(map(lambda sel_phoneme: sel_phoneme[1] % 32, sel_phonemes))
    
    if curr_permit_len == 6:
        if places[12] + places[4] + places[9] + places[0] >= 3:
            return True
        
    else:
        if places[18] or places[19]:
            return True
        
    return False