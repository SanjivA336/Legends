from fastapi import FastAPI
from backend.routes import account_routes, auth_routes, home_routes

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(account_routes.router)
app.include_router(home_routes.router)
