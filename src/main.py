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
from utils.api.baseModels import ConsTable, Phonos
from utils.inputManagement.ipaDecoder import ipaToBinary
from utils.inputManagement.calcNumCons import numCons

app = FastAPI()
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","DELETE","OPTIONS"],
    allow_headers=["*"]
)

def main(phonologies: list[list[str]]):
    for i in range(len(phonologies)): 
        phonologies[i] = ipaToBinary(phonologies[i], True)

    consonants = loadPhonemes(True)
    probs = relangProbs(phonologies)
    num = numCons(phonologies)
    print(num)

    return selectConsonants(consonants, probs, num)

temp_cons = {"Consonants": [""]}

@app.get("/cons", response_model=ConsTable)
def getCons():
    return temp_cons

@app.post("/cons", response_model=ConsTable)
def createConsList(phonos: Phonos):
    phonos = phonos.model_dump()["phonos"]
    cons_list = main(phonos)
    
    global temp_cons
    temp_cons = ConsTable(constable=tableFormatter(cons_list))
    return temp_cons
    

if __name__ == "__main__":
    useApp = sys.argv[1]
    
    if useApp == "app":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    
    else:
        use_relang = sys.argv[2] != "base"

        sel_phones = []
        if use_relang:
            p = ["m", "n", "ŋ", "p", "t", "k", "p'", "t'", "k'", "s", "w", "l", "j"]
            q = ["b", "d", "g", "p", "t", "k", "s", "w", "l", "j"]

            phonos = [p, q]

            sel_phones = main(phonos)

        else:
            sel_phones = main([])
        
        
        for i in range(len(sel_phones)):
            print(f"{i+1}.\t{sel_phones[i][0]}\n\t{sel_phones[i][1]}")
    