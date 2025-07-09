import random
import sys
from collections import Counter

sys.path.append(".")
from old_files.phoneProb import calcBaseProb
from utils.phoneLinkedList import PhonemeList

def adjustProb(phonemes: PhonemeList, sel_bin, laryngs, num_types):
    curr_phone = phonemes.getHead()
    
    for _ in range(phonemes.getCount()):
        curr_bin = curr_phone.getBin()
        curr_prob = curr_phone.getProb()

        # Get Bin Segments Helpful for Modding Probs
        sel_place = sel_bin % 32
        curr_place = curr_bin % 32

        sel_major_place = sel_bin % 8
        curr_major_place = curr_bin % 8

        sel_son = (sel_bin >> 8) % 2
        curr_son = (curr_bin >> 8) % 2

        sel_manner = (sel_bin >> 8) % 8
        curr_manner = (curr_bin >> 8) % 8

        sel_suprs = (sel_bin >> 11) % 32
        curr_suprs = (curr_bin >> 11) % 32

        # Place (make consonants in current place more likely, and makes consonants in nearby places less likely)
        if sel_place != curr_place:
            curr_prob -= 0.001

            if sel_major_place == curr_major_place:
                curr_prob -= 0.003

        # Laryngeal features
        curr_laryng = (curr_bin >> 5) % 8
        if len(laryngs) >= 2 and not (curr_son == 1 or curr_laryng == 8):

            if curr_laryng not in laryngs:
                curr_prob -= 0.09 * len(laryngs)
        
        # Manner
        if sel_manner != curr_manner:
            curr_prob -= 0.0007

            if sel_place == curr_place and sel_manner & 5 == 4 and curr_manner & 5 == 4: # Prevent occurrence of fricatives and sibilants of the same place
                curr_prob -= 10
                
        if sel_manner == 1 and curr_manner == 1: # Nasal
            curr_prob -= 0.1 * (num_types["nasals"] - 1)

        # Suprs/Coarts
        if sel_suprs != curr_suprs:
            curr_prob -= 0.1

        # Sonorance (If previous consonant was an obstruent, favor sonorants and vice versa)
        if sel_son == curr_son:
            if sel_son == 0: # Last consonant picked was an obstruent
                curr_prob -= 0.001

            else: # Last consonant picked was an sonorant
                curr_prob -= 0.01

        phonemes.modNodeProb(curr_bin, curr_prob)
        curr_phone = curr_phone.getNext()

    return


""" 
Takes in the probabilities for every phoneme and returns a list of length
num_phones. When selecting each phoneme, the most probable one is considered,
and then, based on temp, phonemes up to a certain lower probability are also
considered. Next, one of these phonemes are randomly selected, and every 
other phoneme's probability is adjusted based on the selection.
"""
def selectPhonemes(phonemes: PhonemeList, num_phones, temp):
    selected_phones = []
    laryngs = set()
    num_types = Counter()
    for _ in range(num_phones):
        sel_phone_list = []

        # Choose phonemes to select from
        head = phonemes.getHead()
        tail = phonemes.getTail()

        prob_range = abs(head.getProb() - tail.getProb())
        min_prob = head.getProb() - (prob_range * temp)

        sel_phone_list = [head]
        curr_phone = head.getNext()

        while curr_phone.getProb() >= min_prob:
            sel_phone_list += [curr_phone]
            curr_phone = curr_phone.getNext()

            if not curr_phone:
                break

        # print(sel_phone_list)
        # print()

        # Randomly select phoneme from sel_phone_list
        pick = sel_phone_list[random.randint(0, len(sel_phone_list) - 1)]
        selected_phones += [pick.getPhoneme()]

        # Adjust probabilities based on selected phoneme
        sel_bin = pick.getBin()
        phonemes.removeNode(sel_bin)

        if (sel_bin >> 8) % 2 == 0:
            laryngs.add((sel_bin >> 5) % 8)

        if (sel_bin >> 8) % 8 == 1:
            num_types["nasals"] += 1

        adjustProb(phonemes, sel_bin, laryngs, num_types)
        
    return selected_phones


if __name__ == "__main__":
    num = int(sys.argv[1])
    temp = float(sys.argv[2])

    probs = calcBaseProb(True)
    sel_phones = selectPhonemes(probs, num, temp)
    for i in range(len(sel_phones)):
        print(f"{i+1}. {sel_phones[i]}")