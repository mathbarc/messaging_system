from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Chat:
    id:int
    name:str
    user_list:Optional[List[str]] = None
