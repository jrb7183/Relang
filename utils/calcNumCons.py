from random import randrange
import sys

"""
Based on the average size of the inputted phonologies, calculate a number of
consonants for the output phonology. Phonologies are separated into 7 categories:
Nonexistant (0), Unnaturalistically Small (1-7), Small (8-19), Medium (20-45), 
Large (46-84), Click Large (85-180), and Unnaturalistically Large (181+).
"""

def numCons(phonologies: list[list]) -> int:
    # If no phonology entered, randomly pick naturalistic size
    if len(phonologies) == 0:
        return randrange(8, 181)
    
    # Calculate average size of phonologies
    size = 0
    for phonology in phonologies:
        size += len(phonology)

    size /= len(phonologies)

    # Randomly pick num consonants from range based on average size
    """
    1-7    > 46-181 : 0 > 2-4
    8-19   > 46-85  : 1 > 2-3
    20-45  > 85-181 : 2 > 3-4
    46-84  > 8-20   : 3 > 0-1
    85-180 > 20-46  : 4 > 1-2
    181+   > 20-85  : 5 > 1-3
    """
    bounds = [8, 20, 46, 85, 181]
    ubi = 0

    for i in range(len(bounds) + 1):
        if i == 5:
            return randrange(bounds[1], bounds[3])
        
        if size < bounds[i]:

            # Find the index of the upper bound to generate the number of consonants
            ubi = 4 - i
            if i and i % 2 == 0:
                ubi += 2

            if i:
                return randrange(bounds[ubi - 1], bounds[ubi])
            
            return randrange(bounds[ubi - 2], bounds[ubi])

    # Shouldn't reach here
    return 0
        
    
if __name__ == "__main__":
    lower = int(sys.argv[1])
    upper = int(sys.argv[2])

    phonologies = [ ["t" for _ in range(randrange(lower, upper))] for _ in range(30)]

    for _ in range(30):
        print(numCons(phonologies), "\n")