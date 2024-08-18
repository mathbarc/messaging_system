from typing import List
from uuid import UUID
from dataclasses import dataclass

@dataclass
class Chat:
    id:int
    name:str
    user_list:List[str] = None
