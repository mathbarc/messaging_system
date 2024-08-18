from uuid import UUID
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

class MessageType(Enum):
    TEXT="text"
    IMAGE="image"
    VIDEO="video"
    FILE="file"

@dataclass
class Message:
    id:int
    type:MessageType
    timestamp: datetime
    content:str


    

