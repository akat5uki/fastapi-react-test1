from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class JsonData(BaseModel):
    name: str
    age: int
    username: str

app = FastAPI()

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


@app.get("/", tags=["root"])
async def get_root() -> dict:
    return {"message": "Hello World"}

@app.post("/", tags=["root"], response_model=JsonData)
async def post_root(data: JsonData) -> dict:
    print(data.model_dump())
    return data.model_dump()