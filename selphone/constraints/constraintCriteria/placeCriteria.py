from collections import Counter

"""
This criteria function helps determine how to update the current constraints for the
phoneme selector. Based on the phonemes in the selected phoneme list, and the current
number of places, they check which criteria are met. If any are, then they return the
corresponding places.
"""

# Determines which places to add to the constraints
def placeCriteria(curr_num_places: int, sel_phonemes: list[list]) -> list[int]:
    places = Counter(map(lambda sel_phoneme: sel_phoneme[1] % 32, sel_phonemes))
    manners = Counter(map(lambda sel_phoneme: (sel_phoneme[1] & (7 << 8)) % 2048, sel_phonemes))

    match curr_num_places:
        case 1: # Add velar, glottal, and both labial places
            return [12, 4, 9, 0]
        
        case 5: # Add post-alveolar and palatal places
            if places[12] + places[4] + places[9] + places[0] >= 3:
                return [18, 19]
        
        case 7: # Add retroflex and uvular places
            if places[18] or places[19]:
                return [26, 2, 17]
        
        # RIGHT NOW WHEN A PALATAL OR POST-ALVEOLAR CONSONANT OCCURS, THE OTHER PLACE IS PURGED FROM CONSTRAINTS, LEAVING 9 PLACES
        # IF DECIDE TO INCORPORATE CONSTRAINT EXCEPTIONS INTO CONSTRAINT LIMITS, CHANGE CASE BELOW TO 10
        case 9 if manners[1024] + manners[1536] > 8: # Add pharyngeal place
            return [25]
        
    return []