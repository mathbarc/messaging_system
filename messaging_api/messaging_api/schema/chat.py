from typing import List
from uuid import UUID
from dataclasses import dataclass

@dataclass
class Chat:
    _id:int
    uuid:UUID
    name:str
    user_list:List[str] = None
