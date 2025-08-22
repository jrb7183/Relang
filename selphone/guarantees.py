from typing import Generator


# Selects potential candidates for place and manner of guaranteed
def pickCandidates(curr_place: int, curr_manner: int, curr_laryng: int, curr_supr: int, sel_phonemes: list[tuple]) -> Generator:
    for phoneme in sel_phonemes:
        
        # Laryngeal and nasalization guarantees
        if curr_supr < (1 << 12):
            manner = phoneme[1] & (7 << 8)
            if manner == curr_manner:

                place = phoneme[1] & 31
                if place != curr_place:
                    yield place + curr_laryng + manner + curr_supr

        # Other suprasegmental guarantees
        else:
            place = phoneme[1] & 31
            if place == curr_place:

                manner = phoneme[1] & (7 << 8)
                laryng = phoneme[1] & (7 << 5)

                if not (manner == curr_manner and laryng == curr_laryng):    
                    yield place + laryng + manner + curr_supr

                
"""
Creates guarantees for Phoneme Selector based on selected phonemes. When a 
non-tenuis phoneme of a given manner is selected, manageGuarantees finds
all of places where tenuis phonemes of that manner are selected. Then, it 
creates a list of all the phonemes at those places with the same manner and
laryngeal features for guarantees.

The same process occurs for nasals and other suprasegmentals, although the
other suprasegmentals guarantees will apply to phonemes of the same place
and different manners instead.
"""
def manageGuarantees(sel_phonemes: list[tuple]) -> list:
    curr_phoneme = sel_phonemes[-1][1]

    # Check if guarantees are applicable
    curr_laryng = curr_phoneme & (7 << 5)
    curr_nasal = curr_phoneme & (1 << 11)
    curr_suprs = curr_phoneme & (7 << 13)

    if not (curr_laryng or curr_nasal or curr_suprs):
        return []
    
    curr_place = curr_phoneme % 32
    curr_manner = curr_phoneme & (7 << 8)
    candidates = []

    if curr_laryng: # Laryngeal Feature Guarantees
        candidates = list(set(pickCandidates(curr_place, curr_manner, curr_laryng, 0, sel_phonemes)))

    if curr_nasal: # Nasalization Guarantees
        candidates += list(set(pickCandidates(curr_place, curr_manner, curr_laryng, curr_nasal, sel_phonemes)))

    if curr_suprs: # Other Suprasegmental Guarantees
        candidates += list(set(pickCandidates(curr_place, curr_manner, curr_laryng, curr_suprs, sel_phonemes)))

    # Filter out any phonemes that are already selected
    for phoneme in sel_phonemes:
        if phoneme[1] in candidates:
            candidates.pop(candidates.index(phoneme[1]))

    return candidates


if __name__ == "__main__":
    sps = [('p', 12), ('t', 10), ('k', 9), ('s', 1546), ('d', 138)]
    print(manageGuarantees(sps))

    sps = [('p', 12), ('t', 10), ('k', 9), ('s', 1546), ('b', 140), ('d', 138), ('g', 137)]
    print(manageGuarantees(sps))

    sps = [('p', 12), ('t', 10), ('k', 9), ('s', 1546), ('d', 138), ('ⁿt', 2058)]
    print(manageGuarantees(sps))

    sps = [('p', 12), ('t', 10), ('k', 9), ('s', 1546), ('d', 138), ('ⁿt', 2058), ('tʲ', 24586)]
    print(manageGuarantees(sps))

    sps = [('p', 12), ('t', 10), ('k', 9), ('s', 1546), ('d', 138), ('ⁿt', 2058), ('dʲ', 24714)]
    print(manageGuarantees(sps))