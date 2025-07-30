import sys
import uvicorn
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append("..")
from probs.relangProbs import relangProbs
from utils.phonemeLoader import loadPhonemes
from selphone.selectPhonemes import selectConsonants
from utils.tableFormatter import tableFormatter
from utils.api.baseModels import ConsTable
from utils.ipaDecoder import ipaToBinary

app = FastAPI()
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET,POST,DELETE"],
    allow_headers=["*"]
)

def main(num, use_relang = False):
    # temp = float(sys.argv[2])

    consonants = loadPhonemes(True)
    # print(consonants[(consonants.index % 8 == 0) & (consonants.index < 1300)])
    probs = {}
    if use_relang:
        p = ["m", "n", "ŋ", "p", "t", "k", "s", "w", "l", "j"]
        p = ipaToBinary(p, True)
        q = ["b", "d", "g", "p", "t", "k", "s", "w", "l", "j"]
        q = ipaToBinary(q, True)
        probs = relangProbs([p, q])
        return selectConsonants(consonants, probs, num)


    with open("../data/baseProbs.json", "r", encoding="utf-8") as f:
        probs = json.load(f)

    return selectConsonants(consonants, probs["Consonants"], num)

temp_cons = {"Consonants": [""]}

@app.get("/cons", response_model=ConsTable)
def getCons():
    return temp_cons

@app.post("/cons", response_model=ConsTable)
def createConsList(cons_num: int):
    cons_list = main(cons_num)
    global temp_cons
    temp_cons = ConsTable(constable=tableFormatter(cons_list))
    return temp_cons
    

if __name__ == "__main__":
    useApp = sys.argv[1]
    
    if useApp == "app":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    
    else:
        num = int(sys.argv[2])
        use_relang = sys.argv[3] != "base"
        sel_phones = main(num, use_relang)
        
        for i in range(len(sel_phones)):
            print(f"{i+1}.\t{sel_phones[i][0]}\n\t{sel_phones[i][1]}")
    