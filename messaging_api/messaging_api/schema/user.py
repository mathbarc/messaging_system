from uuid import UUID
from dataclasses import dataclass, asdict
import datetime
import jwt
from messaging_api.config import API_KEY
from ..exceptions import TokenInvalidException

@dataclass
class User:
    id:int
    username:str
    name:str

    def create_token(self) -> str:
        expiration_date = datetime.datetime.now()+datetime.timedelta(hours=8)
        
        payload = {
            "user":asdict(self),
            "exp": int(expiration_date.timestamp()),
        }    
        
        return jwt.api_jwt.encode(payload=payload, key=API_KEY)

    @classmethod
    def from_token(cls, token:str):
        try:
            data = jwt.api_jwt.decode(token, API_KEY, ["HS256"])
        except jwt.exceptions.InvalidTokenError:
            raise TokenInvalidException()
        
        return cls(**data["user"])