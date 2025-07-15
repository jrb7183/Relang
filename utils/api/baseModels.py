from pydantic import BaseModel
from typing import List, Dict, Any

class ConsTable(BaseModel):
    constable: Dict[str, List]