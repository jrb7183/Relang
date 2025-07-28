
# Determines if current phoneme is a rhotic
def isRhotic(phoneme_bin: int) -> bool:
    major_place = phoneme_bin & 7
    manner = phoneme_bin & (7 << 8)

    if manner % 512 == 256:
        if ((manner >> 9) & 1) ^ (manner >> 10):
            return True
        
        if manner != 256 and major_place == 2:
            is_lateral = (phoneme_bin >> 12) & 1
            
            if not is_lateral:
                return True

    return False

# Determines if a phonology has its max number of rhotics, and, if so, remmoves possibility of manners that are specifically rhotic (taps and trills)
def removeRhotics(sel_phonemes: list[list[str, int]], num_phonemes: int, curr_permit: dict[int, dict[int, list[int]]]) -> list[dict[int, dict[int, list[int]]], bool]:
    curr_rhotics = set()
    removed_rhotics = False

    for phoneme in sel_phonemes:
        if isRhotic(phoneme[1]):
            curr_rhotics.add(phoneme[1] & ((7 << 8) + 31)) # Ignore laryngeals + suprasegmentals

    if len(curr_rhotics) >= (num_phonemes // 50 + 1):
        removed_rhotics = True
        for place in curr_permit:
            if 768 in curr_permit[place]:
                if (place + 768) not in curr_rhotics:
                    del curr_permit[place][768]

            if 1280 in curr_permit[place]:
                if (place + 1280) not in curr_rhotics:
                    del curr_permit[place][1280]

    return [curr_permit, removed_rhotics]