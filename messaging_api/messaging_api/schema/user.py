from uuid import UUID
from dataclasses import dataclass, asdict
import datetime
import jwt
import os
from ..config import API_KEY
from ..exceptions import TokenInvalidException
import base64

def create_token(user_id) -> str:
    expiration_date = datetime.datetime.now()+datetime.timedelta(hours=8)
    
    payload = {
        "iss": user_id,
        "exp": int(expiration_date.timestamp()),
    }    
    
    return jwt.api_jwt.encode(payload=payload, key=API_KEY)

def get_user_id_from_token(token:str) -> int:
    try:
        data = jwt.api_jwt.decode(token, API_KEY, ["HS256"])
    except jwt.exceptions.InvalidTokenError:
        raise TokenInvalidException()
    
    return data["iss"]


@dataclass
class User:
    id:str
    username:str
    name:str
    email:str
    photo:str = None
    
    
    def __init__(
            self,
            id:str,
            username:str,
            name:str,
            email:str,
            photo_path:str
    ):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self._photo_path = photo_path
        
        
    def set_photo(self, photo_data:bytes):
        extension = os.path.splitext(self._photo_path)[-1][1,:]
        self.photo = f"data:image/{extension};base64,"+base64.b64encode(photo_data)
    