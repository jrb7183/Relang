"""
Removes selected phonemes from the pool of currently permitted phonemes,
preventing repeated selections from occuring. 

The function does permit already selected phonemes to reappear
after a inventory size-based number of phonemes have been selected so 
that suprasegmentals have the possibility of being added. 
"""
def removeSelected(curr_permit: dict[int, dict[int, list[int]]], sel_phonemes: list[tuple], total_phonemes: int, max_stops: int) -> dict[int, dict[int, list[int]]]:
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

            # THERE'S SOME REALLY RARE EDGE CASE WHERE NEW_PERMIT[PLACE] DOESN'T CONTAIN MANNER
            # PROBABLY SHOULD LOOK INTO IT
            if place in new_permit and manner in new_permit[place]:
                laryngs = new_permit[place][manner]
                spot = laryngs.index(laryng)
                laryngs.pop(spot)

                if len(laryngs) == 0:
                    del new_permit[place][manner]

                    if len(new_permit[place].keys()) == 0:
                        del new_permit[place]

    # If max stops has been reached, no stops should be permitted
    if max_stops < 1:
        places = list(new_permit.keys())
        for place in places:

            if 0 in new_permit[place]:
                del new_permit[place][0]
            
            if 256 in new_permit[place]:
                del new_permit[place][256]

            if place == 18 and 512 in new_permit[place]:
                del new_permit[place][0]

            if len(new_permit[place].keys()) == 0:
                del new_permit[place]

    return new_permit

