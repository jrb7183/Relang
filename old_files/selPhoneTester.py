import sys
import pandas as pd
from collections import Counter

sys.path.append("..")
from old_files.newphoneProb import calcBaseProb
from selphone.selectPhonemes import selectPhonemes

""" OUT OF DATE """

def spTester(probs: pd.DataFrame, num, temp, iter):
    phones = Counter()
    for _ in range(iter):
        sel_phones = selectPhonemes(probs, num, temp)
        phones.update(sel_phones)

        probs.loc[:, "Selected"] = False

    print(phones)


if __name__ == "__main__":
    num = int(sys.argv[1])
    temp = float(sys.argv[2])
    iter = int(sys.argv[3])

    probs = calcBaseProb(True)
    spTester(probs, num, temp, iter)