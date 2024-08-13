from typing import List
from ..schema import User, Chat, Message, MessageType


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

def receive_messages(user_token:str, chat_id:str, itens_per_page:int, offset:int) -> List[Message]:
    pass

def send_message(user_token:str, chat_id:str, message_type:MessageType, message_content:bytes|str, file_name:str = None) -> Message:
    pass

def edit_message(user_token:str, message_id:str, message_type:MessageType, message_content:bytes|str, file_name:str = None) -> Message:
    pass