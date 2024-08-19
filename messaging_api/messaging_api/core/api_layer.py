from typing import List
from ..schema import User, Chat, Message, MessageType
from .system_db import SystemDBController



def register_client(name:str, username:str, password:str, email:str) -> User:
    systemdb = SystemDBController()
    user = systemdb.register_user(name = name, username=username, password=password, email=email)
    
    return user 
    

def login(username:str, password:str) -> str:
    systemdb = SystemDBController()
    token = systemdb.login(username=username, password=password)
    
    return token

def list_contacts(user:User, itens_per_page:int, offset:int) -> List[User]:
    systemdb = SystemDBController()
    
    contact_list = systemdb.list_contacts(user, itens_per_page, offset)
    
    return contact_list

def add_user_to_contacts(user:User, contact:User):
    systemdb = SystemDBController()
    systemdb.add_contact(user, contact)
    

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