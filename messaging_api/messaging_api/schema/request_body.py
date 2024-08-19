from dataclasses import dataclass

@dataclass
class LoginSchema:
    username: str
    password: str
    
@dataclass
class SignUpSchema:
    username: str
    password: str
    name: str
    email: str

@dataclass
class AddContactSchema:
    id: int
    username: str
    name: str
    email: str
    
@dataclass
class TokenResponse:
    token: str