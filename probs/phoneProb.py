import json
import math
import sys

sys.path.append(".")
import utils.phoneLinkedList as PLL

def consProb(base_prob, prob_list = PLL.PhonemeList):
    with open("data/consCorrespondences.json", "r", encoding="utf-8") as f:
        temp_dict = json.load(f)

    for cons in temp_dict:
        bin = int(temp_dict[cons], 16)
        temp_prob = base_prob

        # Place        Bilabial Labiodent Dental    Alveolar Retroflex Post-Alv Palatal  Velar    Uvular   Pharyngeal Glottal
        place_probs = {12: 0.15, 4: 0.07, 26: 0.03, 10: 0.18, 2: 0.05, 18: 0.1, 19: 0.1, 9: 0.14, 17: 0.07, 25: 0.01, 0: 0.1}
        place = bin & 31
        
        if place in place_probs:
            temp_prob += math.log(place_probs[place])
        
        else: # Coarticulated consonant
            front_bin = (bin & 4) or 2 # Fancy way of seeing if Labial or Coronal is the front-most place
            
            place = (bin - front_bin) & 31
            temp_prob += math.log(place_probs[place])

            place = ((bin >> 11) & 24) + front_bin
            temp_prob += math.log(place_probs[place])

        # Laryngeal Features Tenuis    Aspirated Ejective  Ten Click Voiced     Breathy     Implosive  Voiced Click
        laryng_probs =       {0: 0.28, 32: 0.24, 64: 0.16, 96: 0.01, 128: 0.24, 160: 0.025, 192: 0.04, 224: 0.005}
        laryng = bin & 224
        temp_prob += math.log(laryng_probs[laryng])

        # Sonorants
        if bin & 256 != 0:
            if bin & 128 == 0: # Unvoiced
                temp_prob += math.log(0.001)

            else: # Voiced
                temp_prob += math.log(0.999)

        # Manner       Plosive   Affricate  Fricative   Sibilant   Nasal      Trill     Tap        Approximant
        manner_probs = {0: 0.2, 512: 0.04, 1024: 0.09, 1536: 0.12, 256: 0.19, 768: 0.12, 1280: 0.12, 1792: 0.12}
        manner = bin & 1792
        temp_prob += math.log(manner_probs[manner])

        # Laterals
        if manner != 1792: # Ignore Approximants
            if bin & 2**12 != 0:
                temp_prob += math.log(0.1)
            else:
                temp_prob += math.log(0.9)


        prob_list.addNode(cons, bin, temp_prob + math.log(0.8607))

        # Nasalized Versions
        if manner != 256:
            if manner % 512 == 0:
                prob_list.addNode('ⁿ' + cons, bin + 2**11, temp_prob + math.log(0.0625))

            else:
                prob_list.addNode(cons + '̃', bin + 2**11, temp_prob + math.log(0.0625))

        # Suprasegmentals
        suprs = ['ʷ', 'ʲ', 'ˠ', 'ˤ']
        for i in range(len(suprs)):
            prob_list.addNode(cons + suprs[i], bin + (i << 14), temp_prob + math.log(0.0625 / (i + 16)))            

    return


def vowelProb(base_prob, prob_list = PLL.PhonemeList):
    with open("data/vowelCorrespondences.json", "r", encoding="utf-8") as f:
        temp_dict = json.load(f)

    for vowel in temp_dict:
        bin = int(temp_dict[vowel], 16)
        temp_prob = base_prob

        # Fronting/Rounding F UnR   F R       C UnR   C R       B UnR   B R
        fr_probs =         {1: 0.3, 17: 0.15, 0: 0.1, 16: 0.05,	2: 0.1,	18: 0.3}
        fr = bin & 19
        temp_prob += math.log(fr_probs[fr] / 5)

        # Height/Tenseness H T      H L       MH T     MH L    LH T      LH L      L T   (No Low Lax in this representation)
        ht_probs =        {44: 0.25, 12: 0.1, 40: 0.1, 8: 0.15, 36: 0.12, 4: 0.03, 32: 0.25}
        ht = bin & 44
        temp_prob += math.log(ht_probs[ht])

        # Schwa Adjustment

        prob_list.addNode(vowel, bin, temp_prob + math.log(0.955))

    vowel = prob_list.getHead()
    orig_count = prob_list.getCount()
    for _ in range(orig_count):
        temp_prob = vowel.getProb() - math.log(0.955)

        offglide = prob_list.getHead()
        for _ in range(orig_count):
            if not vowel.compareNode(offglide):

                diph_bin = vowel.getBin() + ((offglide.getBin() & 63) << 10)
                prob_list.addNode(vowel.getPhoneme() + offglide.getPhoneme(), diph_bin, vowel.getProb() + offglide.getProb())

            offglide = offglide.getNext()

        # Nasalized
        prob_list.addNode(vowel.getPhoneme() + '̃', bin + (1 << 7), vowel.getProb() + math.log(0.03))

        # Voiceless, Breathy, and Rhotacized
        suprs = {'̥': 6, '̰': 8, '˞': 9}
        for supr in suprs:
            prob_list.addNode(vowel.getPhoneme() + supr, bin + (1 << suprs[supr]), vowel.getProb() + math.log(0.005))

        vowel = vowel.getNext()
    
    return


def calcBaseProb(cons: bool):
    base_prob = 0 # 100% in logprob
    probs = PLL.PhonemeList()

    if cons:
        # Load Consonants and Determine their Probabilities
        consProb(base_prob, probs)

    else:
        # Load Consonants and Determine their Probabilities
        vowelProb(base_prob, probs)

    return probs


if __name__ == "__main__":
    val = sys.argv[1]
    limit = int(sys.argv[2])

    probs = calcBaseProb(val == "cons")
    probs.printList(limit)

    # node = probs.getHead()
    # total = 0
    # while node:

    #     total += math.e**(node.getProb())
    #     node = node.getNext()

    # print(total)

