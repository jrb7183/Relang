    
"""
Deals with common exceptions to the heirarchical feature constraints, mainly consisting
of restrictions on the co-occurrence of consonants with the same manner in neighboring
places.
"""
def manageExceptions(place: int, manner: int, curr_permit: dict[int, dict[int, list[int]]], manners: list[int], num_phonemes: int) -> dict[int, dict[int, list[int]]]:
    # Bilabial and labiodental consonants of the same manner should not co-occur (for the purposes of this model)
    if place % 8 == 4:
        opp_place = place ^ 8 # Bilabial and labiodental places are differentiated by their 4th bit
        if manner in curr_permit[opp_place]:
            del curr_permit[opp_place][manner]

        # Allow initial possibility of fricatives, taps, trills, and approximants in either place (all are currently added at once so check only needs to look for one)
        if 1024 in manners:
            for new_manner in manners:
                if new_manner == 1024:
                    curr_permit[opp_place][new_manner] = [0]
                else:
                    curr_permit[opp_place][new_manner] = [128]

    # Post-alveolar and palatal consonants should not co-occur (except palatal nasals and approximants can appear with post-alveolar consonants)
    if place & 30 == 18:
        opp_place = place ^ 1 # Post-alveolar and palatal places are differentiated by their 1st bit
        if opp_place in curr_permit and (0 in curr_permit[opp_place] or 512 in curr_permit[opp_place]):
            del curr_permit[opp_place]

        if place == 18: 
            if 256 in manners:
                curr_permit[19][256] = [128]

            if 1792 in manners:
                curr_permit[19][1792] = [128]

    # Dental and alveolar consonants of the same manner should not co-occur (for the purposes of this model)
    if place % 16 == 10:
        opp_place = place ^ 16 # Dental and alveolar places are differentiated by their 5th bit
        if opp_place in curr_permit:

            if manner in curr_permit[opp_place] and num_phonemes < max(37, num_phonemes * 2 // 3):
                del curr_permit[opp_place][manner]

            # Allow initial possibility of sibilant fricatives, taps, trills, and approximants in alveolar place (all are currently added at once so check only needs to look for one)
            if 1024 in manners:
                for new_manner in manners:
                    if new_manner == 1024:
                        curr_permit[opp_place][1536] = [0]
                    else:
                        curr_permit[opp_place][new_manner] = [128]

            # Allow initial possibility of non-sibilant fricatives in dental place
            if 1536 in manners:
                curr_permit[opp_place][1024] = [0]

    return curr_permit