import sys
from fastapi import FastAPI
import apiCalls

sys.path.append("..")
from probs.relangProbs import relangProbs
from utils.phonemeLoader import loadPhonemes
from selphone.newselectPhonemes import selectConsonants

app = FastAPI()
app.include_router(apiCalls.router)

num = 30
# temp = float(sys.argv[2])

consonants = loadPhonemes(True)
# print(consonants[(consonants.index % 8 == 0) & (consonants.index < 1300)])
probs = relangProbs()
sel_phones = selectConsonants(consonants, probs["Consonants"], num)

apiCalls.createConsList(sel_phones)


# for i in range(len(sel_phones)):
#     print(f"{i+1}. {sel_phones[i][0]}   {sel_phones[i][1]}")