from messaging_api.exceptions import MessagingSystemException

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dataclasses import asdict

def messaging_system_exception_handler(request:Request, exc:MessagingSystemException):
    return JSONResponse(status_code=exc.status_code, content=exc.message)

def exception_handler(request:Request, exc:Exception):
    return JSONResponse(status_code=500, content=str(exc))