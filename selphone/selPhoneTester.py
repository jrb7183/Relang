import sys
from collections import Counter

sys.path.append(".")
from probs.phoneProb import calcBaseProb
from utils.phoneLinkedList import PhonemeList
from selphone.selectPhonemes import selectPhonemes


def spTester(probs: PhonemeList, num, temp, iter):
    phones = Counter()
    for _ in range(iter):
        temp_probs = probs.copyList()
        sel_phones = selectPhonemes(temp_probs, num, temp)
        phones.update(sel_phones)

    print(phones)


if __name__ == "__main__":
    num = int(sys.argv[1])
    temp = float(sys.argv[2])
    iter = int(sys.argv[3])

    probs = calcBaseProb(True)
    spTester(probs, num, temp, iter)