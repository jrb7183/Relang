from fastapi import APIRouter
from tableFormatter import tableFormatter
router = APIRouter()

@router.post("/cons")
async def createConsList(cons_list):
    return tableFormatter(cons_list)
    

# @router.get("/cons")
# async def getConsList():
#     return