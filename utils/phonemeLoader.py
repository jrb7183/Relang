import json
import sys
from pandas import DataFrame

def loadCons():
    with open("../data/consCorrespondences.json", "r", encoding="utf-8") as f:
        temp_dict = json.load(f)

    # Information about phonemes is stored in these parallel lists and then added to a Data Frame at once
    cons_list = []
    bin_list = []

    for cons in temp_dict:
        bin = int(temp_dict[cons], 16)
        
        # Add Phoneme Information to Lists
        cons_list += [cons]
        bin_list += [bin]

        # Nasalized Versions
        manner = bin & 1792
        if manner != 256:
            if manner % 512 == 0:
                cons_list += ['ⁿ' + cons]
                bin_list += [bin + 2**11]

            else:
                cons_list += [cons + '̃']
                bin_list += [bin + 2**11]

        # Suprasegmentals
        suprs = ['ʷ', 'ʲ', 'ˠ', 'ˤ']
        for i in range(len(suprs)):
            cons_list += [cons + suprs[i]]
            bin_list += [bin + (i << 14) + (1 << 13)]

    cons = DataFrame(data={"Phoneme":cons_list, "Selected":False}, index=bin_list)
    return cons.sort_index()


def loadVowels():
    with open("../data/vowelCorrespondences.json", "r", encoding="utf-8") as f:
        temp_dict = json.load(f)

    # Information about phonemes is stored in these parallel lists and then added to a Data Frame at once
    vowel_list = []
    bin_list = []

    for vowel in temp_dict:
        bin = int(temp_dict[vowel], 16)

        vowel_list += [vowel]
        bin_list += [bin]

    orig_count = len(vowel_list)
    for i in range(orig_count):

        # Generate Diphthongs
        for j in range(orig_count):
            if i != j:
                diph_bin = bin_list[i] + ((bin_list[j] & 63) << 10)

                vowel_list += [vowel_list[i] + vowel_list[j]]
                bin_list += [diph_bin]

        # Nasalized
        vowel_list += [vowel_list[i] + '̃']
        bin_list += [bin_list[i] + (1 << 7)]

        # Voiceless, Breathy, and Rhotacized
        suprs = {'̥': 6, '̰': 8, '˞': 9}
        for supr in suprs:
            vowel_list += [vowel_list[i] + supr]
            bin_list += [bin_list[i] + (1 << suprs[supr])]
    
    vowels = DataFrame(data={"Phoneme":vowel_list, "Selected":False}, index=bin_list)
    return vowels.sort_index()





def loadPhonemes(cons: bool):
    if cons:
        # Load Consonants and Determine their Probabilities
        return loadCons()
    else:
        # Load Vowels and Determine their Probabilities
        return loadVowels()


if __name__ == "__main__":
    val = sys.argv[1]
    # limit = int(sys.argv[2])

    phonemes = loadPhonemes(val == "cons")
    print(phonemes)