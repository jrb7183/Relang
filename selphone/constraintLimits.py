"""
Removes selected phonemes from the pool of currently permitted phonemes,
preventing repeated selections from occuring. 

The function does permit already selected phonemes to reappear
after a inventory size-based number of phonemes have been selected so 
that suprasegmentals have the possibility of being added. 
"""
def removeSelected(curr_permit: dict[int, dict[int, list[int]]], sel_phonemes: list[tuple], total_phonemes: int) -> dict[int, dict[int, list[int]]]:
    new_permit = {}
    
    # Deal with making a deep copy of original dict here
    for place in curr_permit:
        new_permit[place] = {}

        for manner in curr_permit[place]:
            new_permit[place][manner] = curr_permit[place][manner] + []

    reappear_num = total_phonemes * 3 // 5

    for i in range(len(sel_phonemes)):
        if i < len(sel_phonemes) - reappear_num:
            phoneme_bin = sel_phonemes[i][1]

            # Ignore consonants with suprasegmentals/nasalization/lateralization
            if phoneme_bin & (31 << 11) != 0:
                continue

            place = phoneme_bin & 31
            manner = phoneme_bin & (7 << 8)
            laryng = phoneme_bin & (7 << 5)

            laryngs = new_permit[place][manner]
            spot = laryngs.index(laryng)
            laryngs.pop(spot)

            if len(laryngs) == 0:
                del new_permit[place][manner]

                if len(new_permit[place].keys()) == 0:
                    del new_permit[place]

    return new_permit

