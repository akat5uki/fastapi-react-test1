from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..core.routers import users, auth, items

app = FastAPI(root_path="/api/v1")

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(items.router)
















@app.get("/", tags=["root"])
async def get_root() -> dict:
    return {"message": "Hello World"}