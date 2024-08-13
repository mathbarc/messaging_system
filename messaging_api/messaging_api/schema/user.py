from uuid import UUID
from dataclasses import dataclass


@dataclass
class User:
    _id:int
    uuid:UUID
    name:str
    email:str

