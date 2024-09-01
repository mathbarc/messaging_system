from typing import List
from messaging_api.schema import User, Chat, Message, MessageType
from messaging_api.core.system_db import SystemDBController
from messaging_api.core.storage import S3Storage
from messaging_api.config import BUCKET_NAME, BUCKET_ENDPOINT_URL



def register_client(name:str, username:str, password:str, email:str) -> User:
    systemdb = SystemDBController()
    systemdb.register_user(name = name, username=username, password=password, email=email)
    
    return "DONE"
    

def login(username:str, password:str) -> str:
    systemdb = SystemDBController()
    token = systemdb.login(username=username, password=password)
    
    return token

def aboutme(user_id:str):
    systemdb = SystemDBController()
    
    
    
    return ""

def list_contacts(user_id, itens_per_page:int, offset:int) -> List[User]:
    systemdb = SystemDBController()
    
    contact_list = systemdb.list_contacts(user_id, itens_per_page, offset)
    
    storage = S3Storage(BUCKET_NAME, BUCKET_ENDPOINT_URL)
    
    for user in contact_list:
        if user._photo_path is not None:
            data = storage.load(user._photo_path)
            user.set_photo(data)
        
    
    return contact_list

def add_user_to_contacts(user_id:str, contact_id:str):
    systemdb = SystemDBController()
    systemdb.add_contact(user_id, contact_id)
    

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