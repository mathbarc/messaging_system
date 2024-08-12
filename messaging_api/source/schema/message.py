from uuid import UUID
from enum import Enum
from datetime import datetime

class MessageType(Enum):
    TEXT="text"
    IMAGE="image"
    VIDEO="video"
    FILE="file"

class Message:
    message_id:UUID
    type:MessageType
    timestamp: datetime
    content:str


    

