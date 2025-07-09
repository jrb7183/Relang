import json
import sys
import numpy as np
import pandas as pd

def consProb(base_prob):
    with open("data/consCorrespondences.json", "r", encoding="utf-8") as f:
        temp_dict = json.load(f)

    # Information about phonemes is stored in these parallel lists and then added to a Data Frame at once
    cons_list = []
    bin_list = []
    prob_list = []

    for cons in temp_dict:
        bin = int(temp_dict[cons], 16)
        temp_prob = base_prob

        # Place        Bilabial Labiodent Dental    Alveolar Retroflex Post-Alv Palatal  Velar    Uvular   Pharyngeal Glottal
        place_probs = {12: 0.15, 4: 0.07, 26: 0.03, 10: 0.18, 2: 0.05, 18: 0.1, 19: 0.1, 9: 0.14, 17: 0.07, 25: 0.01, 0: 0.1}
        place = bin & 31
        
        if place in place_probs:
            temp_prob += np.log(place_probs[place] / 2)
        
        else: # Coarticulated consonant
            front_bin = (bin & 4) or 2 # Fancy way of seeing if Labial or Coronal is the front-most place
            
            place = (bin - front_bin) & 31
            temp_prob += np.log(place_probs[place] / 2)

            place = ((bin >> 11) & 24) + front_bin
            temp_prob += np.log(place_probs[place] / 2)

        # Laryngeal Features Tenuis    Aspirated Ejective  Ten Click Voiced     Breathy     Implosive  Voiced Click
        laryng_probs =       {0: 0.28, 32: 0.24, 64: 0.16, 96: 0.01, 128: 0.24, 160: 0.025, 192: 0.04, 224: 0.005}
        laryng = bin & 224
        temp_prob += np.log(laryng_probs[laryng] / 8)

        # Sonorants
        if bin & 256 != 0:
            if bin & 128 == 0: # Unvoiced
                temp_prob += np.log(0.001)

        # Manner       Plosive   Affricate  Fricative   Sibilant   Nasal      Trill     Tap        Approximant
        manner_probs = {0: 0.2, 512: 0.04, 1024: 0.09, 1536: 0.12, 256: 0.19, 768: 0.12, 1280: 0.12, 1792: 0.12}
        manner = bin & 1792
        temp_prob += np.log(manner_probs[manner])

        # Laterals
        if bin & 2**12 != 0:
            if manner == 1792:
                temp_prob += np.log(0.5)
            else:
                temp_prob += np.log(0.1)


        # Add Phoneme Information to Lists
        cons_list += [cons]
        bin_list += [bin]
        prob_list += [temp_prob]
        

        # Nasalized Versions
        if manner != 256:
            if manner % 512 == 0:
                cons_list += ['ⁿ' + cons]
                bin_list += [bin + 2**11]
                prob_list += [temp_prob + np.log(0.0625)]

            else:
                cons_list += [cons + '̃']
                bin_list += [bin + 2**11]
                prob_list += [temp_prob + np.log(0.0625)]

        # Suprasegmentals
        suprs = ['ʷ', 'ʲ', 'ˠ', 'ˤ']
        for i in range(len(suprs)):
            cons_list += [cons + suprs[i]]
            bin_list += [bin + (i << 14)]
            prob_list += [temp_prob + np.log(0.0625 / (i + 16))]

    probs = pd.DataFrame(data={"Binary":bin_list, "Probability":prob_list, "Selected":False}, index=cons_list)
    return probs.sort_values(by="Probability", ascending=False)


def vowelProb(base_prob):
    with open("data/vowelCorrespondences.json", "r", encoding="utf-8") as f:
        temp_dict = json.load(f)

    # Information about phonemes is stored in these parallel lists and then added to a Data Frame at once
    vowel_list = []
    bin_list = []
    prob_list = []

    for vowel in temp_dict:
        bin = int(temp_dict[vowel], 16)
        temp_prob = base_prob

        # Fronting/Rounding F UnR   F R       C UnR   C R       B UnR   B R
        fr_probs =         {1: 0.3, 17: 0.15, 0: 0.1, 16: 0.05,	2: 0.1,	18: 0.3}
        fr = bin & 19
        temp_prob += np.log(fr_probs[fr] / 5)

        # Height/Tenseness H T      H L       MH T     MH L    LH T      LH L      L T   (No Low Lax in this representation)
        ht_probs =        {44: 0.25, 12: 0.1, 40: 0.1, 8: 0.15, 36: 0.12, 4: 0.03, 32: 0.25}
        ht = bin & 44
        temp_prob += np.log(ht_probs[ht])

        # Schwa Adjustment

        vowel_list += [vowel]
        bin_list += [bin]
        prob_list += [temp_prob]

    # Generate Diphthongs
    orig_count = len(vowel_list)
    for i in range(orig_count):
        for j in range(orig_count):
            if i != j:
                diph_bin = bin_list[i] + ((bin_list[j] & 63) << 10)

                vowel_list += [vowel_list[i] + vowel_list[j]]
                bin_list += [diph_bin]
                prob_list += [prob_list[i] + prob_list[j]]

        # Nasalized
        vowel_list += [vowel_list[i] + '̃']
        bin_list += [bin_list[i] + (1 << 7)]
        prob_list += [prob_list[i] + np.log(0.03)]

        # Voiceless, Breathy, and Rhotacized
        suprs = {'̥': 6, '̰': 8, '˞': 9}
        for supr in suprs:

            vowel_list += [vowel_list[i] + supr]
            bin_list += [bin_list[i] + (1 << suprs[supr])]
            prob_list += [prob_list[i] + np.log(0.005)]
    
    probs = pd.DataFrame(data={"Binary":bin_list, "Probability":prob_list, "Selected":False}, index=vowel_list)
    return probs.sort_values(by="Probability", ascending=False)





def calcBaseProb(cons: bool):
    base_prob = 0 # 100% in logprob

    if cons:
        # Load Consonants and Determine their Probabilities
        return consProb(base_prob)
    else:
        # Load Vowels and Determine their Probabilities
        return vowelProb(base_prob)


if __name__ == "__main__":
    val = sys.argv[1]
    limit = int(sys.argv[2])

    probs = calcBaseProb(val == "cons")
    print(probs[probs["Probability"] > limit])