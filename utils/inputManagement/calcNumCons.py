from random import randrange, random
import sys

"""
Based on the average size of the inputted phonologies, calculate a number of
consonants for the output phonology. Phonologies are separated into 8 categories:
Nonexistant (0), Unnaturalistically Small (1-7), Small (8-19), Medium (20-45), 
Large (46-59), Extra Large (60-84), Click Large (85-180), and Unnaturalistically Large (181+).
"""

def num_cons(phonologies: list[list]) -> int:
    # If no phonology entered, randomly pick naturalistic size
    if len(phonologies) == 0:
        return randrange(8, 60)
    
    # Calculate average size of phonologies
    size = 0
    for phonology in phonologies:
        size += len(phonology)

    size /= len(phonologies)

    # Randomly pick num consonants from range based on average size
    """
    1-7    => 20-60          : 0 => 1-3
    8-19   => 20-46          : 1 => 1-2
    20-45  => 8-20 | 46-60   : 2 => 0-1 | 2-3
    46-59  => 8-20           : 3 => 0-1
    60-84  => 8-46           : 4 => 0-2
    85-180 => 20-46          : 5 => 1-2
    181+   => 20-60          : 6 => 1-3
    """
    bounds = [8, 20, 46, 60, 85, 181]
    ubi = 0
    lbi = 0

    for i in range(len(bounds) + 1):
        if i == 6:
            return randrange(bounds[1], bounds[3])
        
        if size < bounds[i]:

            # Find the index of the upper and lower bounds to generate the number of consonants
            if not i % 5 or i == 1:
                lbi = 1

            if i & 4 or i < 2:
                ubi = 2
            else:
                ubi = i // 2

            if i % 3 == 0:
                ubi += 1

            # Small chance to get larger consonant inventory
            if i == 2 or i == 3:
                if random() < 0.001: # Non-click
                    return randrange(bounds[3], bounds[4])
                
                if random() < 0.005: # Click
                    return randrange(bounds[4], bounds[5])

            # Return num cons
            if i == 2:
                if randrange(0, 2):
                    return randrange(bounds[2], bounds[3])
                
                return randrange(bounds[lbi], bounds[ubi])
            
            return randrange(bounds[lbi], bounds[ubi])

    # Shouldn't reach here
    return 0
        
    
if __name__ == "__main__":
    lower = int(sys.argv[1])
    upper = int(sys.argv[2])

    phonologies = [ ["t" for _ in range(randrange(lower, upper))] for _ in range(30)]

    for _ in range(30):
        print(num_cons(phonologies), "\n")