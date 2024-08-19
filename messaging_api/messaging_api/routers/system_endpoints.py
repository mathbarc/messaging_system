from typing import List
from messaging_api.schema import LoginSchema, SignUpSchema, AddContactSchema, TokenResponse, User
from messaging_api.core import api_layer
from fastapi import APIRouter, Request


router = APIRouter(prefix="/api/v1")

@router.post("/login")
def login(request:Request, body:LoginSchema) -> TokenResponse:
    token = api_layer.login(body.username, body.password)
    return TokenResponse(token)

@router.post("/signup")
def signup(request:Request, body:SignUpSchema) -> TokenResponse:
    user = api_layer.register_client(body.name, body.username, body.password, body.email)
    return TokenResponse(user.create_token())

@router.get("/list_contacts")
def list_contacts(request:Request, itens_per_page:int=10, offset:int=0) -> List[User]:
    token = request.headers.get("Authorization").split(" ")[-1]
    user = User.from_token(token)
    contacts = api_layer.list_contacts(user,itens_per_page, offset)
    return contacts
    
@router.post("/add_contact")
def add_contact(request:Request, body:AddContactSchema):
    token = request.headers.get("Authorization").split(" ")[-1]
    user = User.from_token(token)
    api_layer.add_user_to_contacts(user, User(body.id, body.username, body.name, body.email))
    return "OK"