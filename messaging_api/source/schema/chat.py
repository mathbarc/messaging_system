from typing import List
from uuid import UUID

class Chat:
    chat_id:UUID
    name:str
    user_list:List[str] = None
