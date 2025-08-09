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
    
    match curr_num_places:
        case 2: # Add velar, glottal, and both labial places
            return [12, 4, 9, 0]
        
        case 6: # Add post-alveolar and palatal places
            if places[12] + places[4] + places[9] + places[0] >= 3:
                return [18, 19]
        
        case 8: # Add retroflex, uvular, and pharyngeal places
            if places[18] or places[19]:
                return [2, 17, 25]
        
    return []