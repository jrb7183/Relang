import sys
from fastapi import FastAPI

sys.path.append("..")
from probs.relangProbs import relangProbs
from utils.phonemeLoader import loadPhonemes
from selphone.newselectPhonemes import selectConsonants
from utils.tableFormatter import tableFormatter

app = FastAPI()

def main(num):
    # temp = float(sys.argv[2])

    consonants = loadPhonemes(True)
    # print(consonants[(consonants.index % 8 == 0) & (consonants.index < 1300)])
    probs = relangProbs()
    
    return selectConsonants(consonants, probs["Consonants"], num)

@app.get("/cons")
async def createConsList(cons_num: int):
    cons_list = main(cons_num)
    return tableFormatter(cons_list)

# @app.post("/cons")
# async def createConsList(cons_num: int):
#     cons_list = main(cons_num)
#     return tableFormatter(cons_list)
    

if __name__ == "__main__":
    num = int(sys.argv[1])
    sel_phones = main(num)
    
    for i in range(len(sel_phones)):
        print(f"{i+1}.\t{sel_phones[i][0]}\n\t{sel_phones[i][1]}")