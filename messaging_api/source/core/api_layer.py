from typing import List
from ..schema import User, Chat


def register_client(username:str, password:str, email:str) -> str:
    pass

def login(username:str, password:str) -> str:
    pass

def list_contacts(user_token:str, itens_per_page:int, offset:int) -> List[User]:
    pass

def start_chat(user_token:str, user_id_list:List[str]) -> Chat:
    pass

def list_chats(user_token:str, itens_per_page:int, offset:int) -> List[Chat]:
    pass

def receive_messages(username:str, password:str, email:str) -> str:
    pass