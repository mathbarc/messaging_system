from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from messaging_api.routers.system_endpoints import router

app = FastAPI(title="Messaging System")

app.include_router(router)

origins = [
    "http://localhost:5000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

