from collections import Counter

# Calculates average occurrences of types of a given feature in a sound inventory
def averager(phonology: list[int], feature: int, averages: dict[int, int]) -> dict[int, float]:
    feature_cats = Counter()
    
    for phoneme in phonology:
        if feature != (7 << 13) or phoneme & (1 << 13) != 0:
            feature_cats[phoneme & feature] += 1
        
        else:
            feature_cats[0] += 1
            

    for cat in feature_cats:
        if cat in averages:
            averages[cat] += feature_cats[cat] / feature_cats.total()
        
        else:
            averages[cat] = feature_cats[cat] / feature_cats.total()

    return averages


# Normalize averages based on unrepresented categories to get more applicable values
def normalizer(averages: dict[int, int], probs: list[list[int, float]]) -> dict[int, int]:
    norm = 0

    # Find categories of feature represented in averages and add their probability to the norm val
    for prob in probs:
        if prob[0] in averages:
            norm += prob[1]

    # Apply the norm val to all the averages
    for cat in averages:
        averages[cat] *= norm

    return averages


    