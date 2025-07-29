import json
import sys

# Decodes consonants in IPA into binary
def consDecoder(phoneme, corresp_dict):
    temp = 0
    supr = ''
    coarticulate = ''
    err_helper = ''
    pre_err_helper = ''

    # Pre-nasalization
    if phoneme[0] == 'ⁿ':
        temp += 2**11
        pre_err_helper = phoneme[0]
        phoneme = phoneme[1:]

    # Nasalization
    if phoneme[-1] == '̃':
        temp += 2**11
        err_helper = phoneme[-1]
        phoneme = phoneme[:-1]

    # General Suprasegmental
    if phoneme[-1] in ['ʷ', 'ʲ', 'ˠ', 'ˤ']:
        temp += 2**13
        supr = phoneme[-1]
        err_helper = phoneme[-1] + err_helper
        phoneme = phoneme[:-1]

    # Phoneme Check
    if phoneme not in corresp_dict:
        
        # Coarticulated consonants
        if phoneme[0] in corresp_dict and phoneme[1:] in corresp_dict:
            coarticulate = phoneme[1:]
            phoneme = phoneme[0]

        elif phoneme[:2] in corresp_dict and phoneme[2:] in corresp_dict:
            coarticulate = phoneme[2:]
            phoneme = phoneme[:2]

        else:
            print(f"Phoneme {pre_err_helper + phoneme + err_helper} could not be found.")
            return -1

    temp += int(corresp_dict[phoneme], 16)
    if coarticulate:
        coart_bin = int(corresp_dict[coarticulate], 16)
        
        place = coart_bin & 7
        manner = (coart_bin >> 3) & 3
        laryng = (coart_bin >> 5) & 7

        temp |= place
        temp |= (manner << 14)
        temp |= (laryng << 5)

    # Specific Suprasegmental
    if supr:
        if supr == 'ʲ':
            temp |= (1 << 14)

        elif supr == 'ˠ':
            temp |= (1 << 15)

        elif supr == 'ˤ':
            temp |= (3 << 14)

    return temp


# Decodes vowels in IPA into binary
def vowelDecoder(phoneme, corresp_dict):
    temp = 0
    diphthong = ''
    err_helper = ''


    # Suprasegmentals
    if phoneme[-1] == '̥':
        err_helper = phoneme[-1]
        phoneme = phoneme[:-1]
        temp += 2**6

    elif phoneme[-1] == '̃':
        err_helper = phoneme[-1]
        phoneme = phoneme[:-1]
        temp += 2**7

    elif phoneme[-1] == '̤':
        err_helper = phoneme[-1]
        phoneme = phoneme[:-1]
        temp += 2**8

    elif phoneme[-1] == '˞':
        err_helper = phoneme[-1]
        phoneme = phoneme[:-1]
        temp += 2**9

    # Phoneme Check
    if phoneme not in corresp_dict:

        # Diphthongs
        if phoneme[0] in corresp_dict and phoneme[1:] in corresp_dict:
            diphthong = phoneme[1:]
            phoneme = phoneme[0]

        elif phoneme[:2] in corresp_dict and phoneme[2:] in corresp_dict:
            diphthong = phoneme[2:]
            phoneme = phoneme[:2]

        else:
            print(f"Phoneme {phoneme + err_helper} could not be found.")
            return -1


    temp += int(corresp_dict[phoneme], 16)
    if diphthong:
        diph_bin = int(corresp_dict[diphthong], 16)
        temp += (diph_bin << 10)

    return temp


""" Converts a phonology (input as a list of phonemes) into the appropriate binary representation
    with the correspondences.json file contains a list of IPA to hex correspondences. Any
    unrepresented suprasegmentals are made after binary conversion.
"""
def ipaToBinary(phonology, cons):
    corresp_dict = {}
    if cons:
        with open("../data/consCorrespondences.json", "r", encoding="utf-8") as f:
            corresp_dict = json.load(f)

    else:
        with open("../data/vowelCorrespondences.json", "r", encoding="utf-8") as f:
            corresp_dict = json.load(f)

    # Find phoneme and convert to hex
    temp = 0
    bin_phones = []
    for phoneme in phonology:
        

        # Consonant Case
        if cons:
            temp = consDecoder(phoneme, corresp_dict)

        # Vowel Case
        else:
            temp = vowelDecoder(phoneme, corresp_dict)

        if temp != -1:
            bin_phones += [temp]
            # print(f"{phoneme}: {bin(temp)}")

    return bin_phones


if __name__ == "__main__":
    val = sys.argv[1]
    if val == "cons":
        phonology = ["p", "t", "b", "d", "ɸ’", "β", "s", "zʱ", "ɹ", "ⱱ̟̊ʰ", "tʲ", "pʲ", "ⁿp", "ⁿpʲ", "m", "ⁿⁿp", "kp", "kpʰ", "t̪p", "f", "cç", "ɦ", "w"]
        val = True
    else:
        phonology = ["a", "ʊ", "ɯ̞", "ø", "e", "ẽ", "e̥", "e̤", "e˞", "ẽ̥", "ai", "au", "ø̞y"]
        val = False

    ipaToBinary(phonology, val)