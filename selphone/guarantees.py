from typing import Generator

# Retroactively find consonants that would have triggered guarantees
# and apply them in the context of the current phoneme
def applyRetroGuarantees(curr_place: int, curr_manner: int, curr_laryng: int, curr_lat: int, sel_phonemes: list[tuple]):
    for phoneme in sel_phonemes:
        
        # Laryngeal and nasalization guarantees
        supr = phoneme[1] & (1 << 11) + phoneme[1] & (7 << 13)
        if supr < (1 << 12):

            manner = phoneme[1] & (7 << 8)
            if manner == curr_manner:

                place = phoneme[1] & 31
                laryng = phoneme[1] & (7 << 5)
                if not (place == curr_place or laryng == curr_laryng):

                    yield curr_place + laryng + curr_manner + curr_lat + supr

        # Other suprasegmental guarantees
        else:
            place = phoneme[1] & 31
            if place == curr_place:

                manner = phoneme[1] & (7 << 8)
                laryng = phoneme[1] & (7 << 5)

                if not (manner == curr_manner and laryng == curr_laryng):
                    yield curr_place + curr_laryng + curr_manner + curr_lat + supr


# Selects potential candidates for place and manner of guaranteed
def pickCandidates(curr_place: int, curr_manner: int, curr_laryng: int, curr_supr: int, sel_phonemes: list[tuple]) -> Generator:
    for phoneme in sel_phonemes:
        
        # Laryngeal and nasalization guarantees
        if curr_supr < (1 << 12):
            manner = phoneme[1] & (7 << 8)
            if manner == curr_manner:

                place = phoneme[1] & 31
                if place != curr_place:

                    lat = phoneme[1] & (1 << 12)
                    yield place + curr_laryng + manner + lat + curr_supr

        # Other suprasegmental guarantees
        else:
            place = phoneme[1] & 31
            if place == curr_place:

                manner = phoneme[1] & (7 << 8)
                laryng = phoneme[1] & (7 << 5)

                if not (manner == curr_manner and laryng == curr_laryng):
                    lat = phoneme[1] & (1 << 12)
                    yield place + laryng + manner + lat + curr_supr

                
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
    candidates = []
    curr_phoneme = sel_phonemes[-1][1]

    # Check if guarantees are applicable
    curr_place = curr_phoneme % 32
    curr_manner = curr_phoneme & (7 << 8)
    curr_laryng = curr_phoneme & (7 << 5)
    curr_nasal = curr_phoneme & (1 << 11)
    curr_lat = curr_phoneme & (1 << 12)
    curr_suprs = curr_phoneme & (7 << 13)
    curr_son = curr_phoneme & (1 << 8)

    candidates = list(set(applyRetroGuarantees(curr_place, curr_manner, curr_laryng, curr_lat, sel_phonemes)))

    if ((curr_laryng == 128 and curr_son) or not (curr_laryng or curr_son)) and not (curr_nasal or curr_suprs):
        return candidates

    if curr_laryng or curr_son: # Laryngeal Feature Guarantees
        candidates += list(set(pickCandidates(curr_place, curr_manner, curr_laryng, 0, sel_phonemes)))

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

    sps = [('p', 12), ('t', 10), ('k', 9), ('s', 1546), ('d', 138), ('ⁿt', 2058), ('l', 6026), ('dʲ', 24714)]
    print(manageGuarantees(sps))

    sps = [('p', 12), ('t', 10), ('m', 393), ('n', 394), ('n̥', 266)]
    print(manageGuarantees(sps))

    sps = [('p', 12), ('t', 10), ('k', 9), ('s', 1546), ('d', 138), ('ⁿt', 2058), ('l', 6026), ('dʲ', 24714), ('ʈ', 2)]
    print(manageGuarantees(sps))